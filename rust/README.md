# Rust Example: flashblock_sendTransactions

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
