import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate_any_email(email: str) -> None:
    email = (email or "").strip().lower()
    if not EMAIL_RE.match(email):
        raise ValueError("Correo inválido")
