class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        if not hasattr(account, "pesel"):
            raise TypeError("Only personal accounts can be added")
        if self.find_by_pesel(account.pesel):
            return False
        self.accounts.append(account)
        return True

    def find_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def all_accounts(self):
        return list(self.accounts)

    def count(self):
        return len(self.accounts)

    def remove_by_pesel(self, pesel: str) -> bool:
        acc = self.find_by_pesel(pesel)
        if not acc:
            return False
        self.accounts.remove(acc)
        return True
