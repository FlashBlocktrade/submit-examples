// English: Demo entry for NodeJS — calls flashblock_sendTransactions and prints result.
// 中文：NodeJS 演示入口——调用 flashblock_sendTransactions 并打印结果。
// Usage/用法:
//   AUTH_HEADER='Bearer YOUR_TOKEN' node index.js
// Optional preferred endpoint/可选首选端点: pass as third argument in code (e.g. 'fra').
import { flashblock_sendTransactions } from './flashblock_sendTransactions.js';

async function main() {
  const AUTH = process.env.AUTH_HEADER || 'Bearer YOUR_TOKEN';
  const txs = ['AaBU8zC90i...MAAAAAAAA='];
  const ret = await flashblock_sendTransactions(AUTH, txs /*, 'fra' */);
  console.log('signatures:', ret.signatures, 'status:', ret.status, 'message:', ret.message, 'ms:', ret.durationMs, 'ep:', ret.endpoint);
}

main().catch(e => { console.error(e); process.exit(1); });


