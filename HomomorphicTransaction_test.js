const addr = "0xe8e7c10967dbe7f3fbfe381db73dd16af9e5e33c";

const Web3 = require('web3');
const elliptic = require('elliptic');
const ec = elliptic.ec("secp256k1");
const web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545/'))
const BN = require("bn.js");
const SHA3 = require('sha3');

function calculate_addr(key) {
  const d = new SHA3.SHA3Hash(256)
  d.update(Buffer.from(key.pub.x.toString('hex') + key.pub.y.toString('hex'), 'hex'))
  return '0x' + d.digest('hex').slice(24)
}

const k1 = ec.keyFromPrivate("test sono itchi dayo")
k1.getPublic();
const k1addr = calculate_addr(k1); // 0xd4be9d252318628613b786c893560152c711763d

const k2 = ec.keyFromPrivate("test sono ni dayo wowowow")
k2.getPublic();
const k2addr = calculate_addr(k2); // 0xbde7a982a5da1d64dabb867db6d015384e67bda6

const hom = new web3.eth.Contract([
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "txouts",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "isSpent",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_outputs",
				"type": "uint256[3][]"
			}
		],
		"name": "mint",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "numTxs",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_inputs",
				"type": "uint256[5][]"
			},
			{
				"name": "_outputs",
				"type": "uint256[3][]"
			}
		],
		"name": "createTransaction",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "txins",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "NewTransaction",
		"type": "event"
	}
], addr);

one_ether = "1000000000000000000";
one_ether_encrypted = ec.g.mul(new bn(one_ether));
// [["0x29f1348bd6c634cc19c31aec3bb052a3bef0f603c73997fb0f841c12d236d372", "0xee4f8cbcd1b522c4949168ca9f9731f261de719dbf8aaab488b8801c8dd3b2a7", "0xd4be9d252318628613b786c893560152c711763d"]]
mint([[one_ether_encrypted.x.toString(), one_ether_encrypted.y.toString(), k1addr]], {value: one_ether});

