package main

// English: Minimal Go client with endpoint selection, Keep-Alive, retry, and batch submit.
// 中文：最小化的 Go 客户端，包含端点选择、Keep-Alive、自动重试与批量提交。

import (
	"bytes"
	"context"
	"encoding/json"
	"net"
	"net/http"
	"sort"
	"time"
)

// Disclaimer / 免责声明
// English: This example only demonstrates how to use our product. It does not constitute trading
// advice or a trading/execution system. Use at your own risk. We are not responsible for any loss
// caused by using this code.
// 中文：本示例仅演示如何使用我们的产品，不构成任何交易建议或交易/执行系统。使用本代码所造成的任何损失，概不负责。

// English: Public endpoints; modify as needed.
// 中文：公开端点列表；可按需调整。
type Endpoint struct {
	Name    string
	BaseURL string
}

var endpoints = []Endpoint{
	{Name: "ny", BaseURL: "http://ny.flashblock.trade"},
	{Name: "slc", BaseURL: "http://slc.flashblock.trade"},
	{Name: "ams", BaseURL: "http://ams.flashblock.trade"},
	{Name: "fra", BaseURL: "http://fra.flashblock.trade"},
	{Name: "singapore", BaseURL: "http://singapore.flashblock.trade"},
	{Name: "london", BaseURL: "http://london.flashblock.trade"},
}

// English: Tip addresses; choose randomly to distribute support.
// 中文：小费地址列表；随机选择以便更公平地分配支持。
var tipAddresses = []string{
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
}

// English: Get a random tip address.
// 中文：获取一个随机小费地址。
func GetRandomTipAddress() string {
	return tipAddresses[int(time.Now().UnixNano())%len(tipAddresses)]
}

// English: Reusable HTTP client with Keep-Alive.
// 中文：复用 HTTP 客户端并启用 Keep-Alive。
var httpClient = &http.Client{
	Timeout: 10 * time.Second,
	Transport: &http.Transport{
		Proxy:               http.ProxyFromEnvironment,
		DialContext:         (&net.Dialer{Timeout: 5 * time.Second, KeepAlive: 15 * time.Second}).DialContext,
		MaxIdleConns:        256,
		MaxIdleConnsPerHost: 64,
		IdleConnTimeout:     30 * time.Second,
	},
}

type pingRes struct {
	EP Endpoint
	OK bool
	MS int64
}

// English: Ping root; success if 2xx.
// 中文：Ping 根路径；2xx 视为可用。
func ping(ep Endpoint) pingRes {
	url := ep.BaseURL
	t0 := time.Now()
	ctx, cancel := context.WithTimeout(context.Background(), 1500*time.Millisecond)
	defer cancel()
	req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
	resp, err := httpClient.Do(req)
	ms := time.Since(t0).Milliseconds()
	if err != nil {
		return pingRes{EP: ep, OK: false, MS: ms}
	}
	defer resp.Body.Close()
	return pingRes{EP: ep, OK: resp.StatusCode >= 200 && resp.StatusCode < 300, MS: ms}
}

// English: Select fastest healthy endpoint (fallback to lowest latency).
// 中文：选择最快可用端点（或退化为最低延迟）。
func selectBestEndpoint(preferred string) Endpoint {
	if preferred != "" {
		for _, ep := range endpoints {
			if ep.Name == preferred {
				return ep
			}
		}
	}
	ch := make(chan pingRes, len(endpoints))
	for _, ep := range endpoints {
		go func(e Endpoint) { ch <- ping(e) }(ep)
	}
	results := make([]pingRes, 0, len(endpoints))
	for range endpoints {
		results = append(results, <-ch)
	}
	healthy := make([]pingRes, 0)
	for _, r := range results {
		if r.OK {
			healthy = append(healthy, r)
		}
	}
	list := results
	if len(healthy) > 0 {
		list = healthy
	}
	sort.Slice(list, func(i, j int) bool { return list[i].MS < list[j].MS })
	return list[0].EP
}

// English: HTTP submit with simple retry for 429/5xx.
// 中文：POST 提交；对 429/5xx 进行简单重试。
type submitResp struct {
	Status int
	Data   map[string]any
}

func submitBatch(baseURL, auth string, txs []string) (submitResp, error) {
	url := baseURL + "/api/v2/submit-batch"
	body, _ := json.Marshal(map[string]any{"transactions": txs})
	attempts := 0
	for {
		req, _ := http.NewRequest("POST", url, bytes.NewReader(body))
		req.Header.Set("Authorization", auth)
		req.Header.Set("Content-Type", "application/json")
		resp, err := httpClient.Do(req)
		if err != nil {
			if attempts < 2 {
				attempts++
				continue
			}
			return submitResp{}, err
		}
		defer resp.Body.Close()
		var m map[string]any
		_ = json.NewDecoder(resp.Body).Decode(&m)
		if resp.StatusCode == 429 || resp.StatusCode >= 500 {
			if attempts < 2 {
				attempts++
				continue
			}
		}
		return submitResp{Status: resp.StatusCode, Data: m}, nil
	}
}

// English: Extract signatures from top-level or data.signatures.
// 中文：从顶层或 data.signatures 中解析签名。
func extractSignatures(raw map[string]any) (bool, int64, string, []string) {
	top, ok := raw["data"].(map[string]any)
	if !ok {
		top = raw
	}
	success, _ := top["success"].(bool)
	codeF, _ := top["code"].(float64)
	message, _ := top["message"].(string)
	sigs := make([]string, 0)
	if d, ok := top["data"].(map[string]any); ok {
		if arr, ok := d["signatures"].([]any); ok {
			for _, x := range arr {
				if s, ok := x.(string); ok {
					sigs = append(sigs, s)
				}
			}
		}
	}
	if len(sigs) == 0 {
		if arr, ok := top["signatures"].([]any); ok {
			for _, x := range arr {
				if s, ok := x.(string); ok {
					sigs = append(sigs, s)
				}
			}
		}
	}
	return success, int64(codeF), message, sigs
}

// English: Public result shape for convenience method.
// 中文：便捷方法的统一返回结构。
type Result struct {
	Status     int
	Success    bool
	Code       int64
	Message    string
	Signatures []string
	DurationMs int64
	Endpoint   Endpoint
	Raw        map[string]any
}

// English: Convenience method; retry once on transport error.
// 中文：便捷方法；发生传输错误时重选端点再试一次。
func FlashblockSendTransactions(auth string, txs []string, preferred string) (Result, error) {
	ep := selectBestEndpoint(preferred)
	t0 := time.Now()
	res, err := submitBatch(ep.BaseURL, auth, txs)
	if err != nil {
		ep = selectBestEndpoint("")
		res, err = submitBatch(ep.BaseURL, auth, txs)
		if err != nil {
			return Result{}, err
		}
	}
	dur := time.Since(t0).Milliseconds()
	success, code, message, sigs := extractSignatures(res.Data)
	return Result{
		Status:     res.Status,
		Success:    success,
		Code:       code,
		Message:    message,
		Signatures: sigs,
		DurationMs: dur,
		Endpoint:   ep,
		Raw:        res.Data,
	}, nil
}
