#!/usr/bin/python3
""" script that gathers data from an api """

import requests
import sys
import csv


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

    with open("{}.csv".format(employee_id), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])
        for task in todos_data:
            writer.writerow([employee_id, username, task.get('completed'), task.get('title')])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
    else:
        try:
            employee_id = int(sys.argv[1])
            get_employee_todo_progress(employee_id)
        except ValueError:
            print("Please provide a valid integer as employee ID")