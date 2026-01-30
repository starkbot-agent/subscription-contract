# StarkBot Subscription Contract

A Solidity smart contract that handles StarkBot token subscriptions on the Base network.

## Features

- **Subscribe Function**: Allows users to subscribe by transferring 1000 STARKBOT tokens to a designated recipient
- **Token Integration**: Works with StarkBot token (STARKBOT) on Base network
- **Subscription Tracking**: Maintains a registry of subscribed addresses
- **Admin Controls**: Recipient address can be updated by the current recipient

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