# Aave V3 Rate Monitor

Telegram bot that monitors Aave V3 lending protocol across multiple chains and sends real-time updates.

## What it tracks
- Total Value Locked (TVL) per chain
- Borrowed amount per chain  
- Utilization Rate (warns if >80%)

## Supported chains
- Ethereum
- Arbitrum
- Base
- Polygon

## How it works
Fetches data from DeFi Llama API every 30 minutes and sends formatted report to Telegram.

## Setup
1. Clone the repository
2. Install dependencies: pip install requests python-dotenv
3. Copy .env.example to .env and fill in your values
4. Create Telegram bot via @BotFather and get token
5. Get your Chat ID via @userinfobot
6. Run: python monitor.py

## Data source
[DeFi Llama](https://defillama.com) — open source DeFi analytics
