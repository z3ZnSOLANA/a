from tkinter import messagebox
import base58
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.pubkey import Pubkey

def get_wallet_from_private_key_bs58(private_key_bs58: str) -> Keypair:
    private_key_bytes = base58.b58decode(private_key_bs58)
    wallet = Keypair.from_bytes(private_key_bytes)
    return wallet

def check_sol_balance(public_key_str: str) -> float:
    solana_client = Client("https://api.mainnet-beta.solana.com")
    public_key = Pubkey.from_string(public_key_str)
    balance_response = solana_client.get_balance(public_key)
    
    # Adjusted line to use the correct attribute access method
    sol_balance = balance_response.value / 1e9
    
    return sol_balance

def check_wsol_balance(public_key_str: str) -> float:
    solana_client = Client("https://api.mainnet-beta.solana.com")
    public_key = Pubkey.from_string(public_key_str)
    wsol_balance_response = solana_client.get_token_account_balance(public_key)
    
    # Adjusted line to use the correct attribute access method
    wsol_balance = wsol_balance_response.value.amount / 1e9
    
    return wsol_balance
