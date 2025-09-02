# Go Example: flashblock_sendTransactions / Go 示例

- EN: Helper file: `flashblock_sendTransactions.go`; entry: `main.go` (calls helper)
- 中文：方法文件 `flashblock_sendTransactions.go`；入口 `main.go`（仅调用方法）

## Prerequisites / 前置要求
- EN: Go 1.21+, valid `AUTH_HEADER`
- 中文：Go 1.21+，准备有效的 `AUTH_HEADER`

## Run / 运行
```bash
cd examples/go
AUTH_HEADER='Bearer YOUR_TOKEN' go run .
```

## Behavior / 行为
- EN: Ping root, select fastest endpoint, Keep-Alive, retry 429/5xx, submit `/api/v2/submit-batch`.
- 中文：Ping 根地址、选择最快端点、Keep-Alive、429/5xx 重试、提交 `/api/v2/submit-batch`。

## Sample / 示例
```go
ret, err := FlashblockSendTransactions("Bearer YOUR_TOKEN", []string{"AaBU8zC90i...MAAAAAAAA="}, "")
fmt.Println("signatures:", ret.Signatures, "status:", ret.Status, "message:", ret.Message, "ms:", ret.DurationMs, "ep:", ret.Endpoint)
```
