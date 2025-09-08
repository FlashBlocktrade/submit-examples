// Disclaimer / 免責聲明
// English: This example only demonstrates how to use our product. It does not
// constitute trading advice or a trading/execution system. Use at your own risk.
// We are not responsible for any loss caused by using this code.
// 中文：本範例僅示範如何使用本產品，不構成任何交易建議或交易／執行系統。
// 使用本程式碼所造成的任何損失，概不負責。

mod flashblock_sendTransactions;
use flashblock_sendTransactions::{run};
use std::fs;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // English: Read real transactions (JSON array) as input entry.
    // 中文：範例入口，讀取實際交易（JSON 陣列）。
    // English: AUTH_HEADER is required; exit if missing or empty.
    // 中文：AUTH_HEADER 為必填；若缺失或為空則報錯退出。
    let auth_env = std::env::var("AUTH_HEADER").unwrap_or_else(|_| String::new());
    let auth = auth_env.trim().to_string();
    if auth.is_empty() {
        return Err(anyhow::anyhow!("missing AUTH_HEADER: please export AUTH_HEADER with your token"));
    }

    let args: Vec<String> = std::env::args().collect();
    let tx_file = if args.len() > 1 { &args[1] } else { "transactions.json" };

    let content = fs::read_to_string(tx_file).map_err(|e| {
        anyhow::anyhow!("failed to read transactions file '{}': {}", tx_file, e)
    })?;

    // English: Expected JSON array like ["base64_tx1", "base64_tx2"].
    // 中文：期望檔案內容為 JSON 陣列，例如：["base64_tx1", "base64_tx2"]。
    let txs: Vec<String> = serde_json::from_str(&content).map_err(|e| {
        anyhow::anyhow!("invalid JSON in '{}': {}'", tx_file, e)
    })?;

    if txs.is_empty() {
        return Err(anyhow::anyhow!("no transactions found in '{}'", tx_file));
    }

    // English: Submit the real transactions.
    // 中文：傳入真實交易集合。
    run(&auth, txs).await
}


