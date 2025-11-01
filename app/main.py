from fastapi import FastAPI, Request
import time
from app.routes import auth, accounts, transactions
from app.core.memory import get_memory
from app.core.security import hash_password
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="In-Memory Banking API")

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = (time.time() - start) * 1000
        print(f"{request.method} {request.url.path} completed in {duration_ms:.2f}ms")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    mem = get_memory()
    async with mem.lock:
        if not mem.users:
            mem.users["alice"] = {
                "password_hash": hash_password("alicepass"),
                "full_name": "Alice Example",
                "created_at": "startup"
            }
            mem.users["bob"] = {
                "password_hash": hash_password("bobpass"),
                "full_name": "Bob Example",
                "created_at": "startup"
            }
        if not mem.accounts:
            acct1 = mem.next_account_id()
            acct2 = mem.next_account_id()
            mem.accounts[acct1] = {
                "account_id": acct1,
                "owner": "alice",
                "account_type": "checking",
                "balance": 1000.0,
                "created_at": "startup"
            }
            mem.accounts[acct2] = {
                "account_id": acct2,
                "owner": "bob",
                "account_type": "savings",
                "balance": 500.0,
                "created_at": "startup"
            }
            now = time_string()
            mem.transactions.append({
                "tx_id": mem.next_tx_id(),
                "type": "deposit",
                "amount": 1000.0,
                "from_account": None,
                "to_account": acct1,
                "timestamp": now,
                "description": "seed deposit",
                "balance_after": mem.accounts[acct1]["balance"]
            })
            mem.transactions.append({
                "tx_id": mem.next_tx_id(),
                "type": "deposit",
                "amount": 500.0,
                "from_account": None,
                "to_account": acct2,
                "timestamp": now,
                "description": "seed deposit",
                "balance_after": mem.accounts[acct2]["balance"]
            })

def time_string():
    from datetime import datetime
    return datetime.utcnow().isoformat()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
