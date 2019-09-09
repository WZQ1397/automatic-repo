import functools
import itertools
# import numpy
import operator

class flaten_array:
    def __init__(self,array):
        self.array=array
    # 使用两次for循环
    def forfor(self):
        return [item for sublist in self.array for item in sublist]

    # 通过sum
    def sum_brackets(self):
        return sum(self.array, [])

    # 使用functools內建模块
    def functools_reduce(self):
        return functools.reduce(operator.concat, self.array)

    # 使用itertools內建模块
    def itertools_chain(self):
        return list(itertools.chain.from_iterable(self.array))

    # 使用numpy
    # def numpy_flat(self):
    #     return list(numpy.array(self.array).flat)

    # 使用numpy
    # def numpy_concatenate(self):
    #     return list(numpy.concatenate(self.array))

    # 自定义函数
    def flatten(self):
        """Yield items from any nested iterable; see REF."""
        for x in self.array:
            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                yield from flatten(x)
            else:
                yield x

# a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print(a)
#
# print('--------------------------')
# conv=flaten_array(a)
# print(conv.forfor())
# print(conv.sum_brackets())
# print(conv.functools_reduce())
# print(conv.itertools_chain())
# # print(conv.numpy_flat())
# # print(conv.numpy_concatenate())