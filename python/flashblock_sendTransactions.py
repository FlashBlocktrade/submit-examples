"""
Disclaimer / 免责声明
English: This example only demonstrates how to use our product. It does not constitute trading advice
or a trading/execution system. Use at your own risk. We are not responsible for any loss caused by
using this code.
中文：本示例仅演示如何使用我们的产品，不构成任何交易建议或交易/执行系统。使用本代码所造成的任何损失，概不负责。
"""

# English: Minimal Python client using httpx with endpoint selection, Keep-Alive, retry, and batch submit.
# 中文：最小化的 Python 客户端（httpx），包含端点选择、Keep-Alive、自动重试与批量提交。
import asyncio
import time
import httpx
from typing import Optional
import os
import base64
from solana.rpc.commitment import Confirmed
from solana.rpc.api import Client as SolClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.message import Message, MessageV0
from solders.transaction import VersionedTransaction, Transaction as LegacyTransaction
from solders.hash import Hash
from base58 import b58encode
from solders.system_program import TransferParams, transfer

# English: Public endpoints; modify as needed.
# 中文：公开端点列表；可按需调整。
ENDPOINTS = [
    {"name": "ny", "baseUrl": "http://ny.flashblock.trade"},
    {"name": "slc", "baseUrl": "http://slc.flashblock.trade"},
    {"name": "ams", "baseUrl": "http://ams.flashblock.trade"},
    {"name": "fra", "baseUrl": "http://fra.flashblock.trade"},
    {"name": "singapore", "baseUrl": "http://singapore.flashblock.trade"},
    {"name": "london", "baseUrl": "http://london.flashblock.trade"},
]

# English: Tip addresses; choose randomly to distribute support.
# 中文：小费地址列表；随机选择以便更公平地分配支持。
TIP_ADDRESSES = [
    "FLaShB3iXXTWE1vu9wQsChUKq3HFtpMAhb8kAh1pf1wi",
    "FLashhsorBmM9dLpuq6qATawcpqk1Y2aqaZfkd48iT3W",
    "FLaSHJNm5dWYzEgnHJWWJP5ccu128Mu61NJLxUf7mUXU",
    "FLaSHR4Vv7sttd6TyDF4yR1bJyAxRwWKbohDytEMu3wL",
    "FLASHRzANfcAKDuQ3RXv9hbkBy4WVEKDzoAgxJ56DiE4",
    "FLasHstqx11M8W56zrSEqkCyhMCCpr6ze6Mjdvqope5s",
    "FLAShWTjcweNT4NSotpjpxAkwxUr2we3eXQGhpTVzRwy",
    "FLasHXTqrbNvpWFB6grN47HGZfK6pze9HLNTgbukfPSk",
    "FLAshyAyBcKb39KPxSzXcepiS8iDYUhDGwJcJDPX4g2B",
    "FLAsHZTRcf3Dy1APaz6j74ebdMC6Xx4g6i9YxjyrDybR",
]

def get_random_tip_address() -> str:
    import random
    # English: TIP_ADDRESSES is non-empty; safe to choose.
    # 中文：TIP_ADDRESSES 非空；可安全随机选择。
    return random.choice(TIP_ADDRESSES)

# English: In-process cache for the fastest endpoint
# 中文：进程内缓存最快端点
_CACHED_ENDPOINT = None  # type: Optional[dict]

# English: Ping root; success if 2xx.
# 中文：Ping 根路径；2xx 视为成功。
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
# 中文：选择最快可用端点（或退化为最低延迟）。
async def select_best_endpoint(client: httpx.AsyncClient):
    rs = await asyncio.gather(*[ping(client, ep) for ep in ENDPOINTS])
    healthy = [r for r in rs if r["ok"]]
    lst = healthy if healthy else rs
    lst.sort(key=lambda x: x["ms"])
    return lst[0]["ep"]

# English: Submit with simple retry for 429/5xx.
# 中文：提交时对 429/5xx 做简单重试。
async def submit_batch(client: httpx.AsyncClient, base_url: str, auth_header: str, txs):
    url = f"{base_url}/api/v2/submit-batch"
    attempts = 0
    while True:
        r = await client.post(
            url,
            json={"transactions": txs},
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
            },
        )
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
# 中文：便捷方法（与其他语言一致）；
# - 可选指定首选端点名；传输错误时重选端点再试一次。
async def flashblock_sendTransactions(auth_header: str, transactions, preferred: Optional[str] = None):
    if not auth_header:
        raise ValueError("auth_header required")
    if not isinstance(transactions, list) or len(transactions) == 0:
        raise ValueError("transactions empty")

    limits = httpx.Limits(max_keepalive_connections=64, max_connections=64)
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        global _CACHED_ENDPOINT
        ep = None
        if preferred:
            ep = next((e for e in ENDPOINTS if e["name"] == preferred), None)
        if ep is None:
            # Use cached endpoint if available; otherwise select and cache
            ep = _CACHED_ENDPOINT
            if ep is None:
                ep = await select_best_endpoint(client)
                _CACHED_ENDPOINT = ep

        start = time.monotonic()
        try:
            res = await submit_batch(client, ep["baseUrl"], auth_header, transactions)
        except Exception:
            # On transport error, invalidate cache and reselect
            _CACHED_ENDPOINT = None
            ep = await select_best_endpoint(client)
            _CACHED_ENDPOINT = ep
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


# English: Build/sign a 1-lamport transfer for mainnet using sender secret; return base64 tx.
# 中文：使用发送方私钥在主网构造并签名 1 lamport 转账；返回 base64 交易。
def build_one_lamport_transfer_base64(sender_secret: str, receiver_address: Optional[str] = None, amount_lamports: int = 5000):
    # sender_secret supports: base58 (compact) or JSON array of 64/32 bytes
    try:
        sec = sender_secret.strip()
        if os.path.exists(sec):
            import json
            with open(sec, "r", encoding="utf-8") as f:
                arr = json.load(f)
            kp = Keypair.from_bytes(bytes(arr))
        elif sec.startswith("["):
            import json
            arr = json.loads(sec)
            kp = Keypair.from_bytes(bytes(arr))
        else:
            # Assume base58 string form
            kp = Keypair.from_base58_string(sec)
    except Exception as e:
        raise ValueError(f"Invalid SENDER_SECRET: {e}")

    # Receiver: fixed address if provided, otherwise generate new wallet
    receiver = None
    to_pub: Pubkey
    if receiver_address:
        try:
            to_pub = Pubkey.from_string(receiver_address)
        except Exception as e:
            raise ValueError(f"Invalid RECEIVER_ADDRESS: {e}")
    else:
        receiver = Keypair()
        to_pub = receiver.pubkey()
    from_pub = kp.pubkey()

    # Fetch recent blockhash via JSON-RPC (finalized) to ensure compatibility
    rpc_url = os.environ.get("MAINNET_RPC", "https://api.mainnet-beta.solana.com")
    try:
        with httpx.Client(timeout=10.0) as c:
            body = {"jsonrpc":"2.0","id":1,"method":"getLatestBlockhash","params":[{"commitment":"finalized"}]}
            r = c.post(rpc_url, json=body)
            r.raise_for_status()
            j = r.json()
            bh_str = j["result"]["value"]["blockhash"]
            recent = Hash.from_string(bh_str)
    except Exception as e:
        raise RuntimeError(f"failed to fetch recent blockhash via JSON-RPC at {rpc_url}: {e}")

    # Build legacy transaction via solders
    instruction = transfer(TransferParams(from_pubkey=from_pub, to_pubkey=to_pub, lamports=amount_lamports))
    try:
        legacy_msg = Message.new(instructions=[instruction], payer=from_pub, recent_blockhash=recent)
        legacy_tx = LegacyTransaction(legacy_msg, [kp])
        b = bytes(legacy_tx)
    except Exception:
        # Fallback to v0 if legacy new not available
        msg = MessageV0.try_compile(
            payer=from_pub,
            instructions=[instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent,
        )
        vtx = VersionedTransaction(msg, [kp])
        b = bytes(vtx)
    b64 = base64.b64encode(b).decode()
    ret = {
        "sender": str(from_pub),
        "receiver": str(to_pub),
        "transaction_b64": b64,
    }
    if receiver is not None:
        # include generated receiver secrets for convenience
        ret["receiver_secret_base58"] = b58encode(bytes(receiver)).decode()
        ret["receiver_secret_json"] = list(bytes(receiver))
    return ret


# English: Query minimum balance for rent exemption (for plain account, data_len=0)
# 中文：查询租金豁免所需最小余额（普通账户，数据长度为 0）
def get_min_rent_exempt_lamports():
    rpc_url = os.environ.get("MAINNET_RPC", "https://api.mainnet-beta.solana.com")
    with httpx.Client(timeout=10.0) as c:
        body = {"jsonrpc":"2.0","id":1,"method":"getMinimumBalanceForRentExemption","params":[0]}
        r = c.post(rpc_url, json=body)
        r.raise_for_status()
        j = r.json()
        return int(j["result"]) if "result" in j else 0


# English: Generate a new wallet, return address and secrets in both base58 and JSON forms.
# 中文：生成新钱包，返回地址和私钥（base58 与 JSON 数组两种形式）。
def generate_wallet():
    kp = Keypair()
    secret_bytes = bytes(kp)
    # base58 form compatible with many tools
    base58_secret = b58encode(bytes(kp)).decode()
    # JSON array form
    json_array = list(secret_bytes)
    return {
        "address": str(kp.pubkey()),
        "secret_base58": base58_secret,
        "secret_json": json_array,
    }


