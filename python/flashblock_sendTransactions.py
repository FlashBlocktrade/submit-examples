# English: Minimal Python client using httpx with endpoint selection, Keep-Alive, retry, and batch submit.
# 中文：最小化的 Python 用戶端（httpx），包含端點選擇、Keep-Alive、自動重試與批次提交。
import asyncio
import time
import httpx

# English: Public endpoints; modify as needed.
# 中文：公開端點清單；可按需調整。
ENDPOINTS = [
    {"name": "ny", "baseUrl": "http://ny.flashblock.trade"},
    {"name": "slc", "baseUrl": "http://slc.flashblock.trade"},
    {"name": "ams", "baseUrl": "http://ams.flashblock.trade"},
    {"name": "fra", "baseUrl": "http://fra.flashblock.trade"},
    {"name": "singapore", "baseUrl": "http://singapore.flashblock.trade"},
    {"name": "london", "baseUrl": "http://london.flashblock.trade"},
]

# English: Ping root; success if 2xx.
# 中文：Ping 根路徑；2xx 視為成功。
async def ping(client: httpx.AsyncClient, ep):
    t0 = time.monotonic()
    try:
        r = await client.get(ep["baseUrl"])  # root path
        ok = 200 <= r.status_code < 300
    except Exception:
        ok = False
    ms = int((time.monotonic() - t0) * 1000)
    return {"ep": ep, "ok": ok, "ms": ms}

# English: Select fastest healthy endpoint (fallback to lowest latency).
# 中文：選擇最快可用端點（或退化為最低延遲）。
async def select_best_endpoint(client: httpx.AsyncClient):
    rs = await asyncio.gather(*[ping(client, ep) for ep in ENDPOINTS])
    healthy = [r for r in rs if r["ok"]]
    lst = healthy if healthy else rs
    lst.sort(key=lambda x: x["ms"])
    return lst[0]["ep"]

# English: Submit with simple retry for 429/5xx.
# 中文：提交時對 429/5xx 做簡單重試。
async def submit_batch(client: httpx.AsyncClient, base_url: str, auth_header: str, txs):
    url = f"{base_url}/api/v2/submit-batch"
    attempts = 0
    while True:
        r = await client.post(url, json={"transactions": txs}, headers={"Authorization": auth_header})
        if r.status_code == 429 or r.status_code >= 500:
            if attempts < 2:
                attempts += 1
                continue
        return {"status": r.status_code, "data": r.json() if r.content else {}}

async def main():
    auth = "Bearer YOUR_TOKEN"
    txs = ["AaBU8zC90i...MAAAAAAAA="]
    ret = await flashblock_sendTransactions(auth, txs)
    print("signatures:", ret["signatures"], "status:", ret["status"], "message:", ret["message"], "ms:", ret["durationMs"], "ep:", ret["endpoint"])

if __name__ == "__main__":
    asyncio.run(main())

# English: Convenience function (same behavior as other languages);
# - preferred endpoint name optional; retry once on transport error.
# 中文：便捷方法（與其他語言一致）；
# - 可選指定首選端點名；傳輸錯誤時重選端點再試一次。
async def flashblock_sendTransactions(auth_header: str, transactions, preferred: str | None = None):
    if not auth_header:
        raise ValueError("auth_header required")
    if not isinstance(transactions, list) or len(transactions) == 0:
        raise ValueError("transactions empty")

    limits = httpx.Limits(max_keepalive_connections=64, max_connections=64)
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        ep = None
        if preferred:
            ep = next((e for e in ENDPOINTS if e["name"] == preferred), None)
        if ep is None:
            ep = await select_best_endpoint(client)

        start = time.monotonic()
        try:
            res = await submit_batch(client, ep["baseUrl"], auth_header, transactions)
        except Exception:
            ep = await select_best_endpoint(client)
            res = await submit_batch(client, ep["baseUrl"], auth_header, transactions)

        duration_ms = int((time.monotonic() - start) * 1000)
        top = res.get("data", {})
        data_obj = top.get("data") or {}
        signatures = data_obj.get("signatures") or top.get("signatures") or []
        return {
            "status": res["status"],
            "success": bool(top.get("success")),
            "code": int(top.get("code") or 0),
            "message": str(top.get("message") or ""),
            "signatures": signatures,
            "durationMs": duration_ms,
            "endpoint": ep,
            "raw": res,
        }


