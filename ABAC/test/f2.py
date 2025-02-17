import json
from web3 import Web3

# 🏦 Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# 🔍 Check if connected
if not w3.is_connected():
    print("[ERROR] Failed to connect to Ganache ❌")
    exit()
print("[SUCCESS] Connected to Ganache ✅\n")

# 📜 Load Deployed Contract Addresses
with open('deployed_addresses.json', 'r') as f:
    deployed_addresses = json.load(f)

# Validate Contract Addresses
required_contracts = ["ABAC", "PolicyManagement", "SubjectAttributes", "AddressLister"]
for contract in required_contracts:
    if contract not in deployed_addresses:
        print(f"[ERROR] {contract} contract not found in deployed addresses!")
        exit()

# Load Contract ABIs
def load_abi(contract_name):
    abi_path = f"compiled_ABIs/{contract_name}.json"
    try:
        with open(abi_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] ABI file {abi_path} not found! Ensure you re-run deployment.")
        exit()

# Load Contracts
ABAC_CONTRACT = w3.eth.contract(address=deployed_addresses["ABAC"], abi=load_abi("ABAC"))
POLICY_CONTRACT = w3.eth.contract(address=deployed_addresses["PolicyManagement"], abi=load_abi("PolicyManagement"))
SUBJECT_CONTRACT = w3.eth.contract(address=deployed_addresses["SubjectAttributes"], abi=load_abi("SubjectAttributes"))

# 🏦 Use the first account from Ganache as the admin
admin_account = w3.eth.accounts[0]
user_account = w3.eth.accounts[1]  # Regular user
policy_admin = w3.eth.accounts[2]  # Policy admin

# ======================== 🧪 TEST FUNCTIONS ========================

# 🛠 Test 1: Register a User in SubjectAttributes.sol
def test_register_user():
    try:
        print(f"[INFO] Registering user {user_account} in SubjectAttributes...")
        tx_hash = SUBJECT_CONTRACT.functions.CreateUser(user_account, "Manager", 3).transact({'from': admin_account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("[SUCCESS] User registered in SubjectAttributes ✅")
    except Exception as e:
        print(f"[ERROR] Failed to register user: {e}")

# 🛠 Test 2: Retrieve User Attributes
def test_get_user_attributes():
    try:
        print(f"[INFO] Fetching user attributes from SubjectAttributes...")
        user_data = SUBJECT_CONTRACT.functions.users(user_account).call()
        print(f"[DATA] User Role: {user_data[0]}, Clearance Level: {user_data[1]}, Active: {user_data[2]}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch user attributes: {e}")

# 🛠 Test 3: Modify User Role
def test_change_user_role():
    try:
        print(f"[INFO] Changing role of {user_account} to 'Admin'...")
        tx_hash = SUBJECT_CONTRACT.functions.ChangeUserRoles(user_account, "Admin").transact({'from': admin_account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("[SUCCESS] User role updated ✅")
    except Exception as e:
        print(f"[ERROR] Failed to change user role: {e}")

# 🛠 Test 4: Deactivate User
def test_deactivate_user():
    try:
        print(f"[INFO] Deactivating user {user_account}...")
        tx_hash = SUBJECT_CONTRACT.functions.DeactiveUser(user_account).transact({'from': admin_account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("[SUCCESS] User deactivated ✅")
    except Exception as e:
        print(f"[ERROR] Failed to deactivate user: {e}")

# 🛠 Test 5: Grant Policy Admin
def test_grant_policy_admin():
    try:
        print(f"[INFO] Granting policy admin rights to {policy_admin}...")
        tx_hash = POLICY_CONTRACT.functions.GrantPolicyAdmin(policy_admin).transact({'from': admin_account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("[SUCCESS] Policy admin granted ✅")
    except Exception as e:
        print(f"[ERROR] Failed to grant policy admin: {e}")

# 🛠 Test 6: Create a Policy
def test_create_policy():
    try:
        print("[INFO] Creating a new access policy in PolicyManagement...")
        condition = ("user", "role", "==", "Manager")  # Policy condition: "Manager" role required
        tx_hash = POLICY_CONTRACT.functions.CreatePolicy("Policy1", "Admin Resource", [condition]).transact({'from': policy_admin})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("[SUCCESS] Policy created ✅")
    except Exception as e:
        print(f"[ERROR] Failed to create policy: {e}")

# 🛠 Test 7: Retrieve Policies
def test_get_policies():
    try:
        print("[INFO] Fetching active policies from PolicyManagement...")
        policies = POLICY_CONTRACT.functions.GetAllPolicies().call()
        print(f"[DATA] Active Policies: {policies}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch policies: {e}")

# 🛠 Test 8: Check Access Control in ABAC
def test_check_access():
    try:
        print(f"[INFO] Checking access for {user_account} on 'Admin Resource'...")
        access_granted = ABAC_CONTRACT.functions.checkAccess(user_account, "Admin Resource").call()
        if access_granted:
            print("[ACCESS GRANTED] ✅ User has access!")
        else:
            print("[ACCESS DENIED] ❌ User does not have access.")
    except Exception as e:
        print(f"[ERROR] Failed to check access: {e}")

# ======================== 🏁 RUN ALL TESTS ========================
if __name__ == "__main__":
    test_register_user()  # ✅ Register a user
    test_get_user_attributes()  # ✅ Retrieve attributes
    test_change_user_role()  # ✅ Modify user role
    test_deactivate_user()  # ✅ Deactivate user
    test_grant_policy_admin()  # ✅ Grant policy admin
    test_create_policy()  # ✅ Create a policy
    test_get_policies()  # ✅ Retrieve policies
    test_check_access()  # ✅ Check access control
