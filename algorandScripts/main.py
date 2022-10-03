import json
import base64
import os

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future.transaction import *

import role_maker as rm

from dotenv import load_dotenv
load_dotenv()


# sample program flow:

# 1. initialise an algod client: using purestake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "Im9YmvFb539Ejkc16dQ729IRpYu4FVf34MygRwsG"
algod_client = algod.AlgodClient(
    algod_token=algod_token, algod_address=algod_address)

# 2. create staff account
staff_sk, staff_pk = rm.create_acct()
print("Staff Account Details: ")
print(staff_sk, staff_pk)
print()

# 3. create trainee account
trainee_sk, trainee_pk = rm.create_acct()
print("\nTrainee Account Details: ")
print(trainee_sk, "\n", trainee_pk, "\n")

# mnemonics are:
mnemonic1 = "student jewel rapid slim pelican saddle volume crop inject second glad drama alpha vital inside atom onion ghost emerge stock promote cigar already about canyon"
mnemonic2 = "already purpose cheese beef pulse forum start job sorry model pulse luxury ceiling memory dignity nice tiger bird adjust blast merge strong canvas absent rhythm"
mnemonic3 = "peanut eternal head child fatal spare decorate cloth among portion furnace friend suspect youth ramp fuel crouch pudding good index guitar endless ranch abandon review"


# accounts created are;
accounts = {}
counter = 0
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# 4. staff to create nft
asset_id = rm.create_asset(staff_pk, staff_sk, trainee_pk)
# asset_id = rm.create_asset(mnemonic.to_public_key(os.environ.get('MNEMONIC1')), mnemonic.to_private_key(
#     os.environ.get('MNEMONIC1')), mnemonic.to_public_key(os.environ.get('MNEMONIC2')))
# asset_id = rm.create_asset(
#     accounts[0]['pk'], accounts[0]['sk'], accounts[1]['pk'])


# 5. trainee to opt-in/out of receiving nft
optin_txid = rm.opt_in(asset_id, trainee_pk, trainee_sk)

# 6. staff to receive trainee's opt-in request
# front end?

# 7. staff to approve nft transfer(transfer nft to trainee) or deny nft transfer(send notif to trainee)
transfer_txid = rm.transfer_asset(asset_id, staff_pk, staff_sk, trainee_pk)

# 8. trainee to check approval(+ view subsequent nft) or denial(to opt-in again?)
# front end?
