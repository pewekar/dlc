from btcpy.structs.script import (
    ScriptSig,
    P2pkhScript,
)  # , MultisigScript#, P2shScript,
from btcpy.structs.transaction import (
    TxIn,
    Sequence,
    TxOut,
    Locktime,
    MutableSegWitTransaction,
)  # , Transaction
from Funding import (
    fundingTxIn,
    funding_sig,
    FundingScript,
    fundingInput_value,
    FundingSolver,
)
from parms import txFee


def fundingTxn():
    """Creates a funding transaction.

    Returns:
        A tuple of two values:
            * txid: The transaction ID of the funding transaction.
            * output: The first output of the funding transaction.
    """

    signer = ScriptSig.empty()
    outvalue = fundingInput_value(fundingTxIn, 0) - 400
    multi_sig_tx = MutableSegWitTransaction(
        version=1,  # Publish to the Blockchain
        ins=[
            TxIn(
                txid=fundingTxIn.id, txout=0, script_sig=signer, sequence=Sequence.max()
            )
        ],
        outs=[
            TxOut(value=outvalue, n=0, script_pubkey=FundingScript)
        ],  # todo must change this to access the contract script
        locktime=Locktime(0),
    )

    try:
        multi_sig_tx_signed = multi_sig_tx.spend([fundingTxIn.outs[0]], [funding_sig])
    except AttributeError:
        print("spend attribute not found")
        raise

    print("funding tx signed ", multi_sig_tx_signed.hexlify())
    return multi_sig_tx_signed.txid, multi_sig_tx_signed.outs[0]


def sweepTx(
    multi_sig_tx,
    multi_sig_tx_output,
    multi_sig_tx_solver,
    to_pubkey,
    to_index,
    to_value,
):
    """Sweeps a multi-signature transaction.

    Args:
        multi_sig_tx: The multi-signature transaction to sweep.
        multi_sig_tx_output: The output of the multi-signature transaction to sweep.
        multi_sig_tx_solver: The solver for the multi-signature transaction.
        to_pubkey: The public key of the recipient of the swept funds.
        to_index: The index of the output to sweep.
        to_value: The value to sweep to the recipient.

    Returns:
        The hexlify() representation of the signed sweep transaction.
    """

    to_spend = multi_sig_tx
    unsigned = MutableSegWitTransaction(
        version=1,
        ins=[
            TxIn(
                txid=to_spend.txid,
                txout=to_index,
                script_sig=ScriptSig.empty(),
                sequence=Sequence.max(),
            )
        ],
        outs=[TxOut(value=to_value - txFee, n=0, script_pubkey=P2pkhScript(to_pubkey))],
        locktime=Locktime(0),
    )

    try:
        signed = unsigned.spend([multi_sig_tx_output], [multi_sig_tx_solver])
    except AttributeError:
        print("spend attribute not found")
        raise

    print("Return tx signed ", signed.hexlify())
    return signed.hexlify()
