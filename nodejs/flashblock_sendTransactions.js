// English: Minimal NodeJS client with endpoint selection, Keep-Alive, retry, and batch submit.
// 中文：最小化的 NodeJS 客户端，包含端点选择、Keep-Alive、自动重试与批量提交。
import axios from 'axios';
import http from 'http';
import https from 'https';

// English: Public endpoints; modify as needed.
// 中文：公开端点列表；可按需调整。
const ENDPOINTS = [
  { name: 'ny', baseUrl: 'http://ny.flashblock.trade' },
  { name: 'slc', baseUrl: 'http://slc.flashblock.trade' },
  { name: 'ams', baseUrl: 'http://ams.flashblock.trade' },
  { name: 'fra', baseUrl: 'http://fra.flashblock.trade' },
  { name: 'singapore', baseUrl: 'http://singapore.flashblock.trade' },
  { name: 'london', baseUrl: 'http://london.flashblock.trade' },
];

// English: Reusable Keep-Alive agents to minimize connection setup latency.
// 中文：可复用的 Keep-Alive 连接，减少连接建立时延。
const httpAgent = new http.Agent({ keepAlive: true, maxSockets: 64, keepAliveMsecs: 15000 });
const httpsAgent = new https.Agent({ keepAlive: true, maxSockets: 64, keepAliveMsecs: 15000 });
const pingClient = axios.create({ timeout: 1500, validateStatus: () => true });
const submitClient = axios.create({ timeout: 10000, httpAgent, httpsAgent, validateStatus: () => true });

// English: Ping the root path of an endpoint; success if HTTP 2xx.
// 中文：对端点根路径发起 Ping，请求返回 2xx 即视为可用。
async function pingEndpoint(ep) {
  const url = `${ep.baseUrl}`;
  const t0 = Date.now();
  try {
    const res = await pingClient.get(url);
    return { ep, ok: res.status >= 200 && res.status < 300, ms: Date.now() - t0 };
  } catch {
    return { ep, ok: false, ms: Date.now() - t0 };
  }
}

// English: Select the fastest healthy endpoint (fallback to lowest latency if all unhealthy).
// 中文：选择最快且可用的端点（若都不可用则退化为最低延迟）。
async function selectBestEndpoint() {
  const rs = await Promise.all(ENDPOINTS.map(pingEndpoint));
  const healthy = rs.filter(r => r.ok);
  const list = healthy.length ? healthy : rs;
  list.sort((a, b) => a.ms - b.ms);
  return list[0].ep;
}

// English: Submit transactions with simple retry for 429/5xx.
// 中文：提交交易，针对 429/5xx 进行简单重试。
async function submitBatch(baseUrl, authHeader, transactions, maxRetries = 2) {
  const url = `${baseUrl}/api/v2/submit-batch`;
  let attempts = 0;
  while (true) {
    const res = await submitClient.post(url, { transactions }, {
      headers: { Authorization: authHeader, 'Content-Type': 'application/json' },
    });
    if (res.status === 429 || res.status >= 500) {
      if (attempts++ < maxRetries) continue;
    }
    return { status: res.status, data: res.data };
  }
}

// English: Normalize response and extract signatures from either top-level or data.signatures.
// 中文：标准化响应，兼容顶层或 data.signatures 的签名字段。
function extractSignatures(raw) {
  const top = raw?.data ?? raw;
  const success = !!top?.success;
  const code = Number(top?.code ?? 0);
  const message = String(top?.message ?? '');
  const signatures = Array.isArray(top?.data?.signatures) ? top.data.signatures
    : Array.isArray(top?.signatures) ? top.signatures : [];
  return { success, code, message, signatures };
}

// English: Convenience method (same behavior as TS version).
// 中文：便捷方法（与 TS 版本一致的行为）。
export async function flashblock_sendTransactions(authHeader, transactions, preferred) {
  if (!authHeader) throw new Error('authHeader required');
  if (!Array.isArray(transactions) || transactions.length === 0) throw new Error('transactions empty');

  const start = Date.now();
  let ep = preferred ? ENDPOINTS.find(e => e.name === preferred) : undefined;
  if (!ep) ep = await selectBestEndpoint();

  try {
    const res = await submitBatch(ep.baseUrl, authHeader, transactions);
    const meta = extractSignatures(res);
    return { ...meta, status: res.status, durationMs: Date.now() - start, endpoint: ep, raw: res };
  } catch {
    ep = await selectBestEndpoint();
    const res = await submitBatch(ep.baseUrl, authHeader, transactions);
    const meta = extractSignatures(res);
    return { ...meta, status: res.status, durationMs: Date.now() - start, endpoint: ep, raw: res };
  }
}


