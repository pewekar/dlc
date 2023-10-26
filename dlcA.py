"""
DLC contract script generation and funding transaction creation for Alice.

This script generates a DLC contract script and a funding transaction for the given message.
The contract script allows Alice to bet on the outcome of the message.
The funding transaction funds the contract and locks up Alice's funds.

Args:
    msg: The message to bet on.

Returns:
    A tuple of five values:
        * ContractPrivkeyA: The private key for Alice's contract script.
        * ContractScriptSigA_IF: The signature script for Alice to claim the contract if the message matches her chosen outcome.
        * ContractScriptSigA_ELSE: The signature script for Alice to claim the contract if the message does not match her chosen outcome.
        * ContractPubkeyA: The public key for Alice's contract script.
        * ContractPubScriptA: The P2PKH script for Alice's contract script.
"""

from Alice import hexAlice, AlicePubkey  #

from btcpy.structs.crypto import PrivateKey, PublicKey
from Txn import get_solver
from btcpy.structs.script import (
    P2pkhScript,
)  # ,IfElseScript, RelativeTimelockScript

from dlcO import dlcO
from schnorr import determine_pubkey, n


def generate_contract_priv(s, privkey):
    # TODO separate out privkey processing
    """Generates a private key for a DLC contract script.

    Args:
        s: A random secret salt.
        privkey: Alice's private key.

    Returns:
        The private key for Alice's contract script.
    """

    privContract = (privkey + s) % n
    privk = PrivateKey.unhexlify(format(privContract, "x"))
    return privk


def generate_contract_pub(S, pubkey):  # TODO separate out privkey processing
    """Generates a public key for a DLC contract script.

    Args:
        S: The public key for Alice's contract script.
        pubkey: Alice's public key.

    Returns:
        The public key for Alice's contract script.
    """

    pubContract = pubkey.add(S)
    pubk = get_hexPubkey(pubContract)
    return pubk


def get_outscript(pubContract):  # , pubkey_other): #ToDO generate using Pybtc library
    """Generates a P2PKH script for a DLC contract script.

    Args:
        pubContract: The public key for Alice's contract script.

    Returns:
        A P2PKH script for Alice's contract script.
    """

    pubscript = P2pkhScript(pubContract)
    return pubscript


def setSelectedScript(selectedMessage, outputScriptA, outputScriptB):

    """Selects the appropriate signature script for Alice, based on the chosen message.

    Args:
        selectedMessage: The message that Alice chose.
        outputScriptA: Alice's output script.
        outputScriptB: Bob's output script.

    Returns:
        A tuple of two values:
            * ContractScriptSigA: The signature script for Alice to claim the contract.
    """

    selectedScriptA = outputScriptA[selectedMessage]
    return selectedScriptA


def get_hexPubkey(decPubkey):
    """Compresses a public key.

    Args:
        decPubkey: The uncompressed public key.

    Returns:
        The compressed public key.
    """

    pubk = PublicKey(
        bytearray([0x04])
        + decPubkey.get_x().to_bytes(32, "big")
        + decPubkey.get_y().to_bytes(32, "big")
    )
    pubk = pubk.compress()
    return pubk


def priv_process(key, s):
    """Processes Alice's private key and generates the necessary values for the DLC contract script.

    Args:
        key: Alice's private key.
        s: A random secret salt.

    Returns:
        A tuple of five values:
            * privkey: Alice's private key.
            * pubkey: Alice's public key.
            * ContractPrivkey: The private key for Alice's contract script.
            * ContractScriptSig_IF: The signature script for Alice to claim the contract if the message matches her chosen outcome.
            * ContractScriptSig_ELSE: The signature script for Alice to claim the contract if the message does not match her chosen outcome.
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
    """Processes Alice's public key and generates the necessary values for the DLC contract script.

    Args:
        pubkey: Alice's public key.
        S: The public key for Alice's contract script.

    Returns:
        A tuple of two values:
            * ContractPubkey: The public key for Alice's contract script.
            * ContractPubScript: The P2PKH script for Alice's contract script.
    """

    ContractPubkey = generate_contract_pub(S, pubkey)
    ContractPubScript = get_outscript(ContractPubkey)
    return ContractPubkey, ContractPubScript


def dlcA(msg):
    """Generates a DLC contract script and a funding transaction for the given message.

    Args:
        msg: The message to bet on.

    Returns:
        A tuple of five values:
            * ContractPrivkeyA: The private key for Alice's contract script.
            * ContractScriptSigA_IF: The signature script for Alice to claim the contract if the message matches her chosen outcome.
            * ContractScriptSigA_ELSE: The signature script for Alice to claim the contract if the message does not match her chosen outcome.
            * ContractPubkeyA: The public key for Alice's contract script.
            * ContractPubScriptA: The P2PKH script for Alice's contract script.
    """

    s, S = dlcO(msg)
    (
        privkeyA,
        pubkeyA,
        ContractPrivkeyA,
        ContractScriptSigA_IF,
        ContractScriptSigA_ELSE,
    ) = priv_process(hexAlice, s)
    ContractPubkeyA, ContractPubScriptA = pub_process(pubkeyA, S)
    return (
        ContractPrivkeyA,
        ContractScriptSigA_IF,
        ContractScriptSigA_ELSE,
        ContractPubkeyA,
        ContractPubScriptA,
    )


def pubkeyA():
    """Returns Alice's public key.

    Returns:
        A string representing Alice's public key.
    """

    return AlicePubkey
