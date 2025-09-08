# Python 示例：flashblock_sendTransactions

- 方法文件：`flashblock_sendTransactions.py`
- 入口：`main.py`（仅调用方法）

## 前置要求
- Python 3.9+
- 有效 `AUTH_HEADER`

英文文档：参见 [README.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/python/README.md)。

## 安装与运行
```bash
cd python
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
AUTH_HEADER='YOUR_TOKEN' python main.py
```

## 方法
- `flashblock_sendTransactions(auth_header, transactions, preferred?)`
  - 并发 Ping 根地址选择端点
  - Keep-Alive 连接
  - 对 429/5xx 自动重试
  - 提交到 `/api/v2/submit-batch`

## 示例
```python
from flashblock_sendTransactions import flashblock_sendTransactions
ret = await flashblock_sendTransactions('YOUR_TOKEN', ['AaBU8zC90i...MAAAAAAAA='])
print('signatures:', ret['signatures'], 'status:', ret['status'], 'message:', ret['message'], 'ms:', ret['durationMs'], 'ep:', ret['endpoint'])
```
