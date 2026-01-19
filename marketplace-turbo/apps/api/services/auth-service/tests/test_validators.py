import pytest
from app.core.validators import validate_institutional_email

def test_email_domain_ok():
    validate_institutional_email("test@uce.edu.ec")

def test_email_domain_fail():
    with pytest.raises(ValueError):
        validate_institutional_email("test@gmail.com")
