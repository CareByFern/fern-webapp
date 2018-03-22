from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

from .models import Charge, Shift, Status, Email
from .forms import EmailForm

from datetime import datetime, timezone

def homepage(request):
    print('homepage user', request.user)
    if request.method == 'POST':
        print('got a post request')
        form = EmailForm(request.POST)
        if form.is_valid():
            print('got a valid form')
            email = form.cleaned_data.get('email')
            # Check if the email already exists
            num_results = Email.objects.filter(email=email).count()
            if num_results is 0:
                print('creating email')
                email_obj = Email()
                email_obj.email = email
                email_obj.save()
            return HttpResponseRedirect('/thanks/')
    else:
        email_form = EmailForm(auto_id=False)
        context = {
            'logged_in': request.user.is_authenticated,
            'form' : email_form,
        }
        return render(request, 'giver/index.html', context)

def face(request):
    return render(request, 'giver/face.html')

def thanks(request):
    context = {
            'logged_in': request.user.is_authenticated
        }
    return render(request, 'giver/thanks.html', context)

def simple_error(request, mesg):
    return render(request, 'giver/error.html', {'message': mesg})

def index(request):
    '''Care hub. For aides, shows a list of charges. For fam, shows dashboard.'''
    if hasattr(request.user, 'aide'):
        return aide_hub(request)
    elif hasattr(request.user, 'primarycaregiver'):
        return fam_hub(request)
    else:
        return simple_error(request, 'Sorry, your user was not created properly! Please contact support@carebyfern.com')

def aide_hub(request):
    context = {
        'all_charges': Charge.objects.all(),
    }
    print(context['all_charges'])
    return render(request, 'giver/charge_list.html', context)

def fam_hub(request):
    '''View for family members to view and change schedule.'''
    if not request.user.is_authenticated:
        return redirect('/login') # TODO: test
    if not hasattr(request.user, 'primarycaregiver'):
        print('xxxx hiiiiiii')
        return redirect('/care') # TODO: test

    primary = request.user.primarycaregiver
    charge = primary.charge
    if not charge:
        return simple_error(request, "Sorry! Your account is not properly set up with your senior who is receiving care.  Please contact support@carebyfern.com")

    context = {
        'logged_in': request.user.is_authenticated,
        'charge_name': charge.full_name,
        'charge_nick': charge.casual_name,
    }

    try:
        status = charge.status_set.latest('timestamp')
        context['charge_status'] = status
        interval = (datetime.now(timezone.utc) - status.timestamp)
        context['is_was'] = 'is' if interval.seconds < 60*10 else 'was'
    except Status.DoesNotExist:
        context['charge_status'] = False

    return render(request, 'giver/fam_hub.html', context)

def login_view(request):
    '''Log in.'''
    if request.method == 'GET':
        if not request.user.is_authenticated:
            context = {'redirect_to': request.GET.get('redirect_to')}
            print('[GET] context: {}'.format(context))
            return render(request, 'giver/login.html', context)
        else:
            return render(request, 'giver/logout.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('request.POST: {}'.format(request.POST))
            print('redirect_to: {}'.format(request.POST.get('redirect_to', '/')))
            return redirect(request.POST.get('redirect_to', '/'))
        else:
            context = {
                'redirect_to': request.POST.get('redirect_to') or '/care/',
                'failure_message': request.POST.get('failure_message')
            }
            return render(request, 'giver/login.html', context)

def logout_view(request):
    '''Log out.'''
    if request.method == 'GET':
        return render(request, 'giver/logout.html')
    else:
        logout(request)
        return redirect('/')


def charge(request, chargeid):
    '''View for aides currently taking care of a charge.'''
    charge = Charge.objects.get(pk=chargeid)
    context = {
        'charge_name': charge.full_name,
        'charge_nick': charge.casual_name,
    }
    return render(request, 'giver/operator.html', context)

def hourify(n):
    '''Takes a 24-hr hour and formats it like "8:00 AM"'''
    meridian = 'AM'
    if 11 < n:
        meridian = 'PM'
    if 12 < n:
        n -= 12
    if n == 0:
        n = 12
    return '{}:00 {}'.format(n, meridian)


def shifts(request):
    '''View for family members to view and change schedule.'''
    if not request.user.is_authenticated:
        return redirect('/login') # TODO: test
    if not hasattr(request.user, 'primarycaregiver'):
        print('xxxx hiiiiiii')
        return redirect('/care') # TODO: test

    primary = request.user.primarycaregiver
    if not primary.charge:
        return simple_error(request, "Sorry! Your account is not properly set up with your senior who is receiving care.  Please contact support@carebyfern.com")

    context = {}
    context['primary_name'] = primary.nickname
    context['charge_name'] = primary.charge.casual_name

    hournums = list(range(5, 24)) + list(range(5))
    context['hours'] = list(zip(hournums, map(hourify, hournums)))

    context['shifts'] = Shift.objects.filter(charge=primary.charge)
    return render(request, 'giver/shifts.html', context)

def edit_shift(request):
    if request.method != 'POST':
        return redirect('shifts')
    shift = Shift.objects.get(pk=request.POST.get('shift_id'))
    shift.start = '{}:00'.format(request.POST.get('start'))
    shift.end = '{}:00'.format(request.POST.get('end'))

    print('look:')
    print(request.POST)
    print(request.POST.get('days'))

    for day in ['Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat']:
        if day in request.POST.getlist('days'):
            print('come in on {}'.format(day))
    shift.save()
    return redirect('shifts')


def update_status(request):
    if request.method != 'POST':
        return HttpResponseBadRequest(content='must be a POST request')

    update_summary = request.POST.get('new_status', None)
    update_notes = request.POST.get('new_notes', None)

    if not update_summary:
        return HttpResponseBadRequest(content='status was empty string')

    rockwell = Charge.objects.get(pk=2)
    new_status = rockwell.status_set.create(summary=update_summary, notes=update_notes)
    return JsonResponse({'summary': new_status.summary, 'timestamp': new_status.timestamp})
