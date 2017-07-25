from ggplot import *
import pandas,json
from pandas.core import datetools
import os
path = 'E:\\ssd\\psync\\randr_4k_1job_8dep.json2'
str = '''{'in_queue': 189244,
 'name': 'rbd0',
 'read_ios': 354580,
 'read_merges': 0,
 'read_ticks': 189304,
 'util': 94.74,
 'write_ios': 0,
 'write_merges': 0,
 'write_ticks': 0}'''
data = pandas.read_json(str,orient = 'records')
print(data)
p = ggplot(mtcars, aes('factor(cyl)'))
p + geom_bar()
print(p)