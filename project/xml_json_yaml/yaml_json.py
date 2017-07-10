#https://www.json2yaml.com/
#https://github.com/drbild/json2yaml
import yaml,pprint

choice = "json2"
filepath = "E:\\automatic-repo\salt\chrony\pillar.example"

def yamljson(select):
    if select == 'yaml':
        with open(filepath,'r') as f:
            str = f.read()
        return yaml.load(str)
    elif select == 'json':
        with open(filepath,'r') as f:
            str = f.read()
        return yaml.dump(str)
    else:
        raise Exception("ARG ERROR!")

if choice == 'yaml':
    pprint.pprint(yamljson(choice))
else:
    print(yamljson(choice))