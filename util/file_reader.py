import csv

class FileReader():
    def __init__(self, path, type="csv"):
        self.path = path
        self.type = type


    def return_rows(self):

        with open(self.path) as infile:
            reader = csv.reader(infile, delimiter=",")
            return [row for row in reader]
