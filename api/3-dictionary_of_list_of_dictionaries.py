#!/usr/bin/python3
""" Python script to export data in the JSON format """

import json
import requests
import sys


def get_employee_todo_progress(employee_id):
    base_url = "https://jsonplaceholder.typicode.com"

    user_response = requests.get(f"{base_url}/users/{employee_id}")
    if user_response.status_code != 200:
        print(f"Error fetching user with ID {employee_id}")
        return None, None

    user_data = user_response.json()
    employee_name = user_data.get('username')

    todos_response = requests.get(f"{base_url}/todos?userId={employee_id}")
    if todos_response.status_code != 200:
        print(f"Error fetching TODO list for user with ID {employee_id}")
        return None, None

    todos_data = todos_response.json()

    total_tasks = len(todos_data)
    done_tasks = [task for task in todos_data if task.get('completed')]
    number_of_done_tasks = len(done_tasks)

    employee_tasks = []
    for task in todos_data:
        task_info = {
            "username": employee_name,
            "task": task.get('title'),
            "completed": task.get('completed')
        }
        employee_tasks.append(task_info)

    return employee_name, employee_tasks


def export_all_tasks():
    base_url = "https://jsonplaceholder.typicode.com"
    all_employee_tasks = {}

    for employee_id in range(1, 11):
        employee_name, tasks = get_employee_todo_progress(employee_id)
        if employee_name and tasks:
            all_employee_tasks[employee_id] = tasks

    with open('todo_all_employees.json', 'w') as f:
        json.dump(all_employee_tasks, f, indent=2)

    print("Data exported to todo_all_employees.json")


if __name__ == "__main__":
    export_all_tasks()
