#from btcpy.setup import setup
#setup('testnet')
from btcpy.structs.transaction import Transaction, TxIn, MutableTxIn,Sequence, MutableTransaction, TxOut, Locktime,SegWitTransaction, MutableSegWitTransaction, Witness
from btcpy.structs.script import StackData, ScriptSig, unhexlify#,P2pkhScript,P2shScript,ScriptBuilder,Script
from btcpy.structs.sig import IfElseSolver, P2pkhSolver, P2shSolver,TimelockSolver, Branch #, ScriptSig
# from btcpy.structs.block import Block
#from btcpy.structs.crypto import PublicKey, PrivateKey
#from btcpy.structs.script import IfElseScript, P2pkhScript, RelativeTimelockScript
#from Funding import funding_sig,funding_pubkey,fundingTxn
# todo generalize to segwit
def createContractTx(SigScript,PubScript): # Array of outputs . e.g see outs comment
    #    FundingWitness=SegWit_Witness(funding_sig(),funding_pubkey());

    # SigScript1 = Script.unhexlify('48304502210083e6e7507e838a190f0443441c0b62d2df94673887f4482e27e89ff415a90392022050575339c649b85c04bb410a00b62325c1b82c537135fa62fb34fae2c9a30b0b01210384478d41e71dc6c3f9edde0f928a47d1b724c05984ebfb4e7d0422e80abe95ff')
    ContractTx = MutableSegWitTransaction(version=1,
                           ins=SigScript,#,witness=FundingWitness)],
                           outs=PubScript, #[TxOut(value=1,n=0,script_pubkey=FundingPubkey)], locktime=Locktime(0))
                           locktime=Locktime(0)) #TODO Failing here .why do we need this ?
    return ContractTx;

def createContractInput(fundingTx):
    to_spend = fundingTx #TODO Failing here
    #Signer=fundingTxn() #Todo LATEST Failing here .Change to spend input Transaction
    Signer= ScriptSig.empty() #TOdo create SignFundingTx(FundingTx, Solver)
    SigScript=[MutableTxIn(txid=to_spend, # Input need not be a segwit transaction.
                    txout=0,
                    script_sig=Signer,
                    sequence=Sequence.max())]
    return SigScript;



def createContractOutput(outScriptA,outScriptB,valueA,valueB):
    '''
    PubScript=[TxOut(value=valueA,n=0,script_pubkey=P2pkhScript(pubkeyA))#outScriptA) or P2shScript(outScriptA)) #ToDo how to use OutScriptA, OutScriptB as pubkeys?
               ,TxOut(value=valueB,n=1,script_pubkey=P2pkhScript(pubkeyB))]#outScriptB)] or P2shScript(outScriptB))]# ToDO WORKS !!!
    '''
    PubScript=[TxOut(value=valueA,n=0,script_pubkey=outScriptA)
        ,TxOut(value=valueB,n=1,script_pubkey=outScriptB)]#
    #print ("Funding Output Script:" , PubScript[0].to_json(),"\n",PubScript[1].to_json())
    return PubScript;

def get_solver(ContractPrivkey): # todo to fix if & else solvers
    IFsolver = IfElseSolver(Branch.IF,P2pkhSolver(ContractPrivkey)); #TODO How to check/View ??
    IFsolver =P2pkhSolver(ContractPrivkey);
    #IFscript = P2pkhSolver(ContractPrivkey); #
    #print(IFscript); Doesnt Work
    ELSEsolver=IfElseSolver(Branch.ELSE,TimelockSolver(P2pkhSolver(ContractPrivkey))); #TODO How to check/View ??
    ELSEsolver=P2pkhSolver(ContractPrivkey);
    #ELSEscript=TimelockSolver(P2pkhSolver(ContractPrivkey));
    #print(ELSEscript); # Doesnt Work
    return IFsolver,ELSEsolver;

def SegWit_Witness(sig, pubkey):    #TODO Successfully
    witness_sig = StackData.from_bytes(unhexlify(sig));
    witness_pubkey = StackData.from_bytes(unhexlify(pubkey));
    witness = Witness([witness_sig, witness_pubkey])
    return witness;

def signTx(unsigned,tx_solver):  # ToDo refer her to spend
    signedTx = unsigned.spend([unsigned.outs[0]], [tx_solver])
    return signedTx;



def unsignedTx(intxs,outtxs):
    unsigned = MutableTransaction(version=1, ins=intxs, outs=outtxs)#,locktime=Locktime(0))
    return unsigned;

def tx_in(tx,inscript):  #TODO change from 1 i/p to multi i/p
    to_spend = Transaction.unhexlify(tx)
    intxs=[TxIn(txid=to_spend.txid, txout=0, sequence=Sequence.max(), script_sig=inscript )] #ScriptSig.<something>
    return intxs;

def tx_out(outvalue,outscript):  #TODO change from 1 o/p to multi o/p
    outtxs=[TxOut(value=outvalue, n=0, script_pubkey=outscript)]
    return outtxs;
