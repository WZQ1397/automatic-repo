import xmltodict
import json

def pythonXmlToJson():
    #http://www.bejson.com/xml2json/
    xmlStr = """
<student>
    <stid>10213</stid>
    <info>
        <name>name</name>
        <mail>xxx@xxx.com</mail>
        <sex>male</sex>
    </info>
    <course>
        <name>math</name>
        <score>90</score>
    </course>
    <course>
        <name>english</name>
        <score>88</score>
    </course>
</student>
"""

    convertedDict = xmltodict.parse(xmlStr)
    jsonStr = json.dumps(convertedDict, indent=1)
    print("jsonStr=",jsonStr)

def pythonJsonToXml():
    dictVal = {
        'page': {
            'title': 'King Crimson',
            'ns': 0,
            'revision': {
                'id': 547909091,
            }
        }
    }
    convertedXml = xmltodict.unparse(dictVal)
    print("convertedXml=\n",convertedXml)
###############################################################################
if __name__!="__main__":
    pythonXmlToJson()
else:
    pythonJsonToXml()