# bech32p2pkaddress
Prototype support for p2pk addresses using bech32

Building on Pieter Wuille's python version of the reference implementation of Bech32 (for segwit addresses), we give python code to compute a kind of p2pk address and build transactions spending to p2pk addresses.

Note that there is no fixed format for p2pk addresses. This prototype is only intended as an example format, but it can be used already. It is the responsibility of users to keep up with p2pk utxos for which they have the private key. No current wallet software (as far as I am aware) will keep up with p2pk utxos in a user's wallet.

USE AT YOUR OWN RISK.

Example:

Suppose the pubkey you want to send to is 030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1.

The corresponding bech32 p2pk address can be computed as follows:

python computepkaddr.py 030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1

pk1qv88qcdelvv9w88jgsdj5lhzgxvn8hd2ggauz7r89ng3apu3zctdzgprkqg

An unsigned tx can be formed spending to a p2pk address as follows:

python sendtopk.py '[{"txid":"a491517c28d7eee4e175f47d3235b105576d35e7117642a997cd51c2526cb00c","vout":6}]' '{"pk1qv88qcdelvv9w88jgsdj5lhzgxvn8hd2ggauz7r89ng3apu3zctdzgprkqg":0.00179716}'

01000000010cb06c52c251cd97a9427611e7356d5705b135327df475e1e4eed7287c5191a40600000000010000000104be0200000000002321030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1ac00000000

Multiple inputs and outputs can be given, but for the moment all outputs must be Bech 32 p2pk addresses.

Using Bitcoin Core (either the debug console window or the bitcoind daemon) one can use decoderawtransaction to verify that the tx is what was intended:

decoderawtransaction 01000000010cb06c52c251cd97a9427611e7356d5705b135327df475e1e4eed7287c5191a40600000000010000000104be0200000000002321030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1ac00000000

...
  "vout": [
    {
      "value": 0.00179716,
      "n": 0,
      "scriptPubKey": {
        "asm": "030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1 OP_CHECKSIG",
        "hex": "21030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1ac",
        "reqSigs": 1,
        "type": "pubkey",
        "addresses": [
          "1CjRf1RMrTwyGoBHDbqzXERhVFkPyowt8i"
        ]
      }
    }
  ]

Note that the output has type "pubkey" (meaning it is p2pk, not p2pkh).

The Bitcoin Core signrawtransaction command can be used to sign the transaction and the sendrawtransaction command can be used to publish the signed transaction.

signrawtransaction 01000000010cb06c52c251cd97a9427611e7356d5705b135327df475e1e4eed7287c5191a40600000000010000000104be0200000000002321030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1ac00000000 [] '["L...private key for input..."]'

sendrawtransaction 01000000010cb06c52c251cd97a9427611e7356d5705b135327df475e1e4eed7287c5191a4060000006b483045022100d2fb1e6e099f3572ed7f89659e2366f9b5fcb44552bd83e31b2ebb95c4f4a50f022034904e5cea8affb2cc886d480a9a0dbed9dd42ead138f8cbb7a2c5fc82ce1cb001210335b7e991f239f9097d9f7e5b0d115b6a4983d4d38066016a12b65c5cf8b33eba010000000104be0200000000002321030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1ac00000000

The transaction constructed above (creating a p2pk output) has id

6880c2ae2f417bf6451029b716959ed255f127eeba3d7b40cf0ff3c44c5980c2

for those who wish to inspect it more closely.

The python script is not needed to spend a p2pk utxo. For example, the utxo created above was spent to an ordinary p2pkh address using Bitcoin Core alone as follows:

createrawtransaction '[{"txid":"6880c2ae2f417bf6451029b716959ed255f127eeba3d7b40cf0ff3c44c5980c2","vout":0}]' '{"16P9GwJqir9AXDSkspz9PSJyU2nHZn8mfQ":0.00140411}'

0100000001c280594cc4f30fcf407b3dbaee27f155d29e9516b7291045f67b412faec280680000000000ffffffff017b240200000000001976a9143b08b0003ef9b4f37f8d18a54f9db8ec67f8cbf088ac00000000

signrawtransaction 0100000001c280594cc4f30fcf407b3dbaee27f155d29e9516b7291045f67b412faec280680000000000ffffffff017b240200000000001976a9143b08b0003ef9b4f37f8d18a54f9db8ec67f8cbf088ac00000000 [] '["K...private key for 030e7061b9fb18571cf2441b2a7ee2419933ddaa423bc178672cd11e87911616d1..."]'

sendrawtransaction 0100000001c280594cc4f30fcf407b3dbaee27f155d29e9516b7291045f67b412faec28068000000004948304502210096bf18f3fce1f3ac800f98c12e655240cbdb7127e046a3c1bd72e16d3e16c3fd022030e897e2eea143eca4e87b28ba104625eb316f1a487a72c5aecc93b824c8c74f01ffffffff017b240200000000001976a9143b08b0003ef9b4f37f8d18a54f9db8ec67f8cbf088ac00000000


