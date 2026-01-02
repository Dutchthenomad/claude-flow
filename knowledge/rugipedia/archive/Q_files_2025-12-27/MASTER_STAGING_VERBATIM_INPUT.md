# MASTER STAGING DOCUMENT: Verbatim User Input & Context

**Date**: 2025-12-28
**Session**: WebSocket Documentation Enhancement (Questions 1-4)
**Purpose**: COMPLETE VERBATIM preservation of all user input, observations, and context for canonical review
**Status**: STAGED FOR CANONICAL REVIEW

---

## CRITICAL PRESERVATION NOTICE

This document contains the EXACT verbatim input from the user's DevTools captures and their contextual observations. This is the authoritative source for canonical review.

The structured analysis documents (Q1, Q2, Q3_Q4) contain interpreted summaries. THIS document contains the raw truth.

---

# QUESTION 1: Position Opening Events

## User's Verbatim Question Statement

> "The agent identified 4 position transition cases that must be handled:
>
> 1. Opening position (0 → positive): Record entry_tick = current_tick
>
> I will now show you an example of what a presale trade and sidebet look like when the presale is still active, then on tick 0, then tick 1."

## User's Context: Event Timing

> "this is directly between coolDownTimer:200 and coolDownTimer:100"

## User's Verbatim DevTools Capture: Event 1 (gameStatePlayerUpdate)

```
42["gameStatePlayerUpdate", {gameId: "20251227-65bd74ba1bc54708",…}]
0
:
"gameStatePlayerUpdate"
1
:
{gameId: "20251227-65bd74ba1bc54708",…}
gameId
:
"20251227-65bd74ba1bc54708"
leaderboardEntry
:
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, pnl: 0, pnlPercent: 0,…}
avgCost
:
1
hasActiveTrades
:
true
id
:
"did:privy:cma094vht019il80np6aidhqd"
level
:
14
pnl
:
0
pnlPercent
:
0
position
:
39
positionQty
:
0.001
selectedCoin
:
null
shortPosition
:
null
sideBet
:
{startedAtTick: 0, gameId: "20251227-65bd74ba1bc54708", end: 40, betAmount: 0.001, xPayout: 5,…}
betAmount
:
0.001
bonusPortion
:
0
coinAddress
:
"So11111111111111111111111111111111111111112"
end
:
40
gameId
:
"20251227-65bd74ba1bc54708"
realPortion
:
0.001
startedAtTick
:
0
xPayout
:
5
sidebetActive
:
true
totalInvested
:
0.002
username
:
"N0m4D"
rugpool
:
{instarugCount: 3, rugpoolAmount: 2.1897343695, totalEntries: 8270, threshold: 10,…}
```

## User's Observation: Event Ordering

> "It appears to me that after the coolDownTimer:100, it displays 3 events in this order: gameStatePlayerUpdate, playerUpdate, and gameStateUpdate."

## User's Verbatim DevTools Capture: Event 1 (Second Display)

```
42["gameStatePlayerUpdate", {gameId: "20251227-65bd74ba1bc54708",…}]
0
:
"gameStatePlayerUpdate"
1
:
{gameId: "20251227-65bd74ba1bc54708",…}
gameId
:
"20251227-65bd74ba1bc54708"
leaderboardEntry
:
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, pnl: 0, pnlPercent: 0,…}
avgCost
:
1
hasActiveTrades
:
true
id
:
"did:privy:cma094vht019il80np6aidhqd"
level
:
14
pnl
:
0
pnlPercent
:
0
position
:
39
positionQty
:
0.001
selectedCoin
:
null
shortPosition
:
null
sideBet
:
{startedAtTick: 0, gameId: "20251227-65bd74ba1bc54708", end: 40, betAmount: 0.001, xPayout: 5,…}
sidebetActive
:
true
totalInvested
:
0.002
username
:
"N0m4D"
```

## User's Verbatim DevTools Capture: Event 2 (playerUpdate)

```
42["playerUpdate",…]
0
:
"playerUpdate"
1
:
{id: "did:privy:cma094vht019il80np6aidhqd", role: null, cash: 0.097595869, bonusBalance: 0,…}
authenticated
:
true
autobuysEnabled
:
false
autosellPrice
:
null
avgCost
:
1
bonusBalance
:
0
bonusWagerReq
:
0
bonusWagered
:
0
cash
:
0.097595869
crateKeys
:
{gold: 0, diamond: 0, coal: 0, iron: 0, tier1: 0, tier0: 0}
cumulativePnL
:
0
hasInteracted
:
true
hitMaxWin
:
false
id
:
"did:privy:cma094vht019il80np6aidhqd"
levelInfo
:
{level: 14, xp: 1953, xpForNextLevel: 5000, totalXP: 31953}
leveragedPositions
:
[]
pnlPercent
:
-99.3217
positionQty
:
0.001
recentCrateRewards
:
[,…]
role
:
null
selectedCoin
:
null
shitcoinBalances
:
{0xPractice: 100}
0xPractice
:
100
shortPosition
:
null
sideBet
:
{startedAtTick: 0, gameId: "20251227-65bd74ba1bc54708", end: 40, betAmount: 0.001, xPayout: 5,…}
betAmount
:
0.001
bonusPortion
:
0
coinAddress
:
"So11111111111111111111111111111111111111112"
end
:
40
gameId
:
"20251227-65bd74ba1bc54708"
realPortion
:
0.001
startedAtTick
:
0
xPayout
:
5
sidebetPnl
:
0
sidebets
:
[]
totalInvested
:
0.002
xpBoost
:
{active: false, activeUntil: 0, available: 0}
```

## User's Verbatim DevTools Capture: Event 3 (gameStateUpdate tick 0)

```
42["gameStateUpdate",…]
0
:
"gameStateUpdate"
1
:
{active: true, price: 1, rugged: false, tickCount: 0, cooldownTimer: 0, cooldownPaused: false,…}
active
:
true
allowPreRoundBuys
:
false
connectedPlayers
:
244
cooldownPaused
:
false
cooldownTimer
:
0
gameId
:
"20251227-65bd74ba1bc54708"
gameVersion
:
"v3"
leaderboard
:
[]
partialPrices
:
{startTick: 0, endTick: 0, values: {0: 1}}
endTick
:
0
startTick
:
0
values
:
{0: 1}
0
:
1
pauseMessage
:
""
price
:
1
provablyFair
:
{serverSeedHash: "d74b42aabdce7c6d8aaea9d23aa3453a55ed7b1b19d8ebd0e1380178b7dc12ae", version: "v3"}
serverSeedHash
:
"d74b42aabdce7c6d8aaea9d23aa3453a55ed7b1b19d8ebd0e1380178b7dc12ae"
version
:
"v3"
rugged
:
false
tickCount
:
0
```

---

# QUESTION 2: Adding to Position

## User's Verbatim Question Statement

> "the second question is 2. Adding to position (positive → more positive): Keep original entry_tick"

## User's Scenario Description

> "The following is a series of events extremely close together at many points. In this example, I made a presale trade for .002 SOL, when the game began, the next thing I did was add to the position with another.002 at or about tick 11, then sold a few ticks later."

## User's Verbatim DevTools Capture: Event 1 (gameStatePlayerUpdate)

```
42["gameStatePlayerUpdate", {gameId: "20251228-242b2d81e73e4f27",…}]
0
:
"gameStatePlayerUpdate"
1
:
{gameId: "20251228-242b2d81e73e4f27",…}
gameId
:
"20251228-242b2d81e73e4f27"
leaderboardEntry
:
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14,
pnl: 0.000745529,…}
avgCost
:
1
hasActiveTrades
:
true
id
:
"did:privy:cma094vht019il80np6aidhqd"
level
:
14
pnl
:
0.000745529
pnlPercent
:
37.27645
position
:
39
positionQty
:
0.002
regularPnl
:
0.000745529
selectedCoin
:
null
shortPnl
:
0
shortPosition
:
null
sideBet
:
null
sidebetActive
:
null
sidebetPnl
:
0
totalInvested
:
0.002
username
:
"N0m4D"
```

## User's Observation: Features to Watch

> "As you can see, there are several features we should be observing. avgCost, hasActiveTrades:, pnl, pnlPercent, positionQty, regularPnl, and totalInvested."

## User's Context: DevTools Column Information

> "Now Im not sure if the separate columns in the Messages section in DevTools attaches the information in them, so I will add it for context just in case. The first column entitled "Data" contains the entire event in nested sections, the second column titled "Length": 2350, and the third is "Time": and it says 21:02:55.825."

## User's Verbatim DevTools Capture: Event 2 (buyOrder - CLIENT → SERVER)

**User's Metadata**: Length: 122, Time: 21:02:56.038

```
4229["buyOrder", {__trace: true, traceparent:
"00-55110064298fdee6dc04d093c003b5c9-2870159c41eb0cab-01"},…]
0
:
"buyOrder"
1
:
{__trace: true, traceparent:
"00-55110064298fdee6dc04d093c003b5c9-2870159c41eb0cab-01"}
traceparent
:
"00-55110064298fdee6dc04d093c003b5c9-2870159c41eb0cab-01"
__trace
:
true
2
:
{amount: 0.002}
amount
:
0.002
```

## User's Observation: Event Classification

> "I will show you the next novel event which Im not sure if it is in the canonical pedia, but is called "buyOrder" and is a message from us to the server. This should also be something we create a categorical sort for when we review this for canon verification in the next session and should be noted."

## User's Context: standard/newTrade Timing

> "This next event happened directly after the "buyOrder" and was the second of these 2 events entitled "standard/newTrade". The first was another player entering a trade named "Vmoney" for 0.569271328 SOL. This occured at 21:02:56.081 and the next "standard/newTrade" that my "buyOrder" was emmited by occured just a few microseconds later at 21:02:56.107."

## User's Verbatim DevTools Capture: Event 3 (standard/newTrade)

```
42["standard/newTrade",…]
0
:
"standard/newTrade"
1
:
{__trace: true, traceparent:
"00-55110064298fdee6dc04d093c003b5c9-65b220dcba23a3a0-01"}
traceparent
:
"00-55110064298fdee6dc04d093c003b5c9-65b220dcba23a3a0-01"
__trace
:
true
2
:
{id: "9111d2c8-efcc-449e-b081-0c8c59e0bc45", gameId:
"20251228-242b2d81e73e4f27",…}
amount
:
0.002
bonusPortion
:
0
coin
:
"solana"
gameId
:
"20251228-242b2d81e73e4f27"
id
:
"9111d2c8-efcc-449e-b081-0c8c59e0bc45"
level
:
14
leverage
:
1
playerId
:
"did:privy:cma094vht019il80np6aidhqd"
price
:
1.4444769765026393
qty
:
0.001384584
realPortion
:
0.002
tickIndex
:
16
type
:
"buy"
username
:
"N0m4D"
```

## User's Context: playerUpdate Timing and Observations

> "The next event occurs at 21:02:56.236, its length is 902, and the event is "playerUpdate" The features that stand out as what need to be paid attention to (not an explicit requirement) are: "authenticated", "avgCost", "cash", "cumulitivePnl", "pnlPercent", "positionQty", and "totalInvested". Cash being the current wallet balance, avgCost being an interesting number that appears to me to potentially be a lifetime profile tracking metric to see what my average profitability to the game. This is something Id like to investigate separtely in a different session. Also, positionQty appears to be the current value of my total trade position, however the pnlPercent makes me second guess this assumption."

## User's Verbatim DevTools Capture: Event 4 (playerUpdate)

**User's Metadata**: Length: 902, Time: 21:02:56.236

```
42["playerUpdate",…]
0
:
"playerUpdate"
1
:
{id: "did:privy:cma094vht019il80np6aidhqd", role: null, cash: 0.09503525,
bonusBalance: 0,…}
authenticated
:
true
autobuysEnabled
:
false
autosellPrice
:
null
avgCost
:
1.181828845
bonusBalance
:
0
bonusWagerReq
:
0
bonusWagered
:
0
cash
:
0.09503525
crateKeys
:
{gold: 0, diamond: 0, coal: 0, iron: 0, tier1: 0, tier0: 0}
cumulativePnL
:
0.000888953
hasInteracted
:
true
hitMaxWin
:
false
id
:
"did:privy:cma094vht019il80np6aidhqd"
levelInfo
:
{level: 14, xp: 1956, xpForNextLevel: 5000, totalXP: 31956}
level
:
14
totalXP
:
31956
xp
:
1956
xpForNextLevel
:
5000
leveragedPositions
:
[]
pnlPercent
:
44.44765
positionQty
:
0.003384584
recentCrateRewards
:
[,…]
role
:
null
selectedCoin
:
null
shitcoinBalances
:
{0xPractice: 100}
0xPractice
:
100
shortPosition
:
null
sideBet
:
null
sidebetPnl
:
0
sidebets
:
[]
totalInvested
:
0.004
xpBoost
:
{active: false, activeUntil: 0, available: 0}
active
:
false
activeUntil
:
0
available
:
0
```

## User's Verbatim DevTools Capture: Event 5 (gameStatePlayerUpdate after add)

**User's Metadata**: Length: 421, Time: 21:02:56.251

```
42["gameStatePlayerUpdate", {gameId: "20251228-242b2d81e73e4f27",…}]
0
:
"gameStatePlayerUpdate"
1
:
{gameId: "20251228-242b2d81e73e4f27",…}
gameId
:
"20251228-242b2d81e73e4f27"
leaderboardEntry
:
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, pnl: 0.000888953,…}
avgCost
:
1
hasActiveTrades
:
true
id
:
"did:privy:cma094vht019il80np6aidhqd"
level
:
14
pnl
:
0.000888953
pnlPercent
:
44.44765
position
:
39
positionQty
:
0.002
regularPnl
:
0.000888953
selectedCoin
:
null
shortPnl
:
0
shortPosition
:
null
sideBet
:
null
sidebetActive
:
null
sidebetPnl
:
0
totalInvested
:
0.002
username
:
"N0m4D"
```

## User's Verbatim DevTools Capture: Event 6 (success ACK)

**User's Metadata**: Length: 22, Time: 21:02:56.257

```
4329[{success: true}]
0
:
{success: true}
success
:
true
```

## User's Context: gameStateUpdate with gameHistory

> "I will add a bit more context now for good measure. The next gameStateUpdate occurs at timestamp 21:02:58.054 and has a massive length of 165280!!! It contains the "gameHistory" which contains novel information we absolutely need to mark as highly useful such as averageMultiplier, which is the average peak price of the last 100 games in a rolling window. connectedPlayers, the 4 "countdown--X" metrics that display how many games of the last 100 reached atleast 2x,10x,50x,and100x. It also contains a useful tracker thats going to be highly useful for studying aggregate data across thousands of games which is the godcandle."

## User's Verbatim DevTools Capture: GodCandle Fields

```
godCandle2x
:
null
godCandle2xMassiveJump
:
null
godCandle2xPrices
:
[]
godCandle2xTimestamp
:
null
godCandle10x
:
null
godCandle10xMassiveJump
:
null
godCandle10xPrices
:
[]
godCandle10xTimestamp
:
null
godCandle50x
:
null
godCandle50xMassiveJump
:
null
godCandle50xPrices
:
[]
godCandle50xTimestamp
:
null
```

## User's Observation: Deriving Timestamps

> "As we can see in this example, we can derive the timestamps of when these event occur (or the lack there of in this event)."

## User's Verbatim DevTools Capture: Daily High Fields

```
highestToday
:
1329.9752646165282
highestTodayTimestamp
:
1766855639499
```

## User's Note on Missing Data

> "I was going to provide one more playerGameStateUpdate but the browser was accidentally refreshed."

---

# QUESTIONS 3 & 4: Closing Position / Rug Sequence

## User's Verbatim Question Statement

> "The final 2 questions Im going to attempt to answer together:
> 3. Partial sell (positive → less positive): Keep entry_tick
> 4. Closing position (positive → 0): Reset entry_tick = None"

## User's Scenario Description

> "So in this example, I have both active trade positions, and an active sideBet when the game rugs so I captured the event that shows how sideBets are paid out as well."

## User's Verbatim DevTools Capture: Pre-Rug gameStateUpdate

**User's Metadata**: Time: 22:26:23.018, Length: 4368

```
42["gameStateUpdate",…]
0
:
"gameStateUpdate"
1
:
{active: true, price: 0.7205941557633537, partialPrices: {startTick: 268, endTick: 272,…},…}
active
:
true
allowPreRoundBuys
:
false
averageMultiplier
:
3.378798635001477
connectedPlayers
:
205
cooldownPaused
:
false
cooldownTimer
:
0
count2x
:
46
count10x
:
5
count50x
:
0
count100x
:
0
gameId
:
"20251228-d8d002aba86140ad"
leaderboard
:
[{id: "did:privy:cmen97eeo007tk20bklploj7i", username: "FLYBOI", level: 70, pnl: 5.487196608,…},…]
partialPrices
:
{startTick: 268, endTick: 272,…}
pauseMessage
:
""
price
:
0.7205941557633537
provablyFair
:
{serverSeedHash: "6f67e582cc3f4de0f4a0670975b94772a8f81603e2191aae8615bfabd9f3cfe3", version: "v3"}
rugRoyale
:
{status: "INACTIVE", activeEventId: null, currentEvent: null, upcomingEvents: [], events: []}
rugged
:
false
rugpool
:
{instarugCount: 0, threshold: 10, rugpoolAmount: 0}
tickCount
:
272
tradeCount
:
428
```

## User's Note: DevTools Artifact

> "MCP server
> Let your favourite coding agent debug your pages at runtime, using the Chrome DevTools MCP server.
>
> Improved trace sharing
> Optionally include resource content and script source maps in exported performance traces.
>
> Support for @starting-style
> Debug and identify CSS entry animations using the new adorner in the Elements panel."

*(Note: This appears to be DevTools UI artifact that was captured)*

## User's Verbatim DevTools Capture: gameStatePlayerUpdate with Active Sidebet

**User's Metadata**: Time: 22:26:23.029

```
42["gameStatePlayerUpdate", {gameId: "20251228-d8d002aba86140ad",…}]
0
:
"gameStatePlayerUpdate"
1
:
{gameId: "20251228-d8d002aba86140ad",…}
gameId
:
"20251228-d8d002aba86140ad"
leaderboardEntry
:
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, pnl: -0.001345501,…}
avgCost
:
0.879838878
hasActiveTrades
:
true
id
:
"did:privy:cma094vht019il80np6aidhqd"
level
:
14
pnl
:
-0.001345501
pnlPercent
:
-33.637525000000004
position
:
30
positionQty
:
0.002273142
regularPnl
:
-0.000345501
selectedCoin
:
null
shortPnl
:
0
shortPosition
:
null
sideBet
:
{startedAtTick: 264, gameId: "20251228-d8d002aba86140ad", end: 304, betAmount: 0.001, xPayout: 5,…}
sidebetActive
:
true
sidebetPnl
:
-0.001
totalInvested
:
0.004
username
:
"N0m4D"
```

## User's Verbatim DevTools Capture: currentSidebetResult (NEW EVENT)

**User's Metadata**: Time: 22:26:23.274

```
42["currentSidebetResult",…]
0
:
"currentSidebetResult"
1
:
{__trace: true, traceparent: "00-f89f16bbd99069674a9a54d709743847-3781631892f7fc03-01"}
traceparent
:
"00-f89f16bbd99069674a9a54d709743847-3781631892f7fc03-01"
__trace
:
true
2
:
{playerId: "did:privy:cma094vht019il80np6aidhqd", gameId: "20251228-d8d002aba86140ad",…}
betAmount
:
0.001
coinAddress
:
"So11111111111111111111111111111111111111112"
endTick
:
304
gameId
:
"20251228-d8d002aba86140ad"
level
:
14
payout
:
0.005
playerId
:
"did:privy:cma094vht019il80np6aidhqd"
price
:
0.009250309566210552
profit
:
0.004
startTick
:
264
tickIndex
:
273
timestamp
:
1766892383152
type
:
"payout"
username
:
"N0m4D"
xPayout
:
5
```

## User's Critical Context: Rug Sequence Description

> "After you review this, I still have a few more events to show you that are EXTREMELY INTERESTING to say the least!! They show how the game completes the rug event player calculation before emiting that the game active:false. It also essentially forces the player to enter a sell for their position at the final price which appears to be precalculated somehow due to the unique tiny remainder non-zero price."

## User's Event Sequence Description

> "It first provides a "playerUpdate" event at 22:26:23.286, then the forced sell event "standard/newTrade" at 22:26:23.295, the an additional "playerUpdate" at 22:26:23.295, then a "gameStatePlayerUpdate" at 22:26:23.305, a "rugPassQuestCompleted" at 22:26:23.309, then a gameStateUpdate at 22:26:23.449"

## User's Critical Observation: Delayed active:false

> "that still states 42["gameStateUpdate",…]
> 0
> :
> "gameStateUpdate"
> 1
> :
> {active: true, price: 0.009250309566210552, partialPrices: {startTick: 269, endTick: 273,…},… (DESPITE ALL THESE EVENTS TO END THE GAME OCCURING!!)."

## User's Continued Sequence Description

> "This is followed by a "gameStatePlayerUpdate" at timestamp 22:26:23.449, then an event that simply says 4358[] at timestamp 22:26:24.456. Then another "playerUpdate" at 22:26:24.605 followed by an emission from ourside as a 4259 ping at 22:26:24.456"

## User's Verbatim DevTools Capture: ping Event

```
4259["ping", {lastPing: 169.20000000298023}]
0
:
"ping"
1
:
{lastPing: 169.20000000298023}
lastPing
:
169.20000000298023
```

## User's Continued Description

> "Then ANOTHER "gameStateUpdate" that still states "active:true", a gameStatePlayerUpdate that appears to be the completed calculations for closing out my game positons."

## User's Verbatim DevTools Capture: Final gameStatePlayerUpdate (Position Closed)

```
42["gameStatePlayerUpdate", {gameId: "20251228-d8d002aba86140ad",…}]
0
:
"gameStatePlayerUpdate"
1
:
{gameId: "20251228-d8d002aba86140ad",…}
gameId
:
"20251228-d8d002aba86140ad"
leaderboardEntry
:
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, pnl: 0.0010210280000000002,…}
avgCost
:
0
hasActiveTrades
:
true
id
:
"did:privy:cma094vht019il80np6aidhqd"
level
:
14
pnl
:
0.0010210280000000002
pnlPercent
:
25.525700000000008
position
:
25
positionQty
:
0
regularPnl
:
-0.001978972
selectedCoin
:
null
shortPnl
:
0
shortPosition
:
null
sideBet
:
null
sidebetActive
:
null
sidebetPnl
:
0.003
totalInvested
:
0.004
username
:
"N0m4D"
```

## User's Final Context: Game End gameStateUpdate

> "then this is finally followed by a "gameStateUpdate" with the active:false emmited along with the coolDownTimer: 15000 (which is where it always begins. It states allowPreRoundBuys: False until it reaches 10000 at which point it flips to true. )"

## User's Verbatim DevTools Capture: Final gameStateUpdate (active:false)

```
42["gameStateUpdate", {gameHistory: [{id: "20251228-d8d002aba86140ad", timestamp: 1766892383603,…},…],…}]
0
:
"gameStateUpdate"
1
:
{gameHistory: [{id: "20251228-d8d002aba86140ad", timestamp: 1766892383603,…},…],…}
active
:
false
allowPreRoundBuys
:
false
availableShitcoins
:
[{address: "0xPractice", ticker: "FREE", name: "Practice SOL", max_bet: 10000, max_win: 100000}]
averageMultiplier
:
3.373611953517094
connectedPlayers
:
204
cooldownPaused
:
false
cooldownTimer
:
15000
count2x
:
46
count10x
:
5
count50x
:
0
count100x
:
0
gameHistory
:
[{id: "20251228-d8d002aba86140ad", timestamp: 1766892383603,…},…]
gameId
:
"20251228-d03603c83ac04266"
gameVersion
:
"v3"
godCandle2x
:
null
godCandle2xMassiveJump
:
null
godCandle2xPrices
:
[]
godCandle2xTimestamp
:
null
godCandle10x
:
null
godCandle10xMassiveJump
:
null
godCandle10xPrices
:
[]
godCandle10xTimestamp
:
null
godCandle50x
:
null
godCandle50xMassiveJump
:
null
godCandle50xPrices
:
[]
godCandle50xTimestamp
:
null
highestToday
:
1329.9752646165282
highestTodayPrices
:
[1, 1.0232511670978457, 1.0084532485837796, 1.027798080647492, 0.7733688713742106, 0.779469476137248,…]
highestTodayTimestamp
:
1766855639499
leaderboard
:
[{id: "did:privy:cmen97eeo007tk20bklploj7i", username: "FLYBOI", level: 70, pnl: 5.487196608,…},…]
partialPrices
:
{startTick: 0, endTick: 0, values: {0: 1}}
pauseMessage
:
""
price
:
1
provablyFair
:
{serverSeedHash: "45c89bd5f01735ffc9c91fc5808ff54ec4b7338fd91f06191c58d7b0f45904e3", version: "v3"}
rugged
:
false
tickCount
:
0
```

---

# USER'S OBSERVATIONS & INSIGHTS FOR FUTURE SESSIONS

## avgCost Investigation (User's Note)

> "avgCost being an interesting number that appears to me to potentially be a lifetime profile tracking metric to see what my average profitability to the game. This is something Id like to investigate separtely in a different session."

**Resolution from Q2 Analysis**: avgCost is NOT lifetime profitability - it is the weighted average entry price for the current position. Confirmed by calculation:
- Before add: avgCost=1.0, positionQty=0.002
- After add: avgCost=1.181828845, positionQty=0.003384584
- New avgCost = (0.002 * 1.0 + 0.001384584 * 1.4444769765) / 0.003384584 ≈ 1.1818

## Cooldown Timer Behavior (User's Observation)

> "coolDownTimer: 15000 (which is where it always begins. It states allowPreRoundBuys: False until it reaches 10000 at which point it flips to true.)"

## Event Categorization (User's Request)

> "This should also be something we create a categorical sort for when we review this for canon verification in the next session and should be noted."

## GodCandle Importance (User's Observation)

> "It also contains a useful tracker thats going to be highly useful for studying aggregate data across thousands of games which is the godcandle."

## Forced Sell Mechanism (User's Observation)

> "It also essentially forces the player to enter a sell for their position at the final price which appears to be precalculated somehow due to the unique tiny remainder non-zero price."

## Delayed active:false (User's Emphasis)

User explicitly noted with emphasis (ALL CAPS and exclamation marks):
> "(DESPITE ALL THESE EVENTS TO END THE GAME OCCURING!!)"

---

# STAGING CHECKLIST FOR CANONICAL REVIEW

## Documents in This Staging Package

1. `MASTER_STAGING_VERBATIM_INPUT.md` (THIS FILE) - All raw user input
2. `Q1_position_opening_events.md` - Structured Q1 analysis
3. `Q2_adding_to_position_events.md` - Structured Q2 analysis
4. `Q3_Q4_closing_position_rug_events.md` - Structured Q3/Q4 analysis

## Total New Elements to Review

| Category | Count |
|----------|:-----:|
| New Event Types | 6 |
| New Fields | 72+ |
| Structure Corrections | 1 |
| Behavioral Patterns | 8 |

## New Event Types for Canonical Addition

| Event | Direction | Priority |
|-------|-----------|:--------:|
| `buyOrder` | Client → Server | P0 |
| `standard/newTrade` | Server → Client | P0 |
| `success` | Server → Client (ACK) | P1 |
| `currentSidebetResult` | Server → Client | P0 |
| `rugPassQuestCompleted` | Server → Client | P3 |
| `ping` | Client → Server | P2 |

## Proposed Event Category Taxonomy

| Category | Events | Direction |
|----------|--------|-----------|
| TRADING_ACTION | `buyOrder`, `sellOrder` | Client → Server |
| TRADING_EVENT | `standard/newTrade` | Server → Client (broadcast) |
| SIDEBET_EVENT | `currentSidebetResult` | Server → Client |
| PLAYER_STATE | `playerUpdate`, `gameStatePlayerUpdate` | Server → Client (personal) |
| GAME_STATE | `gameStateUpdate` | Server → Client (broadcast) |
| GAMIFICATION | `rugPassQuestCompleted` | Server → Client |
| SYSTEM_HEARTBEAT | `ping` | Client → Server |
| SYSTEM_ACK | `success`, `4358[]` | Server → Client (ACK) |

## Open Questions for Future Investigation

1. **sidebetPnl discrepancy**: Why 0.003 shown when profit was 0.004?
2. **rugPassQuestCompleted fields**: What data does this event contain?
3. **rugRoyale mechanics**: How do tournaments work?
4. **GodCandle triggers**: What defines a "godCandle" vs normal price movement?
5. **MassiveJump threshold**: What constitutes a "massive jump"?
6. **Leverage > 1**: When is leverage used? Future/margin trading?
7. **avgCost lifetime**: Is there a separate field for lifetime average profitability?
8. **Forced sell price**: Is the rug price deterministic or random?

---

# END OF MASTER STAGING DOCUMENT
