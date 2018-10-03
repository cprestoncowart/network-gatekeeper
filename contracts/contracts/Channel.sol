pragma solidity ^0.4.19;

contract Channel {

  address public client;
  address public server;
  uint public startDate;
  uint8 public channelTimeout;

  function Channel(address to, uint8 timeout) public payable {
    server = to;
    client = msg.sender;
    startDate = now;
    channelTimeout = timeout;
  }

  function payout(bytes32 h, uint8 v, bytes32 r, bytes32 s, uint256 amount) public {
    if (msg.sender != server) { revert(); }
    if (keccak256(amount, this) != h) { revert(); }

    bytes memory prefix = "\x19Ethereum Signed Message:\n32";
    bytes32 prefixedHash = keccak256(prefix, h);
            
    address signer = ecrecover(prefixedHash, v, r, s);

    if (signer != client) { revert(); }

    if (!server.send(amount)) { revert(); }

    selfdestruct(client);
  }

  function timeout() public {
    if (startDate + channelTimeout > now || msg.sender != client)
      { revert();}

    selfdestruct(client);
  }

}