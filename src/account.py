class Account:
    def __init__(self, first_name, last_name,pesel, promocode = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        # if pesel is not None and len(pesel) == 11:
        #     self.pesel = pesel
        # else: 
        #     self.pesel = "Invalid"
        self.pesel = pesel if self.pesel_is_valid(pesel) else "Invalid"
         if 
            promocode is not None
            and self.promocode_is_valid(promocode)
            and self.is_eligible_for_promo(pesel)
        :
            self.balance += 50
        

    def pesel_is_valid(self,pesel):
        if pesel is not None and len(pesel) == 11:
            return True

    def promocode_is_valid(self,promocode):
        if not isinstance(promocode, str):
            return False
        if promocode.startswith("PROM_") and len(promocode) > 5:
            suffix = promocode[5:]  
            if not suffix.isdigit():  
                return True
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

    