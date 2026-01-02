# Candleflip Game - Comprehensive Technical Documentation

**Source**: User-provided comprehensive documentation
**Date Captured**: December 25, 2025
**Status**: STAGED FOR INGESTION
**Priority**: P3 - Side Game (Not actively tracked)

---

## Overview

Candleflip is a multiplayer prediction game on rugs.fun (a Solana-based gambling platform) where players bet on whether a randomly generated candlestick will close above or below a 1.00x multiplier threshold. The game combines elements of traditional candlestick chart visualization with binary outcome betting.

---

## Game Concept

Candleflip presents a simplified version of financial market trading, where players predict the outcome of a single candlestick formation. Each game round generates a candlestick that can be either:

- **Bullish (Green)**: Close price higher than open price
- **Bearish (Red)**: Close price lower than open price

However, the visual appearance (color) may not directly correlate with the win condition, which is based solely on whether the final multiplier is over or under 1.00x.

---

## Core Game Mechanics

### Lobby System

#### Lobby Creation:
- Players create individual game lobbies using the "Create" button
- Each lobby supports configurable room numbers (1-10 rooms)
- Lobbies can be set to "Start immediately" using the lightning bolt icon
- Multiple lobbies can run simultaneously in the "Open Lobbies" section

#### Lobby States:
| State | Description |
|-------|-------------|
| **Waiting** | Lobby created, awaiting additional players (shows "Waiting..." status with prize pot and join button) |
| **Active** | Candle is forming/being generated |
| **Completed** | Result displayed with player profit/loss |

### Betting Interface

#### Bet Configuration:
- **Bet Amount Input**: Numeric input field (minimum 0.001 SOL)
- **Quick Bet Buttons**:
  - +0.01, +0.1, +1 (increment buttons)
  - 1/2 (half current bet)
  - X2 (double current bet)
  - MAX (maximum balance)
  - Clear (X button to reset)
- **Balance Display**: Shows current wallet balance (e.g., "0.000 SOL")
- **Currency**: SOL (Solana blockchain token)

#### Trend Selection:
- **Bullish** (Green button with upward arrow): Predict over 1.00x multiplier
- **Bearish** (Gray/dark button with downward arrow): Predict under 1.00x multiplier

### Room Configuration

#### Rooms Field:
- Number input with +/- controls
- Range: 1-10 rooms
- Each room represents a separate betting instance
- Allows players to place multiple bets simultaneously with the same prediction

---

## Visual Components

### Candlestick Display

Each lobby card shows:
- **Candlestick Chart Area**: Displays generated candle(s) in sequence
- **Dotted Baseline**: Represents the 1.00x threshold
- **Candle Elements**:
  - Body: Rectangle (green for bullish, red for bearish)
  - Wicks: Lines extending from body showing high/low points
  - Progressive rendering as the round progresses

### Lobby Cards

#### Information Display:
- **Security Badge**: Green shield icon (indicates verified/secure lobby)
- **Player Name**: Shows username (e.g., "SooDamnDelicious", "bgst1")
- **Bot Indicator**: Some players may have "Bot" badge
- **Prediction Indicator**: Green upward arrow or red downward arrow
- **Result Display**:
  - Win: "+X.XXX SOL" in green
  - Loss: "-X.XXX SOL" in red
- **Prize Pot**: Total SOL in the pot
- **Join Button**: "Join X.XXX SOL" (red button for joining waiting lobbies)
- **Provably Fair Seed**: Button to verify game fairness

---

## Win Conditions

The subtitle "Over/Under 1.00x wins" indicates:

| Outcome | Description |
|---------|-------------|
| **Win** | Player's prediction matches whether the candle closes above or below 1.00x |
| **Payout** | Appears to be approximately 1:1 (player receives their bet back plus profit) |
| **Loss** | Player loses their bet amount |

**Important Note**: Based on observations, the win condition is based on the multiplier threshold (1.00x), not the candle color. A player can bet "Bullish" and win even if the candle appears red, as long as the final multiplier meets the over/under condition.

---

## Technical Architecture

### Frontend Components

#### Page Structure:
- **Header**: Navigation bar with game mode selectors (Standard, BBC/Pinpoint, Candleflip)
- **Left Sidebar**: Chat interface with online user count
- **Main Content Area**: Game interface with betting controls
- **Lobby Grid**: Displays active and completed lobbies

#### Navigation:
- **URL Pattern**: https://rugs.fun/candleflip
- **Game Mode Switcher**: Buttons at top to switch between Standard, Pinpoint (BBC), and Candleflip

### Real-time Updates

#### WebSocket Connection:
- The game uses WebSocket for real-time updates (window.socketService detected)
- Lobby states update in real-time
- Candle formations animate progressively
- Player joins/results broadcast immediately

#### Data Synchronization:
- Open lobbies count updates dynamically (shown as badge number)
- Multiple simultaneous lobbies supported
- Cross-player visibility of all active games

---

## User Flow

### Creating and Playing a Game

1. **Set Bet Amount**: Enter or adjust SOL amount using controls
2. **Select Trend**: Choose Bullish or Bearish prediction
3. **Configure Rooms**: Set number of rooms (1-10)
4. **Create Lobby**: Click green "Create" button
5. **Wait for Candle**: System generates candlestick
6. **View Result**: Lobby card updates with profit/loss
7. **Next Round**: Can immediately create new lobby

### Joining Existing Lobby

1. **Browse Open Lobbies**: Scroll through waiting lobbies
2. **Check Prize Pot**: View potential winnings
3. **Click Join Button**: Pay entry fee (e.g., "Join 0.001 SOL")
4. **Select Prediction**: Choose Bullish or Bearish
5. **Wait for Result**: Candle generates and displays outcome

---

## Additional Features

### Provably Fair System
- Each lobby has "Provably fair seed" button
- Allows verification of game randomness
- Ensures transparent and verifiable outcomes

### Social Features
- **Live Chat**: Left sidebar with verified Discord users
- **Online Counter**: Shows active players (e.g., "Online (360)")
- **User Levels**: Players display level badges (e.g., "Level 14")
- **Social Links**: Discord, Twitter/X, Telegram integration

### Platform Features
- **Rugpass**: Tier system (e.g., "Tier 0" with stocking indicators)
- **Crates**: Bonus/reward system
- **Deposit/Withdraw**: Wallet management buttons
- **Golden Hour**: Timed promotional event indicator

---

## API/Backend Considerations

### Expected Endpoints (inferred)
- Lobby creation API
- Bet placement API
- Real-time candle generation service
- Win/loss calculation engine
- Wallet transaction processing (Solana blockchain)

### Data Models

#### Lobby Object (inferred):

```javascript
{
  lobbyId: string,
  creatorUsername: string,
  betAmount: number, // in SOL
  prediction: "bullish" | "bearish",
  rooms: number,
  status: "waiting" | "active" | "completed",
  prizePot: number,
  candleData: {
    open: number,
    high: number,
    low: number,
    close: number,
    multiplier: number
  },
  result: {
    won: boolean,
    payout: number
  }
}
```

---

## Game Variations Context

Candleflip is one of three game modes on rugs.fun:

| Mode | Description |
|------|-------------|
| **Standard** | Main trading game with BUY/SELL mechanics and progressive multiplier chart |
| **BBC (Pinpoint)** | Precision-based prediction game |
| **Candleflip** | Binary prediction game (this document's focus) |

---

## Design Patterns

### Visual Theme
- Dark background (navy/black)
- Neon accents (green for positive, red for negative)
- Festive Christmas decorations (snowflakes, colored lights)
- Candlestick motif consistent with financial trading interfaces

### UX Patterns
- Grid-based lobby display
- Progressive disclosure (lobbies expand with more info)
- Color-coded feedback (green=win/profit, red=loss)
- Quick-bet controls for rapid gameplay
- Persistent chat for community engagement

---

## Edge Cases and Considerations

### Balance Management
- Zero balance prevents lobby creation
- Insufficient funds handled at transaction level
- Wallet integration required for SOL deposits

### Concurrent Games
- Players can participate in multiple lobbies simultaneously
- Each lobby operates independently
- Results process asynchronously

### Fairness and Verification
- Provably fair seeds ensure transparency
- Blockchain transactions provide immutable record
- Community visibility of all outcomes

---

## Performance Characteristics

| Characteristic | Details |
|----------------|---------|
| **Real-time Updates** | Sub-second latency for lobby updates |
| **Scalability** | Supports hundreds of concurrent players |
| **Visual Performance** | Smooth candle animations |
| **Load Time** | Fast initial page load with progressive enhancement |

---

## Conclusion

This documentation provides a canonical reference for understanding the Candleflip game mechanics, technical architecture, and implementation details on the rugs.fun platform.

---

*Document created: December 25, 2025*
*Status: STAGED FOR INGESTION*
*Priority: P3 - Side Game (activate when main bot is operational)*
