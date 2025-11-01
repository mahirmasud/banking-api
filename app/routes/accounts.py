from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import AccountCreate, AccountOut, DepositIn, WithdrawIn, TransferIn
from app.utils.helpers import get_current_username
from app.core.memory import get_memory
from datetime import datetime

router = APIRouter(prefix="/account", tags=["accounts"])

@router.post("/create", response_model=AccountOut)
async def create_account(payload: AccountCreate, username: str = Depends(get_current_username)):
    mem = get_memory()
    async with mem.lock:
        account_id = mem.next_account_id()
        now = datetime.utcnow()
        initial = float(payload.initial_deposit or 0.0)
        mem.accounts[account_id] = {
            "account_id": account_id,
            "owner": username,
            "account_type": payload.account_type,
            "balance": initial,
            "created_at": now.isoformat()
        }
        if initial > 0:
            tx = {
                "tx_id": mem.next_tx_id(),
                "type": "deposit",
                "amount": initial,
                "from_account": None,
                "to_account": account_id,
                "timestamp": now.isoformat(),
                "description": "initial_deposit",
                "balance_after": initial,
            }
            mem.transactions.append(tx)
    acct = mem.accounts[account_id]
    return {
        "account_id": acct["account_id"],
        "owner": acct["owner"],
        "account_type": acct["account_type"],
        "balance": acct["balance"],
        "created_at": acct["created_at"]
    }

@router.get("/{account_id}", response_model=AccountOut)
async def get_account(account_id: str, username: str = Depends(get_current_username)):
    mem = get_memory()
    async with mem.lock:
        acct = mem.accounts.get(account_id)
        if not acct:
            raise HTTPException(status_code=404, detail="Account not found")
        if acct["owner"] != username:
            raise HTTPException(status_code=403, detail="Not allowed to view this account")
    return {
        "account_id": acct["account_id"],
        "owner": acct["owner"],
        "account_type": acct["account_type"],
        "balance": acct["balance"],
        "created_at": acct["created_at"]
    }

@router.post("/deposit", response_model=dict)
async def deposit(payload: DepositIn, username: str = Depends(get_current_username)):
    mem = get_memory()
    async with mem.lock:
        acct = mem.accounts.get(payload.account_id)
        if not acct:
            raise HTTPException(status_code=404, detail="Account not found")
        if acct["owner"] != username:
            raise HTTPException(status_code=403, detail="Not allowed to deposit into this account")
        acct["balance"] = round(acct["balance"] + float(payload.amount), 2)
        tx = {
            "tx_id": mem.next_tx_id(),
            "type": "deposit",
            "amount": float(payload.amount),
            "from_account": None,
            "to_account": payload.account_id,
            "timestamp": datetime.utcnow().isoformat(),
            "description": payload.description,
            "balance_after": acct["balance"]
        }
        mem.transactions.append(tx)
    return tx

@router.post("/withdraw", response_model=dict)
async def withdraw(payload: WithdrawIn, username: str = Depends(get_current_username)):
    mem = get_memory()
    async with mem.lock:
        acct = mem.accounts.get(payload.account_id)
        if not acct:
            raise HTTPException(status_code=404, detail="Account not found")
        if acct["owner"] != username:
            raise HTTPException(status_code=403, detail="Not allowed to withdraw from this account")
        amount = float(payload.amount)
        if acct["balance"] < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        acct["balance"] = round(acct["balance"] - amount, 2)
        tx = {
            "tx_id": mem.next_tx_id(),
            "type": "withdraw",
            "amount": amount,
            "from_account": payload.account_id,
            "to_account": None,
            "timestamp": datetime.utcnow().isoformat(),
            "description": payload.description,
            "balance_after": acct["balance"]
        }
        mem.transactions.append(tx)
    return tx

@router.post("/transfer", response_model=dict)
async def transfer(payload: TransferIn, username: str = Depends(get_current_username)):
    mem = get_memory()
    async with mem.lock:
        from_acct = mem.accounts.get(payload.from_account_id)
        to_acct = mem.accounts.get(payload.to_account_id)
        if not from_acct or not to_acct:
            raise HTTPException(status_code=404, detail="One or both accounts not found")
        if from_acct["owner"] != username:
            raise HTTPException(status_code=403, detail="Not allowed to transfer from this account")
        amount = float(payload.amount)
        if from_acct["balance"] < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        from_acct["balance"] = round(from_acct["balance"] - amount, 2)
        to_acct["balance"] = round(to_acct["balance"] + amount, 2)
        tx = {
            "tx_id": mem.next_tx_id(),
            "type": "transfer",
            "amount": amount,
            "from_account": payload.from_account_id,
            "to_account": payload.to_account_id,
            "timestamp": datetime.utcnow().isoformat(),
            "description": payload.description,
            "balance_after": from_acct["balance"]
        }
        mem.transactions.append(tx)
    return tx
