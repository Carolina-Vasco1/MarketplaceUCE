import sys
sys.path.insert(0, '/app')

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate hash for admin123
password = "admin123"
hashed = pwd_context.hash(password)
print(hashed)
