# Rugs.fun: Complete Game Documentation
## A Comprehensive Guide to the Memecoin Crash Gambling Game

### Table of Contents
1. [Game Overview](#game-overview)
2. [Core Game Mechanics](#core-game-mechanics)
3. [Game Phases](#game-phases)
4. [Trading Interface](#trading-interface)
5. [The Side Bet System](#side-bet-system)
6. [Economic Model](#economic-model)
7. [Technical Specifications](#technical-specifications)
8. [Special Events and Features](#special-events)
9. [Player Experience](#player-experience)

---

## 1. Game Overview

### What is Rugs.fun?

Rugs.fun is an online gambling game that simulates the volatile lifecycle of Solana-based memecoins. The game combines elements of traditional "crash" gambling games with the excitement and terminology of cryptocurrency trading, creating a unique gambling experience that mirrors the fast-paced world of memecoin trading.

### Core Concept

- **Memecoin Simulation**: The game recreates the pump-and-dump dynamics of Solana memecoins (similar to those launched on platforms like pump.fun)
- **High Risk, High Reward**: Players can experience potential gains of hundreds of percent within seconds, but also face the constant risk of total loss
- **Transparent Gambling**: All participants understand and accept the high-risk nature of the game
- **Provably Fair**: Uses cryptographic algorithms to ensure game fairness and verifiability

---

## 2. Core Game Mechanics

### The Multiplier System

- **Starting Point**: Every game begins with a multiplier of exactly 1.00x
- **Price Movement**: The multiplier increases or decreases over time based on a predetermined algorithm
- **Visual Display**: Movements are shown on a traditional candlestick chart
- **No Volume Dependency**: Unlike real trading, the outcome is simulated and not dependent on player volume

### The "Rug" Event

- **Definition**: A "rug" (or "rug pull") is when the game suddenly ends, simulating a memecoin crash
- **Timing**: Can occur at any moment during the game
- **Consequence**: All active positions are liquidated at zero value
- **Inevitability**: Every game eventually ends in a rug event
- **Terminology**: Derived from crypto slang for when developers abandon a project and drain liquidity

### Position Management

- **Buying**: Players can purchase positions at the current multiplier
- **Selling**: Players can sell positions at any time during active gameplay
- **Trade Limits**:
  - Minimum: 0.001 SOL per trade
  - Maximum: 5.0 SOL per trade
  - No limit on number of trades per game
- **Profit/Loss**: Calculated as the difference between buy and sell multipliers

---

## 3. Game Phases

### Phase 1: Cooldown Period
- **Duration**: ~5 seconds after previous game ends
- **Purpose**: Settlement and preparation for next game
- **Player Actions**: No trading allowed

### Phase 2: Presale Phase
- **Duration**: Exactly 10 seconds
- **Entry Price**: Fixed at 1.00x multiplier
- **Allowed Actions**: 
  - Buy positions only (no selling)
  - Place side bets
- **Strategic Value**: Guaranteed entry at starting price

### Phase 3: Active Game
- **Start**: Automatically begins at tick 0 after presale
- **Initial Price**: Always 1.00x
- **Allowed Actions**:
  - Buy positions
  - Sell positions (including presale positions)
  - Place side bets
- **Duration**: Variable (0 to 5000 ticks theoretical maximum)
- **End Condition**: Rug event

### Phase Cycle
The game operates in a continuous loop:
```
Cooldown → Presale → Active Game → Rug → [Repeat]
```

---

## 4. Trading Interface

### Candlestick Chart Display

- **Chart Type**: Traditional OHLC (Open, High, Low, Close) candlestick chart
- **Candle Formation**: 
  - Each candle represents 5 ticks
  - This 5-tick grouping is called an "index"
- **Real-Time Updates**: Chart updates with each tick
- **No Volume Bars**: Since outcomes are predetermined, volume is not displayed

### Tick System Explained

- **Definition**: The fundamental unit of time in the game
- **Duration**: Each tick = 250 milliseconds (theoretical)
- **Candle Composition**: 5 ticks = 1 candle = 1.25 seconds
- **Game Measurement**: All game durations are measured in ticks
- **Tick Counter**: Displays current tick number during gameplay

### Trading Controls

- **Buy Button**: Purchase positions at current multiplier
- **Sell Button**: Liquidate positions at current multiplier
- **Amount Input**: Enter trade size (0.001 - 5.0 SOL)
- **Position Display**: Shows current position size and entry price
- **P&L Tracker**: Real-time profit/loss calculation

---

## 5. The Side Bet System

### Concept
The side bet is a separate wagering system where players bet on whether the game will rug within a specific time window.

### Mechanics

- **Bet Window**: 40 ticks (approximately 10 seconds)
- **Bet Timing**: Can be placed at any time during presale or active game
- **Bet Range**: 0.001 to 5.0 SOL
- **Payout Structure**: 5:1 (500% of bet amount)
- **Net Profit**: 400% of original bet if successful

### Rules and Restrictions

- **Single Bet Limit**: Only ONE active side bet allowed per player
- **Cooldown Period**: ~1 second between side bet attempts
- **Independence**: Side bets are separate from main positions
- **Simultaneous Positions**: Players can hold both main positions and side bets

### Strategic Considerations

- **Break-Even Probability**: 20% (1 in 5 bets must win)
- **No Cancellation**: Once placed, cannot be cancelled
- **Immediate Settlement**: Resolved as soon as outcome is determined

---

## 6. Economic Model

### House Revenue Structure

- **Trading Edge**: 0.05% fee on each tick of active positions
- **Rug Captures**: House claims all positions caught in rug events
- **Side Bet Edge**: Built into the 5:1 payout structure
- **Treasury Management**: Balances profits and losses across games

### Player Economics

- **Profit Mechanism**: Buy low, sell high before rug
- **Loss Scenarios**:
  - Caught in rug event (100% loss)
  - Selling below entry price
  - Failed side bets
- **Instant Settlement**: All transactions settle immediately in SOL

### Smart Contract Integration

- **Blockchain**: Operates on Solana
- **Wallet Integration**: Direct connection to player wallets
- **Transaction Speed**: Near-instant settlement
- **Transparency**: All transactions recorded on-chain

---

## 7. Technical Specifications

### PRNG (Pseudo-Random Number Generator) Parameters

- **Rug Probability**: 0.5% per tick (0.005)
- **Price Drift Range**: -2% to +3% per tick (-0.02 to 0.03)
- **Big Move Chance**: 12.5% probability
- **Big Move Range**: 15% to 25% price change (0.15 to 0.25)

### Game Duration Statistics

- **Theoretical Range**: 0 to 5000 ticks
- **Mean Duration**: ~280 ticks (approximately 70 seconds)
- **Instarug**: Games ending in ≤10 ticks
- **Long Games**: Can exceed 1500 ticks (6+ minutes)

### Timing Specifications

- **Tick Rate**: 250ms per tick (theoretical)
- **Actual Variance**: May vary due to server load
- **Candle Update**: Every 1.25 seconds (5 ticks)
- **Minimum Game**: Can end on tick 0

### Server Architecture

- **WebSocket Connection**: Real-time data streaming
- **Event Types**: 
  - gameStateUpdate (primary game data)
  - newTrade (individual trades)
  - playerUpdate (personal stats)
  - sideBet events
- **Latency Target**: <100ms for critical updates

---

## 8. Special Events and Features

### God Candle

- **Definition**: Extreme multiplier jump of 10x
- **Probability**: 0.001% chance per tick
- **Visual Effect**: Dramatic candle spike on chart
- **Impact**: Can create massive instant profits

### Instarug

- **Definition**: Games that end in 10 ticks or less
- **Frequency**: Varies based on algorithm
- **Special Rules**: May trigger different payout mechanics
- **Player Impact**: Presale players lose immediately

### Provably Fair System

- **Method**: SHA-256 cryptographic hashing
- **Components**:
  - Server seed (hidden until game ends)
  - Client seed (optional player input)
  - Game ID (unique identifier)
- **Verification**: Players can verify fairness post-game
- **Transparency**: All game outcomes can be independently verified

---

## 9. Player Experience

### Account Features

- **Authentication**: Secure login system
- **Wallet Connection**: Direct Solana wallet integration
- **Statistics Tracking**: 
  - Total games played
  - Win/loss ratio
  - Profit/loss history
  - Biggest wins/losses

### Social Features

- **Leaderboard**: Top players by profit
- **Recent Winners**: Display of successful trades
- **Chat System**: Player communication (if enabled)
- **Trade Feed**: Real-time display of all trades

### Responsible Gaming

- **Risk Warnings**: Clear disclosure of gambling nature
- **Loss Limits**: Optional self-imposed limits
- **Session Time**: Tracking of play duration
- **Reality Checks**: Periodic reminders of time/money spent

### Mobile Experience

- **Responsive Design**: Full functionality on mobile devices
- **Touch Controls**: Optimized for touchscreen trading
- **Performance**: Lightweight for mobile data usage
- **App Availability**: Web-based, no download required

---

## Summary

Rugs.fun creates a unique gambling experience by combining the mechanics of crash-style games with the terminology and excitement of memecoin trading. The game's appeal lies in its:

1. **Simplicity**: Easy to understand buy/sell mechanics
2. **Excitement**: Potential for massive multipliers
3. **Speed**: Games resolve in seconds to minutes
4. **Transparency**: Provably fair system
5. **Familiarity**: Uses crypto trading interface paradigms

Players must balance the thrill of riding multipliers higher against the ever-present risk of the rug pull, creating a high-stakes psychological challenge that mirrors the real-world dynamics of volatile cryptocurrency markets.

---

*Note: This documentation describes the game mechanics as of January 2025. Game parameters and features may be subject to change.*