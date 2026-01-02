# Comprehensive Documentation: Rugs.fun Bear Bull Crab (BBC) Game

**Source**: User-provided comprehensive documentation
**Date Captured**: December 25, 2025
**Status**: STAGED FOR INGESTION
**Priority**: P3 - Side Game (Not actively tracked)

---

## Overview

| Attribute | Value |
|-----------|-------|
| Game Name | Bear Bull Crab (BBC) |
| Platform | Rugs.fun |
| URL | https://rugs.fun/bearbullcrab |
| Currency | SOL (Solana) |
| Technology Stack | React-based web application |
| Game Type | Multiplayer prediction/betting game with provably fair randomization |

---

## Game Concept

Bear Bull Crab (BBC) is a multiplayer betting game where players predict the outcome of a randomized result among three options: Bull (green), Bear (red), or Crab (yellow/gold). The game is described by the developers as similar to the popular "Crash" game, but with the ability to buy and sell positions at any time without getting "rugged" (a crypto gambling term for losing everything).

---

## Game Mechanics

### Three Betting Options

Players can place bets on three outcomes:

#### BULL (Green) - Bull icon (🦬)
- **Multiplier**: 2x
- **Win condition**: Chart moves up/bull wins

#### BEAR (Red) - Bear icon (🐻)
- **Multiplier**: 2x
- **Win condition**: Chart moves down/bear wins

#### CRAB (Yellow/Gold) - Crab icon (🦀)
- **Multiplier**: 14x
- **Win condition**: Chart moves sideways/crab wins (rarest outcome)

### Betting Process

The game operates in distinct phases:

#### 1. Betting Phase - "PLACE YOUR BETS"
- Players have a countdown timer (visible in top center)
- Players can place bets on Bull, Bear, or Crab
- Betting interface shows three large colored buttons (green, yellow, red)
- Each button displays: "PLACE BET" and "WIN [multiplier]x"

#### 2. Roll Phase - "ROLL!"
- Large text displays "ROLL!" in the center
- Game executes the randomization
- Visual effects appear during the roll

#### 3. Result Phase - "[OUTCOME] WINS!"
- Displays the winning option (e.g., "BULL WINS!")
- Shows number of winners and payouts
- Winners' usernames and amounts are displayed
- Losing bets are shown with negative amounts

---

## User Interface Layout

### Top Navigation Bar

**Left Side:**
- Rugs.fun logo with "BETA" badge
- Game mode indicators showing lit Christmas lights decoration (seasonal theme)

**Center:**
- Navigation arrows (< >)
- Current game status/timer display
- Status indicators (dots showing game progression)

**Right Side:**
- Golden Hour indicator (shows countdown to special event)
- Balance display (in SOL)
- "CRATES" button
- "WITHDRAW" button
- "DEPOSIT" button
- Username display (e.g., "N0m4D")
- Rugpass tier indicator
- Hamburger menu (☰)

### Left Sidebar - Chat & Players

- **Online Counter**: Shows number of players online (e.g., "Online (325)")
- **Social Links**: Discord, X (Twitter), Telegram icons
- **Live Chat**:
  - User avatars with level badges
  - Usernames with Discord verification indicators
  - User-defined tags/clans (e.g., "777", "FTHEDEVS")
  - Real-time chat messages
  - System announcements (crate wins, special events)
- **Bottom Controls**:
  - "Chat Rules" button
  - Provably Fair button (scales icon)
  - FAQ button
  - Muted List button
  - Sound toggle (shows "Sound On" with volume icon)
  - Network latency display (e.g., "229ms")

### Center - Main Game Area

#### Statistics Bar ("Last 100")
Shows distribution of last 100 rolls:
- Bull icon with count (e.g., "46")
- Bear icon with count (e.g., "46")
- Crab icon with count (e.g., "8")
- Color-coded circles showing recent roll history

#### Chart Display Area
- Large rectangular frame with red/orange border
- Dark background with animated stars/particles
- Displays candlestick-style chart showing game progression
- Horizontal dotted line at center (representing crab zone)
- Game ID displayed in top left corner (e.g., "...9f397581e5a9")
- Current countdown timer displayed as large white numbers
- Visual indicators for betting phase vs. result phase

#### Bet Control Panel
- **Balance Display**: Shows current SOL balance (e.g., "≡ 0.000")
- **Bet Amount Input Field**: Text box for entering bet amount (placeholder "0")
- **Clear Button**: "×" to reset bet amount
- **Quick Bet Buttons**:
  - "+0.001" - Add 0.001 SOL
  - "+0.01" - Add 0.01 SOL
  - "+0.1" - Add 0.1 SOL
  - "+1" - Add 1 SOL
  - "1/2" - Halve current bet
  - "X2" - Double current bet
  - "MAX" - Bet maximum balance
- **Balance Display (Right)**: Shows available balance with dropdown (▼)

#### Betting Buttons

Three large rectangular buttons arranged horizontally:

| Button | Icon | Text | Multiplier | Background |
|--------|------|------|------------|------------|
| BULL | 🦬 | "PLACE BET" / "WIN 2x" | 2x | Green with leaf/nature pattern |
| CRAB | 🦀 | "PLACE BET" / "WIN 14x" | 14x | Golden yellow with organic pattern |
| BEAR | 🐻 | "PLACE BET" / "WIN 2x" | 2x | Red with organic pattern |

#### Current Bets Display

Below each betting button:
- **Total Bets**: "X Bets Total"
- **Total Amount**: Shows SOL amount
- **Individual Bets**: Lists usernames and bet amounts
  - Player names (or "Anon" for anonymous)
  - Bet amounts with SOL icon
  - Positive amounts (+) for winners in green
  - Negative amounts (-) for losers in red

### Right Sidebar - Game History

- Vertical scrollable list showing recent game results
- Each entry shows:
  - Small circular icon (Bull, Bear, or Crab)
  - Partial game ID (e.g., "...062bc338")
  - Results displayed as icons
- **Pinpoint Feature**:
  - Circular indicator showing "75 0/5"
  - "BET 0.001 SOL"
  - "WIN 0.140 SOL"
  - Appears to be a special betting mode

---

## Game Modes

Rugs.fun offers three game modes accessible from the top navigation:

| Mode | Icon | Description |
|------|------|-------------|
| 🔥 Standard | Fire | Traditional crash-style game with BUY/SELL |
| 🐻🦬🦀 BBC | Animals | Three-outcome prediction game (this doc) |
| 🕯️ Candleflip | Candle | Coin flip with candlestick animation |

---

## Special Features

### Pinpoint Mode
- Special betting mechanism shown in right sidebar
- Displays as circular gauge (e.g., "75 0/5")
- Shows potential bet and win amounts
- Button to "Tap to toggle pinpoint"
- Appears to offer precision betting on specific outcomes

### Golden Hour
- Special event shown in top navigation
- Countdown timer (e.g., "in 57m 29s")
- Likely offers enhanced rewards or special conditions

### Rugpass System
- Tiered membership system (Tier 0-5+)
- Shows Christmas stockings as tier indicators
- Filled stockings = higher tier
- Affects rewards and daily gifts

### Crates System
- Loot box/reward system
- Can be opened for SOL prizes
- System announcements show big wins (e.g., "2 SOL")
- Different crate types (e.g., "Christmas2025 crate")

### Level System
- Players have levels (shown as badges)
- XP progression (e.g., "Level 14, 1,942/5,000 XP")
- Higher levels likely unlock benefits

---

## Technical Implementation

### Provably Fair System

The game uses a cryptographic provably fair system to ensure randomness:

**How It Works:**
1. **Before each game**: Server generates a random server seed
2. **Hash publication**: Server calculates and publishes a hash of the seed before the game starts
3. **Outcome determination**: Game outcome is determined by combining the seed with the game ID
4. **Seed reveal**: After the game ends, server reveals the original seed
5. **Verification**: Players can verify fairness by confirming:
   - The hash of the revealed seed matches the pre-published hash
   - Running the verification algorithm with the seed produces the same peak multiplier

**Verification Data Provided:**
- Game ID (unique identifier)
- Server Seed (revealed after game)
- Server Seed Hash (published before game)
- "Verify This Game" button links to third-party verification

**Example from captured data:**
```
Game ID: 20251226-f450d120ec1948b6
Server Seed Hash: c60c1d2354a9155146296?ba3220ea1872aa931d5?c4fce874bf696cb6f3149
```

### Architecture

| Component | Technology |
|-----------|------------|
| Frontend | React-based single-page application |
| Backend | WebSocket connection for real-time updates |
| Network | Built on Solana blockchain for SOL transactions |
| Theme System | Dynamic theming (Christmas, Halloween, Thanksgiving, Default) |
| Loading System | Progressive loading with animated progress bar |

### Game Timing

| Parameter | Value |
|-----------|-------|
| Tick Rate | 250ms per game tick |
| House Edge | Approximately 0.05% per tick (very small) |
| Network Latency | Displayed in real-time (e.g., "88ms", "229ms") |

---

## Gameplay Flow

### Complete Round Sequence

#### 1. Game Initialization
- Server generates and hashes server seed
- Game ID created
- Timer starts for betting phase

#### 2. Betting Phase (countdown period)
- Players see "PLACE YOUR BETS" message
- Large countdown number in center
- Players click betting buttons to place bets
- Bet amounts populate below each button
- Chat activity shows player discussions

#### 3. Betting Closes
- Timer reaches zero
- No more bets accepted
- System prepares for roll

#### 4. Roll Phase
- "ROLL!" text appears in large letters
- Visual effects and animations
- Chart begins to form
- Outcome being determined

#### 5. Result Revelation
- Chart completes showing result
- "[OUTCOME] WINS!" message displays
- Example: "BULL WINS!" with bull icon
- Candlestick pattern reveals whether bull (up), bear (down), or crab (sideways)

#### 6. Payout & Display
- Winners shown with green positive amounts
- Losers shown with red negative amounts
- Number of winners displayed (e.g., "4 Bets Total")
- System announcements for big wins
- Game added to history sidebar

#### 7. Next Round Preparation
- Previous result added to "Last 100" statistics
- New game ID generated
- Cycle repeats

---

## Visual Design Elements

### Color Scheme

| Element | Color |
|---------|-------|
| Primary Background | Dark navy/black (#14161a) |
| Bull/Win | Emerald green |
| Bear/Loss | Deep red |
| Crab/Rare | Golden yellow/orange |
| UI Elements | Purple/blue accents |
| Text | White primary, gray secondary |
| Borders | Gold/orange glow effects |

### Seasonal Theme (Christmas)
- Colorful string lights across top of page
- Snowflake decorations in corners
- Christmas-themed crates and gifts
- Filled stockings for Rugpass tiers
- Winter/holiday visual motifs

### Animations
- Particle effects (stars, snowflakes)
- Smooth transitions between game phases
- Glowing borders and buttons
- Countdown animations
- Chart drawing animations
- Win celebration effects

---

## Player Statistics & Analytics

### "Last 100" Distribution

Tracks the previous 100 game outcomes:
- Shows aggregate counts for each outcome
- Provides transparency about odds
- Helps players track patterns (though outcomes are random)
- Example observed: 46 Bulls, 46 Bears, 8 Crabs

### Game History
- Scrollable list of recent games
- Each game shows icon and partial ID
- Click on past game to view details
- Accessible verification data for each round

---

## Social Features

### Live Chat
- Real-time communication between players
- User levels displayed (1-70+)
- Clan/group tags
- Discord verification badges
- System announcements integrated
- Chat rules enforcement
- Mute functionality
- Emoji support

### Player Profiles
- Username display
- Level and XP tracking
- Rugpass tier
- Win/loss records (visible in bet displays)
- Profile view accessible via menu

### Community Integration
- Discord server link
- X (Twitter) account link
- Telegram group link
- Encourages community engagement

---

## Economic Model

### Currency & Transactions

| Aspect | Details |
|--------|---------|
| Base Currency | SOL (Solana) |
| Minimum Bet | 0.001 SOL |
| Deposits | Via Solana wallet connection |
| Withdrawals | Available at any time |
| House Edge | ~0.05% per tick |

### Reward Systems
- **Direct Winnings**: Multiplier-based payouts
- **Crates**: Random reward boxes
- **Daily Gifts**: For active players
- **Rugpass Benefits**: Tiered membership rewards
- **XP/Leveling**: Progression system
- **Special Events**: Golden Hour bonuses

---

## Security & Fairness

### Provably Fair Verification
- Cryptographic hash system
- Third-party verification available
- Complete transparency of game outcomes
- Immutable blockchain-based transactions
- Open verification for all games

### User Safety
- Wallet-based authentication
- No password vulnerabilities
- Solana blockchain security
- Real-time balance tracking
- Instant withdrawal capability

---

## Frequently Asked Questions (from game)

### Q: How does the game work?
A: Rugs.fun is similar to the popular game "Crash", except you can buy and sell any amount at any time. Just don't get rugged! Hold positions for longer periods to earn industry-leading rakebacks via crates. Charts are randomized with a provably fair system and cannot be influenced by buys or sells.

### Q: What's the house edge?
A: Every game tick (250ms) has a very small house edge built in - roughly 0.05%.

### Q: How does Bonus SOL work?
A: (Expandable section - not captured in detail)

### Q: What are crates and keys? What are Valid Bets?
A: (Expandable section - not captured in detail)

### Q: Is this a skill-based game?
A: (Expandable section - not captured in detail)

### Q: How do I know the game is fair?
A: The provably fair system with cryptographic hashing ensures games cannot be manipulated.

---

## Technical Specifications Summary

| Specification | Value |
|---------------|-------|
| Platform | Web-based (responsive design) |
| Framework | React |
| Blockchain | Solana |
| Real-time | WebSocket connections |
| Resolution | Responsive (tested at 999x695 viewport) |
| Browser Support | Modern browsers (Chrome, Firefox, Edge, Safari) |
| Mobile | Appears to support mobile devices |
| Load Time | Progressive loading with visual feedback |

---

## Developer Notes

### Code Structure
- Modular React component architecture
- Theme switching system (URL params, localStorage, date-based)
- Initial loading progress system
- Intercom integration for support
- Console logging for debugging
- Network request tracking

### Identified Files/Scripts
- Main React bundle
- Theme configuration scripts
- Loading progress controller
- Intercom messenger widget
- Event-based theme system (Halloween, Thanksgiving, Christmas)

### Performance Optimizations
- Progressive loading
- Lazy loading of assets
- Network latency monitoring
- Optimized tick rate (250ms)
- Efficient WebSocket usage

---

## Conclusion

Bear Bull Crab (BBC) on Rugs.fun is a sophisticated multiplayer betting game that combines elements of prediction gaming with cryptocurrency transactions. The game features a clean, intuitive interface with a strong emphasis on fairness through cryptographic verification, community engagement through live chat, and economic incentives through multiple reward systems. The seasonal theming and social features create an engaging environment for players, while the provably fair system and blockchain integration provide transparency and security.

---

*Document created: December 25, 2025*
*Status: STAGED FOR INGESTION*
*Priority: P3 - Side Game (activate when main bot is operational)*
