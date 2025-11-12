from src.account import Account


class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        super().__init__(first_name="", last_name="", pesel=None, promocode=None)
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"    

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and nip.isdigit() and len(nip) == 10:
            return True
        return False

    def get_express_fee(self):
        return 5.0