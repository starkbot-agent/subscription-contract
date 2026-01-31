# StarkBot Monorepo

A crypto trading bot and subscription system built on Base network. This repository contains the StarkBot ecosystem including smart contracts, trading algorithms, and subscription management.

## Overview

StarkBot is an autonomous crypto trading agent that operates on Base network with:
- **Automated Trading**: Algorithmic trading strategies and market analysis
- **Subscription System**: Token-gated access to premium features
- **Multi-Network Support**: Primarily on Base with cross-chain capabilities
- **Community Driven**: Open source with community contributions

## Repository Structure

- `/contracts` - Smart contracts for subscription and governance
- `/trading` - Trading algorithms and market analysis tools
- `/api` - API endpoints and integrations
- `/docs` - Documentation and guides

## Features

### Trading Bot Capabilities
- Real-time market analysis and signal generation
- Automated position management and risk controls
- Multi-token support with focus on Base ecosystem
- Performance tracking and analytics

### Subscription System
- **Subscribe Function**: Token-gated access requiring 1000 STARKBOT tokens
- **Token Integration**: Native STARKBOT token integration on Base
- **Subscription Tracking**: On-chain registry of subscribed addresses
- **Admin Controls**: Configurable recipient and subscription parameters

## Contract Details

### StarkBot Token Information
- **Token Address**: `0x587Cd533F418825521f3A1daa7CCd1E7339A1B07`
- **Network**: Base
- **Subscription Amount**: 1000 STARKBOT tokens

### Key Functions

#### `subscribe()`
Transfers 1000 STARKBOT tokens from the caller to the recipient address and marks the caller as subscribed.

**Requirements:**
- Caller must have approved the contract to spend 1000 STARKBOT tokens
- Caller cannot already be subscribed

#### `updateRecipient(address _newRecipient)`
Updates the recipient address. Can only be called by the current recipient.

#### `isSubscribed(address _address)`
Returns whether an address is subscribed.

## Usage

### Deployment
```solidity
// Deploy with initial recipient address
StarkBotSubscription subscription = new StarkBotSubscription(recipientAddress);
```

### Subscribing
```solidity
// First approve the contract to spend tokens
IERC20 starkbotToken = IERC20(0x587Cd533F418825521f3A1daa7CCd1E7339A1B07);
starkbotToken.approve(subscriptionContractAddress, 1000 * 10**18);

// Then subscribe
subscriptionContract.subscribe();
```

## Events

- `SubscriptionReceived`: Emitted when a user successfully subscribes
- `RecipientUpdated`: Emitted when the recipient address is updated

## Security Considerations

- The contract uses OpenZeppelin-style access control for recipient updates
- All transfers are verified before updating subscription status
- Zero address checks are implemented for critical functions

## License

MIT License