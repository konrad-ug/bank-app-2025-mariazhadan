from src.account_firm import CompanyAccount


class TestCompanyAccount:

    def test_create_company_account_valid_nip(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        assert account.company_name == "Tech Corp"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_create_company_account_invalid_nip_short(self):
        account = CompanyAccount("ABC Company", "123456789")
        assert account.nip == "Invalid"

    def test_create_company_account_invalid_nip_long(self):
        account = CompanyAccount("XYZ Ltd", "12345678901")
        assert account.nip == "Invalid"

    def test_create_company_account_invalid_nip_letters(self):
        account = CompanyAccount("Test Corp", "123ABC7890")
        assert account.nip == "Invalid"

    def test_company_account_receive_transfer(self):
        account = CompanyAccount("Transfer Co", "1234567890")
        result = account.receive_transfer(1000.0)
        assert result == True
        assert account.balance == 1000.0

    def test_company_account_send_transfer(self):
        account = CompanyAccount("Sender Co", "1234567890")
        account.receive_transfer(1000.0)
        result = account.send_transfer(300.0)
        assert result == True
        assert account.balance == 700.0

    def test_company_account_send_transfer_insufficient_funds(self):
        account = CompanyAccount("Poor Co", "1234567890")
        account.receive_transfer(100.0)
        result = account.send_transfer(500.0)
        assert result == False
        assert account.balance == 100.0