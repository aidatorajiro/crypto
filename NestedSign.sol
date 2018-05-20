pragma solidity ^0.4.21;

contract NestedSign {
    event Called(); // some restricted function
    uint256 nonce;
    address pub = 0xABCDEABCDE; // last 40 degits of keccak256(pub.x + pub.y)

    function call(uint8 _v, bytes32 _r, bytes32 _s) public {
        bytes32 _message = bytes32(uint256(msg.sender) + nonce);
        address recovered = ecrecover(_message, _v, _r, _s);
        require(recovered == pub);
        emit Called();
        nonce++;
    }
}