import unittest

from Client import Client


class Testing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    def test_loadconfig(self):
        client = Client()
        config = client.load_settings()
        self.assertEqual(type(config).__name__ , 'ConfigParser')
        self.assertEqual(type(client.modules), type({}))



if __name__ == '__main__':
    unittest.main()
