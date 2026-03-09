"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import importlib
from unittest.mock import patch
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app
from service import talisman

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts" 

HTTPS_ENVIRON = {'wsgi.url_scheme': 'https'}


######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        talisman.force_https = False
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  A C C O U N T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], str(account.date_joined))

    def test_bad_request(self):
        """It should not Create an Account when sending the wrong data"""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create an Account when sending the wrong media type"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="text/html"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # ADD YOUR TEST CASES HERE ...

    def test_read_an_account(self):
        """Test reading an account"""
        account = self._create_accounts(1)[0]
        resp = self.client.get(f"/accounts/{account.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_account_not_found(self):
        """It should not Read an Account that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_account_list(self):
        """It should Get a list of Accounts"""
        self._create_accounts(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_update_account(self):
        """It should Update an existing Account"""
        # create an Account to update
        test_account = AccountFactory()
        resp = self.client.post(BASE_URL, json=test_account.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the account
        new_account = resp.get_json()
        new_account["name"] = "Something Known"
        resp = self.client.put(f"{BASE_URL}/{new_account['id']}", json=new_account)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_account = resp.get_json()
        self.assertEqual(updated_account["name"], "Something Known")

    def test_delete_account(self):
        """It should Delete an Account"""
        account = self._create_accounts(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{account.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.delete(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_init_db_failure_exits(self):
        """Test that the service exits if init_db fails"""
        with patch("service.models.init_db") as mock_init_db:
            mock_init_db.side_effect = Exception("DB failure")

            with patch("sys.exit") as mock_exit:
                import service
                importlib.reload(service)

                mock_exit.assert_called_with(4)

    def test_update_account_not_found(self):
        """It should not Update an Account that is not found"""
        account = AccountFactory().serialize()

        resp = self.client.put(f"{BASE_URL}/0", json=account)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_build_database_uri_from_env(self):
        """It should build DATABASE_URI from environment variables"""

        # Remove DATABASE_URI so the config code runs
        os.environ.pop("DATABASE_URI", None)

        os.environ["DATABASE_USER"] = "testuser"
        os.environ["DATABASE_PASSWORD"] = "testpass"
        os.environ["DATABASE_NAME"] = "testdb"
        os.environ["DATABASE_HOST"] = "testhost"

        from service import config
        importlib.reload(config)

        self.assertIn("postgresql://", config.DATABASE_URI)
        self.assertIn("testuser", config.DATABASE_URI)
        self.assertIn("testdb", config.DATABASE_URI)

    def test_security_headers(self):
        """It should return security headers"""
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(resp.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(
            resp.headers.get("Content-Security-Policy"),
            "default-src 'self'; object-src 'none'"
        )
        self.assertEqual(
            resp.headers.get("Referrer-Policy"),
            "strict-origin-when-cross-origin"
        )

