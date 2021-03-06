
from pycc.examples import faucet
from pycc import *
from pycctx import *

class MockChain:
    def get_tx_confirmed(self, txid):
        for tx in [create_tx]:
            if tx.hash == txid:
                return tx
        raise IndexError("Can't find tx with id: %s" % txid)


app = CCApp(faucet.schema, b'_', MockChain())

keypair = {
    "wif": "UuKZRxAR4KYVSVKxgL8oKuyBku7bVhqbGk9onuaEzkXdaxgytpLB",
    "addr": "RWqrNbM3gUr4A9kX9sMXTRyRbviLsSbjAs",
    "pubkey": "038c3d482cd29f75ce997737705fb5287f022ded66093ee7d929aea100c5ef8a63"
}

wifs = (keypair['wif'], faucet.global_addr['wif'])

# Create a dummy tx for input
dummy_tx = Tx(
    inputs = (),
    outputs = (TxOut(2000, ScriptPubKey.from_address(keypair['addr'])),)
)

create_tx = app.create_tx({
    "name": "faucet.create",
    "inputs": [
        { "previous_output": (dummy_tx.hash, 0), "script": { "address": keypair['addr'] } }
    ],
    "outputs": [
        { "amount": 2000 }
    ]
})
create_tx.sign(wifs, [dummy_tx])

drip_tx = app.create_tx({
    "name": "faucet.drip",
    "inputs": [
        { "previous_output": (create_tx.hash, 0) },
    ],
    "outputs": [
        { },
        { "script": {"address": keypair['addr']}, "amount": 1000 }
    ]
})
drip_tx.sign(wifs, [create_tx])



def test_validate_create():
    spec = app.validate_tx(create_tx)
    del spec['inputs'][0]['script']['signature']

    assert spec == {
        'name': 'faucet.create',
        'txid': create_tx.hash,
        'inputs': [
            {
                'previous_output': (dummy_tx.hash, 0),
                'script': {
                    'address': keypair['addr'],
                    'pubkey': keypair['pubkey'],
                }
            },
        ],
        'outputs': [
            { 'amount': 2000, 'script': {} }
        ],
    }
    
    # Check it can re-create itself
    create_tx_2 = app.create_tx(spec)
    create_tx_2.sign(wifs, [dummy_tx])
    assert create_tx_2.hash == create_tx.hash


def test_validate_drip():
    spec = app.validate_tx(drip_tx)

    assert spec == {
        'name': 'faucet.drip',
        'txid': drip_tx.hash,
        'inputs': [
            { 'previous_output': (create_tx.hash, 0), 'script': {} },
        ],
        'outputs': [
            { 'amount': 1000, 'script': {} },
            { 'amount': 1000, 'script': { "address": keypair['addr'] } },
        ],
    }

    # TODO: hack, what to do about this?
    spec['outputs'][0] = { }
    
    # Check it can re-create itself
    d2 = app.create_tx(spec)
    d2.sign(wifs, [create_tx])
    assert d2.hash == drip_tx.hash

