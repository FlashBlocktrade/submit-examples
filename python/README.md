# Python Example: flashblock_sendTransactions / Python 示例

- EN: Method file: `flashblock_sendTransactions.py`; entry: `main.py` (calls the method)
- 中文：方法文件 `flashblock_sendTransactions.py`；入口 `main.py`（仅调用方法）

## Prerequisites / 前置要求
- EN: Python 3.9+, valid `AUTH_HEADER`
- 中文：Python 3.9+，准备有效的 `AUTH_HEADER`

## Install & Run / 安装与运行
```bash
cd examples/python
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
AUTH_HEADER='Bearer YOUR_TOKEN' python main.py
```

## Methods / 方法
- EN: `flashblock_sendTransactions(auth_header, transactions, preferred?)`
- 中文：`flashblock_sendTransactions(auth_header, transactions, preferred?)`

- EN: It selects the fastest healthy endpoint (ping root), uses Keep-Alive, retries 429/5xx, and submits to `/api/v2/submit-batch`.
- 中文：并发 ping 根地址选端点、使用 Keep-Alive、对 429/5xx 自动重试，提交到 `/api/v2/submit-batch`。

## Sample / 示例
```python
from flashblock_sendTransactions import flashblock_sendTransactions
ret = await flashblock_sendTransactions('Bearer YOUR_TOKEN', ['AaBU8zC90i...MAAAAAAAA='])
print('signatures:', ret['signatures'], 'status:', ret['status'], 'message:', ret['message'], 'ms:', ret['durationMs'], 'ep:', ret['endpoint'])
```
