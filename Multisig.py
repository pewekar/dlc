from btcpy.structs.crypto import PrivateKey,PublicKey
from btcpy.structs.script import MultisigScript, P2shScript,ScriptSig,P2pkhScript
from btcpy.structs.hd import ExtendedPrivateKey, ExtendedPublicKey
from Alice import AlicePubkey, hexAlice
from Bob import Bob_pubkey, hexBob
from btcpy.structs.transaction import  TxIn, Sequence , TxOut, Locktime,MutableSegWitTransaction, Transaction
from btcpy.structs.sig import IfElseSolver, P2pkhSolver, TimelockSolver, MultisigSolver,P2shSolver

def Multisig_solver(key1,key2):
    privkAlice= PrivateKey.unhexlify(key1) # Scriptbuilder
    privkBob=PrivateKey.unhexlify(key2)
    Msolver = MultisigSolver(privkAlice,privkBob)
    return Msolver

def Multisig__script(pubkey1,pubkey2):
    script = MultisigScript(2, pubkey1, pubkey2, 2)  # a 2-of-2 multisig
    return script