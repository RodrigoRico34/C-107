from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Clé privée metamask
private_key = os.getenv("PRIVATE_KEY")

# Adresse Ethereum
deployer_address = "0x90565314833E596E57D744C6D26D174653eFf658"

# URL image
URI = "https://raw.githubusercontent.com/RodrigoRico34/C-107/refs/heads/main/ex_nft/metadata.json"

# Adresse du contrat déjà déployé sur la blockchain CPNV
contract_address = "0x9A8C8E2EB8F6fA1Bd7EF9161417F64E48bf54225"

#Connexion Ethereum Cpnv
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))
assert w3.is_connected(), "Echec de la connexion"

print(" Connecté au nœud Ethereum CPNV")

sender_address = w3.to_checksum_address(deployer_address)


# chargement du contrat

with open(r"SimpleMintContract.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

nft_contract = w3.eth.contract(address=contract_address, abi=contract_abi)


# vérifications avant mint

is_mint_enabled = nft_contract.functions.isMintEnabled().call()
total_supply    = nft_contract.functions.totalSupply().call()
max_supply      = nft_contract.functions.maxSupply().call()
already_minted  = nft_contract.functions.mintedWallets(sender_address).call()

print(f"Mint activé      : {is_mint_enabled}")
print(f"Supply actuelle  : {total_supply} / {max_supply}")
print(f"Déjà minté (toi) : {already_minted}")

if not is_mint_enabled:
    print(" Le mint n'est pas activé. Demandez au propriétaire du contrat d'appeler toggleIsMintEnabled().")
    exit()

if already_minted >= 1:
    print(" Tu as déjà minté 1 NFT avec ce portefeuille (max 1 par wallet).")
    exit()

if total_supply >= max_supply:
    print(" Le supply maximum est atteint, plus de NFT disponibles.")
    exit()

#mint NFT

valueEth = 0.05  # Prix fixé dans le contrat
nonce = w3.eth.get_transaction_count(sender_address)

mint_txn = nft_contract.functions.mint(URI).build_transaction({
    "chainId": 32383,                          # Chain ID du réseau CPNV
    "gas": 2000000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "value": w3.to_wei(valueEth, "ether"),     # 0.05 ETH requis par le contrat
    "nonce": nonce
})

signed_mint_txn = w3.eth.account.sign_transaction(mint_txn, private_key)

try:
    mint_tx_hash = w3.eth.send_raw_transaction(signed_mint_txn.raw_transaction)
    print(f"\n⏳ Transaction de mint envoyée : {mint_tx_hash.hex()}")

    mint_receipt = w3.eth.wait_for_transaction_receipt(mint_tx_hash)
    print(f" Mint confirmé dans le bloc {mint_receipt.blockNumber}")
    print(f"   Adresse du contrat : {mint_receipt.contractAddress or contract_address}")

except Exception as e:
    print(f" Erreur lors du mint : {str(e)}")
    exit()

# ============================================================
# VÉRIFICATION POST-MINT
# ============================================================

token_id = nft_contract.functions.totalSupply().call()
print(f"\n Token ID minté : {token_id}")

owner = nft_contract.functions.ownerOf(token_id).call()
print(f"   Propriétaire   : {owner}")

token_uri = nft_contract.functions.tokenURI(token_id).call()
print(f"   Metadata URI   : {token_uri}")