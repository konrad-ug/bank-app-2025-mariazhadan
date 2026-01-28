from src.account import Account


class CompanyAccount(Account):
    def __init__(self, company_name=None, nip=None):
        self.company_name = company_name
        self.nip = nip if self.nip_is_valid(nip) else "Invalid"
        self.balance = 0.0
        self.history = []

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