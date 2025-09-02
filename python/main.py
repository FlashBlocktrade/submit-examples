"""
English: Demo entry for Python — calls flashblock_sendTransactions and prints result.
中文：Python 演示入口——调用 flashblock_sendTransactions 并打印结果。
Usage/用法:
  AUTH_HEADER='Bearer YOUR_TOKEN' python main.py
Optional preferred endpoint/可选首选端点:
  修改调用传入第三参数，如 preferred='fra'
"""
import asyncio
import os
from typing import List

from flashblock_sendTransactions import flashblock_sendTransactions

async def main():
    auth = os.environ.get("AUTH_HEADER", "Bearer YOUR_TOKEN")
    txs: List[str] = ["AaBU8zC90i...MAAAAAAAA="]
    ret = await flashblock_sendTransactions(auth, txs)
    print("signatures:", ret["signatures"], "status:", ret["status"], "message:", ret["message"], "ms:", ret["durationMs"], "ep:", ret["endpoint"])

if __name__ == "__main__":
    asyncio.run(main())


