from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.utils.helpers import get_current_username
from app.core.memory import get_memory

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/{account_id}", response_model=List[dict])
async def get_transactions(account_id: str, username: str = Depends(get_current_username)):
    mem = get_memory()
    async with mem.lock:
        acct = mem.accounts.get(account_id)
        if not acct:
            raise HTTPException(status_code=404, detail="Account not found")
        if acct["owner"] != username:
            raise HTTPException(status_code=403, detail="Not allowed to view transactions for this account")
        results = []
        for tx in mem.transactions:
            if tx.get("from_account") == account_id or tx.get("to_account") == account_id:
                results.append(tx)
    return results
