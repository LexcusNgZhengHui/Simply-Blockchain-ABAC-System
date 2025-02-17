import json
from web3 import Web3
from solcx import compile_standard, install_solc
from web3.middleware import geth_poa_middleware

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
assert w3.is_connected(), "Ganache connection failed!"

# Set account (use a Ganache private key)
private_key = "0xa1290a55c286f1f174e1891df818922cc6a928b562b267e96f65f3e325332233"  # Replace with your Ganache account private key
account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address

# Load compiled contract ABI and address (replace with your values)
contract_address = "0x29006e70481b47d9264B2E45E85e58C52b5eE079"
abi = [...]  # Paste the ABI from compilation (e.g., from Remix or solcx output)

# Initialize contract instance
abac = w3.eth.contract(address=contract_address, abi=abi)

# --------------------------
# Test Case 1: Basic Setup
# --------------------------
def test_admin_setup():
    # Verify the deployer is the admin
    admin = abac.functions.admin().call()
    assert admin == account.address, "Admin setup failed!"
    print("✅ Admin setup correct")

# --------------------------
# Test Case 2: User Attributes
# --------------------------
def test_user_attributes():
    # Set user attributes
    tx = abac.functions.setUserAttributes(
        account.address,  # User address
        "admin",          # Role
        "finance",        # Department
        3                 # Clearance level
    ).build_transaction({
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(account.address)
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # Check user attributes
    user = abac.functions.users(account.address).call()
    assert user[0] == "admin", "User role not set!"
    print("✅ User attributes set correctly")

# --------------------------
# Test Case 3: Resource Setup
# --------------------------
def test_resource_setup():
    # Define a resource
    tx = abac.functions.setResourceAttributes(
        "RESOURCE_1",     # Resource ID
        "medical_record", # Asset type
        2                 # Sensitivity level
    ).build_transaction({
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(account.address)
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # Check resource attributes
    resource = abac.functions.resources("RESOURCE_1").call()
    assert resource[1] == 2, "Resource sensitivity level not set!"
    print("✅ Resource setup correct")

# --------------------------
# Test Case 4: Policy Creation
# --------------------------
def test_policy_creation():
    # Grant policy admin role
    tx = abac.functions.grantPolicyAdmin(account.address).build_transaction({
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(account.address)
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # Create a policy
    conditions = [
        ("user", "role", "==", "admin"),
        ("resource", "sensitivityLevel", ">=", "2")
    ]
    condition_structs = [
        {"attributeType": c[0], "attributeName": c[1], "operator": c[2], "value": c[3]}
        for c in conditions
    ]

    tx = abac.functions.createPolicy(
        "POLICY_1",
        "Admin access to high-sensitivity resources",
        condition_structs
    ).build_transaction({
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(account.address)
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # Check policy existence
    policy = abac.functions.policies("POLICY_1").call()
    assert policy[0] == "POLICY_1", "Policy creation failed!"
    print("✅ Policy created successfully")

# --------------------------
# Test Case 5: Access Control Check
# --------------------------
def test_access_control():
    # Check access (should return True)
    has_access = abac.functions.checkAccess(
        account.address,
        "RESOURCE_1"
    ).call()
    assert has_access, "Access check failed for valid policy!"
    print("✅ Access granted for valid user/resource")

    # Test a denied scenario (e.g., non-admin user)
    # Create a new user (non-admin)
    non_admin_address = "0xAnotherGanacheAddress"
    try:
        has_access = abac.functions.checkAccess(
            non_admin_address,
            "RESOURCE_1"
        ).call()
        assert not has_access, "Access should be denied!"
        print("✅ Access denied for invalid user")
    except Exception as e:
        print(f"❌ Error: {e}")

# --------------------------
# Run All Tests
# --------------------------
if __name__ == "__main__":
    test_admin_setup()
    test_user_attributes()
    test_resource_setup()
    test_policy_creation()
    test_access_control()