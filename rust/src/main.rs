mod flashblock_sendTransactions;
use flashblock_sendTransactions::{run};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // 示例入口：仅调用方法
    let auth = std::env::var("AUTH_HEADER").unwrap_or_else(|_| "Bearer YOUR_TOKEN".to_string());
    let txs: Vec<String> = vec!["AaBU8zC90i...MAAAAAAAA=".to_string()];
    run(&auth, txs).await
}


