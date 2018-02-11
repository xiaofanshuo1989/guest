import unittest
from sign.unittestLearning.module import Caculator

class WANGYI(unittest.TestCase):
    def setUp(self):
        self.verifyString = 'test'
        self.cal = Caculator(8, 4)

    def test01(self):
        '''测试方法'''
        self.assertEqual('test',self.verifyString,msg='两个值不相等')  #msg 定义出错信息

    def test_add(self):
        result = self.cal.add()
        self.assertEqual(result, 19, msg='结果不对')

    def tearDown(self):
        pass


if __name__ == '__main__':
   # unittest.main()
   suite = unittest.TestSuite()
   suite.addTest(WANGYI("test_add"))
   runner = unittest.TextTestRunner()
   runner.run(suite)