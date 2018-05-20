// import {EC} from "./EC.sol";
import {Secp256k1} from "https://github.com/androlo/standard-contracts/contracts/src/crypto/Secp256k1.sol";

contract HomomorphicTransaction {
    uint constant p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f;
    uint constant baseX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798;
    uint constant baseY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8;
    
    uint public numTxs = 0;
    
    event NewTransaction(uint index);
    
    mapping (uint => bool) public isSpent;
    mapping (uint => uint[5][]) public txins;  // txindex, txoutindex, v, r, s
    mapping (uint => uint[3][]) public txouts; // amount_x, amount_y, pubkeyHash
    
    function mint(uint[3][] _outputs) public payable {
        require(msg.value > 0);
        
        uint[3] memory amount_in = Secp256k1._mul(msg.value, [baseX, baseY]);
        
        uint[3] memory amount_out;
        
        for (uint8 j = 0; j < _outputs.length; j++) {
            uint[3] memory _out = _outputs[j];
            require(Secp256k1.onCurve([_out[0], _out[1]]));
            Secp256k1._addMixedM(amount_out, [_out[0], _out[1]]);
        }
        
        // x_1z_2^2 = x_2z_1^2
        require(
            mulmod(mulmod(amount_out[2], amount_out[2], p), amount_in[0], p)
            ==
            mulmod(mulmod(amount_in[2], amount_in[2], p), amount_out[0], p)
        );
        
        // y_1z_2^3 = y_2z_1^3
        require(
            mulmod(mulmod(mulmod(amount_out[2], amount_out[2], p), amount_out[2], p), amount_in[1], p)
            == 
            mulmod(mulmod(mulmod(amount_in[2], amount_in[2], p), amount_in[2], p), amount_out[1], p)
        );
        
        emit NewTransaction(numTxs);
        
        txouts[numTxs] = _outputs;
        
        numTxs++;
    }
    
    function send(uint[5][] _inputs, uint[3][] _outputs) public {
        require(_inputs.length <= 10);
        require(_outputs.length <= 10);
        
        uint[3] memory amount_in;
        for (uint8 i = 0; i < _inputs.length; i++) {
            uint[5] memory _in = _inputs[i];
            bytes32 message = keccak256(_in[0], _in[1]); // message to sign; composite of txindex and txoutindex;
            require(isSpent[uint256(message)] == false); // check if corresponding txout is spent
            uint[3] memory out = txouts[_in[0]][_in[1]]; // get txout pointer
            Secp256k1._addMixedM(amount_in, [out[0], out[1]]);
            require(uint256(ecrecover(message, uint8(_in[2]), bytes32(_in[3]), bytes32(_in[4]))) == out[2]);
            isSpent[uint256(message)] = true;
        }
        
        uint[3] memory amount_out;
        for (uint8 j = 0; j < _outputs.length; j++) {
            uint[3] memory _out = _outputs[j];
            require(Secp256k1.onCurve([_out[0], _out[1]]));
            Secp256k1._addMixedM(amount_out, [_out[0], _out[1]]);
        }
        
        // x_1z_2^2 = x_2z_1^2
        require(
            mulmod(mulmod(amount_out[2], amount_out[2], p), amount_in[0], p)
            ==
            mulmod(mulmod(amount_in[2], amount_in[2], p), amount_out[0], p)
        );
        
        // y_1z_2^3 = y_2z_1^3
        require(
            mulmod(mulmod(mulmod(amount_out[2], amount_out[2], p), amount_out[2], p), amount_in[1], p)
            == 
            mulmod(mulmod(mulmod(amount_in[2], amount_in[2], p), amount_in[2], p), amount_out[1], p)
        );
        
        txins[numTxs] = _inputs;
        txouts[numTxs] = _outputs;
        
        emit NewTransaction(numTxs);
        
        numTxs++;
    }
}