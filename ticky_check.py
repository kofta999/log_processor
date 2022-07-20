#!/usr/bin/env python3
import operator
import re
import csv
import sys
errors = {}
user_infos = {"Username": ["INFO", "ERROR"]}

def error_collector(logfile):
    with open (logfile, 'r') as file:
        for line in file.readlines():
            error_result = re.search(r"ticky: ERROR ([\w ']*)", line)
            if error_result != None:
                error_result = error_result.group(1)
                if error_result not in errors :
                    errors[error_result] = 0
                errors[error_result] += 1
    file.close()
    return  sorted(errors.items(), key=operator.itemgetter(1),reverse=True)

def user_collector(logfile):
    with open(logfile, 'r') as file:
        for line in file.readlines():
            user_result = re.search(r"ticky: (\w*) .* \((\w.*)\)", line)
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
        writer = csv.writer()
        for row in error:
            writer.writerow(row)
    file.close()



if __name__ == "__main__":
    error = error_collector(sys.argv[1])
    error.insert(0, ("Error", "Count"))
    per_user = user_collector(sys.argv[1])
    to_csv(error, per_user)