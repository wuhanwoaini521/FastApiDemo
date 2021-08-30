from ddt import *
import unittest

# 在测试类前必须首先声明使用 ddt
@ddt
class imoocTest(unittest.TestCase):
    tuples = ((1, 2, 3), (1, 2, 3))
    lists = [[1, 2, 3], [1, 2, 3],[4,5,6]]

    # 元组
    @data((1, 2, 3), (1, 2, 3))
    def test_tuple(self, n):
        print("test_tuple", n)

    # 列表
    @data([1, 2, 3], [1, 2, 3])
    @unpack
    def test_list(self, n1, n2, n3):
        print("test_list", n1, n2, n3)

    # 元组2
    @data(*tuples)
    def test_tuples(self, n):
        print("test_tuples", n)

    # 列表2
    @data(*lists)
    @unpack
    def test_lists(self, n1, n2, n3):
        print("test_lists", n1, n2, n3)

    # 字典
    @data({'value1': 1, 'value2': 2}, {'value1': 1, 'value2': 2})
    @unpack
    def test_dict(self, value1, value2):
        print("test_dict", value1, value2)

if __name__ == '__main__':
    unittest.main()