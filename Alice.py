from btcpy.structs.crypto import PrivateKey
from schnorr import determine_pubkey
__Alice_wifkey='cQRUTJvxCM4mCRBkwwa7QCi5yiJG6M2zdXrVLkJqFwSBTze4oUdv';
privAlice= PrivateKey.from_wif(__Alice_wifkey);
hexAlice=privAlice.hexlify() #privkey
AlicePubkey=privAlice.pub()
def Alice_curve_pubkey():
    return determine_pubkey(int(hexAlice, 16));



