import sys
from time import time  # timing
from btcpy.setup import setup # TODO Remove??
setup('testnet')
from dlcA import dlcA,pubkeyA
from dlcB import dlcB,pubkeyB
from Txn import createContractOutput,createContractTx,createContractInput,get_solver
from dlcF import fundingTxn,fundingInput_value,sweepTx,FundingSolver #sendBack,fundingTxIn,FundingScript
from dlcO import set_message,OraclePub,onetimekey
from parms import txFee,cutA

def value_split(contractValue,ratio): # TODo Accept a list of ratios or even absolute values with error checks
    first=int(round(contractValue*ratio))
    return [first,contractValue-first]

def set_choice(): # for Alice
    chosen_message ="sun"#input(user_prompt);
    print("Alice chose ",chosen_message)
    return chosen_message

def set_messageOptions():
    if len(sys.argv) > 1:  # =2:
        messageOptions = sys.argv[1].split(
            ',');  # pass a comma-separated string (without the brackets):python3 test.py 1,2,3,4,5 0
        #    lockTime = sys.argv[2]
        return messageOptions;  # lockTime;
    else:
        sys.exit("List of outcomes not specified");


A=OraclePub() # Part 1 of Pubkey
R = onetimekey();  # Part 2 of pubkey TODO remove direct dependency on k from DLC
def main(): #TODO Seperate out private key processing for A & B. They should not reside in the same routine
    start = time();
    messageOptions = set_messageOptions();
    msg=set_message(messageOptions);
    ContractPrivkeyA,ContractScriptSigA_IF,ContractScriptSigA_ELSE,ContractPubkeyA,ContractPubScriptA =dlcA(msg)
    ContractPrivkeyB,ContractScriptSigB_IF,ContractScriptSigB_ELSE,ContractPubkeyB,ContractPubScriptB =dlcB(msg) #TODO Seperate out privkey processing
    valueA,valueB=value_split(fundingInput_value()-txFee*2,cutA)
    Pub_Script=createContractOutput(ContractPubScriptA,ContractPubScriptB,valueA,valueB) #todo    print("OutScript A:\n", str(ContractPubScriptA), "\nOutScript B:\n", str(ContractPubScriptB),"\nValue Split a,b =",valueA,",",valueB,"from",fundingInput_value());  # Works !
    fundingTxId,fundingTxOutput=fundingTxn()  # todo replace fundingTxOutput with multisig txoutput
    Sig_Script=createContractInput(fundingTxId) # todo Use Signed transaction ??
    ContractTx=createContractTx(Sig_Script,Pub_Script)
    ContractTxFunded = ContractTx.spend([fundingTxOutput], [FundingSolver]) # ToDo spend multisig tx output instead of fundingtxoutput Sign and Unlock (Solve) this transaction using solvers in lines 463 & 464
    #TOdo setup different signature scripts for different choices from A,B
    sendBackTxA=sweepTx(ContractTxFunded.txid,ContractTxFunded.outs[0],ContractScriptSigA_IF,pubkeyA(),0,valueA)# todo To Test & case switch for different eventualities
    sendBackTxB=sweepTx(ContractTxFunded.txid,ContractTxFunded.outs[1],ContractScriptSigB_ELSE,pubkeyB(),1,valueB) #Todo Correct???
    print("\nContract tx signed ",ContractTxFunded.hexlify())#"Contract Tx " , ContractTx.hexlify(),"\nReturn tx signed ",sendBackTx); # todo to test
    print("\nReturn tx to Alice ",sendBackTxA,"\nReturn tx to Bob ",sendBackTxB); # todo to test
    print("Schnorr elapsed=", time() - start, " seconds");
if __name__ == "__main__":
    main()

'''

a=Oracle() # TODO to remove
k=nonce # TODO to remove

def generate_contract_priv(s, privkey): #TODO separate out privkey processing
    privContract = (privkey+s) % n; # Verified pubkey can be derived independently #Todo Gives 'Odd length string' error sometimes
    privk =PrivateKey.unhexlify(format(privContract,'x'))#hex(privContract).split('x')[-1])); # format(privContract,'x')
    return privk; #pubContract,privContract

def generate_contract_pub(S, pubkey): #TODO separate out privkey processing
    #S = determine_pubkey(G, s);
    pubContract=pubkey.add(S);
    pubk = get_hexPubkey(pubContract); # todo verify pubkey calc
    return pubk; #pubContract,privContract

def get_sig(msg):
    e = hashThis(msg, R);  # part 1 of signature
    s = (k + e * a) % n;#s = (k - e * a) % n;  # part 2 of signature
    return s  # signature

def get_sig1(msg):
    return hashThis(msg, R);  # part 1 of signature

def get_sig2(e):
    return (k - e * a) % n;#s = (k - e * a) % n;  # part 2 of signature


def pub_sig(msg):
    return R.add(A.mul(hashThis(msg,R)))  # TOdo - doesent seem to work



def setSelectedScript(selectedMessage, outputScriptA, outputScriptB):
    selectedScriptA = outputScriptA[selectedMessage];
    selectedScriptB = outputScriptB[selectedMessage];
    return selectedScriptA, selectedScriptB;

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

def get_hexPubkey(decPubkey):
    pubk = PublicKey(bytearray([0x04])
                     + decPubkey.get_x().to_bytes(32, 'big')
                     + decPubkey.get_y().to_bytes(32, 'big'))
    pubk = pubk.compress()
    return pubk;

def get_outscript(pubContract):#, pubkey_other): #ToDO generate using Pybtc library
    pubscript = P2pkhScript(pubContract)
    return pubscript;

#s=get_sig(msg)
    #S= pub_sig(msg); #determine_pubkey(s)#print("Signature Pubkey1 :",S,"\nSignature Pubkey2 :",pub_sig(msg)) # checking
    #privkeyA,pubkeyA,ContractPrivkeyA,ContractScriptSigA_IF,ContractScriptSigA_ELSE = priv_process(Alice(),s)
    #ContractPubkeyA,ContractPubScriptA = pub_process(pubkeyA,S)  #print("Alice's pubkey ",curve_pubkey(),"\n Compare to ",pubkeyA) # unable to relate with point todo move one line up ?
    #privkeyB,pubkeyB,ContractPrivkeyB,ContractScriptSigB_IF,ContractScriptSigB_ELSE = priv_process(Bob(),s)
    #ContractPubkeyB,ContractPubScriptB = pub_process(pubkeyB,S)#todo Shouldent be passing private key

'''
