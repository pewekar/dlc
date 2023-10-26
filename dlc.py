"""
DLC contract script generation and funding transaction creation.

This script generates a DLC contract script and a funding transaction for the given message options.
The contract script allows the two parties to bet on the outcome of the message.
The funding transaction funds the contract and locks up the funds of both parties.

Usage:

python dlc_create.py <message_options>

Where <message_options> is a comma-separated list of message options.

Example:

python dlc_create.py sun,moon,rain

This will generate a contract script and funding transaction for a DLC contract where the two parties bet on the outcome of the message "sun", "moon", or "rain".
"""

import sys
from time import time  # timing
from btcpy.setup import setup  # TODO Remove??

setup("testnet")
from dlcA import dlcA, pubkeyA
from dlcB import dlcB, pubkeyB
from Txn import createContractOutput, createContractTx, createContractInput, get_solver
from dlcF import (
    fundingTxn,
    fundingInput_value,
    sweepTx,
    FundingSolver,
)  # sendBack,fundingTxIn,FundingScript
from dlcO import set_message, OraclePub, onetimekey
from parms import txFee, cutA


def value_split(
    contractValue, ratio
):  # TODo Accept a list of ratios or even absolute values with error checks
    """Splits the contract value into two parts, according to the given ratio.

    Args:
        contractValue: The total value of the contract.
        ratio: The ratio to split the contract value into.

    Returns:
        A list of two values, representing the split contract values.
    """

    first = int(round(contractValue * ratio))
    return [first, contractValue - first]


def set_choice():  # for Alice
    """Returns the user's chosen message option.

    Returns:
        The user's chosen message option.
    """

    chosen_message = "sun"  # input(user_prompt)
    print("Alice chose ", chosen_message)
    return chosen_message


def set_messageOptions():
    """Returns a list of message options, from the command line arguments.

    Returns:
        A list of message options.
    """

    if len(sys.argv) > 1:  # =2:
        messageOptions = sys.argv[1].split(",")
        # pass a comma-separated string (without the brackets):python3 test.py 1,2,3,4,5 0
        #    lockTime = sys.argv[2]
        return messageOptions
        # lockTime
    else:
        sys.exit("List of outcomes not specified")


A = OraclePub()  # Part 1 of Pubkey
R = onetimekey()
# Part 2 of pubkey TODO remove direct dependency on k from DLC


def main():  # TODO Seperate out private key processing for A & B. They should not reside in the same routine
    """Generates a DLC contract script and a funding transaction.

    Returns:
        None.
    """

    start = time()
    messageOptions = set_messageOptions()
    msg = set_message(messageOptions)
    (
        ContractPrivkeyA,
        ContractScriptSigA_IF,
        ContractScriptSigA_ELSE,
        ContractPubkeyA,
        ContractPubScriptA,
    ) = dlcA(msg)
    (
        ContractPrivkeyB,
        ContractScriptSigB_IF,
        ContractScriptSigB_ELSE,
        ContractPubkeyB,
        ContractPubScriptB,
    ) = dlcB(
        msg
    )  # TODO Seperate out privkey processing
    valueA, valueB = value_split(fundingInput_value() - txFee * 2, cutA)
    Pub_Script = createContractOutput(
        ContractPubScriptA, ContractPubScriptB, valueA, valueB
    )  # todo    print("OutScript A:\n", str(ContractPubScriptA), "\nOutScript B:\n", str(ContractPubScriptB),"\nValue Split a,b =",valueA,",",valueB,"from",fundingInput_value())  # Works !
    (
        fundingTxId,
        fundingTxOutput,
    ) = fundingTxn()  # todo replace fundingTxOutput with multisig txoutput
