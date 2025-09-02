package main

// English: Demo entry for Go — calls FlashblockSendTransactions and prints result.
// 中文：Go 示範入口——呼叫 FlashblockSendTransactions 並列印結果。
// Usage/用法:
//   AUTH_HEADER='Bearer YOUR_TOKEN' go run .
import (
    "fmt"
    "os"
)

func main() {
    auth := os.Getenv("AUTH_HEADER")
    if auth == "" { auth = "Bearer YOUR_TOKEN" }
    txs := []string{"AaBU8zC90i...MAAAAAAAA="}

    ret, err := FlashblockSendTransactions(auth, txs, "")
    if err != nil { fmt.Println("error:", err); os.Exit(1) }
    fmt.Println("signatures:", ret.Signatures, "status:", ret.Status, "message:", ret.Message, "ms:", ret.DurationMs, "ep:", ret.Endpoint)
}


