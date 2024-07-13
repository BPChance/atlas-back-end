#!/usr/bin/python3
""" script that gathers data from an api """

import requests
import sys
import json


def get_employee_todo_progress(employee_id):
    base_url = "https://jsonplaceholder.typicode.com/"

    user_response = requests.get("{}/users/{}".format(base_url, employee_id))
    if user_response.status_code != 200:
        print("Error fetching user with ID {}".format(employee_id))
        return

    user_data = user_response.json()
    employee_name = user_data.get('name')
    username = user_data.get('username')

    todos_response = requests.get("{}/todos?userId={}".format(base_url, employee_id))
    if todos_response.status_code != 200:
        print("Error fetching TODO list for user with ID {}".format(employee_id))

    todos_data = todos_response.json()

    total_tasks = len(todos_data)
    done_tasks = [task for task in todos_data if task.get('completed')]
    number_of_done_tasks = len(done_tasks)

    print("Employee {} is done with tasks({}/{}):".format(employee_name, number_of_done_tasks, total_tasks))

    for task in done_tasks:
        print(f"\t {task.get('title')}")

    tasks = [{"task": task.get('title'), "completed": task.get('completed'), "username": username} for task in todos_data]
    json_data = {str(employee_id): tasks}

    with open("{}.json".format(employee_id), 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
    else:
        try:
            employee_id = int(sys.argv[1])
            get_employee_todo_progress(employee_id)
        except ValueError:
            print("Please provide a valid integer as employee ID")
