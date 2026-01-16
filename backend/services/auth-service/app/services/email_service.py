import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

class EmailService:
    def send_otp(self, to_email: str, code: str) -> None:
        # DEV MODE
        if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            print(f"[DEV OTP] Enviar OTP a {to_email}: {code}")
            return

        msg = MIMEText(
            f"Tu código OTP es: {code}\nExpira en {settings.OTP_TTL_SECONDS//60} minutos."
        )
        msg["Subject"] = "OTP - Marketplace UCE"
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email

        try:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"[SMTP OK] OTP enviado a {to_email}")
        except Exception as e:
            print(f"[SMTP ERROR] No se pudo enviar OTP a {to_email}: {e}")
            raise
