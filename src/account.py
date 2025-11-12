class Account:
    def __init__(self, first_name, last_name, pesel, promocode=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel if self.pesel_is_valid(pesel) else "Invalid"
        
        # Give bonus if promo code is valid
        if promocode is not None and self.promocode_is_valid(promocode):
            self.balance += 50

    def pesel_is_valid(self, pesel):
        return pesel is not None and len(pesel) == 11 and pesel.isdigit()

    def promocode_is_valid(self, promocode):
        if not isinstance(promocode, str):
            return False
        if promocode.startswith("PROM_") and len(promocode) > 5:
            suffix = promocode[5:]
            return not suffix.isdigit()
        return False

    def extract_birth_year(self, pesel):
        if not self.pesel_is_valid(pesel):
            return None

        year = int(pesel[0:2])
        month = int(pesel[2:4])

        if 1 <= month <= 12:
            century = 1900
        elif 21 <= month <= 32:
            century = 2000
            month -= 20
        elif 41 <= month <= 52:
            century = 2100
            month -= 40
        elif 61 <= month <= 72:
            century = 2200
            month -= 60
        elif 81 <= month <= 92:
            century = 1800
            month -= 80
        else:
            return None
        return century + year

    def is_eligible_for_promo(self, pesel):
        year = self.extract_birth_year(pesel)
        return year is not None and year > 1960

    def receive_transfer(self, amount):
        if isinstance(amount, (int, float)) and amount > 0:
            self.balance += float(amount)
            return True
        return False
    def send_transfer(self, amount):
        if isinstance(amount, (int, float)) and 0 < amount <= self.balance:
            self.balance -= float(amount)
            return True
        return False

    def get_express_fee(self):
        return 1.0

    def send_express_transfer(self, amount):
        if isinstance(amount, (int, float)) and amount > 0:
            express_fee = self.get_express_fee()
            total_cost = float(amount) + express_fee
            if self.balance >= amount - express_fee:
                self.balance -= total_cost
                return True
        return False
