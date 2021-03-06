
import pytest
from pycctx import *
import base64

address0 = "RWqrNbM3gUr4A9kX9sMXTRyRbviLsSbjAs"
outpoint0 = ("d21633ba23f70118185227be58a63527675641ad37967e2aa461559f577aec43", 3)

keypair = {
    "wif": "UuKZRxAR4KYVSVKxgL8oKuyBku7bVhqbGk9onuaEzkXdaxgytpLB",
    "addr": "RWqrNbM3gUr4A9kX9sMXTRyRbviLsSbjAs",
    "pubkey": "038c3d482cd29f75ce997737705fb5287f022ded66093ee7d929aea100c5ef8a63"
}


def test_encode_vin():
    vin = TxIn(outpoint0, ScriptSig.from_address(address0))
    assert vin.to_py() == {
        "previous_output": outpoint0,
        "script": {
            "address": address0,
        }
    }

def test_tx_decode():
    tx = Tx.decode('01000000000000000000')
    assert tx.hash == "d21633ba23f70118185227be58a63527675641ad37967e2aa461559f577aec43"
    assert tx.to_py() == {
        "inputs": [],
        "outputs": []
    }

def test_known_good():
    rawtx = "010000000100b7a74ee48ac1f9a4ba3234b7398302a84e4b618bb463b46a2c23fe5a628700000000007b4c79a276a072a26ba067a565802103682b255c40d0cde8faee381a1a50bbb89980ff24539cb8518e294d3a63cefe128140b65222f7057268e48bb729ab43b7279e4eb22b82f8e6f0e559c05ff68ec4e3ed24f7d1c8095d04c21c9ce926a5bcb0b91da86e3614f46babd074c9776bc7978aa100af038001e4a10001ffffffff03e0e99b1c00000000302ea22c8020e029c511da55523565835887e412e5a0c9b920801b007000df45e545f25028248103120c008203000401cc8096980000000000232103174bf5ead8d6cf74c2e2a3dbb7149455c850243a14684baf41db1c0b19e6cc5dac0000000000000000086a06e44767458b0b00000000"
    tx = Tx.decode(rawtx)
    assert tx.to_py() == {
        'inputs': [
            {'previous_output': ('0087625afe232c6ab463b48b614b4ea8028339b73432baa4f9c18ae44ea7b700',
                                 0),
             'script': b'Ly\xa2v\xa0r\xa2k\xa0g\xa5e\x80!\x03h+%\\@'
                       b'\xd0\xcd\xe8\xfa\xee8\x1a\x1aP\xbb\xb8\x99'
                       b'\x80\xff$S\x9c\xb8Q\x8e)M:c\xce\xfe\x12\x81@\xb6R"'
                       b"\xf7\x05rh\xe4\x8b\xb7)\xabC\xb7'\x9eN\xb2+"
                       b'\x82\xf8\xe6\xf0\xe5Y\xc0_\xf6\x8e\xc4\xe3'
                       b'\xed$\xf7\xd1\xc8\t]\x04\xc2\x1c\x9c\xe9'
                       b'&\xa5\xbc\xb0\xb9\x1d\xa8n6\x14\xf4k\xab\xd0t\xc9'
                       b'wk\xc7\x97\x8a\xa1\x00\xaf\x03\x80\x01\xe4'
                       b'\xa1\x00\x01'
            }
        ],
        'outputs': [
            {'script': b'.\xa2,\x80 \xe0)\xc5\x11\xdaUR5e\x83X'
                       b'\x87\xe4\x12\xe5\xa0\xc9\xb9 \x80\x1b\x00p'
                       b'\x00\xdfE\xe5E\xf2P($\x81\x03\x12'
                       b'\x0c\x00\x82\x03\x00\x04\x01\xcc',
             'amount': 479980000
            },
            {'script': b'!\x03\x17K\xf5\xea\xd8\xd6\xcft\xc2\xe2'
                       b'\xa3\xdb\xb7\x14\x94U\xc8P$:\x14hK\xafA\xdb'
                       b'\x1c\x0b\x19\xe6\xcc]\xac',
             'amount': 10000000
             },
             {'script': b'j\x06\xe4GgE\x8b\x0b',
              'amount': 0
             }
        ]
    }

    input_script = tx.inputs[0].script.to_py()
    ffill_hex = base64.b16encode(input_script[2:-1]).decode()
    cond = Condition.decode_fulfillment(ffill_hex)

    mtx = Tx(
        inputs = [
            TxIn(tx.inputs[0].previous_output, ScriptSig.from_condition(cond)),
        ],
        outputs = [
            tx.outputs[0],
            tx.outputs[1],
            TxOut.op_return(b'\xe4GgE\x8b\x0b')
        ],
        version = 1
    )
    assert mtx.encode() == rawtx

def test_known_2():
    rawtx = "010000000126f19af8dcb4ebe16c21a118d16acbe4fd066670e656274ffb35b0ea55dc7ca8010000006a473044022034222d405a2d6b96da43da581faa369cbebeab5a255ddc111d5ed71c28013fc4022050fbd32d4c3f8845425e2c11acbb72ce2368569b7765e80ed32f1f3f2f72ed4d01210281fa0af5067ad1680a462f71535da66f290bb3a2f8ea0fa180d255b21c0e0caeffffffff01f0a29a3b000000001976a9144ac0524906dbeda34e9edfcb01c7a0f4e125b0f388ac00000000"
    wif = "UpWLKEQ1229EveQGTvr9qM5He8H8LARPFo9qoZxToswR2vkDAGQx"
    addr = "RG6SUSPQZmQLoZmH9yMVywMX1wUgYzD4Tf"

    in_tx = Tx.decode(rawtx)
    mtx = Tx(
        inputs = [
            TxIn(in_tx.inputs[0].previous_output, ScriptSig.from_address(addr),
                input_amount=999990000)
        ],
        outputs = in_tx.outputs,
        version=1
    )
    mtx.sign([wif])
    assert mtx.encode() == rawtx

def test_construct():
    # test invalid hash
    with pytest.raises(ValueError):
        TxIn(("876",1), ScriptSig(b"\0a"))

    # test valid hash
    some_hash = "0087625afe232c6ab463b48b614b4ea8028339b73432baa4f9c18ae44ea7b700"
    vin = TxIn((some_hash, 1), ScriptSig(b"\0a"))
    vout = TxOut(1, ScriptPubKey(b""))

    # test full tx
    mtx = Tx()
    mtx.inputs = (vin,)
    mtx.outputs = (vout,)
    assert mtx.to_py() == {
        'inputs': [
            {'previous_output': (some_hash, 1),
             'script': b'\x00a'}
        ],
        'outputs': [{'script': b'', 'amount': 1}]
    }


def test_sign():
    tx = Tx()
    tx.inputs = (TxIn(outpoint0, ScriptSig.from_address(keypair["addr"]), input_amount=0),
            TxIn(outpoint0, ScriptSig.from_condition(cc_secp256k1(keypair["pubkey"])), input_amount=0))

    with pytest.raises(TxSignError):
        tx.sign(["UroCh5e8855Cv31jBvR8zYH3ykuEVK84U8QsELHubSsJRemD35QV"])

    tx.sign([keypair['wif']])
    tx.hash

def test_spend_asset_tx_1():
    rawtx = "010000000126f19af8dcb4ebe16c21a118d16acbe4fd066670e656274ffb35b0ea55dc7ca8010000006a473044022049083e4c5de4c6f21f872c5abfa6ab39092fc60999bf56493004ae9650d594e90220014fb041b34ed7c7ffbd4fc5b0e327a71245ee6bbd8c1fd794f32343f98e6bd601210281fa0af5067ad1680a462f71535da66f290bb3a2f8ea0fa180d255b21c0e0caefeffffff0278d5a435000000001976a91450ad72f95bea6f640a48c3b4a7a33930bdcc541088ac00e1f505000000001976a9144ac0524906dbeda34e9edfcb01c7a0f4e125b0f388acdbad8f5e"

    wif = "UpWLKEQ1229EveQGTvr9qM5He8H8LARPFo9qoZxToswR2vkDAGQx"
    addr = "RG6SUSPQZmQLoZmH9yMVywMX1wUgYzD4Tf"

    mtx = Tx(
        inputs = [
            TxIn(("a87cdc55eab035fb4f2756e6706606fde4cb6ad118a1216ce1ebb4dcf89af126", 1),
                 ScriptSig.from_address(addr), sequence=0xFFFFFFFE,
                 input_amount=0)
        ],
	outputs = [
            TxOut(amount = 899995000,
                  script = ScriptPubKey.from_address("RGdmvKRX7ZsPkcWVuJADeEkruofZm963Gm")),
            TxOut(amount = 100000000,
                  script = ScriptPubKey.from_address("RG6SUSPQZmQLoZmH9yMVywMX1wUgYzD4Tf"))
        ],
        version = 1
    )
    mtx.lock_time = 1586474459
    mtx.sign([wif], [])
    assert mtx.encode() == rawtx
    
def test_spend_asset_tx_2():
    prevout = ("80add174937a475aebf7f5a93827f0f6565098ec5078ad7ac5c4bf7fe915696d", 1)
    wif = "UpWLKEQ1229EveQGTvr9qM5He8H8LARPFo9qoZxToswR2vkDAGQx"
    addr = "RG6SUSPQZmQLoZmH9yMVywMX1wUgYzD4Tf"
    
    mtx = Tx(
        inputs = [
            TxIn(prevout, ScriptSig.from_address(addr))
        ],
	outputs = [
            TxOut(amount = 899995000,
                  script = ScriptPubKey.from_address(addr))
        ],
        version = 1
    )

    mtx.sign([wif])

    assert mtx.encode() == "01000000016d6915e97fbfc4c57aad7850ec985056f6f02738a9f5f7eb5a477a9374d1ad80010000006a47304402202fcb2329e5d7a7d478cd7a7a876ec65e639458aef68e2cb0e51b66afb7c1ca7302205803fd35b4801cc88eb656c1a3660bd21ae2a061fbaa25e5aa47ed5e05288a3601210281fa0af5067ad1680a462f71535da66f290bb3a2f8ea0fa180d255b21c0e0caeffffffff0178d5a435000000001976a9144ac0524906dbeda34e9edfcb01c7a0f4e125b0f388ac00000000"


def test_sapling_known_good():
    rawtx = "0400008085202f89019070433375037d2a4a367d802fecd4f378ffa382d810e9a0461d05170b959184010000006b48304502210087bfa06512394890d44ea2884256f26d57f4e09723d096657d6e2f3814834e29022000cdfc1c1eb2b9d338b3e056fefdbbbf7f0354428ff420cbf8a203f76decd60201210386c12f36b585898dc4e6bc3e94a2fa6cdca45dc0e507797b59095548f8640892ffffffff0100e1f505000000001976a9145c04c6834cf94ba95110bcb92e8be7e0af4e03a388ac00000000f60000000000000000000000000000"
    wif = "UtVEQjd6qiEab5cB6ZSCi6yDj1QTND4DZJYRfKw77WbfPoTihBhV"
    addr = "RHfjxy6L2FRc6NQmiKfPS7GkqHuEHg6dQC"

    tx_in = Tx.decode(rawtx)

    mtx = Tx(
        expiry_height = 246,
        inputs = [
            TxIn(tx_in.inputs[0].previous_output, ScriptSig.from_address(addr), input_amount=100000000)
        ],
        outputs = tx_in.outputs
    )
    mtx.sign([wif])
    assert mtx.encode() == rawtx

def test_sapling_spend():
    addr = "RLiHfBnLqTiPcFr9TVPri338QU24ydAsQu"
    wif = "UpXFeRt5fatwkjqFJinyh3pLuS9MQiQzn54NtbaBMHevdZCeS3ke"
    input_amount = 1000000000000
    
    mtx = Tx(
        inputs = [
            TxIn(("adc3812216c9e2d6e54cf2581348daf96be6f77098cf496fcbd142c8388f72b5", 1),
                 ScriptSig.from_address(addr),
                 input_amount=input_amount)
        ],
        outputs = [
            TxOut(input_amount-10000, ScriptPubKey.from_address(addr))
        ]
    )
    mtx.sign([wif])
    assert mtx.hash == 'db1da66bd9b9d7d6c553a0ff64b8fb5cc4af29a4ed420891df6ca2cdb24cfbf3'


def test_cc_tx():
    txbin = "0100000001c66ef7581dd99b512e968fc3d646f1b707fa35a3b13f651f34d266ac382de614000000007b4c79a276a072a26ba067a565802103682b255c40d0cde8faee381a1a50bbb89980ff24539cb8518e294d3a63cefe1281401fa48a63559e0ac4217e107ca9b1e33c174a5240def4b9029b80f744984585b45c5c68f6a3cdd9dbe386ca562f7821dbc27ade213d68e775e8941508e5e81013a100af038001e4a10001ffffffff037026735302000000302ea22c8020e029c511da55523565835887e412e5a0c9b920801b007000df45e545f25028248103120c008203000401cc8096980000000000232103d52f33d23c236621de78be5263550fe7aa4f78c13d7992e233761697ac0ce7f6ac0000000000000000086a06e4470200000000000000"

    faucet_pk = "03682b255c40d0cde8faee381a1a50bbb89980ff24539cb8518e294d3a63cefe12"
    cond = cc_threshold(2,[cc_eval(bytes([228])),cc_threshold(1,[cc_secp256k1(faucet_pk)])])

    tx = Tx.decode(txbin)
    cond_in = tx.inputs[0].script.parse_condition()
    cond_out = tx.outputs[0].script.parse_condition()

    assert cond_in.to_anon().to_py() == cond.to_anon().to_py()
    assert cond_out.to_anon().to_py() == cond.to_anon().to_py()
