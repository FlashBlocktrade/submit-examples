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


