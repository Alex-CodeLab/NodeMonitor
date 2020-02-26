"""
 this requires python3.8
 https://docs.python.org/3.8/library/unittest.html#unittest.IsolatedAsyncioTestCase
"""


from unittest import  IsolatedAsyncioTestCase
# from modules import interval
from modules import load


class Testing(IsolatedAsyncioTestCase):

    # @classmethod
    # def setUpClass(cls):
    #     pass

    async def test_load(self):
        result = await load()
        result.split(' ')[0]
        self.assertEqual('load', result.split(' ')[0])

    async def test_memory(self):
        result = await load()
        result.split(' ')[0]
        self.assertEqual('memory', result.split(' ')[0])


if __name__ == '__main__':
    unittest.main()
