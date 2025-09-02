// English: Demo entry for Rust — calls run(auth, txs) and prints result inside library.
// 中文：Rust 示範入口——呼叫 run(auth, txs)，列印在函式庫內部完成。
// Usage/用法:
//   AUTH_HEADER='Bearer YOUR_TOKEN' cargo run
mod flashblock_sendTransactions;
use flashblock_sendTransactions::{run};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let auth = std::env::var("AUTH_HEADER").unwrap_or_else(|_| "Bearer YOUR_TOKEN".to_string());
    let txs: Vec<String> = vec!["AaBU8zC90i...MAAAAAAAA=".to_string()];
    run(&auth, txs).await
}


