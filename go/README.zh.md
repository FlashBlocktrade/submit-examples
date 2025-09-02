# Go 示例：flashblock_sendTransactions

- 方法文件：`flashblock_sendTransactions.go`
- 入口：`main.go`（仅调用方法）

## 前置要求
- Go 1.21+
- 有效 `AUTH_HEADER`

英文文档：参见 [README.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/go/README.md)。

## 运行
```bash
cd go
AUTH_HEADER='Bearer YOUR_TOKEN' go run .
```

## 行为说明
- Ping 根地址选择最快端点
- Keep-Alive 连接复用
- 对 429/5xx 简单重试
- 提交 `/api/v2/submit-batch`

## 示例
```go
ret, err := FlashblockSendTransactions("Bearer YOUR_TOKEN", []string{"AaBU8zC90i...MAAAAAAAA="}, "")
fmt.Println("signatures:", ret.Signatures, "status:", ret.Status, "message:", ret.Message, "ms:", ret.DurationMs, "ep:", ret.Endpoint)
```
