import json
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future.transaction import *

# [TODO] Keep it as private in practice
private_key = "xAZp8u5vALq0+a8fpNotkR694mkW5YOFwLbG8bHMyqY9IBHOcBYtWRsIHjoyiQbkRJGc1OH10/KkXb5cIFQsig=="
public_key = "HUQBDTTQCYWVSGYIDY5DFCIG4RCJDHGU4H25H4VELW7FYICUFSFG255KCQ"
mnemonic_value = mnemonic.from_private_key(private_key)

algod_address = "https://testnet-api.algonode.cloud"
# token can be any value with the above address
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
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

# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()
params.flat_fee = constants.MIN_TXN_FEE
params.fee = 1000
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True

txn = AssetConfigTxn(
    sender=public_key,
    sp=params,
    total=1,
    default_frozen=False,
    unit_name="GLD",
    asset_name="Guild NFT#3",
    manager=public_key,
    reserve=public_key,
    freeze=public_key,
    clawback=public_key,
    url="https://path/to/my/asset/details", 
    decimals=0)
# Sign with secret key of creator
stxn = txn.sign(private_key)

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction ID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("Confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)


try:
    # Get new asset's information
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print("Created asset ID: {}".format(asset_id))
    print_created_asset(algod_client, public_key, asset_id)
    print_asset_holding(algod_client, public_key, asset_id)
except Exception as e:
    print(e)
