# NodeJS Example: flashblock_sendTransactions

- Method file: `flashblock_sendTransactions.js`
- Entry: `index.js` (calls the method)

## Prerequisites
- Node.js >= 18
- Valid `AUTH_HEADER`

Chinese documentation: see [README.zh.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/nodejs/README.zh.md).

## Install & Run
```bash
cd nodejs
npm i
AUTH_HEADER='Bearer YOUR_TOKEN' node index.js
```

## Method signature
```js
// flashblock_sendTransactions(authHeader, transactions, preferred?) => Promise<{
//   status, success, code, message, signatures, durationMs, endpoint, raw
// }>
```
- `transactions`: array of base64 strings
- `preferred` (optional): endpoint name such as `ny`, `fra`

## Sample
```js
import { flashblock_sendTransactions } from './flashblock_sendTransactions.js';

const AUTH = process.env.AUTH_HEADER;
const txs = ['AaBU8zC90i...MAAAAAAAA='];
const ret = await flashblock_sendTransactions(AUTH, txs /* , 'fra' */);
console.log('signatures:', ret.signatures, 'status:', ret.status, 'message:', ret.message, 'ms:', ret.durationMs, 'ep:', ret.endpoint);
```
