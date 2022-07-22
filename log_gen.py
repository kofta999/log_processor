#!/usr/bin/env python3
def log_generator():
    import random
    process_name = open("apps.txt").readlines()
    type_name = ["ERROR", "INFO", "DEBUG", "WARNING"]
    ticket_num = random.randint(1000,9999)
    username = open("users.txt").readlines()
    tasks = open("tasks.txt").readlines()

    with open("syslog", "w+") as file:
        for i in range(500):
            log = "ubuntu.local {}: {} {} [#{}] ({})\n".format(random.choice(process_name).strip(), random.choice(type_name).strip(), random.choice(tasks).strip(), ticket_num, random.choice(username).strip())
            file.writelines(log)
    file.close()