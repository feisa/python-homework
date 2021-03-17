
import subprocess
import json
import os
from constants import *
from dotenv import load_dotenv
from bit import Key, PrivateKey, PrivateKeyTestnet
from bit.network import NetworkAPI, satoshi_to_currency
from web3 import Web3
from eth_account import Account

load_dotenv()
mnemonic = os.getenv('MNEMONIC')

def derive_wallets(mnemonic,coin,numderive):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --coin="{coin}" --numderive="{numderive}" --format=json'
    p = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    (output, err) = p.communicate()
    return json.loads(output)

coins = {
            'eth':derive_wallets(mnemonic=mnemonic,coin=ETH,numderive=3),
            'btc-test': derive_wallets(mnemonic=mnemonic,coin=BTCTEST,numderive=3)
        }

eth_coin = coins['eth'][0]['privkey']
btc_coin = coins['btc-test'][0]['privkey']

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        print(Account.privateKeyToAccount(priv_key))
        return Account.privateKeyToAccount(priv_key)
    else:
        print(PrivateKeyTestnet(priv_key))
        return PrivateKeyTestnet(priv_key)
    
eth_account = priv_key_to_account(ETH,eth_coin)
btc_account = priv_key_to_account(BTCTEST,btc_coin)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def create_tx(coin,account,recipient,amount):
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
    else:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])    
    
def send_tx(coin,account, recipient, amount):
    if coin =='eth':
        tx = create_tx(coin,account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    else:
        tx_data= create_tx(coin,account,recipient,amount)
        tx_hex = account.sign_transaction(tx_data)
        NetworkAPI.broadcast_tx_testnet(tx_hex)       
        return tx_hex


