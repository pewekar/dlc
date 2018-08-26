from Bob import hexBob,Bob_pubkey
from btcpy.structs.crypto import PrivateKey,PublicKey
from Txn import get_solver
from btcpy.structs.script import IfElseScript, P2pkhScript, RelativeTimelockScript
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
    #pubkey=determine_pubkey(priv)#G.add(int(pub.hexlify(),16)) #ToDO Failing  Must check
    ContractPubkey=generate_contract_pub(S,pubkey);
    ContractPubScript=get_outscript(ContractPubkey)
    return ContractPubkey,ContractPubScript;

def dlcB(msg): #TODO Seperate out private key processing for B. It should not reside in the same routine
    s,S=dlcO(msg);
    privkeyB,pubkeyB,ContractPrivkeyB,ContractScriptSigB_IF,ContractScriptSigB_ELSE = priv_process(hexBob, s)
    ContractPubkeyB,ContractPubScriptB = pub_process(pubkeyB,S)
    return ContractPrivkeyB,ContractScriptSigB_IF,ContractScriptSigB_ELSE,ContractPubkeyB,ContractPubScriptB

def pubkeyB():
    #priv_key=PrivateKey.unhexlify(Bob())
    return Bob_pubkey;#priv_key.pub()

#if __name__ == "__main__":
#    main()