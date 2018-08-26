#from btcpy.structs.hd import ExtendedPrivateKey
from btcpy.structs.crypto import PrivateKey
from schnorr import determine_pubkey
__Bob_wifkey='cQvNSZX3YPuKz2Qx5JPsgzgw66UmRZpR7E1HcTHhBpaiX9EWF5Aj' # Make private
privBob = privkey=PrivateKey.from_wif(__Bob_wifkey)
hexBob = privBob.hexlify()
Bob_pubkey=privBob.pub()

def Bob_Curve_pubkey():
    return  determine_pubkey(int(hexBob(), 16));

 #
