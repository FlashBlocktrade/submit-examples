# Python 範例：flashblock_sendTransactions

- 方法檔案：`flashblock_sendTransactions.py`
- 入口：`main.py`（僅呼叫方法）

## 前置需求
- Python 3.9+
- 有效 `AUTH_HEADER`

英文文档：参见 [README.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/python/README.md)。

## 安裝與執行
```bash
cd python
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
AUTH_HEADER='Bearer YOUR_TOKEN' python main.py
```

## 方法
- `flashblock_sendTransactions(auth_header, transactions, preferred?)`
  - 併發 Ping 根地址選擇端點
  - Keep-Alive 連線
  - 對 429/5xx 自動重試
  - 提交到 `/api/v2/submit-batch`

## 範例
```python
from flashblock_sendTransactions import flashblock_sendTransactions
ret = await flashblock_sendTransactions('Bearer YOUR_TOKEN', ['AaBU8zC90i...MAAAAAAAA='])
print('signatures:', ret['signatures'], 'status:', ret['status'], 'message:', ret['message'], 'ms:', ret['durationMs'], 'ep:', ret['endpoint'])
```
