from btcpy.structs.script import ScriptSig,P2pkhScript#, MultisigScript#, P2shScript,
from btcpy.structs.transaction import  TxIn, Sequence , TxOut, Locktime,MutableSegWitTransaction#, Transaction
from Funding import fundingTxIn,funding_sig,fundingTxIn_id, FundingScript, fundingInput_value,FundingSolver
from parms import txFee

def fundingTxn():
    Signer= ScriptSig.empty()
    outvalue = fundingInput_value(fundingTxIn,0)-400
    MultiSigTx= MutableSegWitTransaction(version=1,  #Publish to the Blockchain
                                  ins=[TxIn(txid=fundingTxIn_id,
                                            txout=0,
                                            script_sig=Signer,
                                            sequence=Sequence.max())],
                                  outs=[TxOut(value=outvalue,
                                              n=0,
                                              script_pubkey=FundingScript)], # todo must change this to access the contract script
                                  locktime=Locktime(0))

    MultiSigTxSigned = MultiSigTx.spend([fundingTxIn.outs[0]], [funding_sig])  # ToDo Failing here - spend attribute not found
    print ("funding tx signed ",MultiSigTxSigned.hexlify())
#    return MultiSigTx,p2sh_solver,MultiSigTxSigned.outs[0]; # TODo when to Return Signed MultiSigTransaction
    return MultiSigTxSigned.txid,MultiSigTxSigned.outs[0];

def sweepTx(MultiSigTx,MultiSigTxOutput,MultiSigTxSolver,to_pubkey,to_index,to_value):
    to_spend = MultiSigTx
    unsigned = MutableSegWitTransaction(version=1,
                                  ins=[TxIn(txid=to_spend,#.txid,
                                            txout=to_index,
                                            script_sig=ScriptSig.empty(),
                                            sequence=Sequence.max())],
                                  outs=[TxOut(value=to_value-txFee,
                                              n=0,
                                              script_pubkey=P2pkhScript(to_pubkey))], # todo make funding_pubkey a parameter. This must sweep back tp A & B
                                  locktime=Locktime(0))

    solver = MultiSigTxSolver
    signed = unsigned.spend([MultiSigTxOutput], [solver])     #print ("Return tx signed ",signed.hexlify())
    return signed.hexlify()


    #from btcpy.structs.crypto import PrivateKey,PublicKey
    #from FundingPub import FundingScript
    #from btcpy.structs.sig import IfElseSolver, P2pkhSolver, TimelockSolver, MultisigSolver,P2shSolver
    #from btcpy.structs.sig import IfElseSolver, P2pkhSolver
    #    multisig_solver, Multisig_script=Funding()
    #    p2sh_multisig = P2shScript(Multisig_script)
    #    p2sh_solver = P2shSolver(Multisig_script, multisig_solver)
    #    to_spend = fundingTxIn  # Todo Must change this to derive first output from funding_txin()