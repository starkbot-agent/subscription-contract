// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function decimals() external view returns (uint8);
}

contract StarkBotSubscription {
    // StarkBot token address on Base network
    address public constant STARKBOT_TOKEN = 0x587Cd533F418825521f3A1daa7CCd1E7339A1B07;
    uint256 public constant SUBSCRIPTION_AMOUNT = 1000 * 10**18; // 1000 STARKBOT tokens with 18 decimals
    
    address public recipient;
    mapping(address => bool) public subscribers;
    
    event SubscriptionReceived(address indexed subscriber, uint256 amount);
    event RecipientUpdated(address indexed oldRecipient, address indexed newRecipient);
    
    constructor(address _recipient) {
        require(_recipient != address(0), "Recipient cannot be zero address");
        recipient = _recipient;
    }
    
    function subscribe() external {
        require(!subscribers[msg.sender], "Already subscribed");
        
        IERC20 token = IERC20(STARKBOT_TOKEN);
        
        // Transfer 1000 STARKBOT tokens from subscriber to recipient
        bool success = token.transferFrom(msg.sender, recipient, SUBSCRIPTION_AMOUNT);
        require(success, "Transfer failed");
        
        subscribers[msg.sender] = true;
        
        emit SubscriptionReceived(msg.sender, SUBSCRIPTION_AMOUNT);
    }
    
    function updateRecipient(address _newRecipient) external {
        require(msg.sender == recipient, "Only current recipient can update");
        require(_newRecipient != address(0), "Recipient cannot be zero address");
        
        address oldRecipient = recipient;
        recipient = _newRecipient;
        
        emit RecipientUpdated(oldRecipient, _newRecipient);
    }
    
    function isSubscribed(address _address) external view returns (bool) {
        return subscribers[_address];
    }
    
    function getSubscriptionAmount() external pure returns (uint256) {
        return SUBSCRIPTION_AMOUNT;
    }
}