# Rust 示例：flashblock_sendTransactions

- 方法文件：`src/flashblock_sendTransactions.rs`（导出 `run(auth, txs)`）
- 入口：`src/main.rs`（仅调用 `run`）

## 前置要求
- Rust（stable）
- 有效 `AUTH_HEADER`

英文文档：参见 [README.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/rust/README.md)。

## 运行
```bash
cd rust
AUTH_HEADER='Bearer YOUR_TOKEN' cargo run
```

## 行为说明
- 并发 Ping 根地址选择最近端点
- Keep-Alive 连接
- 对 429/5xx 自动重试
- 提交 `/api/v2/submit-batch`

## 示例
```rust
mod flashblock_sendTransactions;
use flashblock_sendTransactions::run;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let auth = std::env::var("AUTH_HEADER").unwrap_or_else(|_| "Bearer YOUR_TOKEN".to_string());
    let txs = vec!["AaBU8zC90i...MAAAAAAAA=".to_string()];
    run(&auth, txs).await
}
```
