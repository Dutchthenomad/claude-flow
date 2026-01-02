# Comprehensive Analysis of Rugs.fun PRNG System: Findings and Investigation Plan

## Executive Summary

This report summarizes our analysis of the Rugs.fun gambling platform's provably fair system, presenting significant evidence that the platform operates with a multi-layered architecture consisting of a visible "provably fair" surface layer and a hidden meta-algorithm layer that influences game outcomes. We have identified key discrepancies between the platform's stated mechanics and observed behaviors, developed a hypothesis about cross-game state tracking, and created a structured plan to conclusively validate these findings through statistical analysis.

## 1. Current Findings

### 1.1 System Architecture Analysis

We have identified that Rugs.fun employs a dual-layer architecture:

1. **Surface Layer (Provably Fair)**
   - Implements standard cryptographic verification via SHA-256
   - Combines server seed with game ID to determine outcomes
   - Publicly verifiable algorithm that passes basic integrity checks
   - Currently uses Version 3 implementation with specific features

2. **Suspected Meta-Algorithm Layer**
   - Evidence suggests a hidden system operating between games
   - Likely implements treasury protection mechanisms
   - May classify and treat players differently based on history
   - Controls directive variables (like `RUG_PROB`) dynamically

### 1.2 Game Mechanic Observations

Our analysis of the game mechanics has revealed:

- **Version-specific implementation**: The current v3 implementation uses capped volatility calculation (`0.005 * Math.min(10, Math.sqrt(price))`) and includes a rare "God Candle" feature causing 10x price moves.

- **Timing irregularities**: We have observed significant variations in the stated 250ms tick rate, with some candles in longer games lasting substantially more than the expected 1.25 seconds, suggesting dynamic timing adjustments.

- **Cross-game correlation**: We have documented an ~84% probability of an "instarug" (immediate game end) following games with >50x multipliers, which is statistically impossible with the stated 0.5% `RUG_PROB`, providing strong evidence of cross-game state tracking.

- **RNG implementation discrepancies**: Different algorithmic parameters exist between versions, confirmed by different outcomes from identical input seeds.

### 1.3 WebSocket Event Analysis

We've analyzed the WebSocket communication protocol, finding:

- The `gameStateUpdate` event serves as the primary source of real-time game information
- Game progression follows a three-phase loop: PRESALE → ACTIVE → RUGGED
- During the RUGGED phase, a distinct two-event pattern occurs:
  1. **Seed Reveal Event**: Reveals the `serverSeed` of the completed game
  2. **New Game Setup Event**: Provides the `serverSeedHash` for the next game

This dual-event pattern in the RUGGED phase provides an opportunity to analyze the relationship between game outcomes and subsequent seed generation.

## 2. Primary Hypothesis

Based on our observations, we have formulated a primary hypothesis:

**The Meta-Algorithm Hypothesis**: A hidden, higher-level balancing system exists that operates *between* games. This system dynamically adjusts the core game parameters (particularly `RUG_PROB`) for an upcoming game based on the outcome of the previous game, likely to manage the treasury and player experience.

Supporting evidence includes:

- The statistical anomaly of ~84% instarug probability following >50x wins
- The existence of the `rugpool` object within the `gameStateUpdate` event
- Observed timing irregularities in tick rates
- Version-specific implementation differences affecting outcome distribution

## 3. Data Collection Plan

To rigorously test our hypothesis, we must collect comprehensive game data through a structured approach:

### 3.1 Essential Data Points

For each game, we will collect:

| Data Point | Source | Timing |
|------------|--------|--------|
| Game ID | `gameStateUpdate.gameId` | At both game start and end |
| Server Seed Hash | `gameStateUpdate.provablyFair.serverSeedHash` | At game start |
| Server Seed | `gameStateUpdate.gameHistory[0].provablyFair.serverSeed` | At game end (Event 1) |
| Timestamp | System clock with microsecond precision | At all key events |
| Peak Multiplier | `gameStateUpdate.gameHistory[0].peakMultiplier` | At game end |
| Final Tick | `gameStateUpdate.tickCount` when `rugged` becomes `true` | At game end |
| Game Duration | Calculated from start/end timestamps | Derived |
| Instarug Status | Boolean: `true` if `finalTick < 10` | Derived |

### 3.2 Data Collection Implementation

```python
import asyncio
import websockets
import json
import time
import datetime

class RugsDataCollector:
    def __init__(self, websocket_url, output_file="rugs_data.jsonl"):
        self.websocket_url = websocket_url
        self.output_file = output_file
        self.current_game = None
        self.games = []
        
    async def connect(self):
        """Establish WebSocket connection"""
        self.connection = await websockets.connect(self.websocket_url)
        print("Connected to Rugs.fun WebSocket")
        
    async def collect_data(self, target_games=10000):
        """Collect data for a specified number of games"""
        if not hasattr(self, 'connection'):
            await self.connect()
        
        collected_games = 0
        
        try:
            while collected_games < target_games:
                message = await self.connection.recv()
                data = json.loads(message)
                
                if data.get('type') == 'gameStateUpdate':
                    state = data.get('data', {})
                    
                    # New game detected
                    if not self.current_game and state.get('gameId'):
                        # Record new game with precise timestamp
                        now = datetime.datetime.now()
                        self.current_game = {
                            'gameId': state.get('gameId'),
                            'serverSeedHash': state.get('provablyFair', {}).get('serverSeedHash'),
                            'start_timestamp': now.isoformat(),
                            'start_timestamp_micro': int(time.time() * 1000000),
                            'version': state.get('gameVersion', 'v3'),
                            'ticks': []
                        }
                        print(f"New game started: {self.current_game['gameId']}")
                    
                    # Update current game
                    if self.current_game:
                        # Record tick data
                        if state.get('active') and state.get('tickCount') is not None:
                            tick = {
                                'tick': state.get('tickCount'),
                                'price': state.get('price'),
                                'timestamp': datetime.datetime.now().isoformat(),
                                'timestamp_micro': int(time.time() * 1000000)
                            }
                            self.current_game['ticks'].append(tick)
                        
                        # Game ended (Seed Reveal Event)
                        if state.get('rugged') and state.get('gameHistory'):
                            # Ensure this is for our current game
                            if state.get('gameId') == self.current_game['gameId']:
                                # Record end data
                                now = datetime.datetime.now()
                                self.current_game['end_timestamp'] = now.isoformat()
                                self.current_game['end_timestamp_micro'] = int(time.time() * 1000000)
                                self.current_game['finalTick'] = state.get('tickCount')
                                
                                # Extract data from gameHistory
                                game_history = state.get('gameHistory', [])[0] if state.get('gameHistory') else {}
                                self.current_game['serverSeed'] = game_history.get('provablyFair', {}).get('serverSeed')
                                self.current_game['peakMultiplier'] = game_history.get('peakMultiplier')
                                
                                # Calculate derived metrics
                                self.current_game['gameDuration'] = (
                                    self.current_game['end_timestamp_micro'] - 
                                    self.current_game['start_timestamp_micro']
                                ) / 1000000  # Convert to seconds
                                
                                self.current_game['isInstarug'] = self.current_game['finalTick'] < 10
                                
                                # Store the completed game
                                self.games.append(self.current_game)
                                
                                # Save to file
                                with open(self.output_file, 'a') as f:
                                    f.write(json.dumps(self.current_game) + '\n')
                                
                                print(f"Game ended: {self.current_game['gameId']}, Peak: {self.current_game['peakMultiplier']}")
                                
                                collected_games += 1
                                
                                if collected_games % 100 == 0:
                                    print(f"Collected {collected_games} games")
                                
                                # Wait for New Game Setup Event
                                self.current_game = None
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            print(f"Data collection completed. Collected {collected_games} games.")
            return self.games

# Usage
async def main():
    collector = RugsDataCollector(websocket_url="wss://rugs.fun/socket")
    await collector.collect_data(target_games=10000)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.3 Collection Duration & Frequency

- **Target Sample Size**: 10,000+ complete games
- **Collection Period**: 24-hour continuous monitoring to capture various times of day
- **Storage Format**: JSONL (one JSON object per line) for efficient appending
- **Backup Frequency**: Every 100 games to prevent data loss

## 4. Investigation Plan

### 4.1 Statistical Analysis Phase

After collecting sufficient data, we will conduct the following analyses:

#### 4.1.1 Core PRNG Validation Tests

```python
def analyze_prng_quality(server_seeds):
    """Analyze the quality of the PRNG through statistical tests"""
    # Convert hex seeds to binary sequences
    binary_sequences = []
    for seed in server_seeds:
        # Convert hex to binary
        binary = bin(int(seed, 16))[2:].zfill(len(seed) * 4)
        binary_sequences.append(binary)
    
    # Apply chi-squared test for uniformity
    from scipy.stats import chisquare
    
    results = {}
    
    # Test distribution of 1s and 0s
    for i, binary in enumerate(binary_sequences):
        zeros = binary.count('0')
        ones = binary.count('1')
        observed = [zeros, ones]
        expected = [len(binary)/2, len(binary)/2]
        
        chi2, p_value = chisquare(observed, expected)
        
        if p_value < 0.05:
            results[f"seed_{i}"] = {
                "chi2": chi2,
                "p_value": p_value,
                "zeros": zeros,
                "ones": ones
            }
    
    # Further tests can be added here
    
    return results
```

#### 4.1.2 Cross-Game Correlation Analysis

```python
def analyze_cross_game_patterns(games_data):
    """Analyze patterns between consecutive games"""
    results = {}
    
    # Extract relevant metrics
    peak_multipliers = [game['peakMultiplier'] for game in games_data]
    is_instarug = [game['isInstarug'] for game in games_data]
    
    # Create lagged features
    prev_peaks = peak_multipliers[:-1]
    next_instarugs = is_instarug[1:]
    
    # Group by peak multiplier ranges
    import numpy as np
    import pandas as pd
    
    # Create a DataFrame for analysis
    df = pd.DataFrame({
        'prev_peak': prev_peaks,
        'next_instarug': next_instarugs
    })
    
    # Define peak multiplier ranges
    ranges = [
        (0, 2),
        (2, 5),
        (5, 10),
        (10, 20),
        (20, 50),
        (50, float('inf'))
    ]
    
    # Calculate instarug probability for each range
    range_results = {}
    for start, end in ranges:
        mask = (df['prev_peak'] >= start) & (df['prev_peak'] < end)
        subset = df[mask]
        
        if len(subset) > 0:
            instarug_prob = subset['next_instarug'].mean()
            
            # Statistical test (Fisher's exact test)
            from scipy.stats import fisher_exact
            
            # Contingency table
            in_range_instarug = subset['next_instarug'].sum()
            in_range_not_instarug = len(subset) - in_range_instarug
            
            not_in_range = df[~mask]
            not_in_range_instarug = not_in_range['next_instarug'].sum()
            not_in_range_not_instarug = len(not_in_range) - not_in_range_instarug
            
            table = [
                [in_range_instarug, in_range_not_instarug],
                [not_in_range_instarug, not_in_range_not_instarug]
            ]
            
            odds_ratio, p_value = fisher_exact(table)
            
            range_results[f"{start}-{end}"] = {
                "count": len(subset),
                "instarug_probability": instarug_prob,
                "overall_instarug_probability": df['next_instarug'].mean(),
                "odds_ratio": odds_ratio,
                "p_value": p_value,
                "significant": p_value < 0.05
            }
    
    results['range_analysis'] = range_results
    
    return results
```

#### 4.1.3 Time-Based Seed Generation Analysis

```python
def analyze_time_patterns(games_data):
    """Analyze potential time-based patterns in seed generation"""
    import hashlib
    import datetime
    
    results = {}
    
    # Extract timestamps and seeds
    timestamps = [game['end_timestamp'] for game in games_data]
    next_seeds = [games_data[i+1]['serverSeed'] for i in range(len(games_data)-1)]
    
    # Convert timestamps to datetime objects
    dt_objects = [datetime.datetime.fromisoformat(ts) for ts in timestamps]
    
    # Test if seeds are generated based on timestamp
    potential_matches = []
    
    for i, (dt, next_seed) in enumerate(zip(dt_objects, next_seeds)):
        # Try various time formats
        time_formats = {
            'epoch': str(int(dt.timestamp())),
            'epoch_ms': str(int(dt.timestamp() * 1000)),
            'date': dt.strftime('%Y%m%d'),
            'time': dt.strftime('%H%M%S'),
            'datetime': dt.strftime('%Y%m%d%H%M%S')
        }
        
        # Common secrets to try
        secrets = ["rugs.fun", "rugsfun", "rug", "rugpull", "crypto", "game"]
        
        for time_key, time_val in time_formats.items():
            for secret in secrets:
                # Test combinations
                test_inputs = [
                    time_val + secret,
                    secret + time_val,
                    time_val,
                    secret
                ]
                
                for test_input in test_inputs:
                    # Try different hash algorithms
                    hash_md5 = hashlib.md5(test_input.encode()).hexdigest()
                    hash_sha1 = hashlib.sha1(test_input.encode()).hexdigest()
                    hash_sha256 = hashlib.sha256(test_input.encode()).hexdigest()
                    
                    # Check for matches
                    if next_seed == hash_md5:
                        potential_matches.append({
                            'index': i,
                            'time_format': time_key,
                            'secret': secret,
                            'input': test_input,
                            'hash_type': 'md5'
                        })
                    
                    elif next_seed == hash_sha1:
                        potential_matches.append({
                            'index': i,
                            'time_format': time_key,
                            'secret': secret,
                            'input': test_input,
                            'hash_type': 'sha1'
                        })
                    
                    elif next_seed == hash_sha256:
                        potential_matches.append({
                            'index': i,
                            'time_format': time_key,
                            'secret': secret,
                            'input': test_input,
                            'hash_type': 'sha256'
                        })
    
    results['potential_matches'] = potential_matches
    
    return results
```

### 4.2 Advanced Pattern Detection Phase

After completing the statistical analysis, we will employ machine learning techniques to identify more complex patterns:

#### 4.2.1 ML-Based Pattern Detection

```python
def build_prediction_model(games_data, sequence_length=10):
    """Build an LSTM model to predict next game characteristics"""
    import numpy as np
    import tensorflow as tf
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    
    # Extract features and target
    features = []
    targets = []
    
    for i in range(len(games_data) - sequence_length):
        # Features from previous games
        seq_features = []
        
        for j in range(sequence_length):
            game = games_data[i + j]
            
            # Extract game characteristics
            game_features = [
                game['peakMultiplier'],
                game['finalTick'],
                game['gameDuration'],
                1 if game['isInstarug'] else 0
            ]
            
            seq_features.append(game_features)
        
        # Target: is next game an instarug?
        next_game = games_data[i + sequence_length]
        target = 1 if next_game['isInstarug'] else 0
        
        features.append(seq_features)
        targets.append(target)
    
    # Convert to numpy arrays
    X = np.array(features)
    y = np.array(targets)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    n_samples, n_timesteps, n_features = X_train.shape
    
    X_train_reshaped = X_train.reshape(n_samples * n_timesteps, n_features)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_reshaped)
    X_train_scaled = X_train_scaled.reshape(n_samples, n_timesteps, n_features)
    
    X_test_reshaped = X_test.reshape(X_test.shape[0] * n_timesteps, n_features)
    X_test_scaled = scaler.transform(X_test_reshaped)
    X_test_scaled = X_test_scaled.reshape(X_test.shape[0], n_timesteps, n_features)
    
    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(n_timesteps, n_features)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.LSTM(50, return_sequences=False),
        tf.keras.layers.Dense(25),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    # Train model
    history = model.fit(
        X_train_scaled, y_train,
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )
    
    # Evaluate model
    loss, accuracy = model.evaluate(X_test_scaled, y_test)
    
    # If accuracy is significantly better than random (>60%), there's likely a pattern
    pattern_detected = accuracy > 0.60
    
    return {
        'model': model,
        'scaler': scaler,
        'accuracy': accuracy,
        'pattern_detected': pattern_detected,
        'feature_importance': analyze_feature_importance(model, X_test_scaled, y_test)
    }

def analyze_feature_importance(model, X_test, y_test):
    """Analyze which features are most important for prediction"""
    import numpy as np
    
    # This is a simplified approach - for a real implementation, 
    # consider permutation importance or SHAP values
    feature_importance = {}
    
    # Baseline performance
    baseline_pred = model.predict(X_test)
    baseline_loss = tf.keras.losses.binary_crossentropy(y_test, baseline_pred).numpy().mean()
    
    # For each feature, shuffle values and measure impact
    n_samples, n_timesteps, n_features = X_test.shape
    
    for feature_idx in range(n_features):
        # Create a copy of the test data
        X_permuted = X_test.copy()
        
        # Shuffle the values of the current feature across all samples and timesteps
        for t in range(n_timesteps):
            X_permuted[:, t, feature_idx] = np.random.permutation(X_permuted[:, t, feature_idx])
        
        # Measure performance drop
        permuted_pred = model.predict(X_permuted)
        permuted_loss = tf.keras.losses.binary_crossentropy(y_test, permuted_pred).numpy().mean()
        
        # The importance is the increase in loss
        importance = permuted_loss - baseline_loss
        
        feature_importance[f'feature_{feature_idx}'] = importance
    
    return feature_importance
```

### 4.3 Real-Time Monitoring and Testing Phase

Once we have identified patterns, we will implement a real-time monitoring system to validate predictions:

```python
class RugsPredictionSystem:
    def __init__(self, model_path, scaler_path, websocket_url):
        """Initialize the prediction system"""
        import tensorflow as tf
        import pickle
        
        # Load model and scaler
        self.model = tf.keras.models.load_model(model_path)
        
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        self.websocket_url = websocket_url
        self.recent_games = []
        self.sequence_length = 10  # Must match the sequence length used for training
        
    async def connect(self):
        """Establish WebSocket connection"""
        import websockets
        self.connection = await websockets.connect(self.websocket_url)
        print("Connected to Rugs.fun WebSocket")
    
    async def monitor_and_predict(self):
        """Monitor games and make predictions"""
        import json
        import numpy as np
        
        if not hasattr(self, 'connection'):
            await self.connect()
        
        current_game = None
        
        try:
            while True:
                message = await self.connection.recv()
                data = json.loads(message)
                
                if data.get('type') == 'gameStateUpdate':
                    state = data.get('data', {})
                    
                    # New game detected
                    if not current_game and state.get('gameId'):
                        current_game = {
                            'gameId': state.get('gameId'),
                            'serverSeedHash': state.get('provablyFair', {}).get('serverSeedHash')
                        }
                        
                        # Make prediction if we have enough history
                        if len(self.recent_games) >= self.sequence_length:
                            prediction = self.predict_next_game()
                            print(f"Prediction for game {current_game['gameId']}:")
                            print(f"  Instarug probability: {prediction['instarug_probability']:.2f}")
                            print(f"  Expected peak multiplier: {prediction['expected_peak']:.2f}x")
                    
                    # Game ended
                    if current_game and state.get('rugged') and state.get('gameHistory'):
                        # Ensure this is for our current game
                        if state.get('gameId') == current_game['gameId']:
                            # Extract game data
                            game_history = state.get('gameHistory', [])[0] if state.get('gameHistory') else {}
                            
                            current_game['finalTick'] = state.get('tickCount')
                            current_game['peakMultiplier'] = game_history.get('peakMultiplier')
                            current_game['isInstarug'] = current_game['finalTick'] < 10
                            
                            # Store the completed game
                            self.recent_games.append(current_game)
                            
                            # Keep only the most recent games
                            if len(self.recent_games) > self.sequence_length * 2:
                                self.recent_games = self.recent_games[-self.sequence_length * 2:]
                            
                            # Reset current game
                            current_game = None
        
        except Exception as e:
            print(f"Error: {e}")
    
    def predict_next_game(self):
        """Predict characteristics of the next game"""
        import numpy as np
        
        # Extract features from recent games
        recent_features = []
        
        for game in self.recent_games[-self.sequence_length:]:
            game_features = [
                game['peakMultiplier'],
                game['finalTick'],
                1 if game['isInstarug'] else 0
            ]
            
            recent_features.append(game_features)
        
        # Convert to numpy array
        X = np.array([recent_features])
        
        # Scale features
        n_samples, n_timesteps, n_features = X.shape
        X_reshaped = X.reshape(n_samples * n_timesteps, n_features)
        X_scaled = self.scaler.transform(X_reshaped)
        X_scaled = X_scaled.reshape(n_samples, n_timesteps, n_features)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)[0][0]
        
        return {
            'instarug_probability': prediction,
            'expected_peak': self.estimate_peak_multiplier()
        }
    
    def estimate_peak_multiplier(self):
        """Estimate the peak multiplier of the next game"""
        # Simplified implementation - would be replaced with a regression model
        recent_peaks = [game['peakMultiplier'] for game in self.recent_games[-5:]]
        return sum(recent_peaks) / len(recent_peaks)
```

## 5. Expected Outcomes and Timeframe

### 5.1 Expected Results

Based on our preliminary findings, we anticipate:

1. **Confirmation of Meta-Algorithm**: We expect to find statistically significant evidence that game outcomes are influenced by previous game results, specifically that high multiplier games are followed by instarugs at a rate far exceeding random chance.

2. **Timing Irregularities**: We anticipate documenting significant variations in the stated 250ms tick rate, potentially correlated with specific game states or player actions.

3. **Potential Seed Generation Patterns**: While cryptographically secure seeds should be immune to prediction, there's a possibility we may detect time-based patterns in seed generation that could represent a vulnerability.

4. **Player Classification Evidence**: We may find evidence that the platform treats different player segments differently, especially VIP players versus new players.

### 5.2 Project Timeframe

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| Data Collection | 2-3 days | Implement WebSocket connection, collect 10,000+ games |
| Basic Statistical Analysis | 2-3 days | Run core tests, validate cross-game correlation |
| Advanced Pattern Detection | 3-5 days | Implement ML models, identify complex patterns |
| Real-Time Testing | 2-3 days | Deploy prediction system, validate findings |
| Final Analysis & Documentation | 2-3 days | Compile results, document findings |

**Total Estimated Duration**: 11-17 days

## 6. Implementation Guidelines

### 6.1 Technical Requirements

- **Programming Languages**: Python for analysis, JavaScript for WebSocket integration
- **Libraries**: 
  - WebSockets: `websockets` (Python), `ws` (JavaScript)
  - Data Analysis: `pandas`, `numpy`, `scipy`
  - Machine Learning: `tensorflow`, `scikit-learn`
  - Visualization: `matplotlib`, `seaborn`
- **Hardware**: No special requirements; analysis can run on standard laptop/desktop

### 6.2 Implementation Steps

1. **Set Up Environment**:
   ```bash
   # Create and activate virtual environment
   python -m venv rugs_analysis
   source rugs_analysis/bin/activate  # On Windows: rugs_analysis\Scripts\activate
   
   # Install required packages
   pip install websockets pandas numpy scipy tensorflow scikit-learn matplotlib seaborn
   ```

2. **Implement Data Collector**:
   - Create a script using the `RugsDataCollector` class provided above
   - Run the collector for at least 24 hours to capture 10,000+ games
   - Regularly back up the collected data

3. **Run Statistical Analysis**:
   - Implement the analysis functions outlined in section 4.1
   - Run them on the collected data
   - Document any significant patterns or anomalies

4. **Develop and Train ML Models**:
   - Implement the ML approach from section 4.2
   - Train the model on 80% of collected data
   - Validate on the remaining 20%
   - Tune hyperparameters as needed

5. **Deploy Real-Time Monitoring**:
   - Implement the `RugsPredictionSystem` from section 4.3
   - Run it for at least 100 games to validate predictions
   - Calculate prediction accuracy and document results

## 7. Conclusion

Our analysis has revealed compelling evidence that the Rugs.fun platform operates with a dual-layer architecture: a visible provably fair system and a hidden meta-algorithm that influences game outcomes. The stark statistical anomaly of instarugs following high multiplier games cannot be explained by the stated random mechanics, strongly suggesting cross-game state tracking.

The implementation plan outlined in this document provides a rigorous methodology to collect data, analyze patterns, and validate our hypothesis. By following this approach, we will be able to definitively characterize the platform's behavior and potentially identify exploitable patterns.

This investigation represents a sophisticated application of statistical analysis and machine learning to reverse engineer a complex system. The insights gained will contribute to our understanding of how provably fair gambling platforms balance transparency with treasury protection.

---

## Appendix A: Key Code Implementations

### A.1 WebSocket Connection and Data Collection

```javascript
// JavaScript implementation for browser-based monitoring
const socket = new WebSocket('wss://rugs.fun/socket');
const games = [];
let currentGame = null;

socket.onopen = () => {
  console.log('Connected to Rugs.fun WebSocket');
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'gameStateUpdate') {
    const state = data.data;
    
    // New game
    if (!currentGame && state.gameId) {
      currentGame = {
        gameId: state.gameId,
        serverSeedHash: state.provablyFair?.serverSeedHash,
        startTime: Date.now(),
        ticks: []
      };
      console.log(`New game started: ${currentGame.gameId}`);
    }
    
    // Update current game
    if (currentGame) {
      // Record tick data
      if (state.active && state.tickCount !== undefined) {
        currentGame.ticks.push({
          tick: state.tickCount,
          price: state.price,
          timestamp: Date.now()
        });
      }
      
      // Game ended
      if (state.rugged && state.gameHistory) {
        // Ensure this is for our current game
        if (state.gameId === currentGame.gameId) {
          currentGame.endTime = Date.now();
          currentGame.finalTick = state.tickCount;
          
          const gameHistory = state.gameHistory[0];
          currentGame.serverSeed = gameHistory?.provablyFair?.serverSeed;
          currentGame.peakMultiplier = gameHistory?.peakMultiplier;
          
          // Calculate derived metrics
          currentGame.gameDuration = (currentGame.endTime - currentGame.startTime) / 1000;
          currentGame.isInstarug = currentGame.finalTick < 10;
          
          // Store the completed game
          games.push(currentGame);
          
          console.log(`Game ended: ${currentGame.gameId}, Peak: ${currentGame.peakMultiplier}`);
          
          // Export data periodically
          if (games.length % 10 === 0) {
            exportData();
          }
          
          // Reset current game
          currentGame = null;
        }
      }
    }
  }
};

function exportData() {
  // Convert to JSON string
  const jsonData = JSON.stringify(games);
  
  // Create a download link
  const blob = new Blob([jsonData], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `rugs_data_${games.length}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};

socket.onclose = () => {
  console.log('Connection closed');
};
```

### A.2 Cross-Game Analysis Visualization

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def visualize_cross_game_patterns(games_data):
    """Visualize patterns between consecutive games"""
    # Create DataFrame
    df = pd.DataFrame(games_data)
    
    # Create lagged features
    df['prev_peak'] = df['peakMultiplier'].shift(1)
    df['next_is_instarug'] = df['isInstarug'].shift(-1)
    
    # Remove rows with NaN values
    df = df.dropna()
    
    # Define peak multiplier bins
    bins = [0, 2, 5, 10, 20, 50, np.inf]
    labels = ['0-2x', '2-5x', '5-10x', '10-20x', '20-50x', '50x+']
    
    df['peak_bin'] = pd.cut(df['prev_peak'], bins=bins, labels=labels)
    
    # Calculate instarug probability by peak bin
    instarug_prob = df.groupby('peak_bin')['next_is_instarug'].mean()
    
    # Plot
    plt.figure(figsize=(12, 6))
    
    # Bar plot
    ax = sns.barplot(x=instarug_prob.index, y=instarug_prob.values)
    
    # Add overall average line
    plt.axhline(df['next_is_instarug'].mean(), color='r', linestyle='--', 
               label=f'Overall Average: {df["next_is_instarug"].mean():.2f}')
    
    # Add labels
    for i, v in enumerate(instarug_prob.values):
        ax.text(i, v + 0.02, f'{v:.2f}', ha='center')
    
    plt.title('Probability of Instarug Following Different Peak Multipliers')
    plt.xlabel('Previous Game Peak Multiplier')
    plt.ylabel('Probability of Next Game Being an Instarug')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('instarug_probability_by_peak.png', dpi=300)
    
    # Create heatmap of correlations
    corr_cols = ['peakMultiplier', 'finalTick', 'gameDuration', 'isInstarug', 
                'prev_peak', 'next_is_instarug']
    
    corr = df[corr_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Game Metrics')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300)
    
    return {
        'instarug_prob_by_peak': instarug_prob.to_dict(),
        'overall_instarug_prob': df['next_is_instarug'].mean()
    }
```

## Appendix B: Glossary of Terms

| Term | Definition |
|------|------------|
| PRNG | Pseudorandom Number Generator - an algorithm that produces a sequence of numbers with properties similar to random numbers |
| Server Seed | A secret value generated by the server before each game to ensure randomness |
| Server Seed Hash | A SHA-256 hash of the server seed, published before the game to commit to the outcome |
| Game ID | A unique identifier for each game session |
| Instarug | A game that ends very early (within the first 10 ticks) |
| Peak Multiplier | The highest price multiplier achieved during a game |
| ACTIVE Phase | The main gameplay phase where price fluctuates |
| RUGGED Phase | The end phase of a game, consisting of two distinct events |
| RUG_PROB | The per-tick probability that the game will instantly end |
| Meta-Algorithm | A hypothesized higher-level system that operates between games |
