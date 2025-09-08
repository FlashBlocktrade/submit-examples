// Disclaimer / 免責聲明
// English: This example only demonstrates how to use our product. It does not
// constitute trading advice or a trading/execution system. Use at your own risk.
// We are not responsible for any loss caused by using this code.
// 中文：本範例僅示範如何使用本產品，不構成任何交易建議或交易／執行系統。
// 使用本程式碼所造成的任何損失，概不負責。

// English: Minimal Rust client using reqwest; includes endpoint selection, Keep-Alive, retry, batch submit.
// 中文：最小化的 Rust 用戶端（reqwest），包含端點選擇、Keep-Alive、自動重試與批次提交。
use reqwest::{Client, StatusCode};
use serde_json::Value;
use std::time::Instant;
use rand::{seq::SliceRandom, thread_rng};

#[derive(Clone)]
pub struct Endpoint { pub name: &'static str, pub base: &'static str }

// English: Public endpoints; modify as needed.
// 中文：公開端點清單；可按需調整。
pub static ENDPOINTS: &[Endpoint] = &[
    Endpoint { name: "ny", base: "http://ny.flashblock.trade" },
    Endpoint { name: "slc", base: "http://slc.flashblock.trade" },
    Endpoint { name: "ams", base: "http://ams.flashblock.trade" },
    Endpoint { name: "fra", base: "http://fra.flashblock.trade" },
    Endpoint { name: "singapore", base: "http://singapore.flashblock.trade" },
    Endpoint { name: "london", base: "http://london.flashblock.trade" },
];

// English: Tip addresses; choose randomly to distribute support.
// 中文：打賞地址清單；隨機選擇以更公平地分配支持。
static TIP_ADDRESSES: &[&str] = &[
    "FLaShB3iXXTWE1vu9wQsChUKq3HFtpMAhb8kAh1pf1wi",
    "FLashhsorBmM9dLpuq6qATawcpqk1Y2aqaZfkd48iT3W",
    "FLaSHJNm5dWYzEgnHJWWJP5ccu128Mu61NJLxUf7mUXU",
    "FLaSHR4Vv7sttd6TyDF4yR1bJyAxRwWKbohDytEMu3wL",
    "FLASHRzANfcAKDuQ3RXv9hbkBy4WVEKDzoAgxJ56DiE4",
    "FLasHstqx11M8W56zrSEqkCyhMCCpr6ze6Mjdvqope5s",
    "FLAShWTjcweNT4NSotpjpxAkwxUr2we3eXQGhpTVzRwy",
    "FLasHXTqrbNvpWFB6grN47HGZfK6pze9HLNTgbukfPSk",
    "FLAshyAyBcKb39KPxSzXcepiS8iDYUhDGwJcJDPX4g2B",
    "FLAsHZTRcf3Dy1APaz6j74ebdMC6Xx4g6i9YxjyrDybR",
];

fn select_random_tip_address() -> &'static str {
    let mut rng = thread_rng();
    // Safety: TIP_ADDRESSES is non-empty.
    TIP_ADDRESSES.choose(&mut rng).copied().unwrap_or(TIP_ADDRESSES[0])
}

// English: Ping the root; success if HTTP 2xx.
// 中文：Ping 根路徑；2xx 視為可用。
async fn ping(client: &Client, ep: &Endpoint) -> (Endpoint, bool, u128) {
    let url = ep.base.to_string();
    let t0 = Instant::now();
    let ok = match client.get(&url).send().await { Ok(r) => r.status().is_success(), Err(_) => false };
    (ep.clone(), ok, t0.elapsed().as_millis())
}

// English: Select fastest healthy endpoint (fallback to lowest latency).
// 中文：選擇最快可用端點（或退化為最低延遲）。
async fn select_best_endpoint(client: &Client) -> Endpoint {
    let futs = ENDPOINTS.iter().map(|e| ping(client, e));
    let results = futures::future::join_all(futs).await;
    let mut healthy: Vec<_> = results.iter().filter(|(_, ok, _)| *ok).collect();
    if healthy.is_empty() {
        let mut all = results.clone();
        all.sort_by_key(|(_, _, ms)| *ms);
        return all[0].0.clone();
    }
    healthy.sort_by_key(|(_, _, ms)| *ms);
    healthy[0].0.clone()
}

// English: Parse response and extract signatures from top-level or data.signatures.
// 中文：解析回應，相容頂層或 data.signatures 的簽名欄位。
fn extract_signatures(v: &Value) -> (bool, i64, String, Vec<String>) {
    let top = v.get("data").unwrap_or(v);
    let success = top.get("success").and_then(|x| x.as_bool()).unwrap_or(false);
    let code = top.get("code").and_then(|x| x.as_i64()).unwrap_or(0);
    let message = top.get("message").and_then(|x| x.as_str()).unwrap_or("").to_string();
    let mut sigs: Vec<String> = vec![];
    if let Some(d) = top.get("data").and_then(|x| x.as_object()) {
        if let Some(arr) = d.get("signatures").and_then(|x| x.as_array()) {
            sigs = arr.iter().filter_map(|s| s.as_str().map(|s| s.to_string())).collect();
        }
    }
    if sigs.is_empty() {
        if let Some(arr) = top.get("signatures").and_then(|x| x.as_array()) {
            sigs = arr.iter().filter_map(|s| s.as_str().map(|s| s.to_string())).collect();
        }
    }
    (success, code, message, sigs)
}

// English: Convenience function; retry once on transport error.
// 中文：便捷方法；傳輸錯誤時重選端點再試一次。
pub async fn run(auth_header: &str, transactions: Vec<String>) -> anyhow::Result<()> {
    let client = Client::builder()
        .pool_max_idle_per_host(64)
        .tcp_keepalive(Some(std::time::Duration::from_secs(15)))
        .timeout(std::time::Duration::from_secs(10))
        .build()?;

    let best = select_best_endpoint(&client).await;
    let url = format!("{}/api/v2/submit-batch", best.base);
    let t0 = Instant::now();
    let mut attempts = 0u8;
    let (status, body) = loop {
        let resp = client.post(&url)
            .header("Authorization", auth_header)
            .json(&serde_json::json!({"transactions": transactions}))
            .send().await?;
        let status = resp.status();
        let json: Value = resp.json().await.unwrap_or(Value::Null);
        if status == StatusCode::TOO_MANY_REQUESTS || status.is_server_error() {
            if attempts < 2 { attempts += 1; continue; }
        }
        break (status.as_u16(), json);
    };
    let dur = t0.elapsed().as_millis();
    let (success, code, message, signatures) = extract_signatures(&body);
    let tip = select_random_tip_address();
    println!("status: {status}, success: {success}, code: {code}, message: {message}");
    println!("endpoint: {} ({}), durationMs: {}", best.name, best.base, dur);
    println!("signatures: {:?}", signatures);
    println!("tipAddress: {}", tip);
    Ok(())
}


