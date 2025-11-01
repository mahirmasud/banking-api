import asyncio
import uuid

class BankMemory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BankMemory, cls).__new__(cls)
            cls._instance.users = {}          # username -> {password_hash, full_name, created_at}
            cls._instance.accounts = {}       # account_id -> {owner, account_type, balance, created_at}
            cls._instance.transactions = []   # list of tx dicts
            cls._instance.lock = asyncio.Lock()
        return cls._instance

    def next_tx_id(self) -> str:
        return uuid.uuid4().hex

    def next_account_id(self) -> str:
        return uuid.uuid4().hex[:12]

def get_memory() -> BankMemory:
    return BankMemory()
