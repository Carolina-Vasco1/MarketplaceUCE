import sys
sys.path.insert(0, '/app')

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "admin123"
hashed = pwd_context.hash(password)
print(hashed)
