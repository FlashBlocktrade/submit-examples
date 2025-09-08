# Rust Example: flashblock_sendTransactions

> Disclaimer / 免责声明
>
> English: This example only demonstrates how to use our product. It does not constitute trading advice or a trading/execution system. Use at your own risk. We are not responsible for any loss caused by using this code.
>
> 中文：本示例仅演示如何使用我们的产品，不构成任何交易建议或交易/执行系统。使用本代码所造成的任何损失，概不负责。

- Method file: `src/flashblock_sendTransactions.rs` (exports `run(auth, txs)`)
- Entry: `src/main.rs` (calls `run`)

Chinese documentation: see `README.zh.md`.

## Prerequisites
- Rust (stable)
- Valid `AUTH_HEADER`

## Run
```bash
cd rust
AUTH_HEADER='Bearer YOUR_TOKEN' cargo run
```

## Behavior
- Ping root, select fastest healthy endpoint
- Keep-Alive
- Retry 429/5xx
- Submit to `/api/v2/submit-batch`

## Sample
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
