from algosdk import account, mnemonic
from algosdk.v2client import algod

# build transaction
from algosdk.future import transaction
from algosdk import constants

# to submit transaction + wait for confirmation
import json
import base64


def generate_algorand_keypair():
    private_key, public_key = account.generate_account()
    print("My address: {}".format(public_key))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))


# generate_algorand_keypair()  # commented out so as to only create one acct this time.

# account has been created. this account can be used on mainnet, testnet and on betanet
# acct balance will differ based on which network you're on, but we'll use the same acct for all networks

# use "address" to fund your account on the testnet faucet

# 3rd acct created (using sandbox testnet this time). here are its details. it's empty now
# My address: STXMMDRBVLRBN4TUTJDXQK6GWM322BPDVGVMZLYUSBU2LN6SZX3VM444RY
# My private key: D2UT1H7CqUEjxys/EKq8zmXt/S/2XaFJ68gs57MmMRaU7sYOIariFvJ0mkd4K8azN60F46mqzK8UkGmlt9LN9w==
# My passphrase: peanut eternal head child fatal spare decorate cloth among portion furnace friend suspect youth ramp fuel crouch pudding good index guitar endless ranch abandon review


# 2nd acct that i created. has 20 algos in it.
# My address: V4YIBC2Q4YMOY2V4KZ5WKZYUASZBCEHZLIFBVENW5JR4D5CDOMKCXQVL3Y
# My private key: OZhrTkDB1m6VGnh7piNbVXiSK8JnlQ+nBQd2scVcN6SvMICLUOYY7Gq8VntlZxQEshEQ+VoKGpG26mPB9ENzFA==
# My passphrase: already purpose cheese beef pulse forum start job sorry model pulse luxury ceiling memory dignity nice tiger bird adjust blast merge strong canvas absent rhythm


# the 1st acct i created. has 5 algos
# My address: B2KUFIJ7RGBHLOKHZLK2LV7HEPBF3MCWFGARU7I6ZLEBH4KVMXDS7BFWGU
# My private key: u/7dY70sUfe6/jOgmzDFIoQD1KdODtZkWJFgHdaj5GAOlUKhP4mCdblHytWl1+cjwl2wVimBGn0eysgT8VVlxw==
# My passphrase: student jewel rapid slim pelican saddle volume crop inject second glad drama alpha vital inside atom onion ghost emerge stock promote cigar already about canyon

def first_transaction_example(private_key, my_address):
    # creating the algod client with sandbox
    # algod_address depends on node client you use e.g. sandbox, purestake, etc
    # algod_address = "http://localhost:4001"
    # algod_address = "http://testnet-api.algonode.cloud/"

    # algod_token depends on node client you use. e.g. sandbox, purestake, etc
    # algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # algod_client = algod.AlgodClient(algod_token, algod_address)

    # dummyaddress = "https://testnet-api.algonode.cloud/"
    # dummytoken = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # algod_client = algod.AlgodClient(dummytoken, dummyaddress)
    # print(algod_client)

    # creating the algod client with a PureStake Key
    purestake_key = 'Im9YmvFb539Ejkc16dQ729IRpYu4FVf34MygRwsG'
    endpoint_address = 'https://testnet-algorand.api.purestake.io/ps2'
    purestake_header = {'X-Api-key': purestake_key}
    algod_client = algod.AlgodClient(
        purestake_key, endpoint_address, headers=purestake_header)

    # print(dummyaddress)
    # print(my_address)

    # to check your balance on algorand
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


# 2nd acct created.
# My address: V4YIBC2Q4YMOY2V4KZ5WKZYUASZBCEHZLIFBVENW5JR4D5CDOMKCXQVL3Y
# My private key: OZhrTkDB1m6VGnh7piNbVXiSK8JnlQ+nBQd2scVcN6SvMICLUOYY7Gq8VntlZxQEshEQ+VoKGpG26mPB9ENzFA==
# My passphrase: already purpose cheese beef pulse forum start job sorry model pulse luxury ceiling memory dignity nice tiger bird adjust blast merge strong canvas absent rhythm


pk = "OZhrTkDB1m6VGnh7piNbVXiSK8JnlQ+nBQd2scVcN6SvMICLUOYY7Gq8VntlZxQEshEQ+VoKGpG26mPB9ENzFA=="
addr = "V4YIBC2Q4YMOY2V4KZ5WKZYUASZBCEHZLIFBVENW5JR4D5CDOMKCXQVL3Y"
first_transaction_example(pk, addr)
