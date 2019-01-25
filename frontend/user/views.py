from django.shortcuts import render, redirect
import requests
from django.contrib import messages
import json
import smtplib
from email.mime.text import MIMEText


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


def get_userid(email, all_users):
    for user in all_users:
        if email == user['email']:
            return user['id']


def send_mail(email, code):
    msg = MIMEText(code)
    msg['Subject'] = 'This is the OTP'
    msg['From'] = 'storm_breaker2698@outlook.com'
    msg['To'] = email

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login('storm_breaker2698@outlook.com', 'Zxcvbnm@123')
    server.sendmail('storm_breaker2698@outlook.com', email, msg.as_string())
    server.quit()
    print('mail sent')


def check_email(email):
    url = 'http://localhost:1234/rest/users'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        all_emails = [x['email'] for x in data]
        print(all_emails)
        if email in all_emails:
            return False
        else:
            return True


def signup(request):
    if request.method == 'POST':
        if check_email(request.POST['email']):
            print('email is valid')
            body = {
                'email': request.POST['email'],
                'name': request.POST['username'],
                'role': request.POST['role']
            }
            url = 'http://localhost:1234/rest/user'
            response = requests.post(url, json=body)
            if response.status_code == 200:
                url = 'http://localhost:1234/rest/users'
                all_users = requests.get(url)
                data = json.loads(all_users.text)
                id = get_userid(request.POST['email'], data)
                code_url = 'http://localhost:1234/rest/user/credentials/{}'.format(id)
                code_response = requests.get(code_url)
                if code_response.status_code == 200:
                    send_mail(request.POST['email'], code_response.text)
                    return redirect('/verify_code/{}'.format(id))
                else:
                    messages.error(request, 'username or password not correct')
                    return redirect('/signup')
        else:
            messages.error(request, 'email already exists')
            return redirect('/signup')
    else:
        return render(request, template_name="views/signup.html")


def verify_code(request, id):
    if request.method == 'POST':
        code = int(request.POST['code'])
        print(code)
        url = 'http://localhost:1234/rest/user/verify/{}/{}'.format(id, code)
        response = requests.get(url)
        print(response.text)
        if response.text == 'true':
            return redirect('/set_credentials/{}'.format(id))
        else:
            messages.error(request, 'Enter a valid OTP')
            return redirect('/verify_code/{}'.format(id))
    else:
        return render(request, template_name='views/verify_code.html')


def get_username(id):
    url = 'http://localhost:1234/rest/user/{}'.format(id)
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data['email']


def set_creds(request, id):
    if request.method == 'POST':
        if request.POST['pass'] == request.POST['pass1']:
            username = get_username(id)
            body = {
                'username': username,
                'password': request.POST['pass']
            }
            print(body)
            url = 'http://localhost:1234/rest/user/password/{}'.format(id)
            response = requests.post(url, json=body)
            if response.status_code == 200:
                return redirect('/')
            else:
                messages.error(request, 'something went wrong')
                return redirect('/set_credentials/{}'.format(id))
        else:
            messages.error(request, 'Password does not match')
            return redirect('/set_credentials/{}'.format(id))
    else:
        return render(request, template_name='views/set_credentials.html')




