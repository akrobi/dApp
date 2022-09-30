from algosdk import account, mnemonic
from algosdk.v2client import algod

# build transaction
from algosdk.future import transaction
from algosdk import constants

# to submit transaction + wait for confirmation
import json
import base64


def generate_algorand_keypair():
    private_key, my_address = account.generate_account()
    print("My address: {}".format(my_address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))


# generate_algorand_keypair()

# account has been created. this account can be used on mainnet, testnet and on betanet
# acct balance will differ based on which network you're on, but we'll use the same acct for all networks

# use "address" to fund your account on the testnet faucet


def first_transaction_example(private_key, my_address):
    # creating the algod client with sandbox
    # # algod_address depends on node client you use e.g. sandbox, purestake, etc
    # algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    # # algod_token depends on node client you use. e.g. sandbox, purestake, etc
    # algod_token = "Im9YmvFb539Ejkc16dQ729IRpYu4FVf34MygRwsG"
    # algod_client = algod.AlgodClient(algod_token, algod_address)

    # creating the algod client with a PureStake Key
    purestake_key = 'Im9YmvFb539Ejkc16dQ729IRpYu4FVf34MygRwsG'
    endpoint_address = 'https://testnet-algorand.api.purestake.io/ps1'
    purestake_header = {'X-Api-key': purestake_key}
    algod_client = algod.AlgodClient(
        purestake_key, endpoint_address, headers=purestake_header)

    # to check your balance
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(
        account_info.get('amount')) + "\n")

    # to build the transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE  # params.fee is 1000 in the video
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    note = "Hello World".encode()
    amount = 1000000

    unsigned_txn = transaction.PaymentTxn(
        my_address, params, receiver, amount, None, note)

    # sign transaction. note that there are many ways of signing transactions. details on dev portal
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    # usually takes 4-5 seconds on the algorand network
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(
        account_info.get('amount')))
    print("Amount transfered: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))

    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(
        account_info.get('amount')) + "\n")


first_transaction_example("u/7dY70sUfe6/jOgmzDFIoQD1KdODtZkWJFgHdaj5GAOlUKhP4mCdblHytWl1+cjwl2wVimBGn0eysgT8VVlxw==",
                          "B2KUFIJ7RGBHLOKHZLK2LV7HEPBF3MCWFGARU7I6ZLEBH4KVMXDS7BFWGU")
