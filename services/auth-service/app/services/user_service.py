from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.security import hash_password, verify_password, create_access_token

MAX_BCRYPT_BYTES = 72


class UserService:
    @staticmethod
    def _check_bcrypt_limit(password: str):
        # bcrypt límite: 72 bytes (NO caracteres)
        if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
            raise ValueError(
                "La contraseña es demasiado larga (máx. 72 bytes). "
                "Evita emojis o textos muy largos."
            )

    @staticmethod
    def _validate_register_password(password: str):
        
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        UserService._check_bcrypt_limit(password)

    @staticmethod
    async def register(session: AsyncSession, email: str, password: str, role: str):
        UserService._validate_register_password(password)

     
        q = text("SELECT id FROM users WHERE email = :email")
        r = await session.execute(q, {"email": email})
        if r.first():
            raise ValueError("El usuario ya existe")

        pw_hash = hash_password(password)

        
        ins = text("""
            INSERT INTO users (email, hashed_password, role, is_active)
            VALUES (:email, :hashed_password, :role, true)
            RETURNING id, role
        """)
        res = await session.execute(
            ins,
            {"email": email, "hashed_password": pw_hash, "role": role}
        )
        await session.commit()

        user_id, user_role = res.first()
        return create_access_token({"sub": email, "role": user_role, "uid": user_id})

    @staticmethod
    async def login(session: AsyncSession, email: str, password: str):
        
        UserService._check_bcrypt_limit(password)

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

        return create_access_token({"sub": user_email, "role": role, "uid": user_id})
