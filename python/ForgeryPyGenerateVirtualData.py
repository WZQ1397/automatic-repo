from forgery_py import *
for x in range(20):
  randPerson=name.first_name(),name.last_name(),personal.gender(),name.location(),address.phone()
  randCV=lorem_ipsum.title(),lorem_ipsum.sentence()
  randAddr=address.city(),address.state(),address.country(),address.continent()
  randEmail=internet.email_address()
  randColor=basic.hex_color()
  randComment=basic.text(200)
  randDate=date.date()
  print("name: {}\n gender: {}\n home: {}\n phone: {}\n email: {}".
        format(randPerson[:2],randPerson[2],randPerson[3],randPerson[4],randEmail))
  print(f" CV: {randCV}")
  print(f" favourite color: {randColor}")
  print(f" comment: {randComment}")
  print("handout date: {:#^50s}".format(str(randDate)))