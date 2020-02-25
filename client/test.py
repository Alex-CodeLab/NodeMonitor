import unittest

from Client import Client


class Testing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    def test_loadconfig(self):
        client = Client()
        c = client.load_settings()
        print(c)
        # self.assertEqual()


if __name__ == '__main__':
    unittest.main()
