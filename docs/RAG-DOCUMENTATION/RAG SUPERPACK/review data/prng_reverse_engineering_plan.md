# Comprehensive PRNG Reverse Engineering Framework for Rugs.fun

## 1. Analysis of System Architecture

Based on our analysis of the three Rugs.fun verification versions and ML_CORE_REFACTORED project findings, we've identified a multi-layered system:

**Surface Layer**
- Provably fair cryptographic system using SHA-256 hash verification
- Server seed + game ID deterministically generates outcomes
- Publicly verifiable algorithm with version differences (v1, v2, v3)

**Business Logic Layer** 
- Meta-algorithm for treasury protection
- Player classification & retention systems
- Cross-game pattern management (instarug detection)

**Technical Differences Between Versions**
- V1: Simple volatility calculation (`0.005 * Math.sqrt(price)`)
- V2: Capped volatility (`0.005 * Math.min(10, Math.sqrt(price))`)
- V3: God Candle feature (0.001% chance, 10x price move)

## 2. Statistical Testing Framework

### 2.1 Test Suite Selection

For thorough PRNG analysis, we'll implement a combination of established test suites:

| Test Suite | Strengths | Implementation |
|------------|-----------|----------------|
| **NIST STS** | Comprehensive statistical tests | Use for bitstream analysis of server seeds |
| **Dieharder** | Extensive battery, command-line friendly | Stream-based analysis of game outcomes |
| **TestU01** | Catches unique biases | Integration with custom generators |
| **Custom Tests** | Domain-specific pattern detection | Implement Python correlation analysis |

### 2.2 Data Collection Requirements

The minimum sample size requirements for conclusive testing:

- **Statistical Randomness**: 10,000+ game outcomes
- **Pattern Detection**: 8,192+ sequential games (power of 2 for FFT)
- **Meta-algorithm Detection**: 2,000+ games with complete metadata
- **Time-based Seeding**: 1,000+ games with precise timestamps

### 2.3 Core Test Implementation

```python
import numpy as np
from scipy.stats import chisquare, kstest, norm, pearsonr
from statsmodels.tsa.stattools import acf
from scipy.fft import fft
import pandas as pd
import math

class RugsAnalyzer:
    def __init__(self, data_path):
        """Initialize with path to dataset of game outcomes"""
        self.data = pd.read_json(data_path, lines=True)
        self.results = {}
        
    def preprocess_data(self):
        """Extract key metrics for analysis"""
        # Core game metrics
        self.peak_multipliers = self.data['peakMultiplier'].values
        self.final_ticks = self.data['finalTick'].values
        self.game_durations = self.data['gameDuration'].values
        self.server_seeds = self.data['serverSeed'].values
        
        # Create derived features
        self.is_instarug = self.final_ticks < 10
        self.timestamps = pd.to_datetime(self.data['timestamp'])
        
        # Create lag features for cross-game analysis
        self.data['prev_peak'] = self.data['peakMultiplier'].shift(1)
        self.data['prev_is_instarug'] = (self.data['finalTick'].shift(1) < 10)
        
    def chi_squared_test(self, metric, bins=100):
        """Test for uniform distribution of a metric"""
        values = getattr(self, metric)
        observed, _ = np.histogram(values, bins=bins)
        expected = len(values) / bins
        chi2_stat, p_value = chisquare(observed)
        return {'statistic': chi2_stat, 'p_value': p_value, 'passed': p_value > 0.05}
    
    def runs_test(self, metric, threshold=None):
        """Test for sequential dependencies"""
        values = getattr(self, metric)
        if threshold is None:
            threshold = np.median(values)
        
        binary_seq = (values >= threshold).astype(int)
        runs = 1
        n1 = np.sum(binary_seq)
        n2 = len(binary_seq) - n1
        
        for i in range(1, len(binary_seq)):
            if binary_seq[i] != binary_seq[i-1]:
                runs += 1
        
        expected_runs = (2 * n1 * n2) / (n1 + n2) + 1
        var_runs = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2)**2 * (n1 + n2 - 1))
        z_score = (runs - expected_runs) / math.sqrt(var_runs)
        p_value = 2 * (1 - norm.cdf(abs(z_score)))
        
        return {'z_score': z_score, 'p_value': p_value, 'passed': p_value > 0.05}
    
    def autocorrelation_analysis(self, metric, max_lag=100):
        """Detect periodic patterns in game outcomes"""
        values = getattr(self, metric)
        autocorr = acf(values, nlags=max_lag, fft=True)
        
        # Find significant lags
        n = len(values)
        confidence_interval = 1.96 / np.sqrt(n)  # 95% CI
        
        significant_lags = []
        for i, corr in enumerate(autocorr[1:], 1):
            if abs(corr) > confidence_interval:
                significant_lags.append((i, corr))
        
        return significant_lags
    
    def spectral_analysis(self, metric):
        """FFT analysis to detect hidden periodicities"""
        values = getattr(self, metric)
        # Pad to power of 2 for efficient FFT
        padded_length = 2 ** int(np.ceil(np.log2(len(values))))
        padded_values = np.pad(values, (0, padded_length - len(values)))
        
        # Compute FFT
        fft_result = fft(padded_values)
        power_spectrum = np.abs(fft_result) ** 2
        
        # Find peaks in power spectrum
        mean_power = np.mean(power_spectrum[1:])  # Exclude DC component
        std_power = np.std(power_spectrum[1:])
        threshold = mean_power + 3 * std_power
        
        peaks = []
        for i in range(1, len(power_spectrum) // 2):  # Only look at first half (Nyquist)
            if power_spectrum[i] > threshold:
                frequency = i / padded_length
                period = 1 / frequency if frequency > 0 else float('inf')
                peaks.append((i, period, power_spectrum[i]))
        
        return peaks
    
    def cross_game_correlation(self):
        """Analyze correlation between consecutive games"""
        # Test if high multipliers lead to instarugs
        high_mult_threshold = np.percentile(self.peak_multipliers, 90)  # Top 10%
        
        # Create a dataframe of high multiplier games and their next games
        high_mult_games = self.data[self.data['peakMultiplier'] > high_mult_threshold].copy()
        high_mult_games['next_is_instarug'] = high_mult_games['peakMultiplier'].shift(-1) < 1.1
        
        # Calculate conditional probability
        p_instarug_after_high = high_mult_games['next_is_instarug'].mean()
        p_instarug_overall = self.is_instarug.mean()
        
        # Statistical significance test
        from scipy.stats import fisher_exact
        
        # Contingency table
        # [after high mult & instarug, after high mult & not instarug]
        # [not after high mult & instarug, not after high mult & not instarug]
        
        after_high_count = len(high_mult_games)
        after_high_instarug = high_mult_games['next_is_instarug'].sum()
        after_high_not_instarug = after_high_count - after_high_instarug
        
        total_games = len(self.data)
        total_instarug = self.is_instarug.sum()
        not_after_high_instarug = total_instarug - after_high_instarug
        not_after_high_not_instarug = (total_games - after_high_count) - not_after_high_instarug
        
        table = [[after_high_instarug, after_high_not_instarug],
                 [not_after_high_instarug, not_after_high_not_instarug]]
        
        odds_ratio, p_value = fisher_exact(table)
        
        return {
            'p_instarug_after_high': p_instarug_after_high,
            'p_instarug_overall': p_instarug_overall,
            'odds_ratio': odds_ratio,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    def time_correlation_analysis(self):
        """Test for time-based patterns in seed generation"""
        # Extract time components
        hour_of_day = self.timestamps.dt.hour
        day_of_week = self.timestamps.dt.dayofweek
        minute_of_hour = self.timestamps.dt.minute
        second_of_minute = self.timestamps.dt.second
        
        # Convert timestamps to seconds since epoch
        time_values = self.timestamps.astype(int) // 10**9
        
        # Check various time correlations with game outcomes
        correlations = {}
        
        # Direct correlation
        correlations['time_vs_peak'] = pearsonr(time_values, self.peak_multipliers)
        correlations['time_vs_duration'] = pearsonr(time_values, self.game_durations)
        
        # Modulo correlations (cyclical patterns)
        correlations['minute_vs_peak'] = pearsonr(minute_of_hour, self.peak_multipliers)
        correlations['second_vs_peak'] = pearsonr(second_of_minute, self.peak_multipliers)
        correlations['hour_vs_peak'] = pearsonr(hour_of_day, self.peak_multipliers)
        correlations['day_vs_peak'] = pearsonr(day_of_week, self.peak_multipliers)
        
        # Time modulo correlations
        mod_1000 = time_values % 1000
        mod_60 = time_values % 60
        mod_3600 = time_values % 3600
        mod_86400 = time_values % 86400  # Daily pattern
        
        correlations['mod_1000_vs_peak'] = pearsonr(mod_1000, self.peak_multipliers)
        correlations['mod_60_vs_peak'] = pearsonr(mod_60, self.peak_multipliers)
        correlations['mod_3600_vs_peak'] = pearsonr(mod_3600, self.peak_multipliers)
        correlations['mod_86400_vs_peak'] = pearsonr(mod_86400, self.peak_multipliers)
        
        # Filter for significant correlations
        significant_correlations = {k: v for k, v in correlations.items() if v[1] < 0.05}
        
        return significant_correlations
    
    def analyze_player_profiling(self, player_data):
        """Analyze if outcomes are influenced by player behavior"""
        # Requires player-specific data like bet size, history, etc.
        # For now, stub implementation
        pass
    
    def run_full_analysis(self):
        """Run all tests and compile results"""
        self.preprocess_data()
        
        # Basic statistical tests
        self.results['chi_squared_peak'] = self.chi_squared_test('peak_multipliers')
        self.results['chi_squared_duration'] = self.chi_squared_test('game_durations')
        self.results['runs_test_peak'] = self.runs_test('peak_multipliers')
        
        # Advanced pattern detection
        self.results['autocorr_peak'] = self.autocorrelation_analysis('peak_multipliers')
        self.results['spectral_peak'] = self.spectral_analysis('peak_multipliers')
        
        # Cross-game pattern detection
        self.results['cross_game'] = self.cross_game_correlation()
        
        # Time-based pattern detection
        self.results['time_correlation'] = self.time_correlation_analysis()
        
        return self.results
```

## 3. Real-Time Monitoring Framework

### 3.1 Data Collection System

```python
import asyncio
import websockets
import json
from datetime import datetime
import pandas as pd
import os

class RugsMonitor:
    def __init__(self, websocket_url, output_path='rugs_data.jsonl'):
        """Initialize with Rugs.fun WebSocket URL"""
        self.websocket_url = websocket_url
        self.output_path = output_path
        self.games = []
        self.current_game = None
        self.connection_active = False
    
    async def connect(self):
        """Establish WebSocket connection to Rugs.fun"""
        try:
            self.connection = await websockets.connect(self.websocket_url)
            self.connection_active = True
            print("Connected to Rugs.fun WebSocket")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    async def listen(self):
        """Listen for game events"""
        if not self.connection_active:
            success = await self.connect()
            if not success:
                return
        
        try:
            while True:
                message = await self.connection.recv()
                data = json.loads(message)
                
                # Process different event types
                if 'type' in data:
                    if data['type'] == 'gameStateUpdate':
                        await self.handle_game_state_update(data)
                    elif data['type'] == 'gameHistory':
                        await self.handle_game_history(data)
                    elif data['type'] == 'newTrade':
                        await self.handle_new_trade(data)
        
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed, attempting to reconnect...")
            self.connection_active = False
            await asyncio.sleep(5)
            await self.listen()
        
        except Exception as e:
            print(f"Error in WebSocket listener: {e}")
            self.connection_active = False
    
    async def handle_game_state_update(self, data):
        """Process game state updates"""
        state = data.get('state', {})
        
        # New game started
        if state.get('status') == 'playing' and not self.current_game:
            self.current_game = {
                'gameId': state.get('gameId'),
                'serverSeedHash': state.get('serverSeedHash'),
                'timestamp': datetime.now().isoformat(),
                'startTime': datetime.now(),
                'ticks': [],
                'trades': [],
                'rugpool': state.get('rugpool', {})
            }
            print(f"New game started: {self.current_game['gameId']}")
        
        # Game tick update
        if self.current_game and state.get('status') == 'playing':
            tick = {
                'tick': state.get('tick'),
                'price': state.get('price'),
                'timestamp': datetime.now().isoformat()
            }
            self.current_game['ticks'].append(tick)
        
        # Game ended
        if self.current_game and state.get('status') == 'rugged':
            self.current_game['endTime'] = datetime.now()
            self.current_game['finalTick'] = state.get('tick')
            self.current_game['peakMultiplier'] = state.get('peakMultiplier')
            self.current_game['gameDuration'] = (self.current_game['endTime'] - self.current_game['startTime']).total_seconds()
            self.current_game['serverSeed'] = state.get('serverSeed')
            
            # Store the completed game
            self.games.append(self.current_game)
            
            # Save to file
            with open(self.output_path, 'a') as f:
                f.write(json.dumps(self.current_game) + '\n')
            
            print(f"Game ended: {self.current_game['gameId']}, Peak: {self.current_game['peakMultiplier']}")
            
            # Reset current game
            self.current_game = None
            
            # Run analysis every 100 games
            if len(self.games) % 100 == 0:
                await self.run_analysis()
    
    async def handle_game_history(self, data):
        """Process game history updates"""
        history = data.get('history', [])
        
        # Process historical games if needed
        pass
    
    async def handle_new_trade(self, data):
        """Process new trade events"""
        if self.current_game:
            trade = {
                'tradeId': data.get('tradeId'),
                'player': data.get('player'),
                'amount': data.get('amount'),
                'entryPrice': data.get('entryPrice'),
                'timestamp': datetime.now().isoformat()
            }
            self.current_game['trades'].append(trade)
    
    async def run_analysis(self):
        """Run analysis on collected games"""
        if len(self.games) < 100:
            print("Not enough games for analysis")
            return
        
        # Create temporary file with latest data
        temp_file = 'temp_analysis_data.jsonl'
        with open(temp_file, 'w') as f:
            for game in self.games:
                f.write(json.dumps(game) + '\n')
        
        # Initialize analyzer
        analyzer = RugsAnalyzer(temp_file)
        results = analyzer.run_full_analysis()
        
        # Check for significant patterns
        if results['cross_game']['significant']:
            print("ALERT: Significant cross-game pattern detected!")
            print(f"Instarug probability after high multiplier: {results['cross_game']['p_instarug_after_high']:.2f}")
            print(f"Overall instarug probability: {results['cross_game']['p_instarug_overall']:.2f}")
            print(f"Odds ratio: {results['cross_game']['odds_ratio']:.2f}, p-value: {results['cross_game']['p_value']:.4f}")
        
        # Check for time correlations
        if results['time_correlation']:
            print("ALERT: Time-based patterns detected!")
            for key, (corr, p_val) in results['time_correlation'].items():
                print(f"{key}: correlation={corr:.4f}, p-value={p_val:.4f}")
        
        # Save full analysis results
        with open('analysis_results.json', 'w') as f:
            # Convert numpy values to Python native types for JSON serialization
            import numpy as np
            def convert_to_serializable(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, tuple) and len(obj) == 2 and isinstance(obj[0], np.floating):
                    return (float(obj[0]), float(obj[1]))
                return obj
            
            serializable_results = json.loads(
                json.dumps(results, default=convert_to_serializable)
            )
            json.dump(serializable_results, f, indent=2)
        
        # Clean up
        os.remove(temp_file)

    async def start_monitoring(self):
        """Start the monitoring process"""
        await self.listen()
```

### 3.2 Integration with ML Framework

To integrate with the existing ML_CORE_REFACTORED project:

```python
import torch
from rugs_transformer import RugsTransformer, RugsFeatureExtractor

class PredictiveMonitor(RugsMonitor):
    def __init__(self, websocket_url, model_path, output_path='rugs_data.jsonl'):
        """Initialize with Rugs.fun WebSocket URL and ML model path"""
        super().__init__(websocket_url, output_path)
        self.model = self.load_model(model_path)
        self.feature_extractor = RugsFeatureExtractor()
        self.predictions = []
    
    def load_model(self, model_path):
        """Load the pre-trained transformer model"""
        model = RugsTransformer(
            input_dim=12,  # 12 features as mentioned in ML_CORE_REFACTORED
            d_model=128,
            nhead=8,
            num_encoder_layers=6
        )
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model
    
    async def predict_outcome(self):
        """Generate prediction for current game"""
        if not self.current_game or len(self.current_game['ticks']) < 10:
            return None
        
        # Extract features from current game
        features = self.feature_extractor.extract_features(self.current_game)
        
        # Convert to tensor
        features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        
        # Generate prediction
        with torch.no_grad():
            prediction = self.model(features_tensor).item()
        
        return prediction
    
    async def handle_game_state_update(self, data):
        """Override to include prediction"""
        await super().handle_game_state_update(data)
        
        # Generate prediction every 10 ticks
        if self.current_game and len(self.current_game['ticks']) % 10 == 0:
            prediction = await self.predict_outcome()
            if prediction:
                print(f"Prediction for game {self.current_game['gameId']}: Peak multiplier = {prediction:.2f}x")
                
                # Store prediction
                self.predictions.append({
                    'gameId': self.current_game['gameId'],
                    'tick': self.current_game['ticks'][-1]['tick'],
                    'current_price': self.current_game['ticks'][-1]['price'],
                    'predicted_peak': prediction,
                    'timestamp': datetime.now().isoformat()
                })
```

## 4. Advanced PRNG Analysis Techniques

### 4.1 Seed Generation Investigation

```python
import hashlib
import datetime
import itertools

class SeedAnalyzer:
    def __init__(self, seed_data):
        """Initialize with list of server seeds and timestamps"""
        self.seeds = seed_data['serverSeed']
        self.timestamps = seed_data['timestamp']
        
    def analyze_seed_entropy(self):
        """Analyze entropy distribution in server seeds"""
        entropy_scores = []
        
        for seed in self.seeds:
            # Convert to binary
            binary = bin(int(seed, 16))[2:].zfill(len(seed) * 4)
            
            # Count 1s and 0s
            ones = binary.count('1')
            zeros = binary.count('0')
            
            # Calculate entropy
            total_bits = ones + zeros
            p_one = ones / total_bits
            p_zero = zeros / total_bits
            
            import math
            entropy = 0
            if p_one > 0:
                entropy -= p_one * math.log2(p_one)
            if p_zero > 0:
                entropy -= p_zero * math.log2(p_zero)
            
            entropy_scores.append(entropy)
        
        return {
            'mean_entropy': sum(entropy_scores) / len(entropy_scores),
            'min_entropy': min(entropy_scores),
            'max_entropy': max(entropy_scores)
        }
    
    def test_time_based_generation(self):
        """Test if seeds are generated based on timestamp"""
        # Convert timestamps to various formats
        formats = []
        
        for ts in self.timestamps:
            dt = datetime.datetime.fromisoformat(ts)
            formats.append({
                'unix': int(dt.timestamp()),
                'unix_ms': int(dt.timestamp() * 1000),
                'date_str': dt.strftime('%Y%m%d'),
                'time_str': dt.strftime('%H%M%S'),
                'datetime_str': dt.strftime('%Y%m%d%H%M%S')
            })
        
        # Test if any of these formats match seed patterns
        matches = []
        
        for i, (seed, fmt) in enumerate(zip(self.seeds, formats)):
            for key, value in fmt.items():
                # Generate various hash possibilities
                hashes = {
                    f'md5_{key}': hashlib.md5(str(value).encode()).hexdigest(),
                    f'sha1_{key}': hashlib.sha1(str(value).encode()).hexdigest(),
                    f'sha256_{key}': hashlib.sha256(str(value).encode()).hexdigest()
                }
                
                # Check for matches or partial matches
                for hash_key, hash_value in hashes.items():
                    if seed == hash_value:
                        matches.append({
                            'index': i,
                            'method': hash_key,
                            'time_value': value,
                            'full_match': True
                        })
                    elif seed.startswith(hash_value[:16]):
                        matches.append({
                            'index': i,
                            'method': hash_key,
                            'time_value': value,
                            'match_length': 16,
                            'full_match': False
                        })
        
        return matches
    
    def brute_force_seed_algorithm(self, sample_size=5):
        """Attempt to brute force the seed generation algorithm"""
        # This is a simplified version for demonstration
        # In practice, would test many more combinations
        
        # Take a sample of seeds to test
        sample_seeds = self.seeds[:sample_size]
        sample_times = self.timestamps[:sample_size]
        
        common_secrets = ["rugs.fun", "rugsfun", "rugpull", "rug", "game", "crypto"]
        
        results = []
        
        for seed, ts in zip(sample_seeds, sample_times):
            dt = datetime.datetime.fromisoformat(ts)
            
            # Generate various time formats
            time_formats = [
                str(int(dt.timestamp())),
                str(int(dt.timestamp() * 1000)),
                dt.strftime('%Y%m%d'),
                dt.strftime('%H%M%S'),
                dt.strftime('%Y%m%d%H%M%S')
            ]
            
            # Try combinations with common secrets
            for time_fmt, secret in itertools.product(time_formats, common_secrets):
                test_inputs = [
                    time_fmt + secret,
                    secret + time_fmt,
                    time_fmt,
                    secret
                ]
                
                for test_input in test_inputs:
                    hash_md5 = hashlib.md5(test_input.encode()).hexdigest()
                    hash_sha1 = hashlib.sha1(test_input.encode()).hexdigest()
                    hash_sha256 = hashlib.sha256(test_input.encode()).hexdigest()
                    
                    if seed == hash_md5 or seed == hash_sha1 or seed == hash_sha256:
                        results.append({
                            'seed': seed,
                            'input': test_input,
                            'hash_type': 'md5' if seed == hash_md5 else ('sha1' if seed == hash_sha1 else 'sha256'),
                            'match': 'full'
                        })
                    elif seed.startswith(hash_md5[:16]) or seed.startswith(hash_sha1[:16]) or seed.startswith(hash_sha256[:16]):
                        results.append({
                            'seed': seed,
                            'input': test_input,
                            'hash_type': 'md5' if seed.startswith(hash_md5[:16]) else 
                                        ('sha1' if seed.startswith(hash_sha1[:16]) else 'sha256'),
                            'match': 'partial'
                        })
        
        return results
```

### 4.2 ML-Based Pattern Detection

```python
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class PatternDetector:
    def __init__(self):
        """Initialize pattern detector"""
        self.model = None
        self.scaler = StandardScaler()
    
    def prepare_data(self, data, sequence_length=50):
        """Prepare data for LSTM model"""
        # Extract target variable
        y = data['peakMultiplier'].values
        
        # Create sequences
        X = []
        y_seq = []
        
        for i in range(len(data) - sequence_length):
            # Extract features for sequence
            seq_features = []
            
            for j in range(sequence_length):
                idx = i + j
                features = [
                    data['peakMultiplier'].iloc[idx],
                    data['finalTick'].iloc[idx],
                    data['gameDuration'].iloc[idx],
                    # Add more features as needed
                ]
                seq_features.append(features)
            
            X.append(seq_features)
            y_seq.append(y[i + sequence_length])
        
        X = np.array(X)
        y_seq = np.array(y_seq)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y_seq, test_size=0.2, random_state=42)
        
        # Reshape for LSTM [samples, time steps, features]
        n_samples, n_timesteps, n_features = X_train.shape
        
        # Scale data
        X_train_reshaped = X_train.reshape(n_samples * n_timesteps, n_features)
        X_train_scaled = self.scaler.fit_transform(X_train_reshaped)
        X_train = X_train_scaled.reshape(n_samples, n_timesteps, n_features)
        
        X_test_reshaped = X_test.reshape(X_test.shape[0] * n_timesteps, n_features)
        X_test_scaled = self.scaler.transform(X_test_reshaped)
        X_test = X_test_scaled.reshape(X_test.shape[0], n_timesteps, n_features)
        
        return X_train, X_test, y_train, y_test
    
    def build_model(self, input_shape):
        """Build LSTM model for sequence prediction"""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(50, return_sequences=True, input_shape=input_shape),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(50, return_sequences=False),
            tf.keras.layers.Dense(25),
            tf.keras.layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model
    
    def train(self, X_train, y_train, epochs=50, batch_size=32):
        """Train the model"""
        if not self.model:
            self.model = self.build_model((X_train.shape[1], X_train.shape[2]))
        
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.1,
            verbose=1
        )
        
        return history
    
    def evaluate(self, X_test, y_test):
        """Evaluate the model"""
        return self.model.evaluate(X_test, y_test)
    
    def predict(self, sequence):
        """Predict next outcome based on sequence"""
        # Scale sequence
        sequence_reshaped = sequence.reshape(sequence.shape[0] * sequence.shape[1], sequence.shape[2])
        sequence_scaled = self.scaler.transform(sequence_reshaped)
        sequence = sequence_scaled.reshape(1, sequence.shape[1], sequence.shape[2])
        
        return self.model.predict(sequence)[0][0]
    
    def analyze_error_patterns(self, X_test, y_test):
        """Analyze patterns in prediction errors"""
        predictions = self.model.predict(X_test)
        errors = y_test - predictions.flatten()
        
        # Check for patterns in errors
        from scipy.stats import normaltest
        
        # Test if errors are normally distributed
        k2, p = normaltest(errors)
        
        # Look for autocorrelation in errors
        from statsmodels.tsa.stattools import acf
        error_autocorr = acf(errors, nlags=20)
        
        return {
            'mean_error': np.mean(errors),
            'std_error': np.std(errors),
            'normal_test': {'statistic': k2, 'p_value': p},
            'autocorrelation': error_autocorr.tolist()
        }
```

## 5. Implementation Plan

### 5.1 Phase 1: Data Collection (1-2 weeks)
- Set up WebSocket connection to Rugs.fun
- Implement continuous monitoring system
- Collect at least 10,000 game outcomes with full metadata
- Store data in structured format (JSONL)

### 5.2 Phase 2: Basic Statistical Analysis (1 week)
- Implement core statistical tests
- Run NIST STS, Dieharder, and TestU01 on seed data
- Analyze distribution of game outcomes
- Validate basic randomness properties

### 5.3 Phase 3: Meta-Algorithm Investigation (2 weeks)
- Implement cross-game correlation analysis
- Test instarug hypothesis rigorously
- Analyze time-based patterns in seed generation
- Investigate player profiling effects

### 5.4 Phase 4: Predictive Modeling (2-3 weeks)
- Integrate with ML_CORE_REFACTORED
- Train pattern detection models
- Implement real-time prediction system
- Evaluate prediction accuracy

### 5.5 Phase 5: Strategy Development (1-2 weeks)
- Develop trading strategies based on findings
- Implement risk management rules
- Back-test strategies on historical data
- Optimize parameters for profitability

## 6. Key Metrics to Monitor

| Metric | Description | Threshold | Action |
|--------|-------------|-----------|--------|
| **Instarug Probability** | Probability of game ending in first 10 ticks | >5% (10x normal) | Potential meta-algorithm identified |
| **Cross-Game Correlation** | Correlation between consecutive game outcomes | p < 0.05 | Evidence of treasury protection |
| **Time-Seed Correlation** | Correlation between time and seed generation | Any significant pattern | Potential seed prediction vulnerability |
| **Version Differences** | Performance metrics between v1, v2, v3 | >10% difference | Version-specific strategy opportunity |
| **Player Classification** | Evidence of different RNG behavior by player | Any significant pattern | Player profiling confirmed |

## 7. Execution Environment Setup

Required libraries:
- numpy, scipy, pandas, statsmodels
- tensorflow, pytorch (for ML components)
- websockets, aiohttp (for real-time monitoring)
- TestU01, Dieharder (for comprehensive PRNG testing)

Environment setup:
```bash
# Python environment
conda create -n rugs_analysis python=3.9
conda activate rugs_analysis

# Core data science packages
pip install numpy scipy pandas statsmodels matplotlib seaborn

# Machine learning
pip install tensorflow torch torchvision

# Real-time connectivity
pip install websockets aiohttp

# Statistical testing
# TestU01 and Dieharder require system installation
# For Ubuntu:
sudo apt-get install dieharder
# TestU01 requires manual compilation
```

## 8. Conclusion

This comprehensive framework provides a structured approach to reverse engineering the Rugs.fun PRNG system. By combining statistical analysis, real-time monitoring, and machine learning, we can identify both the visible algorithmic components and hidden meta-algorithms that influence game outcomes. The findings from this analysis can be used to develop more accurate predictive models and potentially profitable trading strategies.
