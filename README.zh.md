# Flashblock 示例（中文）

`examples` 目录是本项目的主要使用入口，提供 NodeJS、Python、Rust、Go 的可运行示例。

每个示例均实现：
- 端点选择（Ping 根地址）
- HTTP Keep-Alive 长连接
- 对 429/5xx 的简单重试
- 调用 `/api/v2/submit-batch` 进行批量提交

安装与运行方法请查看各示例目录内的 README。

## 快速开始
- NodeJS: `npm run example:node`
- Python: `npm run example:py`
- Go: `npm run example:go`
- Rust: `npm run example:rust`

运行前请设置环境变量 `AUTH_HEADER`。
