# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 12:32

backforth = []
backforth.append(eval(input().replace(' ',',')))
backforth.append(eval(input().replace(' ',',')))
cow_farm1_type = set(backforth[0])
cow_farm2_type = set(backforth[1])
print(cow_farm1_type,cow_farm2_type)
day1types = cow_farm1_type.copy()
day3types = cow_farm1_type.copy()
day2types = cow_farm2_type.copy()
day4types = cow_farm2_type.copy()

result=set()
# todo  2      3       4       5
# todo 1/2  (1/2)/5   1/2/5   1/2/5
for day1bucket in day1types:
  day2types.add(day1bucket)
  for day2bucket in day2types:
    day3types.add(day2bucket)
    for day3bucket in day3types:
      day4types.add(day3bucket)
      for day4bucket in day4types:
        # day1types.add(day4bucket)
        result.add(-day1bucket+day2bucket-day3bucket+day4bucket)
        print(day1bucket,day2bucket,day3bucket,day4bucket)
        # day1types.discard(day4bucket)
      day4types.discard(day3bucket)
    day3types.discard(day2bucket)
  day2types.discard(day1bucket)

print(result)






