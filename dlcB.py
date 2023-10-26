from Bob import hexBob, Bob_pubkey
from btcpy.structs.crypto import PrivateKey, PublicKey
from Txn import get_solver
from btcpy.structs.script import IfElseScript, P2pkhScript, RelativeTimelockScript
from dlcO import dlcO
from schnorr import determine_pubkey, n


"""
Generates a DLC contract script and a funding transaction for the given message.

Args:
    msg: The message to bet on.

Returns:
    A tuple of five values:
        * ContractPrivkeyB: The private key for Bob's contract script.
        * ContractScriptSigB_IF: The signature script for Bob to claim the contract if the message matches his chosen outcome.
        * ContractScriptSigB_ELSE: The signature script for Bob to claim the contract if the message does not match his chosen outcome.
        * ContractPubkeyB: The public key for Bob's contract script.
        * ContractPubScriptB: The P2PKH script for Bob's contract script.
"""


def dlcB(msg):
    """Generates a DLC contract script and a funding transaction for the given message.

    Args:
        msg: The message to bet on.

    Returns:
        A tuple of five values:
            * ContractPrivkeyB: The private key for Bob's contract script.
            * ContractScriptSigB_IF: The signature script for Bob to claim the contract if the message matches his chosen outcome.
            * ContractScriptSigB_ELSE: The signature script for Bob to claim the contract if the message does not match his chosen outcome.
            * ContractPubkeyB: The public key for Bob's contract script.
            * ContractPubScriptB: The P2PKH script for Bob's contract script.
    """

    s, S = dlcO(msg)
    (
        privkeyB,
        pubkeyB,
        ContractPrivkeyB,
        ContractScriptSigB_IF,
        ContractScriptSigB_ELSE,
    ) = priv_process(hexBob, s)
    ContractPubkeyB, ContractPubScriptB = pub_process(pubkeyB, S)
    return (
        ContractPrivkeyB,
        ContractScriptSigB_IF,
        ContractScriptSigB_ELSE,
        ContractPubkeyB,
        ContractPubScriptB,
    )


def priv_process(key, s):
    """
    Processes Bob's private key and generates the necessary values for the DLC contract script.

    Args:
        key: Bob's private key.
        s: A random secret salt.

    Returns:
        A tuple of five values:
            * privkey: Bob's private key.
            * pubkey: Bob's public key.
            * ContractPrivkey: The private key for Bob's contract script.
            * ContractScriptSig_IF: The signature script for Bob to claim the contract if the message matches his chosen outcome.
            * ContractScriptSig_ELSE: The signature script for Bob to claim the contract if the message does not match his chosen outcome.
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
    """
    Processes Bob's public key and generates the necessary values for the DLC contract script.

    Args:
        pubkey: Bob's public key.
        S: The public key for Bob's contract script.

    Returns:
        A tuple of two values:
            * ContractPubkey: The public key for Bob's contract script.
            * ContractPubScript: The P2PKH script for Bob's contract script.
    """
    ContractPubkey = generate_contract_pub(S, pubkey)
    ContractPubScript = get_outscript(ContractPubkey)
    return ContractPubkey, ContractPubScript


def pubkeyB():
    """
    Returns Bob's public key.

    Returns:
        A string representing Bob's public key.
    """
    return Bob_pubkey
