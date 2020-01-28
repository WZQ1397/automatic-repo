import re
tmp="asa1_23 fsa2cv afw1 33[s"

pattern_A = re.compile(r'\w+',re.I)
res_A = pattern_A.finditer(tmp)

for x in res_A:
    print(x.group())

pattern_B = re.compile(r'[a-z]+',re.I)

print(pattern_B.findall(tmp))


phone="13317526643"

pattern_C_res = re.search(r'(?P<ISP>[0-9]{3})',phone)
print(pattern_C_res.groupdict())

SN ="CN01201710281951476558510001"

pattern_D_res = re.search(r'(?P<Nation>\w{2})(?P<region>[0-9]{2})(?P<Date>[0-9]{8})(?P<Time>[0-9]{6})',SN)
print(pattern_D_res.groupdict())
