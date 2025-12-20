# WebSocket Recording Coverage Report

*Generated: 2025-12-19 19:55:28*

## Coverage Summary

- **Files Scanned**: 20 files
- **Total Events**: 19,207 events
- **Unique Event Types**: 29 unique event types
- **Parse Errors**: 0

- **Total Unique Field Paths**: 590

## Event Types

| Event | Count | % of Total | Unique Fields |
|-------|------:|:----------:|:-------------:|
| `gameStateUpdate` | 12,360 | 64.4% | 58 |
| `gameStatePlayerUpdate` | 4,794 | 25.0% | 55 |
| `standard/newTrade` | 902 | 4.7% | 26 |
| `newChatMessage` | 586 | 3.1% | 26 |
| `goldenHourUpdate` | 178 | 0.9% | 41 |
| `battleEventUpdate` | 63 | 0.3% | 35 |
| `sidebetEventUpdate` | 51 | 0.3% | 81 |
| `playerUpdate` | 50 | 0.3% | 7 |
| `newSideBet` | 36 | 0.2% | 25 |
| `chatHistory` | 28 | 0.1% | 9 |
| `goldenHourDrawing` | 27 | 0.1% | 23 |
| `usernameStatus` | 14 | 0.1% | 9 |
| `rugRoyaleUpdate` | 13 | 0.1% | 56 |
| `inboxMessages` | 13 | 0.1% | 9 |
| `getLeaderboard` | 8 | 0.0% | 8 |
| `leaderboardData` | 8 | 0.0% | 9 |
| `getPlayerLeaderboardPosition` | 8 | 0.0% | 9 |
| `playerLeaderboardPosition` | 8 | 0.0% | 9 |
| `rugpassStatus` | 8 | 0.0% | 9 |
| `connect` | 7 | 0.0% | 4 |
| `authenticate` | 7 | 0.0% | 9 |
| `getPlayerCosmetics` | 7 | 0.0% | 7 |
| `mutedPlayers` | 7 | 0.0% | 9 |
| `playerCosmetics` | 7 | 0.0% | 9 |
| `checkUsername` | 7 | 0.0% | 7 |
| `maintenanceUpdate` | 6 | 0.0% | 14 |
| `gameNotification` | 2 | 0.0% | 9 |
| `rugpoolDrawing` | 1 | 0.0% | 9 |
| `rugpoolStatus` | 1 | 0.0% | 9 |

## Field Coverage by Event

### authenticate

**Occurrences**: 7

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 7 |  |
| `data.__trace` | boolean | 7 | True |
| `data.traceparent` | string | 7 | 00-c37856d5e5c8910e2f87852550c88ff0-9b76, 00-92523f902403b52450cfa2d0884b2715-a3d6, 00-678b5efbb6477ac5498cfc42e4d80cb9-49b2 |
| `direction` | string | 7 | sent |
| `event` | string | 7 | authenticate |
| `raw` | string | 2 | 42["authenticate",{"__trace":true,"trace, 42["authenticate",{"__trace":true,"trace |
| `seq` | number | 7 | 3 |
| `source` | string | 7 | cdp_intercept |
| `ts` | string | 7 | 2025-12-15T03:43:07.096189+00:00, 2025-12-15T03:44:59.726131+00:00, 2025-12-15T04:04:47.460858+00:00 |

### battleEventUpdate

**Occurrences**: 63

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 63 |  |
| `data.__trace` | boolean | 30 | True |
| `data.traceparent` | string | 30 | 00-4fc7a86262b4519b62afa29f4243fc84-23d8, 00-4fc7a86262b4519b62afa29f4243fc84-018d, 00-c37856d5e5c8910e2f87852550c88ff0-1224 |
| `data[]` | object | 33 |  |
| `data[].__trace` | boolean | 33 | True |
| `data[].activeBattleCount` | number | 33 | 0 |
| `data[].config` | object | 33 |  |
| `data[].config.levelRequired` | number | 33 | 1 |
| `data[].config.prepTimeMinutes` | number | 33 | 30 |
| `data[].config.startingBalance` | number | 33 | 100 |
| `data[].config.token` | string | 33 | 0xPractice |
| `data[].currentEvent` | null | 33 | None |
| `data[].endTime` | null | 33 | None |
| `data[].eventSchedule` | array | 33 |  |
| `data[].fullLeaderboardSize` | number | 33 | 0 |
| `data[].isShowingPreviousEvent` | null | 33 | None |
| `data[].leaderboard` | array | 33 |  |
| `data[].lobbyCreationDisabled` | boolean | 33 | False |
| `data[].nextEvent` | null | 33 | None |
| `data[].nextEventStartTime` | null | 33 | None |
| `data[].participantCount` | number | 33 | 0 |
| `data[].playerPosition` | null | 33 | None |
| `data[].queue` | object | 33 |  |
| `data[].queue.active` | boolean | 33 | False |
| `data[].queue.availableLobbies` | number | 33 | 0 |
| `data[].queue.queueSize` | number | 33 | 0 |
| `data[].startTime` | null | 33 | None |
| `data[].status` | string | 33 | SCHEDULED |
| `data[].traceparent` | string | 33 | 00-779fbe6b1307f0042d9e26927f450883-24a5, 00-001c4e8b5ea3e308e7ba5f7279863781-9f35, 00-9a489f250d019553dce15c970afe2bb6-361a |
| `direction` | string | 30 | received |
| `event` | string | 63 | battleEventUpdate |
| `raw` | string | 5 | 42["battleEventUpdate",{"__trace":true,", 42["battleEventUpdate",{"__trace":true,", 42["battleEventUpdate",{"__trace":true," |
| `seq` | number | 63 | 169, 201, 657 |
| `source` | string | 30 | cdp_intercept |
| `ts` | string | 63 | 2025-12-12T17:17:34.821523, 2025-12-14T11:52:16.893527, 2025-12-14T11:53:15.946978 |

### chatHistory

**Occurrences**: 28

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | null | 28 | None |
| `data.__trace` | boolean | 14 | True |
| `data.traceparent` | string | 14 | 00-557b192cc3d5a495a982ce7eac7dbd8c-4689, 00-5ad8c09b2091ab9330206e9447145caf-f7b7, 00-a5ee6fd2f387ad08ae3a5df0409bee3a-077a |
| `direction` | string | 28 | sent, received |
| `event` | string | 28 | chatHistory |
| `raw` | string | 8 | 42["chatHistory"], 42["chatHistory",{"__trace":true,"tracep, 42["chatHistory",{"__trace":true,"tracep |
| `seq` | number | 28 | 1, 19, 21 |
| `source` | string | 28 | cdp_intercept |
| `ts` | string | 28 | 2025-12-15T03:43:07.096060+00:00, 2025-12-15T03:43:08.781944+00:00, 2025-12-15T03:43:09.317992+00:00 |

### checkUsername

**Occurrences**: 7

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | null | 7 | None |
| `direction` | string | 7 | sent |
| `event` | string | 7 | checkUsername |
| `raw` | string | 2 | 42["checkUsername"] |
| `seq` | number | 7 | 174, 77, 143 |
| `source` | string | 7 | cdp_intercept |
| `ts` | string | 7 | 2025-12-15T03:43:15.304795+00:00, 2025-12-15T03:45:05.015075+00:00, 2025-12-15T04:04:54.150670+00:00 |

### connect

**Occurrences**: 7

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | null | 7 | None |
| `event` | string | 7 | connect |
| `seq` | number | 7 | 1 |
| `ts` | string | 7 | 2025-12-12T17:16:58.624285, 2025-12-14T11:51:33.809733, 2025-12-14T19:18:09.945210 |

### gameNotification

**Occurrences**: 2

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 2 |  |
| `data[]` | object | 2 |  |
| `data[].__trace` | boolean | 2 | True |
| `data[].message` | string | 2 | ⏰ Event time has ended! This will be the, ⏰ Golden Hour has ended! Thanks for part |
| `data[].traceparent` | string | 2 | 00-40249df942713137c368e582bdfd2c79-251f, 00-f74180e1b42328ee8bcabb91b3bb6118-b3ce |
| `data[].type` | string | 2 | event, goldenhour |
| `event` | string | 2 | gameNotification |
| `seq` | number | 2 | 1051, 1143 |
| `ts` | string | 2 | 2025-12-15T00:05:02.177950, 2025-12-15T00:05:21.379793 |

### gameStatePlayerUpdate

**Occurrences**: 4,794

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 4,794 |  |
| `data.gameId` | string | 4,794 | 20251215-89eb875cdef14caf, 20251215-9a01e6bb7dc24df9, 20251215-000858336e594d1b |
| `data.leaderboardEntry` | object | 597 |  |
| `data.leaderboardEntry.avgCost` | number | 597 | 0.831340055, 0.831340295, 0 |
| `data.leaderboardEntry.hasActiveTrades` | boolean | 597 | True |
| `data.leaderboardEntry.id` | string | 597 | did:privy:cmaibr7rt0094jp0mc2mbpfu4 |
| `data.leaderboardEntry.level` | number | 597 | 7 |
| `data.leaderboardEntry.pnl` | number | 597 | 0, 2.6863e-05, 5.9716e-05 |
| `data.leaderboardEntry.pnlPercent` | number | 597 | 0, 2.6862999999999997, 5.9716 |
| `data.leaderboardEntry.position` | number | 597 | 16, 17, 15 |
| `data.leaderboardEntry.positionQty` | number | 597 | 0.001202876, 0, 0.001 |
| `data.leaderboardEntry.regularPnl` | number | 593 | 0, 2.6863e-05, 5.9716e-05 |
| `data.leaderboardEntry.selectedCoin` | null | 597 | None |
| `data.leaderboardEntry.shortPnl` | number | 593 | 0 |
| `data.leaderboardEntry.shortPosition` | null | 597 | None |
| `data.leaderboardEntry.sideBet` | null | 597 | None |
| `data.leaderboardEntry.sidebetActive` | null | 597 | None |
| `data.leaderboardEntry.sidebetPnl` | number | 593 | 0 |
| `data.leaderboardEntry.totalInvested` | number | 597 | 0.001 |
| `data.leaderboardEntry.username` | string | 597 | Dutch |
| `data.rugpool` | object | 4,792 |  |
| `data.rugpool.config` | object | 4,792 |  |
| `data.rugpool.config.instarugThreshold` | number | 4,792 | 6 |
| `data.rugpool.config.rugpoolPercentage` | number | 4,792 | 0.5 |
| `data.rugpool.config.threshold` | number | 4,792 | 10 |
| `data.rugpool.instarugCount` | number | 4,792 | 9, 0 |
| `data.rugpool.lastDrawing` | object | 4,792 |  |
| `data.rugpool.lastDrawing.rewardPerWinner` | number | 4,792 | 3.5956412111666736, 2.213582226666671, 1.994776551666681 |
| `data.rugpool.lastDrawing.timestamp` | number | 4,792 | 1765750336277, 1765794262774, 1765819354240 |
| `data.rugpool.lastDrawing.totalPoolAmount` | number | 4,792 | 10.78692363350002, 6.640746680000013, 5.984329655000043 |
| `data.rugpool.lastDrawing.winners` | array | 4,792 |  |
| `data.rugpool.lastDrawing.winners[]` | object | 4,792 |  |
| `data.rugpool.lastDrawing.winners[].entries` | number | 14,376 | 5000, 1121, 1917 |
| `data.rugpool.lastDrawing.winners[].playerId` | string | 14,376 | did:privy:cmb8sq5at0022js0mp6w3f5hh, did:privy:cma8r35lw00oalc0mmu10cck7, did:privy:cmeygisuf00wyl50civj2950w |
| `data.rugpool.lastDrawing.winners[].reward` | number | 14,376 | 3.5956412111666736, 2.213582226666671, 1.994776551666681 |
| `data.rugpool.lastDrawing.winners[].username` | string | 14,376 | ehiwna, CheckItup, Wolfeee |
| `data.rugpool.maxEntriesPerPlayer` | number | 4,792 | 5000 |
| `data.rugpool.playerEntries` | array | 4,792 |  |
| `data.rugpool.playerEntries[]` | object | 4,574 |  |
| `data.rugpool.playerEntries[].entries` | number | 45,740 | 5000, 4450, 1070 |
| `data.rugpool.playerEntries[].percentage` | number | 45,740 | 22.452736988638915, 19.982935919888632, 4.8048857155687275 |
| `data.rugpool.playerEntries[].playerId` | string | 45,740 | did:privy:cmb8sq5at0022js0mp6w3f5hh, did:privy:cma0m5z4r00afjx0mjpryyqo5, did:privy:cmeygisuf00wyl50civj2950w |
| `data.rugpool.playerEntries[].username` | string | 45,740 | ehiwna, jKolby, Wolfeee |
| `data.rugpool.playersWithEntries` | number | 4,792 | 155, 136, 142 |
| `data.rugpool.rugpoolAmount` | number | 4,792 | 7.440795633500021, 5.523102353500032, 5.984329655000043 |
| `data.rugpool.solPerEntry` | number | 4,792 | 0.001 |
| `data.rugpool.threshold` | number | 4,792 | 10 |
| `data.rugpool.totalEntries` | number | 4,792 | 22269, 15655, 16931 |
| `data.trades` | array | 7 |  |
| `direction` | string | 4,794 | received |
| `event` | string | 4,794 | gameStatePlayerUpdate |
| `raw` | string | 540 | 42["gameStatePlayerUpdate",{"gameId":"20, 42["gameStatePlayerUpdate",{"gameId":"20, 42["gameStatePlayerUpdate",{"gameId":"20 |
| `seq` | number | 4,794 | 23, 33, 35 |
| `source` | string | 4,794 | cdp_intercept |
| `ts` | string | 4,794 | 2025-12-15T03:43:09.319591+00:00, 2025-12-15T03:43:09.897882+00:00, 2025-12-15T03:43:09.921451+00:00 |

### gameStateUpdate

**Occurrences**: 12,360

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 12,360 | <object with 36 keys>, <object with 21 keys> |
| `data.active` | boolean | 35 | True |
| `data.allowPreRoundBuys` | boolean | 5,089 | False, True |
| `data.connectedPlayers` | number | 5,089 | 200, 201, 202 |
| `data.cooldownPaused` | boolean | 5,089 | False |
| `data.cooldownTimer` | number | 5,089 | 14900, 14800, 14700 |
| `data.gameId` | string | 5,089 | 20251212-6114b2ff44ef4b71, 20251212-6f491efbd808458b, 20251214-fe3c0e433c0d429d |
| `data.gameVersion` | string | 35 | v3 |
| `data.leaderboard` | array | 5,089 |  |
| `data.leaderboard[]` | object | 5,019 |  |
| `data.leaderboard[].avgCost` | number | 50,059 | 0, 1, 0.999999999 |
| `data.leaderboard[].hasActiveTrades` | boolean | 50,059 | True |
| `data.leaderboard[].id` | string | 50,059 | did:privy:cmaos0abo03t9kz0mquf6fa4n, did:privy:cmgdz0so100bejm0cfaewe0rw, did:privy:cmi8zyfq4007fl20booupw2jj |
| `data.leaderboard[].level` | number | 50,059 | 28, 19, 16 |
| `data.leaderboard[].pnl` | number | 50,059 | 0.014450205, 0.002079603, 0.000966814 |
| `data.leaderboard[].pnlPercent` | number | 50,059 | 16.055783333333334, 6.301827654656221, 12.085175 |
| `data.leaderboard[].position` | number | 50,059 | 1, 2, 3 |
| `data.leaderboard[].positionQty` | number | 50,059 | 0, 0.001, 0.1 |
| `data.leaderboard[].regularPnl` | number | 16,700 | 0.014450205, 0.002079603, 0.000966814 |
| `data.leaderboard[].selectedCoin` | null | 50,059 | None |
| `data.leaderboard[].selectedCoin.address` | string | 2,575 | 0xPractice |
| `data.leaderboard[].selectedCoin.logoURI` | string | 2,575 | /icons/Icon_Free_Solana.png |
| `data.leaderboard[].selectedCoin.max_bet` | number | 2,575 | 10000 |
| `data.leaderboard[].selectedCoin.max_win` | number | 2,575 | 50000 |
| `data.leaderboard[].selectedCoin.name` | string | 2,575 | Free Practice Token |
| `data.leaderboard[].selectedCoin.ticker` | string | 2,575 | FREE |
| `data.leaderboard[].shortPnl` | number | 16,700 | 0 |
| `data.leaderboard[].shortPosition` | null | 50,059 | None |
| `data.leaderboard[].sideBet` | null | 50,059 | None |
| `data.leaderboard[].sideBet.betAmount` | number | 2,406 | 0.001, 0.003, 0.01 |
| `data.leaderboard[].sideBet.bonusPortion` | number | 2,406 | 0, 0.05, 0.004 |
| `data.leaderboard[].sideBet.coinAddress` | string | 2,406 | So11111111111111111111111111111111111111, 0xPractice |
| `data.leaderboard[].sideBet.end` | number | 2,406 | 40 |
| `data.leaderboard[].sideBet.gameId` | string | 2,406 | 20251212-6114b2ff44ef4b71, 20251212-6f491efbd808458b, 20251214-fe3c0e433c0d429d |
| `data.leaderboard[].sideBet.realPortion` | number | 2,406 | 0.001, 0.003, 0.01 |
| `data.leaderboard[].sideBet.startedAtTick` | number | 2,406 | 0 |
| `data.leaderboard[].sideBet.xPayout` | number | 2,406 | 5 |
| `data.leaderboard[].sidebetActive` | null | 50,059 | None, True |
| `data.leaderboard[].sidebetPnl` | number | 16,700 | 0, 0.052000000000000005, 0.012 |
| `data.leaderboard[].totalInvested` | number | 50,059 | 0.09, 0.032999998, 0.008 |
| `data.leaderboard[].username` | string | 50,059 | Boss, getSmoked, BooMStick1776 |
| `data.partialPrices` | object | 35 |  |
| `data.partialPrices.endTick` | number | 35 | 0 |
| `data.partialPrices.startTick` | number | 35 | 0 |
| `data.partialPrices.values` | object | 35 | <object with 1 keys> |
| `data.pauseMessage` | string | 35 |  |
| `data.price` | number | 35 | 1 |
| `data.provablyFair` | object | 5,089 |  |
| `data.provablyFair.serverSeedHash` | string | 5,089 | f8fb5fc595f23a0c148ad4ebabf4996b20190dd9, 79740423cccd1b29c75bd5b669f1da0fb6020563, 39118e6b97ce6762e5a90785541c500f2179eb97 |
| `data.provablyFair.version` | string | 5,089 | v3 |
| `data.rugged` | boolean | 35 | False |
| `data.tickCount` | number | 35 | 0 |
| `direction` | string | 4,817 | received |
| `event` | string | 12,360 | gameStateUpdate |
| `raw` | string | 543 | 42["gameStateUpdate",{"gameHistory":[{"i, 42["gameStateUpdate",{"active":true,"pri, 42["gameStateUpdate",{"active":true,"pri |
| `seq` | number | 12,360 | 2, 3, 4 |
| `source` | string | 4,817 | cdp_intercept |
| `ts` | string | 12,360 | 2025-12-12T17:16:58.952637, 2025-12-12T17:16:58.964233, 2025-12-12T17:16:59.181524 |

### getLeaderboard

**Occurrences**: 8

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 8 |  |
| `data.period` | string | 8 | 7d |
| `direction` | string | 8 | sent |
| `event` | string | 8 | getLeaderboard |
| `raw` | string | 2 | 42["getLeaderboard",{"period":"7d"}] |
| `seq` | number | 8 | 2, 3943 |
| `source` | string | 8 | cdp_intercept |
| `ts` | string | 8 | 2025-12-15T03:43:07.096091+00:00, 2025-12-15T03:44:59.726014+00:00, 2025-12-15T04:04:47.460694+00:00 |

### getPlayerCosmetics

**Occurrences**: 7

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | null | 7 | None |
| `direction` | string | 7 | sent |
| `event` | string | 7 | getPlayerCosmetics |
| `raw` | string | 2 | 42["getPlayerCosmetics"] |
| `seq` | number | 7 | 22, 15, 11 |
| `source` | string | 7 | cdp_intercept |
| `ts` | string | 7 | 2025-12-15T03:43:09.318370+00:00, 2025-12-15T03:45:01.315041+00:00, 2025-12-15T04:04:49.968484+00:00 |

### getPlayerLeaderboardPosition

**Occurrences**: 8

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 8 |  |
| `data.period` | string | 8 | 7d |
| `data.playerId` | string | 8 | did:privy:cmaibr7rt0094jp0mc2mbpfu4 |
| `direction` | string | 8 | sent |
| `event` | string | 8 | getPlayerLeaderboardPosition |
| `raw` | string | 2 | 42["getPlayerLeaderboardPosition",{"play |
| `seq` | number | 8 | 136, 59, 91 |
| `source` | string | 8 | cdp_intercept |
| `ts` | string | 8 | 2025-12-15T03:43:14.259942+00:00, 2025-12-15T03:45:04.093787+00:00, 2025-12-15T04:04:53.160363+00:00 |

### goldenHourDrawing

**Occurrences**: 27

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 27 |  |
| `data.__trace` | boolean | 10 | True |
| `data.traceparent` | string | 10 | 00-1cedae154c705f079bf05f9666920d62-c572, 00-547d666480c446644587c522025a458e-80d9, 00-2b52e18fb9d76071b2895a408c0aa90e-46a9 |
| `data[]` | object | 17 |  |
| `data[].__trace` | boolean | 17 | True |
| `data[].entries` | array | 17 |  |
| `data[].entries[]` | object | 17 |  |
| `data[].entries[].entryCount` | number | 1,070 | 50, 1, 4 |
| `data[].entries[].entryPercentage` | number | 1,070 | 3.3921302578018993, 0.06784260515603799, 0.27137042062415195 |
| `data[].entries[].playerId` | string | 1,070 | did:privy:cm9g1p6iw00zwjp0m40iwldnz, did:privy:cmgdz0so100bejm0cfaewe0rw, did:privy:cmflkqdrb00p7k00bwga8e74k |
| `data[].entries[].username` | string | 1,070 | ereas, getSmoked, kkimb |
| `data[].gameId` | string | 17 | 20251214-83c1efa1085340c7, 20251214-fe3c0e433c0d429d, 20251214-f670dc0ed0b94d10 |
| `data[].id` | string | 17 | a3621235-6e83-48aa-81ca-4685272ebada, 8fc1f93f-32ba-4e0c-a4a1-f0e418dac9ca, 5e196b55-a7db-4de9-8f8d-890b0be37420 |
| `data[].prizeAmount` | number | 17 | 0.05 |
| `data[].timestamp` | number | 17 | 1765731135035, 1765731176620, 1765731298238 |
| `data[].traceparent` | string | 17 | 00-323c8e5f85e3cdc3d6e9f8c20f4b1cb8-4be7, 00-2202b9fba4bcc46b76d2afe073cefb43-6cb5, 00-e00111a87f63208626213572ee00d56e-e836 |
| `data[].winnerIndex` | number | 17 | 54, 37, 55 |
| `data[].winnerPlayerId` | string | 17 | did:privy:cma8r35lw00oalc0mmu10cck7, did:privy:cmj3bsmny02ull10cj5x3mi5s, did:privy:cmius905i02sul50cuc40nlmy |
| `direction` | string | 10 | received |
| `event` | string | 27 | goldenHourDrawing |
| `seq` | number | 27 | 192, 475, 1141 |
| `source` | string | 10 | cdp_intercept |
| `ts` | string | 27 | 2025-12-14T11:52:16.387658, 2025-12-14T11:52:57.532887, 2025-12-14T11:54:58.828005 |

### goldenHourUpdate

**Occurrences**: 178

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 178 |  |
| `data.__trace` | boolean | 78 | True |
| `data.traceparent` | string | 78 | 00-4fc7a86262b4519b62afa29f4243fc84-48b7, 00-c37856d5e5c8910e2f87852550c88ff0-dc70, 00-3565ca98850b5c9e211e9d22707fc3a8-8628 |
| `data[]` | object | 100 |  |
| `data[].__trace` | boolean | 100 | True |
| `data[].activeEventId` | string | 100 | admin-8ef16a3a-d63d-430a-9224-012b3a11e6 |
| `data[].currentEvent` | object | 100 |  |
| `data[].currentEvent.createdAt` | string | 100 | 2025-12-14T05:01:15.318Z |
| `data[].currentEvent.createdBy` | string | 100 | admin |
| `data[].currentEvent.durationMinutes` | number | 100 | 60 |
| `data[].currentEvent.endTime` | string | 100 | 2025-12-15T05:05:00.000Z |
| `data[].currentEvent.id` | string | 100 | admin-8ef16a3a-d63d-430a-9224-012b3a11e6 |
| `data[].currentEvent.levelRequired` | number | 100 | 10 |
| `data[].currentEvent.maxEntries` | number | 100 | 50 |
| `data[].currentEvent.prepTimeMinutes` | number | 100 | 0 |
| `data[].currentEvent.prizeAmount` | number | 100 | 0.05 |
| `data[].currentEvent.startTime` | string | 100 | 2025-12-14T05:05:00.000Z |
| `data[].currentEvent.status` | string | 100 | SCHEDULED |
| `data[].currentGameIsGolden` | boolean | 100 | True |
| `data[].events` | array | 100 |  |
| `data[].events[]` | object | 100 |  |
| `data[].events[].createdAt` | string | 100 | 2025-12-14T05:01:15.318Z |
| `data[].events[].createdBy` | string | 100 | admin |
| `data[].events[].durationMinutes` | number | 100 | 60 |
| `data[].events[].endTime` | string | 100 | 2025-12-15T05:05:00.000Z |
| `data[].events[].id` | string | 100 | admin-8ef16a3a-d63d-430a-9224-012b3a11e6 |
| `data[].events[].levelRequired` | number | 100 | 10 |
| `data[].events[].maxEntries` | number | 100 | 50 |
| `data[].events[].prepTimeMinutes` | number | 100 | 0 |
| `data[].events[].prizeAmount` | number | 100 | 0.05 |
| `data[].events[].startTime` | string | 100 | 2025-12-14T05:05:00.000Z |
| `data[].events[].status` | string | 100 | SCHEDULED |
| `data[].status` | string | 100 | ACTIVE, ENDING, COMPLETED |
| `data[].traceparent` | string | 100 | 00-e5dfb376634858127568dbe7fff21dd3-d15d, 00-2ac135c0592826871cb466de828c718e-faf4, 00-2e1876208749bda32b4a4b04dc5770e0-4693 |
| `data[].upcomingEvents` | array | 100 |  |
| `direction` | string | 78 | received |
| `event` | string | 178 | goldenHourUpdate |
| `raw` | string | 8 | 42["goldenHourUpdate",{"__trace":true,"t, 42["goldenHourUpdate",{"__trace":true,"t, 42["goldenHourUpdate",{"__trace":true,"t |
| `seq` | number | 178 | 13, 81, 174 |
| `source` | string | 78 | cdp_intercept |
| `ts` | string | 178 | 2025-12-14T11:51:35.698386, 2025-12-14T11:51:50.776031, 2025-12-14T11:52:10.729163 |

### inboxMessages

**Occurrences**: 13

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 13 |  |
| `data.__trace` | boolean | 13 | True |
| `data.traceparent` | string | 13 | 00-4099cd602746f215610daa0de0bc694d-8956, 00-b3ba572a043b31be3ea38d126bc330a2-1364, 00-8d6e29f4be762888ceff87fbdcfb4158-3e68 |
| `direction` | string | 13 | received |
| `event` | string | 13 | inboxMessages |
| `raw` | string | 3 | 42["inboxMessages",{"__trace":true,"trac, 42["inboxMessages",{"__trace":true,"trac, 42["inboxMessages",{"__trace":true,"trac |
| `seq` | number | 13 | 78, 79, 40 |
| `source` | string | 13 | cdp_intercept |
| `ts` | string | 13 | 2025-12-15T03:43:10.925545+00:00, 2025-12-15T03:43:10.931571+00:00, 2025-12-15T03:45:02.650341+00:00 |

### leaderboardData

**Occurrences**: 8

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 8 |  |
| `data.__trace` | boolean | 8 | True |
| `data.traceparent` | string | 8 | 00-51d53b69d051939c5b908db4b9195665-73e4, 00-7536723b90f8c5db42cb294eabe61ef3-9a81, 00-a692ef52ddfc94c4d7498b58adc9ff4e-159d |
| `direction` | string | 8 | received |
| `event` | string | 8 | leaderboardData |
| `raw` | string | 2 | 42["leaderboardData",{"__trace":true,"tr, 42["leaderboardData",{"__trace":true,"tr |
| `seq` | number | 8 | 31, 24, 12 |
| `source` | string | 8 | cdp_intercept |
| `ts` | string | 8 | 2025-12-15T03:43:09.616810+00:00, 2025-12-15T03:45:01.437057+00:00, 2025-12-15T04:04:49.865282+00:00 |

### maintenanceUpdate

**Occurrences**: 6

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 6 |  |
| `data.__trace` | boolean | 2 | True |
| `data.traceparent` | string | 2 | 00-0b052a14ca14d99f3838c3f2ccbd127d-18f2, 00-b635203ba7c53f530db61c3810c1d375-c68a |
| `data[]` | object | 4 |  |
| `data[].__trace` | boolean | 4 | True |
| `data[].active` | boolean | 4 | False |
| `data[].mega` | boolean | 4 | False |
| `data[].message` | string | 4 | Server will reboot after this round. Wil |
| `data[].traceparent` | string | 4 | 00-c3ec2cac69eb66b6ce9cc4c95774c7e0-f417, 00-08456411b75e73ec77500b90de50c03c-92ab, 00-584269909d973fecdfecc834ef52855a-3d7a |
| `direction` | string | 2 | received |
| `event` | string | 6 | maintenanceUpdate |
| `seq` | number | 6 | 8, 10 |
| `source` | string | 2 | cdp_intercept |
| `ts` | string | 6 | 2025-12-14T19:18:10.657917, 2025-12-14T19:35:38.030241, 2025-12-14T19:46:58.195717 |

### mutedPlayers

**Occurrences**: 7

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 7 |  |
| `data.__trace` | boolean | 7 | True |
| `data.traceparent` | string | 7 | 00-c37856d5e5c8910e2f87852550c88ff0-3413, 00-92523f902403b52450cfa2d0884b2715-69df, 00-678b5efbb6477ac5498cfc42e4d80cb9-de65 |
| `direction` | string | 7 | received |
| `event` | string | 7 | mutedPlayers |
| `raw` | string | 2 | 42["mutedPlayers",{"__trace":true,"trace, 42["mutedPlayers",{"__trace":true,"trace |
| `seq` | number | 7 | 25, 18, 14 |
| `source` | string | 7 | cdp_intercept |
| `ts` | string | 7 | 2025-12-15T03:43:09.345974+00:00, 2025-12-15T03:45:01.331730+00:00, 2025-12-15T04:04:50.100386+00:00 |

### newChatMessage

**Occurrences**: 586

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 586 |  |
| `data.__trace` | boolean | 170 | True |
| `data.traceparent` | string | 170 | 00-c1a1507544272c3b9bde563c7116695d-c7e1, 00-f4604eef20a73acda60edae5d84dccbd-64f3, 00-c21755ecf17becfa1f5aa658f4814235-1176 |
| `data[]` | object | 416 |  |
| `data[].__trace` | boolean | 416 | True |
| `data[].discordUsername` | string | 416 | zyzco., bowtrix., demaux |
| `data[].filtered` | boolean | 416 | False |
| `data[].level` | number | 416 | 55, 66, 32 |
| `data[].message` | string | 416 | fuk u bowtrix, im abt ti, get fked |
| `data[].playerId` | string | 416 | did:privy:cmaop45uz00hlla0lwfqcm6h9, did:privy:cmauh6pop009cjp0ljal0roxf, did:privy:cmi5nq4qv00beld0b8739uw7r |
| `data[].replyTo` | null | 416 | None |
| `data[].replyTo.key` | string | 2 | did:privy:cmaop45uz00hlla0lwfqcm6h9-1765, did:privy:cmir9p77o03qll80buq90wzvv-1765 |
| `data[].replyTo.message` | string | 2 | dem rinsed???, How is this not just a scam sites. Like  |
| `data[].replyTo.username` | string | 2 | Zyzco, Greenoodles |
| `data[].role` | null | 416 | None, mod |
| `data[].tag` | string | 416 | ghoul, None, ogplayer |
| `data[].timestamp` | number | 416 | 1765577835613, 1765577844154, 1765577849674 |
| `data[].traceparent` | string | 416 | 00-110726a3a245375ebdad6a1dc00bfbbf-a3cd, 00-48ab2a7c73103d6c2aaa7c224294dc36-525f, 00-8b304b74873814b6d1fad1bbeda36d76-0b78 |
| `data[].username` | string | 416 | Zyzco, bowtrix, Demaux69 |
| `data[].verified` | boolean | 416 | True, False |
| `direction` | string | 170 | received |
| `event` | string | 586 | newChatMessage |
| `raw` | string | 17 | 42["newChatMessage",{"__trace":true,"tra, 42["newChatMessage",{"__trace":true,"tra, 42["newChatMessage",{"__trace":true,"tra |
| `seq` | number | 586 | 75, 114, 140 |
| `source` | string | 170 | cdp_intercept |
| `ts` | string | 586 | 2025-12-12T17:17:14.785930, 2025-12-12T17:17:23.331018, 2025-12-12T17:17:28.862859 |

### newSideBet

**Occurrences**: 36

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 36 |  |
| `data.__trace` | boolean | 19 | True |
| `data.traceparent` | string | 19 | 00-fc856d15bd63b39791db41a0ac4d5901-fc6d, 00-3225cfb3fdfc884db6862ef289c18585-02b7, 00-bf6407dc340974e1337d19708fd6d111-aaab |
| `data[]` | object | 17 |  |
| `data[].__trace` | boolean | 17 | True |
| `data[].betAmount` | number | 17 | 0.1, 0.013, 0.2 |
| `data[].coinAddress` | string | 17 | So11111111111111111111111111111111111111 |
| `data[].endTick` | number | 17 | 72, 105, 44 |
| `data[].gameId` | string | 17 | 20251215-8e73a72051b6458f, 20251215-7233f8519253401d, 20251215-c1e81694e9ce43c9 |
| `data[].level` | number | 17 | 57, 40, 21 |
| `data[].playerId` | string | 17 | did:privy:cmcmrs9kb02jwjo0nhnlrjtto, did:privy:cmfpue0zf002zjr0cb14u2qr0, did:privy:cmi22jn9001m7l10dbwsjj9bp |
| `data[].price` | number | 17 | 1.0842147652620817, 0.9372595754575003, 1.0035868231013891 |
| `data[].startTick` | number | 17 | 32, 65, 4 |
| `data[].tickIndex` | number | 17 | 32, 65, 4 |
| `data[].timestamp` | number | 17 | 1765757912433, 1765757920810, 1765758001120 |
| `data[].traceparent` | string | 17 | 00-3265ebee890380be9c72f84e2616b666-2172, 00-cc2201b94d972fb206f7330e7e6fa46a-4855, 00-b83380d8ba0cf09694e5e52d07b0a852-9d14 |
| `data[].type` | string | 17 | placed |
| `data[].username` | string | 17 | d3e, ecole462469, SideBets |
| `data[].xPayout` | number | 17 | 5 |
| `direction` | string | 19 | received |
| `event` | string | 36 | newSideBet |
| `raw` | string | 9 | 42["newSideBet",{"__trace":true,"tracepa, 42["newSideBet",{"__trace":true,"tracepa, 42["newSideBet",{"__trace":true,"tracepa |
| `seq` | number | 36 | 198, 234, 788 |
| `source` | string | 19 | cdp_intercept |
| `ts` | string | 36 | 2025-12-14T19:18:33.736229, 2025-12-14T19:18:41.898834, 2025-12-14T19:20:02.063618 |

### playerCosmetics

**Occurrences**: 7

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 7 |  |
| `data.__trace` | boolean | 7 | True |
| `data.traceparent` | string | 7 | 00-8d1ee3183410216c5e6a47ce9673b3f8-a9be, 00-2ef1e6d71c8c9e9b606612a4b8438989-fcae, 00-93c202cc7138be5fc62e9e49cdcfeef5-d07a |
| `direction` | string | 7 | received |
| `event` | string | 7 | playerCosmetics |
| `raw` | string | 2 | 42["playerCosmetics",{"__trace":true,"tr, 42["playerCosmetics",{"__trace":true,"tr |
| `seq` | number | 7 | 76, 43, 33 |
| `source` | string | 7 | cdp_intercept |
| `ts` | string | 7 | 2025-12-15T03:43:10.889832+00:00, 2025-12-15T03:45:02.688004+00:00, 2025-12-15T04:04:52.470221+00:00 |

### playerLeaderboardPosition

**Occurrences**: 8

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 8 |  |
| `data.__trace` | boolean | 8 | True |
| `data.traceparent` | string | 8 | 00-f44cf0add30ecdce8b0cbf585578561a-0d01, 00-f3628401273bd552f89a6c59d8c7980e-de42, 00-93b53c210c94d73c6a9771eb820a33c8-0209 |
| `direction` | string | 8 | received |
| `event` | string | 8 | playerLeaderboardPosition |
| `raw` | string | 2 | 42["playerLeaderboardPosition",{"__trace, 42["playerLeaderboardPosition",{"__trace |
| `seq` | number | 8 | 173, 69, 136 |
| `source` | string | 8 | cdp_intercept |
| `ts` | string | 8 | 2025-12-15T03:43:15.253622+00:00, 2025-12-15T03:45:04.483223+00:00, 2025-12-15T04:04:53.998085+00:00 |

### playerUpdate

**Occurrences**: 50

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 50 | <object with 27 keys> |
| `direction` | string | 50 | received |
| `event` | string | 50 | playerUpdate |
| `raw` | string | 7 | 42["playerUpdate",{"id":"did:privy:cmaib, 42["playerUpdate",{"id":"did:privy:cmaib |
| `seq` | number | 50 | 20, 160, 172 |
| `source` | string | 50 | cdp_intercept |
| `ts` | string | 50 | 2025-12-15T03:43:09.293309+00:00, 2025-12-15T03:43:14.693831+00:00, 2025-12-15T03:43:15.236169+00:00 |

### rugRoyaleUpdate

**Occurrences**: 13

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 13 |  |
| `data.activeEventId` | null | 13 | None |
| `data.config` | object | 13 |  |
| `data.config.levelRequired` | number | 13 | 1 |
| `data.config.prepTimeMinutes` | number | 13 | 30 |
| `data.config.prizeTiers` | object | 13 |  |
| `data.config.prizeTiers.1` | number | 13 | 3 |
| `data.config.prizeTiers.2` | number | 13 | 1 |
| `data.config.prizeTiers.3` | number | 13 | 0.5 |
| `data.config.prizeTiers.4` | number | 13 | 0.15 |
| `data.config.prizeTiers.5` | number | 13 | 0.1 |
| `data.config.prizeTiers.6-10` | number | 13 | 0.05 |
| `data.config.startingBalance` | number | 13 | 100 |
| `data.config.token` | string | 13 | 0xPractice |
| `data.currentEvent` | null | 13 | None |
| `data.events` | array | 13 |  |
| `data.finalRound` | boolean | 13 | False |
| `data.history` | array | 13 |  |
| `data.history[]` | object | 13 |  |
| `data.history[].endTime` | string | 13 | 2025-12-11T13:00:00.000Z |
| `data.history[].id` | string | 13 | rugroyale-2025-12-11-1765452603914 |
| `data.history[].leaderboard` | array | 13 |  |
| `data.history[].leaderboard[]` | object | 13 |  |
| `data.history[].leaderboard[].balance` | number | 260 | 5000.965514619, 3700.308356835, 3616.915686586 |
| `data.history[].leaderboard[].lastUpdated` | number | 260 | 1765458003618, 1765458003617, 1765458003619 |
| `data.history[].leaderboard[].level` | number | 260 | 66, 40, 56 |
| `data.history[].leaderboard[].playerId` | string | 260 | did:privy:cmauh6pop009cjp0ljal0roxf, did:privy:cm9g1p6iw00zwjp0m40iwldnz, did:privy:cmgr0n6fu02qvld0djjvkjm59 |
| `data.history[].leaderboard[].rank` | number | 260 | 1, 2, 3 |
| `data.history[].leaderboard[].username` | string | 260 | bowtrix, ereas, Clixmaster |
| `data.history[].savedAt` | string | 13 | 2025-12-11T13:00:10.328Z |
| `data.history[].startTime` | string | 13 | 2025-12-11T12:00:00.000Z |
| `data.history[].winners` | array | 13 |  |
| `data.history[].winners[]` | object | 13 |  |
| `data.history[].winners[].amount` | number | 130 | 1, 0.5, 0.25 |
| `data.history[].winners[].playerId` | string | 130 | did:privy:cmauh6pop009cjp0ljal0roxf, did:privy:cm9g1p6iw00zwjp0m40iwldnz, did:privy:cmgr0n6fu02qvld0djjvkjm59 |
| `data.history[].winners[].rank` | number | 130 | 1, 2, 3 |
| `data.history[].winners[].username` | string | 130 | bowtrix, ereas, Clixmaster |
| `data.isInFinalRound` | boolean | 13 | False |
| `data.leaderboard` | array | 13 |  |
| `data.leaderboard[]` | object | 13 |  |
| `data.leaderboard[].balance` | number | 130 | 5000.965514619, 3700.308356835, 3616.915686586 |
| `data.leaderboard[].lastUpdated` | number | 130 | 1765458003618, 1765458003617, 1765458003619 |
| `data.leaderboard[].level` | number | 130 | 66, 40, 56 |
| `data.leaderboard[].playerId` | string | 130 | did:privy:cmauh6pop009cjp0ljal0roxf, did:privy:cm9g1p6iw00zwjp0m40iwldnz, did:privy:cmgr0n6fu02qvld0djjvkjm59 |
| `data.leaderboard[].rank` | number | 130 | 1, 2, 3 |
| `data.leaderboard[].username` | string | 130 | bowtrix, ereas, Clixmaster |
| `data.playerPosition` | null | 13 | None |
| `data.status` | string | 13 | INACTIVE |
| `data.timeRemaining` | null | 13 | None |
| `data.upcomingEvents` | array | 13 |  |
| `direction` | string | 9 | received |
| `event` | string | 13 | rugRoyaleUpdate |
| `raw` | string | 2 | 42["rugRoyaleUpdate",{"status":"INACTIVE |
| `seq` | number | 13 | 5, 7, 28 |
| `source` | string | 9 | cdp_intercept |
| `ts` | string | 13 | 2025-12-14T19:18:10.650663, 2025-12-14T19:35:38.023933, 2025-12-14T19:46:58.187801 |

### rugpassStatus

**Occurrences**: 8

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 8 |  |
| `data.__trace` | boolean | 8 | True |
| `data.traceparent` | string | 8 | 00-2e73cb06d2b249fe0f9ac7e605d791b1-81dc, 00-626b501b1019b7430bf96ef30d9a442c-6c51, 00-096c617c4127127b1a1896a4f9398744-b0e0 |
| `direction` | string | 8 | received |
| `event` | string | 8 | rugpassStatus |
| `raw` | string | 3 | 42["rugpassStatus",{"__trace":true,"trac, 42["rugpassStatus",{"__trace":true,"trac, 42["rugpassStatus",{"__trace":true,"trac |
| `seq` | number | 8 | 218, 148, 179 |
| `source` | string | 8 | cdp_intercept |
| `ts` | string | 8 | 2025-12-15T03:43:19.405189+00:00, 2025-12-15T03:45:09.287920+00:00, 2025-12-15T04:04:58.170955+00:00 |

### rugpoolDrawing

**Occurrences**: 1

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 1 |  |
| `data.__trace` | boolean | 1 | True |
| `data.traceparent` | string | 1 | 00-ed4eab3cb8080ee46d0b8e709f4a9094-5413 |
| `direction` | string | 1 | received |
| `event` | string | 1 | rugpoolDrawing |
| `raw` | string | 1 | 42["rugpoolDrawing",{"__trace":true,"tra |
| `seq` | number | 1 | 417 |
| `source` | string | 1 | cdp_intercept |
| `ts` | string | 1 | 2025-12-15T17:22:34.608314+00:00 |

### rugpoolStatus

**Occurrences**: 1

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 1 |  |
| `data.__trace` | boolean | 1 | True |
| `data.traceparent` | string | 1 | 00-290d3efbee84e5bae0d9384e67a504d3-4e3c |
| `direction` | string | 1 | received |
| `event` | string | 1 | rugpoolStatus |
| `raw` | string | 1 | 42["rugpoolStatus",{"__trace":true,"trac |
| `seq` | number | 1 | 436 |
| `source` | string | 1 | cdp_intercept |
| `ts` | string | 1 | 2025-12-15T17:22:35.277830+00:00 |

### sidebetEventUpdate

**Occurrences**: 51

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 51 |  |
| `data.__trace` | boolean | 33 | True |
| `data.traceparent` | string | 33 | 00-4fc7a86262b4519b62afa29f4243fc84-292d, 00-c37856d5e5c8910e2f87852550c88ff0-6a2d, 00-e815c828aac943887e520279b4281cc1-c633 |
| `data[]` | object | 18 |  |
| `data[].__trace` | boolean | 18 | True |
| `data[].activeEventId` | null | 18 | None, admin-1179db3a-0bc9-429b-ab58-65d29a9c90 |
| `data[].config` | object | 4 |  |
| `data[].config.levelRequired` | number | 4 | 1 |
| `data[].config.prepTimeMinutes` | number | 4 | 30 |
| `data[].config.prizeTiers` | object | 4 |  |
| `data[].config.prizeTiers.1` | number | 4 | 1 |
| `data[].config.prizeTiers.2` | number | 4 | 0.5 |
| `data[].config.prizeTiers.3` | number | 4 | 0.25 |
| `data[].config.prizeTiers.4` | number | 4 | 0.1 |
| `data[].config.prizeTiers.5-10` | number | 4 | 0.025 |
| `data[].currentEvent` | null | 18 | None |
| `data[].currentEvent.createdAt` | string | 14 | 2025-12-15T05:00:22.120Z |
| `data[].currentEvent.createdBy` | string | 14 | admin |
| `data[].currentEvent.endTime` | string | 14 | 2025-12-15T06:00:00.000Z |
| `data[].currentEvent.id` | string | 14 | admin-1179db3a-0bc9-429b-ab58-65d29a9c90 |
| `data[].currentEvent.levelRequired` | number | 14 | 10 |
| `data[].currentEvent.prepTimeMinutes` | number | 14 | 30 |
| `data[].currentEvent.startTime` | string | 14 | 2025-12-15T05:30:00.000Z |
| `data[].currentEvent.status` | string | 14 | SCHEDULED |
| `data[].events` | array | 18 |  |
| `data[].events[]` | object | 14 |  |
| `data[].events[].createdAt` | string | 14 | 2025-12-15T05:00:22.120Z |
| `data[].events[].createdBy` | string | 14 | admin |
| `data[].events[].endTime` | string | 14 | 2025-12-15T06:00:00.000Z |
| `data[].events[].id` | string | 14 | admin-1179db3a-0bc9-429b-ab58-65d29a9c90 |
| `data[].events[].levelRequired` | number | 14 | 10 |
| `data[].events[].prepTimeMinutes` | number | 14 | 30 |
| `data[].events[].startTime` | string | 14 | 2025-12-15T05:30:00.000Z |
| `data[].events[].status` | string | 14 | SCHEDULED |
| `data[].finalRound` | boolean | 4 | False |
| `data[].history` | array | 4 |  |
| `data[].history[]` | object | 4 |  |
| `data[].history[].endTime` | string | 4 | 2025-11-24T05:00:00.000Z |
| `data[].history[].id` | string | 4 | sidebetevent-2025-11-24-1763958303311 |
| `data[].history[].leaderboard` | array | 4 |  |
| `data[].history[].leaderboard[]` | object | 4 |  |
| `data[].history[].leaderboard[].accuracy` | number | 80 | 33.33333333333333, 28.57142857142857, 25 |
| `data[].history[].leaderboard[].avgTicksOff` | number | 80 | 7.166666666666667, 7.666666666666667, 9.857142857142858 |
| `data[].history[].leaderboard[].lastUpdated` | number | 80 | 1763960402120 |
| `data[].history[].leaderboard[].level` | number | 80 | 6, 3, 10 |
| `data[].history[].leaderboard[].playerId` | string | 80 | did:privy:cmg5lwof500w2l70cczg34vy5, did:privy:cmi2l1t2w0017jv0czi6sjaun, did:privy:cmd05rz9501w9ky0m9toct0e2 |
| `data[].history[].leaderboard[].rank` | number | 80 | 1, 2, 3 |
| `data[].history[].leaderboard[].sidebetsHit` | number | 80 | 2, 1 |
| `data[].history[].leaderboard[].sidebetsPlaced` | number | 80 | 6, 7, 8 |
| `data[].history[].leaderboard[].username` | string | 80 | Rampage, culosucio, Jhhh |
| `data[].history[].savedAt` | string | 4 | 2025-11-24T05:00:08.681Z |
| `data[].history[].startTime` | string | 4 | 2025-11-24T04:55:00.000Z |
| `data[].history[].winners` | array | 4 |  |
| `data[].history[].winners[]` | object | 4 |  |
| `data[].history[].winners[].amount` | number | 40 | 1, 0.5, 0.25 |
| `data[].history[].winners[].playerId` | string | 40 | did:privy:cmg5lwof500w2l70cczg34vy5, did:privy:cmi2l1t2w0017jv0czi6sjaun, did:privy:cmd05rz9501w9ky0m9toct0e2 |
| `data[].history[].winners[].rank` | number | 40 | 1, 2, 3 |
| `data[].history[].winners[].username` | string | 40 | Rampage, culosucio, Jhhh |
| `data[].isInFinalRound` | boolean | 4 | False |
| `data[].leaderboard` | array | 4 |  |
| `data[].leaderboard[]` | object | 4 |  |
| `data[].leaderboard[].accuracy` | number | 40 | 33.33333333333333, 28.57142857142857, 25 |
| `data[].leaderboard[].avgTicksOff` | number | 40 | 7.166666666666667, 7.666666666666667, 9.857142857142858 |
| `data[].leaderboard[].lastUpdated` | number | 40 | 1763960402120 |
| `data[].leaderboard[].level` | number | 40 | 6, 3, 10 |
| `data[].leaderboard[].playerId` | string | 40 | did:privy:cmg5lwof500w2l70cczg34vy5, did:privy:cmi2l1t2w0017jv0czi6sjaun, did:privy:cmd05rz9501w9ky0m9toct0e2 |
| `data[].leaderboard[].rank` | number | 40 | 1, 2, 3 |
| `data[].leaderboard[].sidebetsHit` | number | 40 | 2 |
| `data[].leaderboard[].sidebetsPlaced` | number | 40 | 6, 7, 8 |
| `data[].leaderboard[].username` | string | 40 | Rampage, culosucio, Jhhh |
| `data[].playerPosition` | null | 4 | None |
| `data[].status` | string | 18 | INACTIVE, PREP |
| `data[].timeRemaining` | null | 4 | None |
| `data[].traceparent` | string | 18 | 00-08c1aadc18c8355963863ce7325eee92-78e6, 00-bfbe5e36affc0cdbb914a552ee9115f0-7788, 00-4bc53b2875b25890e503fbb61becd716-ee31 |
| `data[].upcomingEvents` | array | 18 |  |
| `direction` | string | 33 | received |
| `event` | string | 51 | sidebetEventUpdate |
| `raw` | string | 9 | 42["sidebetEventUpdate",{"__trace":true,, 42["sidebetEventUpdate",{"__trace":true,, 42["sidebetEventUpdate",{"__trace":true, |
| `seq` | number | 51 | 6, 8, 29 |
| `source` | string | 33 | cdp_intercept |
| `ts` | string | 51 | 2025-12-14T19:18:10.652184, 2025-12-14T19:35:38.028219, 2025-12-14T19:46:58.192954 |

### standard/newTrade

**Occurrences**: 902

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | array | 902 |  |
| `data.__trace` | boolean | 312 | True |
| `data.traceparent` | string | 312 | 00-dfb772992005c7fb7a05690b2d570aee-9178, 00-6becc03d87e5abd178189f28e0f7243e-718a, 00-0e8811ff0f0dea6bfa34ebf7d328084c-c518 |
| `data[]` | object | 590 |  |
| `data[].__trace` | boolean | 590 | True |
| `data[].amount` | number | 590 | 4.158855049, 5, 0.09 |
| `data[].bonusPortion` | number | 590 | 4.158855048, 5, 0 |
| `data[].coin` | string | 590 | solana |
| `data[].gameId` | string | 590 | 20251212-25dcb17086a24ad7, 20251212-6114b2ff44ef4b71, 20251214-83c1efa1085340c7 |
| `data[].id` | string | 590 | 9d33997e-2bad-4893-9de5-8e8ec708891a, e3c68cb1-b2ed-4224-8568-fe1d099ad643, 30c7a2f0-4083-4ae5-9651-2f34be2ddce1 |
| `data[].level` | number | 590 | 72, 28, 20 |
| `data[].leverage` | number | 278 | 1 |
| `data[].playerId` | string | 590 | did:privy:cmbmoqwxf00uxk40movpxyhjw, did:privy:cmaos0abo03t9kz0mquf6fa4n, did:privy:cmb0dxecy00nckz0nnrs6y7kf |
| `data[].price` | number | 590 | 0.8317710102714284, 0.8283719646298878, 0.5799041862572357 |
| `data[].qty` | number | 590 | 5, 6.035935803, 0.155198051 |
| `data[].realPortion` | number | 590 | 0, 0.09, 0.123 |
| `data[].tickIndex` | number | 590 | 7, 13, 25 |
| `data[].traceparent` | string | 590 | 00-b919294cf518e485acace9c1c391ff34-11e9, 00-e5745f7152844a84442fdde7d30fcd8b-a82a, 00-280b3d8a6216706e1a5582a0980c85c0-907c |
| `data[].type` | string | 590 | sell, buy |
| `data[].username` | string | 590 | Zer02Her0, Boss, GLOSS |
| `direction` | string | 312 | received |
| `event` | string | 902 | standard/newTrade |
| `raw` | string | 24 | 42["standard/newTrade",{"__trace":true,", 42["standard/newTrade",{"__trace":true,", 42["standard/newTrade",{"__trace":true," |
| `seq` | number | 902 | 9, 18, 27 |
| `source` | string | 312 | cdp_intercept |
| `ts` | string | 902 | 2025-12-12T17:17:00.118810, 2025-12-12T17:17:02.258359, 2025-12-12T17:17:04.122813 |

### usernameStatus

**Occurrences**: 14

| Field Path | Type | Count | Sample Values |
|------------|:----:|------:|---------------|
| `data` | object | 14 |  |
| `data.__trace` | boolean | 14 | True |
| `data.traceparent` | string | 14 | 00-c37856d5e5c8910e2f87852550c88ff0-4cd4, 00-ef2fb9766ccb9430cbe6ea907e0ab9b2-f651, 00-92523f902403b52450cfa2d0884b2715-7f66 |
| `direction` | string | 14 | received |
| `event` | string | 14 | usernameStatus |
| `raw` | string | 4 | 42["usernameStatus",{"__trace":true,"tra, 42["usernameStatus",{"__trace":true,"tra, 42["usernameStatus",{"__trace":true,"tra |
| `seq` | number | 14 | 24, 183, 17 |
| `source` | string | 14 | cdp_intercept |
| `ts` | string | 14 | 2025-12-15T03:43:09.331433+00:00, 2025-12-15T03:43:15.541741+00:00, 2025-12-15T03:45:01.326133+00:00 |
