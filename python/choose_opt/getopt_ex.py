from abc import abstractmethod
import sys, getopt

content = "zach"
choice = sys.argv[1:]
try:
    opts, args = getopt.getopt(choice, "f:j:y:i:my:mo", ["folder", "json", "yaml", "influx", "mongo", "mysql"])
except getopt.GetoptError:
    raise "error"


class Search_Record:
    def __init__(self, target: object) -> object:
        self.target = target

    @classmethod
    def search(obj):
        return "for search in diff type"

    def __str__(self):
        return "Search_Record"

    def __repr__(self):
        return repr(Search_Record)


class FindInFolder(Search_Record):
    def __init__(self, target):
        super(FindInFolder, self).__init__(target)

    def search(self):
        print(__class__.__name__, self.target)
        #from zachsearch import dir


class FindInMySQL(Search_Record):
    def __init__(self, target):
        super(FindInMySQL, self).__init__(target)

    def search(self):
        print(__class__.__name__, self.target)
        #from zachsearch import mysql


class FindInMongo(Search_Record):
    def __init__(self, target):
        super(FindInMongo, self).__init__(target)

    def search(self):
        print(__class__.__name__, self.target)
        #from zachsearch import mongo


class FindInJson(Search_Record):
    def __init__(self, target):
        super(FindInJson, self).__init__(target)

    def search(self):
        print(__class__.__name__, self.target)
        #from zachsearch import json


class FindInYaml(Search_Record):
    def __init__(self, target):
        super(FindInYaml, self).__init__(target)

    def search(self):
        print(__class__.__name__, self.target)
        #from zachsearch import yaml


class FindInInfluxDB(Search_Record):
    def __init__(self, target) -> object:
        super(FindInInfluxDB, self).__init__(target)

    def search(self):
        print(__class__.__name__, self.target)
        # http: // influxdb - python.readthedocs.io / en / latest / api - documentation.html
        #from zachsearch import influxdb


def search(obj):
    obj.search()


def select_method_to_find(choice, content):
    for opts, content in choice:
        if opts in ("-f", "--folder"):
            #print(opts, content)
            X = FindInFolder(content)
        elif opts in ("-j", "--json"):
            import json
            X = FindInJson(content)
        elif opts in ("-y", "--yaml"):
            # import yaml
            X = FindInYaml(content)
            # import PyYaml
        elif opts in ("-my", "--mysql"):
            import pymysql
            X = FindInMySQL(content)
        elif opts in ("-mo", "--mongo"):
            # from pymongo import MongoClient
            X = FindInMongo(content)
        elif opts in ("-i", "--influx"):
            # from influxdb import InfluxDBClient
            X = FindInInfluxDB(content)
        else:
            pass
    search(X)


select_method_to_find(opts, content)
