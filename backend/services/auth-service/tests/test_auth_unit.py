from app.core.security import hash_password, verify_password

def test_hash_and_verify():
    h = hash_password("Password123!")
    assert verify_password("Password123!", h)
    assert not verify_password("wrong", h)
