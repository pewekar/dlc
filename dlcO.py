import sys
#from time import time  # timing
#from Alice import Alice#,Alice_pubkey#
from btcpy.structs.crypto import PrivateKey,PublicKey
from Txn import get_solver
#from schnorr import hashThis,determine_pubkey,n,ECpoint
from btcpy.structs.script import IfElseScript, P2pkhScript, RelativeTimelockScript
from dlcF import fundingTxn,fundingInput_value,sweepTx #sendBack,fundingTxIn,
from Oracle import Oracle
#from btcpy.setup import setup
from schnorr import determine_pubkey,generate_privkey,n,hashThis

#setup('testnet')

'''
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
'''
nonce = generate_privkey()# message nonce
a=Oracle
k=nonce

def OraclePub(): #
    return determine_pubkey(a);

A=OraclePub() # Part 1 of Pubkey

def onetimekey():
    R = determine_pubkey(k);  # used to encode
    return R

R = onetimekey();  # Part 2 of pubkey TODO remove direct dependency on k from DLC

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
'''
def get_sig1(msg):
    return hashThis(msg, R);  # part 1 of signature

def get_sig2(e):
    return (k - e * a) % n;#s = (k - e * a) % n;  # part 2 of signature
'''

def pub_sig(msg):
    return R.add(A.mul(hashThis(msg,R)))  # TOdo - doesent seem to work

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

def dlcO(msg): #TODO Seperate out private key processing. It should not reside in the same routine
    s=get_sig(msg)
    S= pub_sig(msg);
    return s,S

def pubkeyO():
    priv_key=PrivateKey.unhexlify(Oracle())
    return priv_key.pub()



def set_message(messageOptions):
    import sys
    from dlc import set_choice
    count = 1
    while count < len(messageOptions):
        user_prompt = "Select one from " + str(messageOptions) + ", Alice: "
        selection = set_choice()#input(user_prompt);
        if selection in messageOptions:
            return selection;  # message
        else:
            count = count + 1;
    sys.exit("Wrong option selected");



 #a, A, k, R

    #if __name__ == "__main__":
    #    main()