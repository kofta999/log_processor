#!/usr/bin/env python3
from log_gen import log_generator
import operator
import re
import csv
import sys
errors = {}
user_infos = {"Username": ["INFO", "ERROR"]}
type_name = ["ERROR", "INFO", "DEBUG", "WARNING"]

def error_collector(logfile, error_name):
    with open (logfile, 'r') as file:
        for line in file.readlines():
            error_result = re.search(r"[\w\-]*: {} ([\w ']*)".format(error_name.upper()), line)
            if error_result != None:
                error_result = error_result.group(1).strip()
                if error_result not in errors :
                    errors[error_result] = 0
                errors[error_result] += 1
    file.close()
    return  sorted(errors.items(), key=operator.itemgetter(1),reverse=True)

def user_collector(logfile):
    with open(logfile, 'r') as file:
        for line in file.readlines():
            user_result = re.search(r"[\w\-]*: (\w*) .* \((\w.*)\)", line)
            if user_result != None:
                user = user_result.group(2)
                error_type = user_result.group(1)
                if user not in user_infos:
                    user_infos[user] = []
                    user_infos[user].insert(1,0)
                    user_infos[user].insert(2,0)
                if error_type == "INFO":
                    user_infos[user][0] +=1
                if error_type == "ERROR":
                    user_infos[user][1] +=1
    file.close()
    return sorted(user_infos.items())

def to_csv(error, per_user):
    with open("error_message.csv", 'w+') as file:
        writer = csv.writer(file)
        for row in error:
            writer.writerow(row)
    file.close()

    with open("user_statistics.csv", 'w+') as file:
        writer = csv.writer(file)
        for row in per_user:
            writer.writerow([row[0]] + [row[1][0]] + [row[1][1]])
    file.close()

if __name__ == "__main__":
    log_generator()
    try: 
        inputfile = sys.argv[1]
    except IndexError:
        inputfile = "syslog"
    process_name = input("Which kind of error do you want to search for?\nAvaliable errors to search : ERROR, WARNING, DEBUG, INFO ")
    if process_name.isalpha() == False or process_name.upper() not in type_name:
        print("Error, Enter a proper error name")
        sys.exit(1)
    error = error_collector(inputfile, process_name)
    error.insert(0, (process_name.capitalize(), "Count"))
    per_user = user_collector(inputfile)
    to_csv(error, per_user)
    print("Done.")
    sys.exit(0)