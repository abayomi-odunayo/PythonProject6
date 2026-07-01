from database import get_db_connection


def get_wallet_balance(user_id):
    conn = get_db_connection()

    wallet = conn.execute(
        "SELECT balance FROM wallets WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if wallet:
        return wallet["balance"]

    return 0


def update_wallet_balance(user_id, amount):
    conn = get_db_connection()

    conn.execute(
        "UPDATE wallets SET balance = balance + ? WHERE user_id = ?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()