# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-02-05 18:10

# hotel1 hotel2 is dict
hotel1 = {'hotelNo':1,'hotelName':"The Beacon Street Inn","hotelCity":"Boston"}
hotel2 = {'hotelNo':2,'hotelName':"The Queen City Lodge","hotelCity":"Manchester"}
# hotels is list
hotels = [hotel1,hotel2]
# hotels.append({'hotelNo':3,'hotelName':"The Bx Street Inn","hotelCity":"Boston"})


guest1 = {'guestNo':1,'guestName':"Joe Smith",'guestAddr':"42 Main street",'guestPhone':'555-555-5555'}
guest2 = {'guestNo':2,'guestName':"Sue Smith",'guestAddr':"44 South Avenue",'guestPhone':'555-555-6666'}
guests = [guest1,guest2]
hotelrooms = [{'roomNo':1,'roomSubNo':1,'roomType':'single','roomPrice':100},
              {'roomNo':1,'roomSubNo':2,'roomType':'double','roomPrice':125},
              {'roomNo':2,'roomSubNo':1,'roomType':'suite','roomPrice':4000},
              {'roomNo':2,'roomType':'double','roomPrice':200}]
# hotelchain is dict
hotelchain = {'hotel':hotels,'guest':guests,'hotelroom':hotelrooms}
bookings = [{'hotelNo':1,'roomNo':1,'guestNo':1,'dateRange':'from 11/01/2017 to 11/04/2017'},
           {'hotelNo':2,'roomNo':2,'guestNo':2,'dateRange':'from 12/03/2017 to 12/17/2017'}]

# TODO ______
hotelchain['booking'] = bookings

# get the booking dict values

# step = 0
# for values in hotelchain.get('booking'):
#   step = step + 1
#   # get each kev and values from the booking dict
#   print(step,values)
#   for k,v in values.items():
#     step += 1
#     print(step,"<{0}>{1}</{0}>".format(k,v))
#     # continue # break
#     # print()

# for k,v in hotelchain.items():
#   # about format ...
#   print("{0} ==> {1}".format(k,v))

# get the booking dict values
blanks = "  "
print("<hotelchain>")
for hotelchain_k,hotelchain_v in hotelchain.items():
  # get each kev and values from the booking dict
  for values in hotelchain_v:
    print("{1}<{0}>".format(hotelchain_k,blanks))
    for k,v in values.items():
      # TODO what this function ???
      print("{2}<{0}>{1}</{0}>".format(k,v,blanks*2))
    print("{1}</{0}>".format(hotelchain_k,blanks))
print("</hotelchain>")

# for hotelchain_k,hotelchain_v in hotelchain.items():
#   # get each kev and values from the booking dict
#   for values in hotelchain_v:
#     sum_v,flag = "",True
#     for k,v in values.items():
#       if k.endswith("No") and flag:
#         sum_v += "{}=\"{}\" ".format(k,v)
#       else:
#         flag = False
#       if not flag and sum_v != "":
#         print("{0}<{2} {1}> ".format(blanks,sum_v,hotelchain_k))
#         flag = True
#         sum_v = ""
#       if not k.endswith("No"):
#         print("{2}<{0}>{1}</{0}>".format(k, v, blanks * 2))
#     print("{1}</{0}>".format(hotelchain_k,blanks))
# print("</hotelchain>")

# elements = []
# subelements = set()
# ATTLIST= set()
# for hotelchain_k,hotelchain_v in hotelchain.items():
#   elements.append(hotelchain_k)
#   for k,_ in hotelchain_v[0].items():
#     if k.endswith("No"):
#       ATTLIST.add(k)
#     else:
#       subelements.add(k)
#
# print("<!ELEMENT hotelchain ({})+>".format(str(elements)[1:-1].replace("\'","")))
#
# for v in subelements:
#   print("<!ELEMENT {} (#PCDATA)>".format(v))
# for v in ATTLIST:
#   print("<!ATTLIST hotelchain {} CDATA #IMPLIED>".format(v))