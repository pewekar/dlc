import sys

from btcpy.structs.crypto import PrivateKey, PublicKey
from Txn import get_solver

from btcpy.structs.script import IfElseScript, P2pkhScript, RelativeTimelockScript
from dlcF import fundingTxn, fundingInput_value, sweepTx  # sendBack,fundingTxIn,
from Oracle import Oracle

from schnorr import determine_pubkey, generate_privkey, n, hashThis

nonce = generate_privkey()  # message nonce
a = Oracle
k = nonce


def OraclePub():  #
    """Returns the Oracle's public key."""
    return determine_pubkey(a)


A = OraclePub()  # Part 1 of Pubkey


def onetimekey():
    """Returns a one-time key used to encode messages."""
    R = determine_pubkey(k)
    return R


R = onetimekey()
# Part 2 of pubkey TODO remove direct dependency on k from DLC


def generate_contract_priv(s, privkey):  # TODO separate out privkey processing
    """Generates a contract private key.

    Args:
        s: The secret key.
        privkey: The private key.

    Returns:
        The contract private key.
    """
    privContract = (privkey + s) % n
    privk = PrivateKey.unhexlify(format(privContract, "x"))
    return privk


def generate_contract_pub(S, pubkey):  # TODO separate out privkey processing
    """Generates a contract public key.

    Args:
        S: The public key of the contract.
        pubkey: The public key.

    Returns:
        The contract public key.
    """
    pubContract = pubkey.add(S)
    pubk = get_hexPubkey(pubContract)
    return pubk


def get_sig(msg):
    """Generates a signature for a message.

    Args:
        msg: The message to sign.

    Returns:
        The signature.
    """
    e = hashThis(msg, R)
    s = (k + e * a) % n
    return s


def pub_sig(msg):
    """Generates a public key signature for a message.

    Args:
        msg: The message to sign.

    Returns:
        The public key signature.
    """
    return R.add(A.mul(hashThis(msg, R)))


def get_outscript(pubContract):  # , pubkey_other): #ToDO generate using Pybtc library
    """Generates an output script for a contract public key.

    Args:
        pubContract: The contract public key.

    Returns:
        The output script.
    """
    pubscript = P2pkhScript(pubContract)
    return pubscript


def setSelectedScript(selectedMessage, outputScriptA, outputScriptB):
    """Selects the appropriate script for a given message.

    Args:
        selectedMessage: The message to select the script for.
        outputScriptA: The output script for party A.
        outputScriptB: The output script for party B.

    Returns:
        The selected script.
    """
    selectedScriptA = outputScriptA[selectedMessage]
    selectedScriptB = outputScriptB[selectedMessage]
    return selectedScriptA, selectedScriptB


def get_hexPubkey(decPubkey):
    """Converts a decimal public key to a hexadecimal public key.

    Args:
        decPubkey: The decimal public key.

    Returns:
        The hexadecimal public key.
    """
    pubk = PublicKey(
        bytearray([0x04])
        + decPubkey.get_x().to_bytes(32, "big")
        + decPubkey.get_y().to_bytes(32, "big")
    )
    pubk = pubk.compress()
    return pubk


def priv_process(key, s):
    """Processes a private key and generates the contract private key and script sigs.

    Args:
        key: The private key in hexadecimal format.
        s: The secret key.

    Returns:
        A tuple containing the private key, public key, contract private key, contract script sig IF, and contract script sig ELSE.
    """

    privkey = int(key, 16)
    pubkey = determine_pubkey(privkey)
    ContractPrivkey = generate_contract_priv(s, privkey)
    ContractScriptSig_IF, ContractScriptSig_ELSE = get_solver(ContractPrivkey)
    return (
        privkey,
        pubkey,
        ContractPrivkey,
        ContractScriptSig_IF,
        ContractScriptSig_ELSE,
    )


def pub_process(pubkey, S):
    """Processes a public key and generates the contract public key and output script.

    Args:
        pubkey: The public key.
        S: The public key of the contract.

    Returns:
        A tuple containing the contract public key and output script.
    """

    ContractPubkey = generate_contract_pub(S, pubkey)
    ContractPubScript = get_outscript(ContractPubkey)
    return ContractPubkey, ContractPubScript


def dlcO(
    msg,
):  # TODO Seperate out private key processing. It should not reside in the same routine
    """Generates a signature and public key signature for a message.

    Args:
        msg: The message to sign.

    Returns:
        A tuple containing the signature and public key signature.
    """

    s = get_sig(msg)
    S = pub_sig(msg)
    return s, S


def pubkeyO():
    """Returns the public key of the Oracle."""

    priv_key = PrivateKey.unhexlify(Oracle())
    return priv_key.pub()


def set_message(messageOptions):
    """Selects a message from a list of options.

    Args:
        messageOptions: A list of message options.

    Returns:
        The selected message.
    """

    import sys
    from dlc import set_choice

    count = 1
    while count < len(messageOptions):
        user_prompt = "Select one from " + str(messageOptions) + ", Alice: "
        selection = set_choice()  # input(user_prompt)
        if selection in messageOptions:
            return selection
        else:
            count = count + 1
    sys.exit("Wrong option selected")
