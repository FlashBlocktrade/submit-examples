"""
Disclaimer / 免责声明
English: This example only demonstrates how to use our product. It does not constitute trading
advice or a trading/execution system. Use at your own risk. We are not responsible for any loss
caused by using this code.
中文：本示例仅演示如何使用我们的产品，不构成任何交易建议或交易/执行系统。使用本代码所造成的任何损失，概不负责。
"""

import asyncio
import json
import os
import random
from typing import List

from flashblock_sendTransactions import (
    flashblock_sendTransactions,
    get_random_tip_address,
)

# English: Tip addresses; choose randomly to distribute support.
# 中文：小费地址列表；随机选择以便更公平地分配支持。
TIP_ADDRESSES = [
    "FLaShB3iXXTWE1vu9wQsChUKq3HFtpMAhb8kAh1pf1wi",
    "FLashhsorBmM9dLpuq6qATawcpqk1Y2aqaZfkd48iT3W",
    "FLaSHJNm5dWYzEgnHJWWJP5ccu128Mu61NJLxUf7mUXU",
    "FLaSHR4Vv7sttd6TyDF4yR1bJyAxRwWKbohDytEMu3wL",
    "FLASHRzANfcAKDuQ3RXv9hbkBy4WVEKDzoAgxJ56DiE4",
    "FLasHstqx11M8W56zrSEqkCyhMCCpr6ze6Mjdvqope5s",
    "FLAShWTjcweNT4NSotpjpxAkwxUr2we3eXQGhpTVzRwy",
    "FLasHXTqrbNvpWFB6grN47HGZfK6pze9HLNTgbukfPSk",
    "FLAshyAyBcKb39KPxSzXcepiS8iDYUhDGwJcJDPX4g2B",
    "FLAsHZTRcf3Dy1APaz6j74ebdMC6Xx4g6i9YxjyrDybR",
]


async def main():
    # English: AUTH_HEADER is required; exit if missing.
    # 中文：AUTH_HEADER 为必填；缺失或为空则退出。
    auth = os.environ.get("AUTH_HEADER", "").strip()
    if not auth:
        raise SystemExit("missing AUTH_HEADER: please export AUTH_HEADER with your token")

    # English: Read transactions from JSON file (first CLI arg) or default to transactions.json
    # 中文：从 JSON 文件读取交易（第一个命令行参数），默认为 transactions.json
    import sys
    tx_file = sys.argv[1] if len(sys.argv) > 1 else "transactions.json"
    try:
        with open(tx_file, "r", encoding="utf-8") as f:
            txs: List[str] = json.load(f)
    except Exception as e:
        raise SystemExit(f"failed to read transactions file '{tx_file}': {e}")
    if not isinstance(txs, list) or not txs:
        raise SystemExit(f"invalid or empty transactions in '{tx_file}'")

    ret = await flashblock_sendTransactions(auth, txs)
    tip = get_random_tip_address()
    print(
        "signatures:", ret["signatures"],
        "status:", ret["status"],
        "message:", ret["message"],
        "ms:", ret["durationMs"],
        "ep:", ret["endpoint"],
    )
    print("tipAddress:", tip)


if __name__ == "__main__":
    asyncio.run(main())

# For pip console_script entry point
def run():
    asyncio.run(main())


