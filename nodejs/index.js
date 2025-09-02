import { flashblock_sendTransactions } from './flashblock_sendTransactions.js';

async function main() {
  const AUTH = process.env.AUTH_HEADER || 'Bearer YOUR_TOKEN';
  const txs = ['AaBU8zC90i...MAAAAAAAA='];
  const ret = await flashblock_sendTransactions(AUTH, txs /*, 'fra' */);
  console.log('signatures:', ret.signatures, 'status:', ret.status, 'message:', ret.message, 'ms:', ret.durationMs, 'ep:', ret.endpoint);
}

main().catch(e => { console.error(e); process.exit(1); });


