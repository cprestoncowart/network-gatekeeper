pragma solidity ^0.4.17;

contract Obligation { 
  address public client;
  address public server;
  uint32 public committedPayment;

  function Obligation(address serverAddress) public {
    client = msg.sender;
    server = serverAddress;
    committedPayment = 0;
  }
  function payout() public returns (bool) {
    if (msg.sender == server) {
      server.transfer(committedPayment);
      client.transfer(this.balance);
      return true;
    } else { return false; }
  }
  function report(uint32 partialPayment) public returns (uint32) {
    if (msg.sender == client) {
      committedPayment += partialPayment;
    }
  }
}

