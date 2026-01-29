from src.account import Account
from src.mongo_account_repository import MongoAccountsRepository
import pytest
from src.account_repository import AccountsRepository
import os
from unittest.mock import patch, MagicMock

class TestMongoAccountsRegistry:
    acc1 = Account("Alice", "Smith", "12345678901")
    acc2 = Account("Bob", "Johnson", "10987654321")

    @pytest.fixture(autouse=True)
    def mongo_repo(self):
        self.acc1.receive_transfer(100.0)

    def test_save_and_load_accounts(self, mocker):
        mock_collection = mocker.Mock()
        mock_collection.find.return_value = [
            self.acc1.to_dict(),
            self.acc2.to_dict()
        ]
        mongo_repo = MongoAccountsRepository(collection=mock_collection)
        mongo_repo.save_all([self.acc1, self.acc2])

        loaded_accounts = mongo_repo.load_all()

        assert len(loaded_accounts) == 2
        assert any(acc.pesel == "12345678901" and acc.first_name == "Alice" for acc in loaded_accounts)
        assert any(acc.pesel == "10987654321" and acc.first_name == "Bob" for acc in loaded_accounts)

    
    def test_account_repository_methods(self):
        class ConcreteRepo(AccountsRepository):
            def save_all(self, accounts):
                super().save_all(accounts)
            
            def load_all(self):
                super().load_all()

        repo = ConcreteRepo()
        
        with pytest.raises(NotImplementedError):
            repo.save_all([])
            
        with pytest.raises(NotImplementedError):
            repo.load_all()
            
        repo.close() 

    def test_mongo_repo_init_mock(self, mocker):
        mocker.patch.dict(os.environ, {"USE_MONGOMOCK": "true"})
        MongoAccountsRepository._mock_client = None
        
        repo = MongoAccountsRepository(collection=None)
        assert repo._client is not None
        import mongomock
        assert isinstance(repo._client, mongomock.MongoClient)
        
        client_first = repo._client
        repo2 = MongoAccountsRepository(collection=None)
        assert repo2._client is client_first

    def test_mongo_repo_init_real(self, mocker):
        mocker.patch.dict(os.environ, {"USE_MONGOMOCK": "false"})
        
        mock_mongo = mocker.patch("src.mongo_account_repository.MongoClient")
        
        repo = MongoAccountsRepository(collection=None, uri="mongodb://fake:27017")
        
        mock_mongo.assert_called_with("mongodb://fake:27017")
        assert repo._client == mock_mongo.return_value

