# NodeJS 示例：flashblock_sendTransactions

- 方法文件：`flashblock_sendTransactions.js`
- 入口：`index.js`（仅调用方法）

## 前置要求
- Node.js >= 18
- 有效 `AUTH_HEADER`

英文文档：参见 [README.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/nodejs/README.md)。

## 安装与运行
```bash
cd nodejs
npm i
AUTH_HEADER='Bearer YOUR_TOKEN' node index.js
```

## 方法签名
```js
// flashblock_sendTransactions(authHeader, transactions, preferred?) => Promise<{
//   status, success, code, message, signatures, durationMs, endpoint, raw
// }>
```
- `transactions`：base64 字符串数组
- `preferred`（可选）：端点名，如 `ny`、`fra`

## 简单示例
```js
import { flashblock_sendTransactions } from './flashblock_sendTransactions.js';

const AUTH = process.env.AUTH_HEADER;
const txs = ['AaBU8zC90i...MAAAAAAAA='];
const ret = await flashblock_sendTransactions(AUTH, txs /* , 'fra' */);
console.log('signatures:', ret.signatures, 'status:', ret.status, 'message:', ret.message, 'ms:', ret.durationMs, 'ep:', ret.endpoint);
```
