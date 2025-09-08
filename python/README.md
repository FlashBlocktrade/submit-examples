# Python Example: flashblock_sendTransactions

- Method file: `flashblock_sendTransactions.py`; entry: `main.py` (calls the method)

Chinese documentation: see [README.zh.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/python/README.zh.md).

## Prerequisites / 前置要求
- EN: Python 3.9+, valid `AUTH_HEADER` (raw token, no "Bearer")
- 中文：Python 3.9+，准备有效的 `AUTH_HEADER`（原始 token，不带 "Bearer"）

## Install & Run
```bash
cd python
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
AUTH_HEADER='YOUR_TOKEN' python main.py
```

## Method
- `flashblock_sendTransactions(auth_header, transactions, preferred?)`

- It selects the fastest healthy endpoint (ping root), uses Keep-Alive, retries 429/5xx, and submits to `/api/v2/submit-batch`.

## Sample
```python
from flashblock_sendTransactions import flashblock_sendTransactions
ret = await flashblock_sendTransactions('YOUR_TOKEN', ['AaBU8zC90i...MAAAAAAAA='])
print('signatures:', ret['signatures'], 'status:', ret['status'], 'message:', ret['message'], 'ms:', ret['durationMs'], 'ep:', ret['endpoint'])
```
