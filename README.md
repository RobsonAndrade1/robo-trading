# 🤖 RG Ultra — High-Frequency Crypto Trading \& Decision Support Engine

[!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[!\[Exchange](https://img.shields.io/badge/Exchange-Binance%20Futures-yellow.svg)](https://www.binance.com/)

> 🚀 \*\*RG Ultra (Radar \& Gatilho)\*\* is an institutional-grade decision-support and trading monitoring system engineered for Cryptocurrency Trading (\*\*BTC/USDT\*\*). It combines \*\*Global Macro Economics\*\*, \*\*Smart Money Concepts (SMC)\*\*, \*\*Real-Time Order Flow (CVD \& Imbalance)\*\*, and \*\*Multi-Timeframe Price Action\*\* into a multi-layered confluence engine to identify high-probability setups and protect trading capital.

\---

## 📸 Overview \& Execution Checklist

!\[Sniper Trading Checklist](assets/Captura%20de%20tela%202026-01-12%20142932.png)

\---

## 🛠️ Intelligence Architecture

The engine runs a **4-Layer Confluence Matrix** before issuing a trade verdict:

```
┌─────────────────────────────────────────────────────────────┐
│                   1. GLOBAL MACRO LAYER                     │
│         DXY/SPX Acceleration \& Inverse Correlation          │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  2. ORDER FLOW \& CVD LAYER                  │
│       1000-Trade Delta, Bid/Ask Imbalance \& Absorption      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│               3. SMART MONEY CONCEPTS (SMC)                 │
│         BOS, CHoCH Detection \& Open Interest Drops          │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│           4. TECHNICAL \& MULTI-TIMEFRAME (MTF)             │
│    Triple EMA (9/20/200), 30+ Candlestick Patterns (1M-4H)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  🎯 FINAL TRADE VERDICT                     │
│            BUY 🟢  |  SELL 🔴  |  NEUTRAL 🔵                │
└─────────────────────────────────────────────────────────────┘
```

### 1\. 🌐 Global Macro Layer

* **DXY \& SPX Correlation:** Tracks real-time acceleration of the US Dollar Index (DXY) and equity indices to anticipate broader institutional risk-on/risk-off sentiment.
* **Inverse Scoring Weight:** Adjusts trade confidence scores based on macroeconomic headwind/tailwind.

### 2\. 📊 Order Flow \& CVD Layer

* **Cumulative Volume Delta (CVD):** Evaluates buyer vs. seller aggression across the latest 1,000 market trades.
* **Order Book Imbalance:** Measures bid-ask volume differential across top 10–20 depth levels.
* **Absorption Lock (Trap Guard):** Invalidate BUY signals automatically when Delta turns negative during heavy order book bid absorption.

### 3\. 🛡️ Smart Money Concepts (SMC) Layer

* **Market Structure Breaks:** Real-time identification of Break of Structure (**BOS**) and Change of Character (**CHoCH**) on 5M/15M charts.
* **Open Interest (OI) Exhaustion:** Detects unwinding positions and potential institutional liquidation sweeps.

### 4\. 📈 Technical \& Multi-Timeframe Layer

* **Triple EMA Trend Filters:** Combines 9, 20, and 200 EMAs. Penalizes trade scores when prices operate counter to the 20 EMA.
* **30+ Candlestick Pattern Engine:** Native geometry scanner identifying Reversals (Hammers, Shooting Stars, Engulfing) and Continuations (Flags, Wedges).

\---

## 📂 Project Structure

```text
Robo\_Trading/
├── assets/
│   └── Captura de tela 2026-01-12 142932.png  # Execution Checklist Preview
├── src/
│   ├── rg.py         # 🤖 RG Ultra Super Robot Core Engine
│   ├── launcher.py   # 🚀 Multi-Process Central Launcher
│   ├── robo.py       # 🛠️ Gatilho (1M Scalp Execution Sniper)
│   ├── radar.py      # 📡 Radar (Liquidity Wall \& SMC Map)
│   └── sinais.py     # 📊 Sinais (MTF Analysis \& Chart Geometry)
├── .gitignore        # Git Exclusions
├── README.md         # Documentation
└── requirements.txt  # Python Dependencies
```

\---

## ⚙️ Module Breakdown

|Module|Script File|Purpose \& Responsibilities|
|-|-|-|
|**Super Robot Core**|`src/rg.py`|Main integrated engine running all 4 layers, scoring matrix, CVD calculations, and terminal state rendering.|
|**Launcher**|`src/launcher.py`|Central launcher orchestrating subprocess execution for concurrent multi-terminal monitoring.|
|**Gatilho**|`src/robo.py`|1-minute execution sniper focusing on 9/20 EMA crossovers and low-latency order flow entry alerts.|
|**Radar**|`src/radar.py`|Maps institutional order walls, stop-loss clusters, and 5M structural CHoCH/BOS shifts.|
|**Sinais**|`src/sinais.py`|Scans 15M, 1H, and 4H timeframes for 30+ candlestick patterns and volume exhaustion setups.|

\---

## 🚦 Decision Matrix \& Score Evaluation

|Verdict|Score Condition|Order Flow \& Absorption Requirement|
|-|-|-|
|🟢 **BUY**|`Score >= 6`|`Ratio > 1.0` + Positive Delta (No Seller Absorption)|
|🔴 **SELL**|`Score >= 6`|`Ratio < 1.0` + Negative Delta|
|🔵 **NEUTRAL**|`Score < 6`|Lack of macro or technical confluence|
|⚠️ **ABSORPTION**|`Ratio > 1.0`|Invalidated to Neutral when `Delta < 0`|

\---

## 💻 Installation \& Usage

### 1\. Requirements

* Python 3.10+
* Binance Futures API Key (**Read-Only**)

### 2\. Setup

```bash
# Clone the repository
git clone https://github.com/RobsonAndrade1/Robo\_Trading.git
cd Robo\_Trading

# Install required dependencies
pip install -r requirements.txt
```

### 3\. Execution Options

Run the full integrated core engine:

```bash
python src/rg.py
```

Or launch all individual process modules concurrently via the central launcher:

```bash
python src/launcher.py
```

\---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

