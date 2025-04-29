from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError    
from django.contrib.auth import logout,authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import openpyxl
from .models import Attendance
from .form import CustomUserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Attendance
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()

   
    try:
        attendance = Attendance.objects.get(user=request.user, check_out_time__isnull=True)
    except Attendance.DoesNotExist:
        attendance = None

  
    if request.method == "POST":
        if 'check_in' in request.POST:
            if not attendance:
               
                role = 'SBS_RESOURS'  
                Attendance.objects.create(user=request.user, check_in_time=timezone.now(), role=role)

        elif 'check_out' in request.POST:
            if attendance:
                attendance.check_out_time = timezone.now()
                attendance.save()

  
    daily_records = Attendance.objects.filter(user=user, date=today)

    return render(request, 'dashboard.html', {
        'attendance': attendance,
        'daily_records': daily_records
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            
            if user.role == "Admin":
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'This email is already registered.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/dashboard/')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password.html', {'form': form})



@login_required
def admin_dashboard(request):
   
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    attendance_records = Attendance.objects.all()

    if search_query:
        attendance_records = attendance_records.filter(user__first_name__icontains=search_query)

    if start_date and end_date:
        attendance_records = attendance_records.filter(date__range=[start_date, end_date])

    return render(request, 'admin_dashboard.html', {
        'daily_records': attendance_records
    })

def export_attendance_to_excel(request):
    # Get the filtered records based on the start and end date
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter your attendance records (adjust based on your model fields)
    records = Attendance.objects.filter(date__range=[start_date, end_date])

    # Create a workbook and add a sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Attendance Records'


    headers = ['S.No', 'Name', 'Role', 'Date', 'Login Time', 'Logout Time']
    sheet.append(headers)
    for i, record in enumerate(records, start=1):
        sheet.append([
            i,
            f"{record.user.first_name} {record.user.last_name}",
            record.user.role,
            record.date,
            record.check_in_time,
            record.check_out_time if record.check_out_time else 'N/A'
        ])

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="attendance_records.xlsx"'

    # Save the workbook to the response
    workbook.save(response)
    return response
