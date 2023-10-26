from btcpy.structs.crypto import PrivateKey, PublicKey
from btcpy.structs.script import (
    MultisigScript,
    P2shScript,
    ScriptSig,
    P2pkhScript,
)
from btcpy.structs.transaction import (
    Transaction,
)  # ,TxIn, Sequence , TxOut, Locktime,MutableSegWitTransaction,
from btcpy.structs.sig import (
    MultisigSolver,
    P2pkhSolver,
)  # , TimelockSolver, ,P2shSolver,, IfElseSolver
from Alice import (
    privAlice,
    AlicePubkey,
)  # TODO Do not access Alices private key directly
from Bob import privBob, Bob_pubkey  # TODO Do not access Bobs private key directly
from parms import FundingPrivkey, hexFundingTx


fundingTxIn = Transaction.unhexlify(hexFundingTx)
funding_sig = P2pkhSolver(PrivateKey.from_wif(FundingPrivkey))
FundingSolver = MultisigSolver(privAlice, privBob)  # TODO Should not be processed here
FundingScript = MultisigScript(2, AlicePubkey, Bob_pubkey, 2)  # a 2-of-2 multisig


def fundingInput_value(inputTx=fundingTxIn, idx=0):
    """Calculates the value of the funding input.

    Args:
        inputTx: The funding input transaction.
        idx: The index of the funding input in the transaction.

    Returns:
        The value of the funding input.
    """

    return inputTx.outs[idx].value
