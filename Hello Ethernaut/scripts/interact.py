# scripts/interact.py
from ape import accounts, Contract, networks
import json

def main():
    account = accounts.load("metamask")
    print(f"[+] Using account: {account.address}")

    CONTRACT_ADDRESS = "0x9b6A44b824D92964713924db10111842CFfB74DB"

    with open("abis/hello_ether.json", "r") as f:
        abi = json.load(f)
    print("[+] ABI loaded")

    with networks.ethereum.sepolia.use_provider("alchemy") as provider:
        print(f"[+] Connected via Alchemy: {provider.network.name}")


        w3 = provider.web3
        print(f"[+] {provider.network.name} connected:", w3.is_connected())

        print("[+] Latest block:", w3.eth.block_number)

        balance = w3.eth.get_balance(account.address)
        print("[+] Balance (ETH):", w3.from_wei(balance, 'ether'))

        try:
            contract = Contract(
                address=CONTRACT_ADDRESS,
                abi=abi,
                contract_type=None
            )
            print(f"[+] Connected to contract: {contract.address}")
        except Exception as e:
            print(f"[-] Failed to create contract: {e}")
            return
    try:
        password = contract.password()
        print(f"[+] Password: {password}")
    except Exception as e:
        print(f"[-] Call failed: {e}")
        return
    
    # Submit password
    try:
        print(f"[+] Submitting password: {password}")
        tx = contract.authenticate(password, sender=account)
        print(f"[+] Success! Tx: {tx.txn_hash}")
    except Exception as e:
        print(f"[-] Authenticate failed: {e}")
        return

    # Check cleared
    try:
        cleared = contract.getCleared()
        print(f"[+] Cleared: {cleared}")
    except Exception as e:
        print(f"[-] Could not check cleared: {e}")