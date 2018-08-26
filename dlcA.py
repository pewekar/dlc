from Alice import hexAlice,AlicePubkey#
from btcpy.structs.crypto import PrivateKey,PublicKey
from Txn import get_solver
from btcpy.structs.script import P2pkhScript#,IfElseScript, RelativeTimelockScript
from dlcO import dlcO
from schnorr import determine_pubkey,n

def generate_contract_priv(s, privkey): #TODO separate out privkey processing
    privContract = (privkey+s) % n; # Verified pubkey can be derived independently #Todo Gives 'Odd length string' error sometimes
    privk =PrivateKey.unhexlify(format(privContract,'x'))#hex(privContract).split('x')[-1])); # format(privContract,'x')
    return privk; #pubContract,privContract

def generate_contract_pub(S, pubkey): #TODO separate out privkey processing
    pubContract=pubkey.add(S);
    pubk = get_hexPubkey(pubContract); # todo verify pubkey calc
    return pubk; #pubContract,privContract

def get_outscript(pubContract):#, pubkey_other): #ToDO generate using Pybtc library
    pubscript = P2pkhScript(pubContract)
    return pubscript;

def setSelectedScript(selectedMessage, outputScriptA, outputScriptB):
    selectedScriptA = outputScriptA[selectedMessage];
    selectedScriptB = outputScriptB[selectedMessage];
    return selectedScriptA, selectedScriptB;

def get_hexPubkey(decPubkey):
    pubk = PublicKey(bytearray([0x04])
                     + decPubkey.get_x().to_bytes(32, 'big')
                     + decPubkey.get_y().to_bytes(32, 'big'))
    pubk = pubk.compress()
    return pubk;

def priv_process(key,s):
    privkey =int(key,16);
    pubkey=determine_pubkey(privkey)
    ContractPrivkey=generate_contract_priv(s,privkey);
    ContractScriptSig_IF,ContractScriptSig_ELSE=get_solver(ContractPrivkey)
    return privkey,pubkey,ContractPrivkey,ContractScriptSig_IF,ContractScriptSig_ELSE;

def pub_process(pubkey,S):
    ContractPubkey=generate_contract_pub(S,pubkey);
    ContractPubScript=get_outscript(ContractPubkey)
    return ContractPubkey,ContractPubScript;

def dlcA(msg): #TODO Seperate out private key processing. It should not reside in the same routine
    s,S=dlcO(msg);
    privkeyA,pubkeyA,ContractPrivkeyA,ContractScriptSigA_IF,ContractScriptSigA_ELSE = priv_process(hexAlice, s) #todo Shouldent be passing private key here
    ContractPubkeyA,ContractPubScriptA = pub_process(pubkeyA,S)
    return ContractPrivkeyA,ContractScriptSigA_IF,ContractScriptSigA_ELSE,ContractPubkeyA,ContractPubScriptA

def pubkeyA():
    return AlicePubkey
    #priv_key=PrivateKey.unhexlify(Alice())
    #priv_key.pub()

#if __name__ == "__main__":
#    main()