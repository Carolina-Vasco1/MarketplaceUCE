from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.security import hash_password, verify_password, create_access_token

MAX_BCRYPT_BYTES = 72


class UserService:
    @staticmethod
    def _validate_password(password: str):
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
            raise ValueError("La contraseña es demasiado larga (máx. 72 bytes). Usa una más corta.")

    @staticmethod
    async def register(session: AsyncSession, email: str, password: str, role: str):
        UserService._validate_password(password)

        q = text("SELECT id FROM users WHERE email = :email")
        r = await session.execute(q, {"email": email})
        if r.first():
            raise ValueError("El usuario ya existe")

        pw_hash = hash_password(password)

        ins = text("""
            INSERT INTO users (email, password_hash, role, is_active)
            VALUES (:email, :password_hash, :role, true)
            RETURNING id, role
        """)
        res = await session.execute(ins, {"email": email, "password_hash": pw_hash, "role": role})
        await session.commit()

        user_id, user_role = res.first()
        return create_access_token(sub=email, role=user_role, uid=user_id)

    @staticmethod
    async def login(session: AsyncSession, email: str, password: str):
        UserService._validate_password(password)

        q = text("""
            SELECT id, email, password_hash, role, is_active
            FROM users
            WHERE email = :email
        """)
        res = await session.execute(q, {"email": email})
        row = res.first()

        if not row:
            raise ValueError("Credenciales inválidas")

        user_id, user_email, pw_hash, role, is_active = row

        if not is_active:
            raise ValueError("Usuario inactivo")

        if not verify_password(password, pw_hash):
            raise ValueError("Credenciales inválidas")

        return create_access_token(sub=user_email, role=role, uid=user_id)
