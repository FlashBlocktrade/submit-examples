# Rust 範例：flashblock_sendTransactions

> 免責聲明 / Disclaimer
>
> 中文：本範例僅示範如何使用本產品，不構成任何交易／執行系統。使用本程式碼所造成的任何損失，概不負責。
>
> English: This example only demonstrates how to use our product. It does not constitute trading advice or a trading/execution system. Use at your own risk. We are not responsible for any loss caused by using this code.

- 方法檔案：`src/flashblock_sendTransactions.rs`（匯出 `run(auth, txs)`）
- 入口：`src/main.rs`（僅呼叫 `run`）

## 前置需求
- Rust（stable）
- 有效 `AUTH_HEADER`

英文文件：參見 [README.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/rust/README.md)。

## 執行
```bash
cd rust
AUTH_HEADER='Bearer YOUR_TOKEN' cargo run
```

## 行為說明
- 併發 Ping 根地址選擇最近端點
- Keep-Alive 連線
- 對 429/5xx 自動重試
- 提交 `/api/v2/submit-batch`

## 範例
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
