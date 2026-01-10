def validate_institutional_email(email: str) -> None:
    email = (email or "").strip().lower()
    if not email.endswith("@uce.edu.ec"):
        raise ValueError("Solo se permiten correos institucionales @uce.edu.ec")
