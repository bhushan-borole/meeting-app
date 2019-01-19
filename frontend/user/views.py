from django.shortcuts import render, redirect
import requests
from django.contrib import messages
import json


def _form_view(request, template_name):
    if request.method == 'POST':
        headers = {
            'username': request.POST['email'],
            'password': request.POST['password']
        }
        print(headers)
        response = requests.get('http://localhost:1234/rest/login', headers=headers)
        if response.status_code == 200:
            print(response.text)
            return redirect('/dashboard')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('/')
    else:
        return render(request, template_name)


def login(request):
    return _form_view(request, template_name='views/login.html')


def dashboard(request):
    return render(request, template_name='views/dashboard.html')


'''
def get_tasks(id):
    url = 'http://localhost:1234/rest/tasks/{}'.format(id)
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        data = json.loads(response.text)
        tasks = [x['details'] for x in data[2]['task']]
        if len(tasks) == 0:
            return ['No Task Assigned']
        else:
            return tasks
'''


def get_all_tasks():
    url = 'http://localhost:1234/rest/all_tasks'
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def get_tasks_for_meeting(id):
    url = 'http://localhost:1234/rest/tasks/{}'.format(id)
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        return list(json.loads(response.text))
    else:
        return ['No Task Assigned']


def all_meetings(request):
    response = requests.get('http://localhost:1234/rest/meetings')
    data = json.loads(response.text)
    meetings = []
    all_tasks = get_all_tasks()

    for x in data:
        id = x['id']
        tasks = get_tasks_for_meeting(id)
        tasks = [x['details'] for x in tasks]
        title = x['title']
        venue = x['venue']
        username = x['user']['name']
        user_id = x['user']['id']
        meetings.append([id, title, venue, username, user_id, tasks])

    return render(request, 'views/all_meetings.html', {'meeting': meetings,
                                                       'all_tasks': all_tasks})


def delete_meeting(request, id):
    url = 'http://localhost:1234/rest/meeting/' + str(id)
    response = requests.delete(url)
    if response.status_code == 200:
        return redirect('/all_meetings')


def add_meeting(request):
    if request.method == 'POST':
        id = request.POST['conductedby']
        body = {
            'title': request.POST['title'],
            'venue': request.POST['venue']
        }
        print(body)
        response = requests.post('http://localhost:1234/rest/meeting/{}'.format(id), json=body)
        if response.status_code == 200:
            return redirect('/all_meetings')
        else:
            messages.error(request, 'something is missing')
            return redirect('/add_meeting')
    else:
        return render(request, 'views/add_meeting.html')


def edit_meeting(request, id):
    print(id)
    if request.method == 'POST':
        body = {
            'title': request.POST['title'],
            'venue': request.POST['venue']
        }
        response = requests.put('http://localhost:1234/rest/meeting/{}'.format(id), json=body)
        print(response.status_code)
        if response.status_code == 200:
            return redirect('/all_meetings')
        else:
            return redirect('/all_meetings')
    else:
        return render(request, 'views/all_meetings.html')


def add_task(request):
    if request.method == 'POST':
        body = {
            'details': request.POST['details']
        }
        response = requests.post('http://localhost:1234/rest/task', json=body)
        if response.status_code == 200:
            return redirect('/all_meetings')
        else:
            return redirect('/add_task')
    else:
        return render(request, template_name='views/add_task.html')


def assign_task(request, mid):
    if request.method == 'POST':
        tid = request.POST['task']
        url = 'http://localhost:1234/rest/assignTask/{}/{}'.format(mid, tid)
        response = requests.post(url)
        if response.status_code == 200:
            return redirect('/all_meetings')
        else:
            return redirect('/all_meetings')
    else:
        return render(request, template_name='views/all_meetings.html')


def all_tasks(request):
    all_tasks = get_all_tasks()
    return render(request, 'views/all_tasks.html', {'tasks': all_tasks})


def delete_task(request, id):
    url = 'http://localhost:1234/rest/task/' + str(id)
    response = requests.delete(url)
    if response.status_code == 200:
        return redirect('/all_tasks')


def edit_task(request, id):
    print(id)
    if request.method == 'POST':
        body = {
            'details': request.POST['details'],
        }
        response = requests.put('http://localhost:1234/rest/task/{}'.format(id), json=body)
        print(response.status_code)
        if response.status_code == 200:
            return redirect('/all_tasks')
        else:
            return redirect('/all_tasks')
    else:
        return render(request, 'views/all_tasks.html')




