# RugPredictor HUD: Test-Driven Development Gameplan
## Building an AI-Powered Rug Prediction System

### Table of Contents
1. [Project Overview](#project-overview)
2. [Salvageable Components](#salvageable-components)
3. [Core Requirements](#core-requirements)
4. [Test-Driven Development Plan](#test-driven-development-plan)
5. [Architecture Design](#architecture-design)
6. [Implementation Roadmap](#implementation-roadmap)
7. [Testing Strategy](#testing-strategy)

---

## 1. Project Overview

### Vision
Build a lightweight, browser-based HUD (Heads-Up Display) that uses Q-Learning to predict when Rugs.fun games will "rug" with increasing accuracy over time.

### Core Features
- Real-time rug probability display (0-100%)
- Confidence indicators based on pattern recognition
- Visual/audio alerts for high-probability scenarios
- Self-improving Q-Learning agent
- No backend required - runs entirely in browser

### Key Insights from Research
Based on our SideBetSysArc analysis:
- **Timing Variance**: Mean tick = 271.5ms (not 250ms), high variability (CV=1.09)
- **Probability Curves**: Well-defined progression from 15% (early) to 96% (late game)
- **40-Tick Window**: Side bets cover exactly 40 ticks (not time-based)
- **Volatility Patterns**: 78% increase in final 5 ticks before rug

---

## 2. Salvageable Components

### From Current RugsDash

#### ✅ Direct Reuse (Minimal Changes)
1. **WebSocketClient** (`client/src/lib/websocketClient.ts`)
   - Already connects to backend.rugs.fun
   - Handles reconnection logic
   - Just remove authentication layer

2. **Type Definitions** (`client/src/types/gameState.ts`)
   - GameStateData interface
   - PredictionData structures
   - ConnectionStatus types

3. **Timing Constants** (`client/src/lib/predictionEngine.ts`)
   - Empirical baseline values
   - Tick interval calculations

#### 🔧 Adapt and Simplify
1. **PredictionEngine Core**
   - Extract volatility calculation logic
   - Simplify to focus on rug prediction only
   - Remove complex features

2. **Q-Learning State Encoding** (`server/qlearning/QLearningAgent.ts`)
   - Convert to browser-compatible code
   - Use localStorage instead of database
   - Simplify action space to confidence levels

---

## 3. Core Requirements

### Functional Requirements

#### FR1: Real-Time Data Processing
- Connect to backend.rugs.fun WebSocket
- Process gameStateUpdate events
- Track tick progression and price movements
- Calculate rolling volatility

#### FR2: Rug Probability Calculation
- Base probability from tick count
- Timing adjustment for variance
- Volatility spike detection
- Pattern recognition (treasury, momentum)

#### FR3: Q-Learning Agent
- State: [tickCount, priceLevel, volatility, patternSignals]
- Action: Confidence level (0-100%)
- Reward: Accuracy of prediction
- Learning: Update Q-values based on outcomes

#### FR4: User Interface
- Probability display (0-100%)
- Confidence indicator
- Visual alerts for high probability
- Learning progress tracker
- Pattern indicators

### Non-Functional Requirements

#### NFR1: Performance
- <50ms calculation latency
- Smooth UI updates (60fps)
- Minimal memory footprint

#### NFR2: Reliability
- Handle WebSocket disconnections
- Persist learning state
- Graceful degradation

#### NFR3: Usability
- One-click activation
- No configuration required
- Clear visual indicators

---

## 4. Test-Driven Development Plan

### Phase 1: Core Data Layer Tests

#### Test Suite 1: WebSocket Connection
```typescript
describe('WebSocketConnection', () => {
  it('should connect to backend.rugs.fun', async () => {
    // Test connection establishment
  });
  
  it('should handle reconnection on disconnect', async () => {
    // Test reconnection logic
  });
  
  it('should parse gameStateUpdate events', () => {
    // Test event parsing
  });
});
```

#### Test Suite 2: Game State Tracking
```typescript
describe('GameStateTracker', () => {
  it('should track tick progression', () => {
    // Test tick counting
  });
  
  it('should detect game phase transitions', () => {
    // Test phase detection (early/mid/late)
  });
  
  it('should calculate tick intervals', () => {
    // Test timing calculations
  });
});
```

### Phase 2: Probability Engine Tests

#### Test Suite 3: Base Probability
```typescript
describe('BaseProbability', () => {
  it('should return correct probability for tick ranges', () => {
    // Test probability curve
    expect(getBaseProbability(0)).toBe(0.15);
    expect(getBaseProbability(100)).toBe(0.50);
    expect(getBaseProbability(300)).toBe(0.88);
  });
  
  it('should interpolate between defined points', () => {
    // Test interpolation
  });
});
```

#### Test Suite 4: Volatility Detection
```typescript
describe('VolatilityDetection', () => {
  it('should calculate rolling volatility', () => {
    // Test volatility calculation
  });
  
  it('should detect 78% spike pattern', () => {
    // Test spike detection
  });
});
```

### Phase 3: Q-Learning Tests

#### Test Suite 5: State Encoding
```typescript
describe('StateEncoding', () => {
  it('should discretize continuous values', () => {
    // Test state discretization
  });
  
  it('should include pattern signals', () => {
    // Test pattern integration
  });
});
```

#### Test Suite 6: Q-Value Updates
```typescript
describe('QLearning', () => {
  it('should initialize Q-table', () => {
    // Test initialization
  });
  
  it('should update Q-values on correct prediction', () => {
    // Test positive reward
  });
  
  it('should update Q-values on incorrect prediction', () => {
    // Test negative reward
  });
  
  it('should persist learning state', () => {
    // Test localStorage persistence
  });
});
```

### Phase 4: UI Component Tests

#### Test Suite 7: HUD Display
```typescript
describe('HUDDisplay', () => {
  it('should render probability meter', () => {
    // Test UI rendering
  });
  
  it('should update smoothly', () => {
    // Test animation
  });
  
  it('should trigger alerts at thresholds', () => {
    // Test alert system
  });
});
```

---

## 5. Architecture Design

### Simplified Architecture
```typescript
// Core components
class RugPredictorHUD {
  private wsClient: SimplifiedWebSocketClient;
  private stateTracker: GameStateTracker;
  private probabilityEngine: ProbabilityEngine;
  private qLearning: QLearningAgent;
  private ui: HUDRenderer;
  
  constructor() {
    this.initialize();
  }
  
  private async initialize() {
    // 1. Connect WebSocket
    // 2. Load saved Q-values
    // 3. Start UI rendering
    // 4. Begin prediction loop
  }
}

// State management
interface GameState {
  tickCount: number;
  price: number;
  volatility: number;
  phase: 'EARLY' | 'MID' | 'LATE';
  patternSignals: PatternSignal[];
}

// Q-Learning simplified
interface QState {
  tickBucket: number;    // 0-10 (discretized)
  priceBucket: number;   // 0-5 (discretized)
  volatilityBucket: number; // 0-3 (low/med/high)
  hasPatterns: boolean;
}
```

### Data Flow
```
WebSocket → State Tracker → Probability Engine → Q-Learning → UI
     ↑                                                           ↓
     └─────────────── Feedback Loop (outcomes) ─────────────────┘
```

---

## 6. Implementation Roadmap

### Week 1: Foundation (Tests First)
**Day 1-2: Project Setup**
- [ ] Initialize TypeScript project
- [ ] Set up Vitest for testing
- [ ] Create test structure
- [ ] Write WebSocket connection tests

**Day 3-4: Core Data Layer**
- [ ] Implement WebSocket client (TDD)
- [ ] Implement game state tracker (TDD)
- [ ] Write and pass all data layer tests

**Day 5-7: Probability Engine**
- [ ] Write probability calculation tests
- [ ] Implement base probability curve
- [ ] Implement timing adjustments
- [ ] Add volatility calculations

### Week 2: Q-Learning Integration
**Day 8-9: Q-Learning Core**
- [ ] Write Q-learning tests
- [ ] Implement state discretization
- [ ] Implement Q-table with localStorage
- [ ] Add learning algorithms

**Day 10-11: Pattern Recognition**
- [ ] Write pattern detection tests
- [ ] Implement volatility spike detection
- [ ] Add treasury pattern signals
- [ ] Integrate with Q-learning

**Day 12-14: Prediction Integration**
- [ ] Write integration tests
- [ ] Connect all components
- [ ] Test end-to-end flow
- [ ] Optimize performance

### Week 3: User Interface
**Day 15-16: HUD Components**
- [ ] Write UI component tests
- [ ] Create probability meter
- [ ] Add confidence indicators
- [ ] Implement alert system

**Day 17-18: Visual Polish**
- [ ] Add animations
- [ ] Create color gradients
- [ ] Add sound alerts
- [ ] Optimize rendering

**Day 19-21: Integration & Testing**
- [ ] Full system integration
- [ ] Performance optimization
- [ ] Edge case handling
- [ ] User testing

### Week 4: Refinement
**Day 22-23: Q-Learning Tuning**
- [ ] Analyze learning curves
- [ ] Tune hyperparameters
- [ ] Add advanced patterns
- [ ] Improve accuracy

**Day 24-25: Production Ready**
- [ ] Build distribution package
- [ ] Create user documentation
- [ ] Set up deployment
- [ ] Launch beta version

**Day 26-28: Monitoring & Iteration**
- [ ] Collect user feedback
- [ ] Monitor prediction accuracy
- [ ] Fix bugs
- [ ] Plan v2 features

---

## 7. Testing Strategy

### Test Coverage Goals
- **Unit Tests**: 90% coverage
- **Integration Tests**: Critical paths
- **E2E Tests**: Happy path scenarios

### Test Data Strategy
```typescript
// Mock game data generator
class MockGameDataGenerator {
  generateGameSequence(options: {
    duration: number;
    rugAtTick: number;
    volatilityProfile: 'normal' | 'high' | 'spike';
  }): GameStateData[] {
    // Generate realistic game data
  }
  
  generateHistoricalGames(count: number): GameHistory[] {
    // Generate training data
  }
}
```

### Performance Benchmarks
- Calculation latency: <50ms (p95)
- Memory usage: <50MB
- Q-table size: <1MB
- UI updates: 60fps

### Continuous Testing
```json
// package.json scripts
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage",
    "test:perf": "vitest bench",
    "test:e2e": "playwright test"
  }
}
```

---

## Key Success Metrics

### Technical Metrics
- **Prediction Accuracy**: >25% for side bet window (vs 20% breakeven)
- **Learning Convergence**: Improvement visible within 50 games
- **Latency**: <50ms calculation time
- **Reliability**: 99.9% uptime

### User Metrics
- **Adoption**: 100+ users in first month
- **Retention**: 50% weekly active users
- **Feedback**: 4+ star average rating

### Business Metrics
- **Development Time**: 4 weeks to MVP
- **Maintenance**: <5 hours/week
- **Cost**: $0 infrastructure (client-side only)

---

## Conclusion

This TDD gameplan provides a structured approach to building a focused, high-performance rug prediction HUD. By starting with tests and building incrementally, we ensure:

1. **Quality**: Every feature is tested before implementation
2. **Focus**: Only essential features are built
3. **Speed**: 4-week timeline to working product
4. **Reliability**: Comprehensive test coverage
5. **Learning**: Q-Learning improves with every game

The key is maintaining discipline - write tests first, implement only what's needed to pass, and resist feature creep. The result will be a clean, fast, effective tool that solves the core problem: predicting rugs with increasing accuracy.

---

*Next Steps: Begin with Week 1, Day 1 - Set up the project and write the first WebSocket connection tests.*