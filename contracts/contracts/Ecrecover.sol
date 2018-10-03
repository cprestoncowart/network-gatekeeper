pragma solidity ^0.4.19;

contract EcRecover {

	function EcRecover() public {}

    function verify(bytes32 hash, uint8 v, bytes32 r, bytes32 s) public pure returns (address) {
        bytes32 prefixedHash = keccak256("\x19Ethereum Signed Message:\n32", hash);
        return ecrecover(prefixedHash, v, r, s);
    }
    
}