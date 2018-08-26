from btcpy.structs.crypto import PrivateKey,PublicKey
from btcpy.structs.script import MultisigScript, P2shScript,ScriptSig,P2pkhScript
from btcpy.structs.transaction import  Transaction#,TxIn, Sequence , TxOut, Locktime,MutableSegWitTransaction,
from btcpy.structs.sig import MultisigSolver, P2pkhSolver#, TimelockSolver, ,P2shSolver,, IfElseSolver
from Alice import privAlice , AlicePubkey#TODO Do not access Alices private key directly
from Bob import privBob , Bob_pubkey#TODO Do not access Bobs private key directly
from parms import FundingPrivkey,hexFundingTx
#from dlcF import fundingTxIn,fundingTxIn_id,funding_sig,funding_pubkey
#priv_key = 'cQQF6fSJEtLVLN7jueHqBWd3tSE7kAEMst8HjoK2xzv7s7SR3Gne' # TODO This must be processed seperately
fundingTxIn=Transaction.unhexlify(hexFundingTx)
fundingTxIn_id= fundingTxIn.txid
funding_sig=P2pkhSolver(PrivateKey.from_wif(FundingPrivkey))
FundingSolver= MultisigSolver(privAlice,privBob) # TODO Should not be processed here
FundingScript = MultisigScript(2, AlicePubkey, Bob_pubkey, 2)  # a 2-of-2 multisig
#        p2sh_multisig = P2shScript(Multisig_script)
#        p2sh_solver = P2shSolver(Multisig_script, multisig_solver)
def fundingInput_value(inputTx=fundingTxIn,idx=0):
    return inputTx.outs[idx].value    #print("Contract Value =",contractValue)
#funding_pubkey=PrivateKey.from_wif(priv_key).pub()



