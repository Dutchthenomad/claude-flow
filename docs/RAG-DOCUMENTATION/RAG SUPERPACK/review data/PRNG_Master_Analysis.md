# PRNG Master Analysis for Rugs.fun

## 1. Executive Summary

This report summarizes our analysis of the Rugs.fun gambling platform's provably fair system, presenting significant evidence that the platform operates with a multi-layered architecture consisting of a visible "provably fair" surface layer and a hidden meta-algorithm layer that influences game outcomes. We have identified key discrepancies between the platform's stated mechanics and observed behaviors, developed a hypothesis about cross-game state tracking, and created a structured plan to conclusively validate these findings through statistical analysis.

## 2. System Architecture

### 2.1 The Dual-Layer System

We have identified that Rugs.fun employs a dual-layer architecture:

1.  **Surface Layer (Provably Fair)**
    *   Implements standard cryptographic verification via SHA-256
    *   Combines server seed with game ID to determine outcomes
    *   Publicly verifiable algorithm that passes basic integrity checks
    *   Currently uses Version 3 implementation with specific features

2.  **Suspected Meta-Algorithm Layer**
    *   Evidence suggests a hidden system operating between games
    *   Likely implements treasury protection mechanisms
    *   May classify and treat players differently based on history
    *   Controls directive variables (like `RUG_PROB`) dynamically

## 3. Data Schema Reference

This unified schema document provides:
- Complete field definitions for all 170+ data points
- Data source information for each field
- Risk calculation formulas
- Bayesian analysis applications
- Coverage across all datasets (raw JSONL, basic CSV, expanded CSV, and player-integrated CSV)

## 4. Core PRNG Analysis

This section summarizes the core analysis of the PRNG's randomness and potential vulnerabilities.

### 4.1 Statistical Testing for Randomness

To verify the randomness of the PRNG, a battery of statistical tests should be employed. These tests help to identify non-random patterns that would not be expected in a truly random sequence.

*   **Chi-Squared Test:** Used to determine if the distribution of outcomes (e.g., tick durations, peak multipliers) is uniform. A non-uniform distribution suggests bias.
*   **Runs Test:** Detects sequential dependencies. For example, are wins or losses clustered together more than expected by chance?
*   **Autocorrelation Analysis:** Reveals periodic patterns in the data. For example, does a high peak multiplier tend to appear every N games?
*   **Spectral Analysis (Fourier Transform):** Identifies hidden periodicities that are not obvious in the time domain.
*   **NIST Statistical Test Suite:** A comprehensive set of tests specifically designed for cryptographic randomness evaluation.

### 4.2 Reverse Engineering Findings

Our analysis, detailed in `PRNG_reverseEngineering_analysis.md`, suggests that while the surface-level "provably fair" system uses sound cryptographic principles (HMAC-SHA512), there are several indications of a non-random meta-layer:

*   **Time-Based Seeding Vulnerabilities:** Many PRNGs use predictable time-based seeds. We must analyze the timestamps of seed generation to look for patterns (e.g., correlations with the time of day, or specific microsecond patterns).
*   **Mersenne Twister:** If the platform were to use a statistical PRNG like Mersenne Twister (MT19937), it could be completely broken with only 624 consecutive outputs. While unlikely for a gambling platform, this highlights the importance of using cryptographically secure PRNGs.
*   **Multi-Layered Architecture:** The most likely scenario is a multi-layered system where the final, player-visible cryptographic step is truly random, but the *inputs* to that step are manipulated by a hidden business logic layer. This is where the meta-algorithm likely resides.

## 5. The Meta-Algorithm Hypothesis

Based on our observations, we have formulated a primary hypothesis:

**The Meta-Algorithm Hypothesis**: A hidden, higher-level balancing system exists that operates *between* games. This system dynamically adjusts the core game parameters (particularly `RUG_PROB`) for an upcoming game based on the outcome of the previous game, likely to manage the treasury and player experience.

### 5.1 Evidence for the Meta-Algorithm

*   **Cross-Game Correlation:** We have documented an ~84% probability of an "instarug" (immediate game end) following games with >50x multipliers. This is statistically impossible with the stated 0.5% `RUG_PROB`, providing strong evidence of cross-game state tracking.
*   **Timing Irregularities:** We have observed significant variations in the stated 250ms tick rate, with some candles in longer games lasting substantially more than the expected 1.25 seconds, suggesting dynamic timing adjustments.
*   **The `rugpool` Object:** The existence of the `rugpool` object within the `gameStateUpdate` event suggests a mechanism for managing funds that could be tied to the meta-algorithm.
*   **Version-Specific Implementations:** Different algorithmic parameters exist between versions, confirmed by different outcomes from identical input seeds. This indicates that the platform can and does alter the game mechanics.

### 5.2 Treasury Protection and Player Profiling

The meta-algorithm likely serves two primary purposes:

1.  **Treasury Protection:** After a large payout (e.g., a >50x multiplier win), the system may increase the probability of an instarug in the next game to recoup losses and protect the treasury.
2.  **Player Profiling:** The system may classify players into segments (e.g., new players, VIPs, consistent winners) and adjust game parameters accordingly. This could include:
    *   A "honeymoon period" for new players with a higher chance of winning.
    *   "Mercy wins" for players on long losing streaks to encourage retention.
    *   Less favorable odds for consistently winning players.

## 6. Predictive Modeling & Indicators

This section focuses on the practical application of our research: building predictive models and identifying key indicators of game outcomes.

### 6.1 Tick-by-Tick Analysis: The Pre-Rug Volatility Spike

A key finding from our tick-by-tick analysis is that **volatility increases by approximately 78% in the final 5 ticks before a rug**. This is a critical early warning signal.

*   **Normal Volatility:** 0.147
*   **Near-Rug Volatility (last 5 ticks):** 0.262

This volatility spike can be used as a primary input for a real-time rug prediction model.

### 6.2 Player Behavior Analysis

By analyzing the `player_integrated_data.csv`, we can classify players into different trading patterns. The presence of certain player types can be an indicator of game outcomes:

*   **Whales (low-frequency, high-volume):** The actions of whales can significantly impact the market. A whale exiting a game can be a strong signal of an impending rug.
*   **Scalpers (high-frequency, low-volume):** A high number of scalpers can indicate a healthy, active market, but can also contribute to volatility.
*   **Hodlers (buy-and-hold):** A large number of hodlers can create a stable price floor, but their eventual exit can cause a sharp drop.

### 6.3 Bayesian Models

Our Bayesian models, detailed in `BAYESIAN_MODELS.md`, provide a framework for updating our beliefs about the probability of a rug in real-time. The core formula is:

`P(rug | evidence) = P(evidence | rug) * P(rug) / P(evidence)`

Where "evidence" can be:

*   The current tick number
*   The current peak multiplier
*   The current volatility
*   The presence of certain player types

By continuously updating our probabilities with new evidence, we can create a dynamic risk assessment tool.

## 7. Trading Strategies & Implementation

This section consolidates our research into actionable trading strategies.

### 7.1 Strategic Trading Zones

Based on our analysis, we have identified six distinct trading zones:

*   **Low Risk Entry Zone (1x-2x):** Safe entry, low volatility.
*   **Balanced Trading Zone (2x-4x):** Optimal risk-reward.
*   **Growth Opportunity Zone (4x-9x):** Good potential, but requires careful timing.
*   **High Risk/High Reward Zone (9x-25x):** Quick scalping only.
*   **Danger Zone (25x-100x):** Exit only.
*   **Extreme Zone (100x+):** Immediate exit.

### 7.2 Optimal Trading Strategies

We have developed two primary strategies:

1.  **Balanced Range Trading (3.2x → 4.8x):**
    *   **Entry:** 3.2x
    *   **Exit:** 4.8x (50% gain)
    *   **Stop Loss:** 2.8x (12.5% loss)
    *   **Risk-Reward Ratio:** 1:4
    *   **Expected Success Rate:** ~65%

2.  **Growth Zone Scalping (8.5x → 14x):**
    *   **Entry:** 8.5x
    *   **Exit:** 14x (65% gain)
    *   **Stop Loss:** 7x (17.6% loss)
    *   **Risk-Reward Ratio:** ~1:3.7
    *   **Expected Success Rate:** ~55%

### 7.3 Risk Management

*   **Position Sizing:** Adjust your position size based on the trading zone, from 50% of bankroll in the low-risk zone to 0% in the extreme zone.
*   **Stop Loss Discipline:** Always use stop losses and never move them lower.
*   **Tick Timer Awareness:** Be more cautious as the game progresses, especially after 100+ ticks.

## 8. Data Collection & Analysis Framework

This section provides a "how-to" guide for ongoing research and analysis.

### 8.1 Data Collection

The primary method for data collection is via a WebSocket connection to the Rugs.fun server. The `comprehensive_rugs_analysis_report.md` contains a Python script (`RugsDataCollector`) that can be used for this purpose. The script should be run continuously to capture as many games as possible.

### 8.2 Data Analysis Workflow

Our analysis is performed by a series of Python scripts:

1.  **`analyze_rugs_data.py`:** Extracts basic game metrics and creates `rugs_bayesian_data.csv`.
2.  **`player_integrated_analysis.py`:** Combines game metrics with player trading data to create `player_integrated_data.csv`.
3.  **`tick_by_tick_analysis.py`:** Performs granular analysis of each tick and creates `tick_by_tick_data.csv`.

These scripts should be run in order to generate the datasets required for our analysis. The resulting CSV files can then be used in Google Sheets, Jupyter notebooks, or other analysis tools.

### 8.3 Living Document

This `PRNG_Master_Analysis.md` document should be treated as a living document. As new data is collected and new insights are discovered, this document should be updated to reflect the latest state of our knowledge.

## 9. Appendices

### 9.1 Volatility Reference Guide

The relationship between price and volatility follows a square root function: `volatility = 0.005 * min(10, sqrt(price))`

| Price | Volatility | Min Change | Max Change | Notes |
|---|---|---|---|---|
| 1x | 0.50% | 0.00%* | 3.50% | Starting price |
| 2x | 0.71% | 0.00%* | 3.71% | × √2 increase from 1x |
| 4x | 1.00% | 0.00%* | 4.00% | × √2 increase from 2x |
| 9x | 1.50% | 0.00%* | 4.50% | × √2.25 increase from 4x |
| 16x | 2.00% | 0.00%* | 5.00% | × √1.78 increase from 9x |
| 25x | 2.50% | 0.50% | 5.50% | One-quarter to max volatility |
| 36x | 3.00% | 1.00% | 6.00% | × √1.44 increase from 25x |
| 49x | 3.50% | 1.50% | 6.50% | × √1.36 increase from 36x |
| 64x | 4.00% | 2.00% | 7.00% | × √1.31 increase from 49x |
| 81x | 4.50% | 2.50% | 7.50% | × √1.27 increase from 64x |
| 100x | 5.00% | 3.00% | 8.00% | Volatility cap reached |
| >100x | 5.00% | 3.00% | 8.00% | No further increase |

*Min change is capped at 0% (cannot be negative)

### 9.2 Source Files

For historical reference, the original research documents can be found in the same directory as this file.
