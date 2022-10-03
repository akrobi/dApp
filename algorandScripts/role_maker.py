import json
import base64

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future.transaction import *

# initialise and algod client: using purestake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "Im9YmvFb539Ejkc16dQ729IRpYu4FVf34MygRwsG"
algod_client = algod.AlgodClient(
    algod_token=algod_token, algod_address=algod_address)


# utility function used to print created asset for account and assetid
# arguments: algodclient, account, assetid
# returns: none
def print_created_asset(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break


# utility function used to print asset holding for account and assetid
# arguments: algodclient, account, assetid
# returns: none
def print_asset_holding(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


# utility fn to retrieve the transaction id after sending the transaction to the network
# arguments: signed transaction
# returns: transaction id of the signed transaction
def retrieve_txid(stxn):
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

    return txid


# fn to create account to be used on the algorand blockchain
# arguments: none
# returns: private key, public key, and #mnemonic of account
def create_acct():
    private_key, public_key = account.generate_account()
    # mymnemonic = mnemonic.from_private_key(private_key)

    return private_key, public_key


# fn to create asset (certificates that are nfts, in our case)
# arguments: public key of asset creator, private key of asset creator, public key of account to undergo account-type change
# returns: asset id
def create_asset(asset_creator_pk, asset_creator_sk, pk_of_acct_to_be_assigned):
    params = algod_client.suggested_params()

    # asset creation transaction
    txn = AssetConfigTxn(
        sender=asset_creator_pk,
        sp=params,
        total=12,  # for the 12 weekly challenges
        default_frozen=False,
        unit_name="certificate",
        asset_name="10 Academy Weekly Challenge Certificate",
        manager=pk_of_acct_to_be_assigned,
        reserve=pk_of_acct_to_be_assigned,
        freeze=pk_of_acct_to_be_assigned,
        clawback=pk_of_acct_to_be_assigned,
        decimals=0)

    # sign with secret key of creator
    stxn = txn.sign(asset_creator_sk)

    # send transaction to network to receive transaction id
    txid = retrieve_txid(stxn)

    # get the new asset's information from the creator account
    try:
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, asset_creator_pk, asset_id)
        print_asset_holding(algod_client, asset_creator_pk, asset_id)
    except Exception as e:
        print(e)

    return asset_id


# fn to change manager of the asset (the certificate nft)
# arguments: asset_id, public key of current manager, private key of current manager, public key of future manager
# returns: transaction id
def change_manager(asset_id, curr_manager_pk, curr_manager_sk, future_manager_pk):
    params = algod_client.suggested_params()

    # curr manager issues asset config txt to assign new account as future manager
    txn = AssetConfigTxn(
        sender=curr_manager_pk,
        sp=params,
        index=asset_id,
        manager=future_manager_pk,
        reserve=curr_manager_pk,
        freeze=curr_manager_pk,
        clawback=curr_manager_pk)

    # sign by the current manager
    stxn = txn.sign(curr_manager_sk)

    # send transaction to network to receive transaction id
    txid = retrieve_txid(stxn)

    # Check asset info to view change in management. manager should now be "future manager"
    print_created_asset(algod_client, future_manager_pk, asset_id)

    return txid

# fn to opt-in/out of reveiving the asset (nft certificate)
# arguments: asset_id, public key of specific account, private key of specific account
# returns: transaction id


def opt_in(asset_id, specific_acct_pk, specific_acct_sk):

    # Check if asset_id is in specific acct's asset holdings prior to opt-in
    params = algod_client.suggested_params()
    account_info = algod_client.account_info(specific_acct_pk)
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
            sender=specific_acct_pk,
            sp=params,
            receiver=specific_acct_pk,
            amt=0,
            index=asset_id)
        stxn = txn.sign(specific_acct_sk)

        # send transaction to network to receive transaction id
        txid = retrieve_txid(stxn)

        # Now check the asset holding for the specific account.
        # This should now show a holding with a balance of 0.
        print_asset_holding(algod_client, specific_acct_pk, asset_id)

    return txid


# fn to transfer a singular unit of asset(nft certificate) from one acct to another
# arguments: asset id, sender public key, sender private key, receiver public key
# returns: transaction id
def transfer_asset(asset_id, sender_pk, sender_sk, receiver_pk):
    params = algod_client.suggested_params()

    txn = AssetTransferTxn(
        sender=sender_pk,
        sp=params,
        receiver=receiver_pk,
        amt=1,
        index=asset_id)

    stxn = txn.sign(sender_sk)

    # send transaction to network to receive transaction id
    txid = retrieve_txid(stxn)

    # the balance should now be 1. balance in receiver acct should be of 1 unit of the asset
    print_asset_holding(algod_client, receiver_pk, asset_id)

    return txid
