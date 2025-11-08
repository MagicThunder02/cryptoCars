# CryptoCars - Blockchain Racing Game with Functional Encryption

A secure and decentralized racing game built on cryptographic primitives, demonstrating multi-party functional encryption and homomorphic operations for privacy-preserving gameplay.

## Overview

CryptoCars is a blockchain-based game where players create, train, and race virtual cars using advanced cryptographic techniques. The system ensures that car data remains encrypted throughout the entire lifecycle while still allowing computation and verification of race results. No single entity can manipulate or reveal private car attributes without collusion.

## Cryptographic Foundation

### Multi-Party Functional Encryption

The game implements a distributed functional encryption scheme based on **inner product encryption**. The system evaluates the function:

```
Speed = g^(<x, z>)
```

where:
- `x` is the encrypted car vector (10 features)
- `z = k * y` is a hidden evaluation vector
- `g` is a generator of a cyclic group G of prime order p

### Three-Server Architecture

The security model relies on three non-colluding servers:

1. **Principal Server** - Holds master secret `S` and partial secret `k`
   - Coordinates user interactions
   - Manages car creation and training
   - Computes final speed values

2. **Generator Server** - Creates random car instances
   - Generates initial car attributes (flags)
   - Produces encrypted car vectors `d = g^x`

3. **Speed Server** - Holds partial secret `y`
   - Evaluates speed function with weather-dependent weights
   - Computes intermediate encrypted values

## How It Works

### Car Creation

1. User requests a new car from the Principal Server
2. Generator Server creates 10 random flags (values 0-1000)
3. Encrypted car vector is computed: `d_i = g^(x_i)`
4. Principal Server encrypts with master key:
   ```
   Ct = g^r
   Ctx_i = d_i * h^r  (where h = g^S)
   ```
5. Encrypted car `(Ct, Ctx)` is assigned to user

### Speed Evaluation (Cryptographic Protocol)

1. **Principal Server** computes `S*k` (element-wise product of secrets)
2. **Speed Server** receives `S*k` and `Ctx`, computes:
   ```
   Sk_y = <S*k, y>
   e_i = (Ctx_i)^(y_i)
   ```
3. **Principal Server** receives `e` and computes:
   ```
   p_i = (e_i)^(k_i)
   Speed = (∏ p_i) / Ct^(Sk_y) mod p
   ```
4. Result: `g^(<x, z>)` - encrypted speed evaluation

### Homomorphic Training

Cars can be improved without decryption:
```
Ctx_i' = Ctx_i * g^(delta)
```
where `delta ∈ [-20, 20]` is the training adjustment. This modifies the underlying secret value while maintaining encryption.

### Weather System

The Speed Server maintains different weight vectors for terrain conditions:
- **Sunny** - Standard weights
- **Rainy** - Different performance profile  
- **Snowy** - Alternative weight distribution

Changing terrain modifies the `y` vector, affecting car performance dynamically.

## Security Guarantees

### Discrete Logarithm Assumption
- Recovering `x` from `Ctx` is computationally infeasible
- Intermediate values `e_i` and `p_i` do not leak secrets `k` or `y`
- No single server can reconstruct the complete evaluation vector `z`

### Non-Collusion Requirement
As long as the three servers don't collude, the system maintains:
- **Privacy**: Car attributes remain secret
- **Integrity**: Race results cannot be forged
- **Verifiability**: Results can be publicly verified

### Extensibility
The system supports multiple Speed Servers with secrets `y_1, y_2, ..., y_n`, where `z = k * y_1 * y_2 * ... * y_n`, further reducing collusion risk.

## Game Mechanics

### Race Cycle
- **Frequency**: Every 10 minutes (blockchain-based timing)
- **Entry Cost**: 1 XPF token per race registration
- **Winner Reward**: 100 XPF tokens (via smart contract)

### User Actions
- **Join Network**: Receive initial car automatically
- **Train Car**: Pay 1 XPF to improve car attributes
- **Enter Race**: Pay 1 XPF to compete
- **Change Terrain**: Affects all cars' performance

### Game Rules
- Each user can create **one car per race**
- Training costs 1 XPF and adjusts selected attributes
- Race participation costs 1 XPF
- Highest speed wins and receives 100 XPF
- Car creation limit resets after each race

## Quick Start

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)

### Installation

```bash
# Clone the repository
git clone https://github.com/MagicThunder02/cryptoCars.git
cd cryptoCars

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Playing the Demo

1. **Select a User** (Alice, Bob, or Charlie)
2. **View Car Details** - See encrypted flags and calculated speed
3. **Train Your Car** - Select attributes to improve (costs 1 XPF)
4. **Create New Car** - One per race cycle allowed
5. **Change Terrain** - Test performance in different conditions
6. **Register for Race** - Enter your car (costs 1 XPF)
7. **Run Race** - Compete! Winner gets 100 XPF
8. **Prove Speed** - Verify encryption correctness

## Project Structure

```
cryptoCars/
├── main.py                  # GUI application entry point
├── principal_server.py      # Main coordinator (holds S and k)
├── generator_server.py      # Car creation (Oracle)
├── speed_server.py          # Speed evaluation (holds y)
├── server.py                # Alternative server implementation
├── car.py                   # Car entity with encrypted attributes
├── user.py                  # User entity with XPF balance
├── prover.py                # Speed verification using secret flags
├── crypto_params.py         # Cryptographic parameters (p, g)
└── requirements.txt         # Python dependencies
```

## Technical Implementation

### Key Components

**Principal Server (`principal_server.py`)**
- Master key management
- Car encryption/decryption coordination
- Race orchestration
- Training operations

**Generator Server (`generator_server.py`)**
- Random flag generation using `secrets` module
- Discrete log protection: `g^(x_i) mod p`
- Oracle pattern for car instantiation

**Speed Server (`speed_server.py`)**
- Weather-dependent weight vectors
- Functional key computation: `Sk_y = <weights, masked_sk>`
- Homomorphic operations on ciphertexts

**Prover (`prover.py`)**
- Verification using secret flags
- Computes expected speed from plaintext
- Enables correctness checking

### Cryptographic Parameters

**Demo Configuration**: The current implementation uses smaller primes for demonstration purposes. These parameters are **not cryptographically secure** for production use.

For a production deployment:
- Use 2048-bit or larger primes
- Implement proper key management
- Add authenticated channels between servers
- Use BLS pairings for public verification

## Educational Purpose

This demo illustrates:
- **Functional Encryption** - Computing on encrypted data
- **Multi-Party Computation** - Distributed secret sharing
- **Homomorphic Operations** - Training without decryption
- **Zero-Knowledge Proofs** - Verification without revealing secrets
- **Blockchain Integration** - Decentralized game logic

## Future Enhancements

- [ ] BLS pairing-based public verification
- [ ] Blockchain smart contract integration
- [ ] Cryptographically secure parameters (2048-bit primes)
- [ ] Multiple Speed Servers (y_1, y_2, ..., y_n)
- [ ] On-chain race result verification
- [ ] NFT representation of cars
- [ ] Tournament mode with brackets
- [ ] Staking and tokenomics

## Verification Process

The system supports public verification through:

1. **Correctness Check**:
   ```
   V * Ct^(Sk_y) = ∏ Ctx_i^(z_i)
   ```

2. **Pairing Verification** (future):
   ```
   e(Ctx_i, h_i) = e(Ctx_i^(z_i), g)
   ```
   where `h_i = g^(z_i)`

These checks ensure the speed computation was performed correctly without revealing secret values.

## Contributing

Contributions are welcome! Areas for improvement:
- Enhanced cryptographic security
- Blockchain integration
- Additional game mechanics
- UI/UX improvements
- Test coverage

## License

This project is open source and available for educational purposes.

## Authors

MagicThunder02

## Acknowledgments

This project demonstrates practical applications of:
- Inner Product Functional Encryption
- Discrete Logarithm-based cryptography
- Multi-party computation protocols
- Homomorphic encryption schemes

---

**Disclaimer**: This is a demonstration project for educational purposes. The cryptographic parameters are intentionally simplified for performance. Do not use in production without proper security hardening.
