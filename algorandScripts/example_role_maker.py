import json
import base64

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future.transaction import *


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

# create_accts() # run the function


# staff acct to issue + distribute the nft

# for ease of reference, add acct public and private keys to an accounts dict

# (using the 3 initial accts i created)
mnemonic1 = "student jewel rapid slim pelican saddle volume crop inject second glad drama alpha vital inside atom onion ghost emerge stock promote cigar already about canyon"
mnemonic2 = "already purpose cheese beef pulse forum start job sorry model pulse luxury ceiling memory dignity nice tiger bird adjust blast merge strong canvas absent rhythm"
mnemonic3 = "peanut eternal head child fatal spare decorate cloth among portion furnace friend suspect youth ramp fuel crouch pudding good index guitar endless ranch abandon review"

accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    # accounts[counter]['pk'] = account.address_from_private_key
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1


# initialise and algod client: using purestake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "Im9YmvFb539Ejkc16dQ729IRpYu4FVf34MygRwsG"
algod_client = algod.AlgodClient(
    algod_token=algod_token, algod_address=algod_address)

#   Utility function used to print created asset for account and assetid


def print_created_asset(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break


#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


# print("Account 1 address: {}".format(accounts[1]['pk']))
# print("Account 2 address: {}".format(accounts[2]['pk']))
# print("Account 3 address: {}".format(accounts[3]['pk']))

# create asset
def create_asset(asset_creator_acct_pk, acct_to_be_assigned_pk):
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True
# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction
    txn = AssetConfigTxn(
        sender=accounts[1]['pk'],
        sp=params,
        total=12,  # for the 12 weekly challenges
        default_frozen=False,
        unit_name="certificate",
        asset_name="10 Academy Weekly Challenge Certificate",
        manager=accounts[2]['pk'],
        reserve=accounts[2]['pk'],
        freeze=accounts[2]['pk'],
        clawback=accounts[2]['pk'],
        # url="https://path/to/my/asset/details",
        decimals=0)
    # Sign with secret key of creator
    stxn = txn.sign(accounts[1]['sk'])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)


# asset_id gotten from the transaction
def change_manager(asset_id, curr_manager_pk, future_manager_pk):
    # The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
    # Keep reserve, freeze, and clawback address same as before, i.e. account 2
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    # asset_id = 328952;

    txn = AssetConfigTxn(
        sender=accounts[2]['pk'],
        sp=params,
        index=asset_id,
        manager=accounts[1]['pk'],
        reserve=accounts[2]['pk'],
        freeze=accounts[2]['pk'],
        clawback=accounts[2]['pk'])
    # sign by the current manager - Account 2
    stxn = txn.sign(accounts[2]['sk'])
    # txid = algod_client.send_transaction(stxn)
    # print(txid)

    # Wait for the transaction to be confirmed
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))

    except Exception as err:
        print(err)
    # Check asset info to view change in management. manager should now be account 1
    print_created_asset(algod_client, accounts[1]['pk'], asset_id)


# trainee acct to opt-in/out to the nft. using their public key


def opt_in(asset_id, specific_accts_pk):
    # OPT-IN
    # Check if asset_id is in account 3's asset holdings prior
    # to opt-in
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    account_info = algod_client.account_info(accounts[3]['pk'])
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break
    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=accounts[3]['pk'],
            sp=params,
            receiver=accounts[3]["pk"],
            amt=0,
            index=asset_id)
        stxn = txn.sign(accounts[3]['sk'])
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(
                confirmed_txn['confirmed-round']))
        except Exception as err:
            print(err)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        print_asset_holding(algod_client, accounts[3]['pk'], asset_id)


# staff acct to see trainee acct's opt-in request + approve/decline nft transfer

def transfer_asset(asset_id, sender_pk, receiver_pk):
    # TRANSFER ASSET
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetTransferTxn(
        sender=accounts[1]['pk'],
        sp=params,
        receiver=accounts[3]["pk"],
        amt=1,
        index=asset_id)
    stxn = txn.sign(accounts[1]['sk'])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    # The balance should now be 1. balance in receiver acct should be of 1 unit of the asset
    print_asset_holding(algod_client, accounts[3]['pk'], asset_id)
