import unittest
import nnpy
import json
from Server import app
from Server import Server


class TestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        # creates a test client
        server = Server()
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True


    def test_loadsettings(self):
        server = Server()
        self.assertEqual(type(server.modules), type({}))

    def test_settings_exist(self):
        server = Server()
        self.assertNotEqual(len(server.modules) , 0)

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_fail_status_code(self):
        result = self.app.get('/fail')
        self.assertEqual(result.status_code, 404)

    def test_data_status_fail(self):
        result = self.app.get('/data/')
        self.assertEqual(result.status_code, 404)

    def test_data_status_code(self):
        result = self.app.get('/data/load')
        jsn = json.loads(result.data.decode())
        keyexists = False
        if 'msg' in jsn:
            keyexists = True
        self.assertTrue(keyexists)
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
