package main

// Disclaimer / 免责声明
// English: This example only demonstrates how to use our product. It does not constitute trading
// advice or a trading/execution system. Use at your own risk. We are not responsible for any loss
// caused by using this code.
// 中文：本示例仅演示如何使用我们的产品，不构成任何交易建议或交易/执行系统。使用本代码所造成的任何损失，概不负责。

import (
	"encoding/json"
	"fmt"
	"os"
)

func main() {
	// English: AUTH_HEADER is required; exit if missing.
	// 中文：AUTH_HEADER 为必填；缺失或为空则退出。
	auth := os.Getenv("AUTH_HEADER")
	if auth == "" {
		fmt.Println("missing AUTH_HEADER: please export AUTH_HEADER with your token")
		os.Exit(1)
	}

	// English: Read transactions from JSON file (first CLI arg) or default to transactions.json
	// 中文：从 JSON 文件读取交易（第一个命令行参数），默认为 transactions.json
	txFile := "transactions.json"
	if len(os.Args) > 1 {
		txFile = os.Args[1]
	}
	var txs []string
	f, err := os.ReadFile(txFile)
	if err != nil {
		fmt.Println("failed to read transactions file:", err)
		os.Exit(1)
	}
	if err := json.Unmarshal(f, &txs); err != nil || len(txs) == 0 {
		fmt.Println("invalid or empty transactions in '", txFile, "'")
		os.Exit(1)
	}

	ret, err := FlashblockSendTransactions(auth, txs, "")
	if err != nil {
		fmt.Println("error:", err)
		os.Exit(1)
	}
	tip := GetRandomTipAddress()
	fmt.Println("signatures:", ret.Signatures, "status:", ret.Status, "message:", ret.Message, "ms:", ret.DurationMs, "ep:", ret.Endpoint)
	fmt.Println("tipAddress:", tip)
}
