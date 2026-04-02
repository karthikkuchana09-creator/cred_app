import os
import random
from datetime import datetime
from pathlib import Path
from typing import Optional

import MySQLdb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, condecimal, constr

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

app = FastAPI(title="Credit Card Payment Service")

DB_HOST = os.getenv('DATABASE_HOST')
DB_PORT = int(os.getenv('DATABASE_PORT'))
DB_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('DATABASE_USER')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PaymentRequest(BaseModel):
    user_email: constr(strip_whitespace=True, min_length=4)
    card_last4: constr(min_length=4, max_length=4)
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)


class PaymentResponse(BaseModel):
    status: str
    transaction_id: int
    amount: float
    processed_at: datetime


def get_db_connection():
    return MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, charset='utf8mb4')


@app.post('/payments', response_model=PaymentResponse)
def make_payment(payload: PaymentRequest):
    status = random.choices(['SUCCESS', 'FAILED'], weights=[0.8, 0.2])[0]
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users_user WHERE email=%s", (payload.user_email,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail='User not found')
        user_id = row[0]

        cursor.execute("SELECT id FROM users_card WHERE user_id=%s AND last4=%s", (user_id, payload.card_last4))
        card_row = cursor.fetchone()
        if not card_row:
            raise HTTPException(status_code=404, detail='Card not found')
        card_id = card_row[0]

        cursor.execute(
            "INSERT INTO users_transaction (user_id, card_id, amount, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, card_id, payload.amount, 'PENDING', datetime.utcnow(), datetime.utcnow())
        )
        trans_id = cursor.lastrowid
        conn.commit()

        final_status = status
        cursor.execute("UPDATE users_transaction SET status=%s, updated_at=%s WHERE id=%s", (final_status, datetime.utcnow(), trans_id))
        conn.commit()

        return PaymentResponse(status=final_status, transaction_id=trans_id, amount=float(payload.amount), processed_at=datetime.utcnow())

    except MySQLdb.Error as e:
        raise HTTPException(status_code=500, detail=f'Database error: {e}')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.get('/health')
def health():
    return {'status': 'ok'}
