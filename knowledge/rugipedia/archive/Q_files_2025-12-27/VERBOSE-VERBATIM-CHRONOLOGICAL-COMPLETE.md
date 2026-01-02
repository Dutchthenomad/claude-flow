

**Date**: 2025-12-28
**Session**: WebSocket Documentation Enhancement
**Status**: OBSERVED (pending canonical review)

---

## COMPLETE VERBATIM/VERBOSE/CHRONOLOGICAL EXAMPLES USED TO CREATE THIS CANONICAL VALIDATION SESSION. 

> I want to invoke the @agent-rugs-expert so we can work on adding 
additional knowledge to our websockets documentation. We will be reviewing
 some events Im going to copy directly from my devtools menu. we will then
 systematically work in a planning type environment to identify anything 
we dont recongnize and add it to a list of all the additions we identify. 
We will then properly add everything when we are at the end of the session
 for documentation and ingestion. We will begin by answering some 
questions the developer in the vectra project has. Question 1: The agent 
identified 4 position transition cases that must be handled:

  1. Opening position (0 → positive): Record entry_tick = current_tick   I
 will now show you an example of what a presale trade andf sidebet look 
like when the presale is still active, then on tick 0, then tick1 1. here 
is the first one: this is directly between coolDownTimer:200 and 
coolDownTimer:100. 42["gameStatePlayerUpdate", {gameId: 
"20251227-65bd74ba1bc54708",…}]
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
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, 
pnl: 0, pnlPercent: 0,…}
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
{startedAtTick: 0, gameId: "20251227-65bd74ba1bc54708", end: 40, 
betAmount: 0.001, xPayout: 5,…}
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
{instarugCount: 3, rugpoolAmount: 2.1897343695, totalEntries: 8270, 
threshold: 10,…} It appears to me that after the coolDownTimer:100, it 
displays 3 events in this order: gameStatePlayerUpdate, playerUpdate, and 
gameStateUpdate. gameStatePlayerUpdate shows this: 
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
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, 
pnl: 0, pnlPercent: 0,…}
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
{startedAtTick: 0, gameId: "20251227-65bd74ba1bc54708", end: 40, 
betAmount: 0.001, xPayout: 5,…}
sidebetActive
: 
true
totalInvested
: 
0.002
username
: 
"N0m4D"  I will ahow you the remaing two next. 

> here is playerUpdate: 42["playerUpdate",…]
0
: 
"playerUpdate"
1
: 
{id: "did:privy:cma094vht019il80np6aidhqd", role: null, cash: 0.097595869,
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
{startedAtTick: 0, gameId: "20251227-65bd74ba1bc54708", end: 40, 
betAmount: 0.001, xPayout: 5,…}
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
{active: false, activeUntil: 0, available: 0} and the the first tick 0 is 
displayed in the gameStateUpdate: 42["gameStateUpdate",…]
0
: 
"gameStateUpdate"
1
: 
{active: true, price: 1, rugged: false, tickCount: 0, cooldownTimer: 0, 
cooldownPaused: false,…}
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
{serverSeedHash: 
"d74b42aabdce7c6d8aaea9d23aa3453a55ed7b1b19d8ebd0e1380178b7dc12ae", 
version: "v3"}
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

> the second question is 2. Adding to position (positive → more positive): Keep original 
entry_tick The following is a series of events extremely close together at many points. In this 
example, I made 
a presale trade for .002 SOL, when the game began, the next thing I did 
was add to the position with another.002 at or about tick 11, then sold a 
few ticks later. This first event is a "gameStatePlayerUpdate" event; 
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
"N0m4D"     As you can see, there are several features we should be 
observing. avgCost, hasActiveTrades:, pnl, pnlPercent, positionQty, 
regularPnl, and totalInvested. Now Im not sure if the separate columns in 
the Messages section in DevTools attaches the information in them, so I 
will add it for context just in case. The first column entitled "Data" 
contains the entire event in nested sections, the second column titled 
"Length": 2350, and the third is "Time": and it says 21:02:55.825. I will 
show you the next novel event which Im not sure if it is in the canonical 
pedia, but is called "buyOrder" and is a message from us to the server. 
This should also be something we create a categorical sort for when we 
review this for canon verification in the next session and should be 
noted. This event Length is: 122, the "time: is 21:02:56.038 and the data 
is: 4229["buyOrder", {__trace: true, traceparent: 
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
0.002 This next event happened directly after the "buyOrder" and was 
the second of these 2 events entitled "standard/newTrade". The first was 
another player entering a trade named "Vmoney" for 0.569271328 SOL. This 
occured at 21:02:56.081 and the next "standard/newTrade" that my 
"buyOrder" was emmited by occured just a few microseconds later at 
21:02:56.107. The following is the entire contents of the 
"standard/newTrade" event that shows my second position being added to the
 game: 42["standard/newTrade",…]
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
"N0m4D"     The next event occurs at 21:02:56.236, its length is 902, and 
the event is "playerUpdate" The features that stand out as what need to be
 paid attention to (not an explicit requirement) are: "authenticated", 
"avgCost", "cash", "cumulitivePnl", "pnlPercent", "positionQty", and 
"totalInvested". Cash being the current wallet balance, avgCost being an 
interesting number that appears to me to potentially be a lifetime profile
 tracking metric to see what my average profitability to the game. This is
 something Id like to investigate separtely in a different session. Also, 
positionQty appears to be the current value of my total trade position, 
however the pnlPercent makes me second guess this assumption. ANyways, 
heres the event: 42["playerUpdate",…]
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
0 I will provide the final events in the next comment which should 
complete the answers for question 2.. 

Ok!!! That makes total sense!!! OK here is the next info for question 2. This 
next event is the following "gameStatePlayerUpdate" with a length of 421 and a 
timestamp 
of 21:02:56.251. 42["gameStatePlayerUpdate", {gameId: 
"20251228-242b2d81e73e4f27",…}]
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
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, pnl: 
0.000888953,…}
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
"N0m4D"   Directly after this event is an event entitled "success". Its length 
is small at 22 and
 time stamp is 21:02:56.257 and the data is 4329[{success: true}]
0
: 
{success: true}
success
: 
true 
 I will add a bit more context now for good measure. The next gameStateUpdate 
occurs at timestamp 21:02:58.054 and has a massive length of 165280!!! It 
contains the "gameHistory" which contains novel information we absolutely need 
to mark as highly useful such as averageMultiplier, which is the average peak 
price of the last 100 games in a rolling window. connectedPlayers, the 4 
"countdown--X" metrics that display how many games of the last 100 reached 
atleast 2x,10x,50x,and100x. It also contains a useful tracker thats going to be 
highly useful for studying aggregate data across thousands of games which is the
 godcandle. 
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
null   As we can see in this example, we can derive the timestamps of when these
 event occur (or the lack there of in this event). We then have the highest peak
 price for the day we can derive which in this example is properly entitled 
highestToday
: 
1329.9752646165282  We can also see the timestamp at which this occured which 
was highestTodayTimestamp
: 
1766855639499. Now, this was not neccesarily of use to answering the question 
but is extremely important tha we document this when we run the canonical 
verifications. I was going to provide one more playerGameStateUpdate but the 
browser was accidentally refreshed. 

> The final 2 questions Im going to attempt to answer together: 3. Partial 
sell (positive → less positive): Keep entry_tick
  4. Closing position (positive → 0): Reset entry_tick = None   So in this 
example, I have both active trade positions, and an active sideBet when the 
game rugs so I captured the event that shows how sideBets are paid out as 
well. This gameStateUpdate occurs at 22:26:23.018 and is a length of 4368 to
 provide the game context: 42["gameStateUpdate",…]
0
: 
"gameStateUpdate"
1
: 
{active: true, price: 0.7205941557633537, partialPrices: {startTick: 268, 
endTick: 272,…},…}
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
[{id: "did:privy:cmen97eeo007tk20bklploj7i", username: "FLYBOI", level: 70, 
pnl: 5.487196608,…},…]
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
{serverSeedHash: 
"6f67e582cc3f4de0f4a0670975b94772a8f81603e2191aae8615bfabd9f3cfe3", version:
 "v3"}
rugRoyale
: 
{status: "INACTIVE", activeEventId: null, currentEvent: null, 
upcomingEvents: [], events: []}
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
MCP server
Let your favourite coding agent debug your pages at runtime, using the 
Chrome DevTools MCP server.

Improved trace sharing
Optionally include resource content and script source maps in exported 
performance traces.

Support for @starting-style
Debug and identify CSS entry animations using the new adorner in the 
Elements panel. The next event is a gameStatePlayerUpdate that occurs at 
22:26:23.029 42["gameStatePlayerUpdate", {gameId: 
"20251228-d8d002aba86140ad",…}]
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
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, 
pnl: -0.001345501,…}
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
{startedAtTick: 264, gameId: "20251228-d8d002aba86140ad", end: 304, 
betAmount: 0.001, xPayout: 5,…}
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
"N0m4D"  The next event is a new one entitled "currentSidebetResult" 
occuring at 22:26:23.274. 42["currentSidebetResult",…]
0
: 
"currentSidebetResult"
1
: 
{__trace: true, traceparent: 
"00-f89f16bbd99069674a9a54d709743847-3781631892f7fc03-01"}
traceparent
: 
"00-f89f16bbd99069674a9a54d709743847-3781631892f7fc03-01"
__trace
: 
true
2
: 
{playerId: "did:privy:cma094vht019il80np6aidhqd", gameId: 
"20251228-d8d002aba86140ad",…}
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
     After you review this, I still have a few more events to show you that 
are EXTREMELY INTERESTING to say the least!! They show how the game 
completes the rug event player calculation before emiting that the game 
active:false. It also essentially forces the player to enter a sell for 
their position at the final price which appears to be precalculated somehow 
due to the unique tiny remainder non-zero price. It first provides a 
"playerUpdate" event at 22:26:23.286, then the forced sell event 
"standard/newTrade" at 22:26:23.295, the an additional "playerUpdate" at 
22:26:23.295, then a "gameStatePlayerUpdate" at 22:26:23.305, a 
"rugPassQuestCompleted" at 22:26:23.309, then a gameStateUpdate at 
22:26:23.449 that still states 42["gameStateUpdate",…]
0
: 
"gameStateUpdate"
1
: 
{active: true, price: 0.009250309566210552, partialPrices: {startTick: 269, 
endTick: 273,…},… (DESPITE ALL THESE EVENTS TO END THE GAME OCCURING!!). 
This is followed by a "gameStatePlayerUpdate" at timestamp 22:26:23.449, 
then an event that simply says 4358[] at timestamp 22:26:24.456.  Then 
another "playerUpdate" at 22:26:24.605 followed by an emission from ourside 
as a 4259 ping at 22:26:24.456 that shows: 4259["ping", {lastPing: 
169.20000000298023}]
0
: 
"ping"
1
: 
{lastPing: 169.20000000298023}
lastPing
: 
169.20000000298023
Then ANOTHER "gameStateUpdate" that still states "active:true", a 
gameStatePlayerUpdate that appears to be the completed calculations for 
closing out my game positons. Here is the entirety of that event: 
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
{id: "did:privy:cma094vht019il80np6aidhqd", username: "N0m4D", level: 14, 
pnl: 0.0010210280000000002,…}
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
"N0m4D" then this is finally followed by a "gameStateUpdate" with the 
active:false emmited along with the coolDownTimer: 15000 (which is where it 
always begins. It states allowPreRoundBuys: False until it reaches 10000 at 
which point it flips to true. ) 42["gameStateUpdate", {gameHistory: [{id: 
"20251228-d8d002aba86140ad", timestamp: 1766892383603,…},…],…}]
0
: 
"gameStateUpdate"
1
: 
{gameHistory: [{id: "20251228-d8d002aba86140ad", timestamp: 
1766892383603,…},…],…}
active
: 
false
allowPreRoundBuys
: 
false
availableShitcoins
: 
[{address: "0xPractice", ticker: "FREE", name: "Practice SOL", max_bet: 
10000, max_win: 100000}]
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
[1, 1.0232511670978457, 1.0084532485837796, 1.027798080647492, 
0.7733688713742106, 0.779469476137248,…]
highestTodayTimestamp
: 
1766855639499
leaderboard
: 
[{id: "did:privy:cmen97eeo007tk20bklploj7i", username: "FLYBOI", level: 70, 
pnl: 5.487196608,…},…]
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
{serverSeedHash: 
"45c89bd5f01735ffc9c91fc5808ff54ec4b7338fd91f06191c58d7b0f45904e3", version:
 "v3"}
rugged
: 
false
tickCount
: 
0 


