package main

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


