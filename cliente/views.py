from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from user.models import *
from cliente.models import Member,GymClass,Enrollment
from custom.models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from custom.utils import *
from .forms import *
import os
import csv
import datetime
import chardet
import logging
from django.db import IntegrityError
from .forms import UploadCSVForm
from .models import *
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Count

#pdf lib
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
def portal_view(request):
    return render(request, 'portal.html')

@login_required
def home(request):
	data = {
	'title':"Varanda",
	'active_varanda':"active"
	}
	return render(request,'index.html',data)

@login_required
def home(request):
    total_member = Member.objects.count()
    mane = Member.objects.filter(sexo='Mane').count()
    feto = Member.objects.filter(sexo='Feto').count()
    context = {
        'total_member': total_member,
        'mane': mane,
        'feto': feto,
    }
    return render(request, 'index.html', context)

@login_required
def member(request):
    listamembru = Member.objects.all()
    data = {
    'title':"Lista Membru",
    'active_estudante':"active",
    'dadus':listamembru
    }
    return render(request, 'listamember.html',data)

@login_required
def createMember(request):
    tinan = Tinan.objects.all().order_by('-id')
    form = MemberForm()

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('member')
    data = {
        'form':form,
        'listaTinan':tinan,
        'title':"Formulariu Membru",
        'page':"form",
    }
    return render(request, 'formmember.html',data)

@login_required
def updateMember(request, id):
    tinan = Tinan.objects.all().order_by('-id')
    member= Member.objects.get(id=id)
    form = MemberForm(instance=member)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member')
    data = {
        'form':form,
        'tinan':tinan,
        'title':"Formulariu Update Membru",
        'page':"form",
    }
    return render(request, 'formmember.html',data)

@login_required
def deleteMember(request,pk):
    member = Member.objects.get(id=pk)
    member.delete()
    return redirect('member')

@login_required
def detailMember(request,pk):
    memberData = get_object_or_404(Member,id=pk)
    data = {
    'title':"Detallu Membru",
    'memberData':memberData,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'formmember.html',data)

@login_required
def csv_member(request):
    # replace with the fields you need 
    fields = ['nu_id','naran','sexo','naturalidade','join_date','end_date','enderesu','municipio__name','status','phone','email']
    # Generate the csv file with datetime
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=listamemberGeral.csv"
    writer = csv.writer(response)
    # Write the header row
    writer.writerow(fields)
    for row in Member.objects.values(*fields):
        writer.writerow([row[field] for field in fields])
        # return
    return response

@login_required
def pdf_member(request):
    member = Member.objects.all()
    data = {'dadus':member,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/memberpdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

@login_required
def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['csv_file']
            
            # Detect file encoding
            raw_data = csvfile.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            # Decode file content
            decoded_file = raw_data.decode(encoding).splitlines()
            reader = csv.reader(decoded_file, delimiter=';')

            # Skip the header row
            next(reader)

            errors = []

            for row in reader:
                # Ensure the row has enough columns
                if len(row) < 14:
                    errors.append(f"Skipping row (not enough columns): {row}")
                    continue

                try:
                    # Check if a Funcionariu with the same `nu` already exists
                    if Member.objects.filter(nu_id=row[0]).exists():
                        errors.append(f"Skipping duplicate row with nu_id: {row[0]}")
                        continue

                    # Create a new Funcionariu object
                    new_member = Member.objects.create(
                        nu_id=row[0],
                        nome_completo=row[1],
                        sexo=row[2],
                        naturalidade=row[3],
                        data_do_nasc=row[4],
                        data_entrada=row[5],
                        validade=row[6],
                        posição=row[7],
                        direção=row[8],
                        endereço=row[9],
                        município_id=row[10],
                        estatuto_id=row[11],
                        nu_contacto=row[12],
                        email=row[13]
                        # Uncomment and handle these fields if necessary
                        # fotografia=row[14] if row[14] else None,
                        # documentos=row[15] if row[15] else None
                    )
                    print(f"Created Funcionariu: {new_member}")
                except IntegrityError as e:
                    print(f"IntegrityError: {e}")
                except Exception as e:
                    print(f"Error creating Funcionariu: {e}")
            
            return render(request, 'success.html')
        else:
            print(f"Form is not valid: {form.errors}")
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def upload_success(request):
    return render(request, 'success.html')


#Gym Class Views
@login_required
def gymclass(request):
    listagymclass = GymClass.objects.all()
    data = {
    'title':"Lista Gym Klasse",
    'active_estudante':"active",
    'dadus':listagymclass
    }
    return render(request, 'listagymclass.html',data)

@login_required
def createGymClass(request):
    form = GymClassForm()

    if request.method == 'POST':
        form = GymClassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gymclass')
    data = {
        'form':form,
        'title':"Formulariu Gym Klasse",
        'page':"form",
    }
    return render(request, 'gymclassform.html',data)

@login_required
def updateGymClass(request, id):
    gymclass= GymClass.objects.get(id=id)
    form = GymClassForm(instance=gymclass)

    if request.method == 'POST':
        form = GymClassForm(request.POST, request.FILES, instance=gymclass)
        if form.is_valid():
            form.save()
            return redirect('gymclass')
    data = {
        'form':form,
        'title':"Formulariu Update Gym Klasse",
        'page':"form",
    }
    return render(request, 'gymclassform.html',data)

@login_required
def deleteGymClass(request,pk):
    gymclass = GymClass.objects.get(id=pk)
    gymclass.delete()
    return redirect('gymclass')

@login_required
def detailGymClass(request,pk):
    gymclassdata = get_object_or_404(GymClass,id=pk)
    data = {
    'title':"Detallu Gym Klasse",
    'gymclassdata':gymclassdata,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'gymclassform.html',data)

@login_required
def csv_gymclass(request):
    # replace with the fields you need 
    fields = ['name','description','start_time','end_time','days_of_week','payment_per_month']
    # Generate the csv file with datetime
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=listagymclass.csv"
    writer = csv.writer(response)
    # Write the header row
    writer.writerow(fields)
    # Use the fields to get the data, specifying the model name
    for row in GymClass.objects.values(*fields):
        writer.writerow([row[field] for field in fields])
        # return
    return response

@login_required
def pdf_gymclass(request):
    gymclass = GymClass.objects.all()
    data = {'dadus':gymclass,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/gymclasspdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

#Enrollments
@login_required
def enrollment(request):
    listaenrollment = Enrollment.objects.all()
    data = {
    'title':"Lista Mmebru Rejistradu",
    'active_estudante':"active",
    'dadus':listaenrollment
    }
    return render(request, 'listaenroll.html',data)

@login_required
def createEnrollment(request):
    form = EnrollmentForm()

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('enrollment')
    data = {
        'form':form,
        'title':"Formulariu Membru Rejistradu",
        'page':"form",
    }
    return render(request, 'enrollform.html',data)

@login_required
def updateEnrollment(request, id):
    enrollment= Enrollment.objects.get(id=id)
    form = EnrollmentForm(instance=enrollment)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, request.FILES, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('enrollment')
    data = {
        'form':form,
        'title':"Formulariu Update Membru Rejistradu",
        'page':"form",
    }
    return render(request, 'enrollform.html',data)

@login_required
def deleteEnrollment(request,pk):
    enrollform = Enrollment.objects.get(id=pk)
    enrollform.delete()
    return redirect('enrollment')

@login_required
def detailEnrollment(request,pk):
    enrolldata = get_object_or_404(Enrollment,id=pk)
    data = {
    'title':"Detallu Membru Rejistradu",
    'enrolldata':enrolldata,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'enrollform.html',data)

@login_required
def csv_enroll(request):
    # Define the fields you want to include in the CSV
    fields = ['member__naran', 'gym_class__name', 'enrollment_date', 'get_total_payment']

    # Generate the CSV file with datetime
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listaenroll.csv"'
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Member Name', 'Gym Class Name', 'Enrollment Date', 'Total Payment'])  # Custom header row

    # Retrieve data from the Enrollment model and write rows to CSV
    enrollments = Enrollment.objects.all()
    for enrollment in enrollments:
        total_payment = enrollment.get_total_payment()  # Calculate total payment using the method
        row = [
            enrollment.member.naran,
            enrollment.gym_class.name,
            enrollment.enrollment_date,
            total_payment if total_payment is not None else ''  # Handle None values gracefully
        ]
        writer.writerow(row)

    return response

@login_required
def pdf_enroll(request):
    enrollment = Enrollment.objects.all()
    data = {'dadus':enrollment,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/enrollpdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None


@login_required
# def dashboard(request):
#     context = {
#         "title":"Dashboard",
#         "active_varanda":"active",
#     }
#     return render(request,'main/dashboard.html',context)

# def dashboard(request):
#     total_member = Member.objects.count()
#     mane = Member.objects.filter(sexo='Mane').count()
#     feto = Member.objects.filter(sexo='Feto').count()
#     context = {
#         'total_member': total_member,
#         'mane': mane,
#         'feto': feto,
#     }
#     return render(request, 'main/dashboard.html', context)
@login_required
class MyPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('password_change_done')

@login_required
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

@login_required
def todays_schedule(request):
    today = date.today().strftime("%A")  # Get current day of the week as string
    classes_today = GymClass.objects.filter(days_of_week__icontains=today)
    
    context = {
        'today': today,
        'classes_today': classes_today,
    }
    return render(request, 'todays_schedule.html', context)

@login_required
def weekly_schedule(request):
    today = date.today()
    week_days = [(today + timedelta(days=i)).strftime("%A") for i in range(7)]  # List of days in the week starting from today
    weekly_classes = {day: GymClass.objects.filter(days_of_week__icontains=day) for day in week_days}
    
    context = {
        'week_days': week_days,
        'weekly_classes': weekly_classes,
    }
    return render(request, 'weekly_schedule.html', context)

@login_required
def member_report(request):
    members = Member.objects.all()
    return render(request, 'member_report.html', {'members': members})

@login_required
def class_report(request):
    classes = GymClass.objects.all()
    return render(request, 'class_report.html', {'classes': classes})

@login_required
def enrollment_report(request):
    enrollments = Enrollment.objects.select_related('member', 'gym_class').all()
    return render(request, 'enrollment_report.html', {'enrollments': enrollments})

@login_required
def charts(request):
	data = {
	'title':"Charts"
	}
	return render(request,'charts.html',data)

@login_required
def chart_seksu_member(request):
	labels = []
	data = []
	queryset = Member.objects.values('sexo').annotate(total_seksu=Count('sexo'))
	for item in queryset:
		labels.append(item['sexo'])
		data.append(item['total_seksu'])
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})

@login_required
def chart_municipiu(request):
	labels = []
	data = []
	queryset = Member.objects.values('municipio__name').annotate(total_municipiu=Count('municipio__name'))
	for item in queryset:
		labels.append(item['municipio__name'])
		data.append(item['total_municipiu'])
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})

@login_required
def profile_view(request, username):
    # Fetch the user based on the username
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})

@login_required
def profile_update(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = UserProfileForm(instance=user.userprofile)
    return render(request, 'profile_update.html', {'form': form})
