import os
import datetime as dt
import requests
from src.account import Account
from datetime import date
from smtp.smtp import SMTPClient

class BusinessAccount(Account):
    history_email_text_template = "Company account history: {}"
    def __init__(self, company_name=None, nip=None):
        self.company_name = company_name
        self.nip = nip if self.nip_is_valid(nip) else "Invalid"
        self.balance = 0.0
        self.history = []
        if isinstance(self.nip, str) and len(self.nip) == 10:
            ok = self.verify_nip_with_mf(self.nip)
            if not ok:
                raise ValueError("Company not registered!!")

    def nip_is_valid(self, nip):
        return nip is not None and len(nip) == 10 and nip.isdigit()

    def receive_transfer(self, amount):
        if isinstance(amount, (int, float)) and amount > 0:
            self.balance += float(amount)
            self.history.append(float(amount))
            return True
        return False

    def send_transfer(self, amount):
        if isinstance(amount, (int, float)) and 0 < amount <= self.balance:
            self.balance -= float(amount)
            self.history.append(-float(amount))
            return True
        return False

    def get_express_fee(self):
        return 5.0

    def take_loan(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        if self.balance < 2 * float(amount):
            return False
        if -1775 not in self.history:
            return False
        self.balance += float(amount)
        return True
    
    def verify_nip_with_mf(self, nip: str) -> bool:
        base = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl").rstrip("/")
        date = dt.date.today().isoformat()  
        url = f"{base}/api/search/nip/{nip}?date={date}"
        try:
            resp = requests.get(url, timeout=5)
            try:
                data = resp.json()
            except Exception:
                data = {"raw": resp.text}
            print(f"[MF] GET {url} -> {resp.status_code} {data}")
            if resp.status_code != 200:
                return False
            result = (data.get("result") or {})
            subject = (result.get("subject") or {})
            return subject.get("statusVat") == "Czynny"
        except Exception as e:
            print(f"[MF] request error: {e}")
            return False

    def send_history_via_email(self, email_address: str) -> bool:
        today_date = date.today().strftime("%Y-%m-%d")
        subject = "Account Transfer History "+ today_date
        text = self.history_email_text_template.format(self.history)
        return SMTPClient.send(subject, text, email_address)