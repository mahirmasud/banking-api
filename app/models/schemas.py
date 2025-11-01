from typing import Optional, List
from pydantic import BaseModel, Field, PositiveFloat
from datetime import datetime

# AUTH
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    username: str
    password: str

# ACCOUNT
class AccountCreate(BaseModel):
    account_type: Optional[str] = "checking"  # savings/checking
    initial_deposit: Optional[PositiveFloat] = 0.0

class AccountOut(BaseModel):
    account_id: str
    owner: str
    account_type: str
    balance: float
    created_at: datetime

# TRANSACTIONS
class TransactionBase(BaseModel):
    amount: PositiveFloat
    description: Optional[str] = None

class DepositIn(TransactionBase):
    account_id: str

class WithdrawIn(TransactionBase):
    account_id: str

class TransferIn(TransactionBase):
    from_account_id: str
    to_account_id: str

class TransactionOut(BaseModel):
    tx_id: str
    type: str
    amount: float
    from_account: Optional[str] = None
    to_account: Optional[str] = None
    timestamp: datetime
    description: Optional[str] = None
    balance_after: Optional[float] = None
