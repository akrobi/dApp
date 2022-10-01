import json
import base64

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants


# def generate_algorand_keypair():
#     private_key, public_key = account.generate_account()
#     print("My address/public key: {}".format(public_key))
#     print("My private key: {}".format(private_key))
#     print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

# create 2 accounts: for staff and for trainee
def create_accts():
    # create staff account
    print("Account 1: Staff")
    private_key1, public_key1 = account.generate_account()
    mnemonic1 = mnemonic.from_private_key(private_key1)

    # create trainee account
    print("Account 2: Trainee")
    private_key2, public_key2 = account.generate_account()
    mnemonic2 = mnemonic.from_private_key(private_key2)

    # print("Account 2: Trainee")
    # acct = account.generate_account()
    # address2 = acct[1]
    # print(address2)
    # mnemonic2 = mnemonic.from_private_key(acct[0])
    # print("mnemonic2 = \"{}\"".format(mnemonic1))

# create_accts()

# staff acct to issue + distribute the nft

# trainee acct to opt-in/out to the nft. using their public key
# staff acct to see trainee acct's opt-in request + approve/decline nft transfer
