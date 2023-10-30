from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    job= jobs.objects.all()[:3]
    return render(request,'index.html',{"jobs":job})


def register_candidate(request):   

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mothers_name = request.POST['mothers_name']
        fathers_name = request.POST['fathers_name']
        address = request.POST.get('address', '')
        gender = request.POST['inlineRadioOptions']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        DOB = request.POST['DOB']
        email = request.POST['email']
        username = request.POST['username']
        qualification = request.POST['qualification']
        stream = request.POST['stream']
        skills = request.POST['skills']
        UDID  = request.POST['UDID']
        functional_difficulties  = request.POST['functional_difficulties']
        assistive_device  = request.POST['assistive_device']
        human_assistance  = request.POST['functional_difficulties']
    

        
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'email is already registered. Please use a different email address.')
                return redirect('register_candidate')
            
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username already exists. Please try different username.')
                return redirect('register_candidate')
            
            else:
                user = User.objects.create_user(username=username,email=email,password=password, first_name=first_name, last_name=last_name,)
                user.save()
                
                candidate_profile = CandidateProfile.objects.create(user=user,mothers_name=mothers_name,
                                                fathers_name=fathers_name,address=address,pincode=pincode,DOB=DOB,stream=stream ,
                                                skills=skills,UDID=UDID,functional_difficulties=functional_difficulties,
                                                assistive_device=assistive_device,human_assistance=human_assistance)
                candidate_profile.save()
                
                messages.success(request, 'You are now registered and can log in')
                return redirect('index')
            
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register_candidate')
    else:
        return render(request, 'register_candidate.html')

    


def register_employer(request):   

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        organization_name = request.POST['organization_name']
        organization_address = request.POST.get('organization_address', '')
        organization_type = request.POST['inlineRadioOptions']
        # state = request.POST['state']
        # city = request.POST['city']
        pincode = request.POST['pincode']
        DOB = request.POST['DOB']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'email is already registered. Please use a different email address.')
                return redirect('register_employer')
            
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username already exists. Please try different username.')
                return redirect('register_employer')
            
            else:
                user = User.objects.create_user(username=username,email=email,password=password, first_name=first_name, last_name=last_name,)
                user.save()
                
                employer_profile = employerProfile.objects.create(user=user,organization_name=organization_name
                                                ,organization_address=organization_address,organization_type=organization_type,pincode=pincode,DOB=DOB)
                employer_profile.save()
                
                messages.success(request, 'You are now registered and can log in')
                return redirect('index')
            
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register_candidate')
    else:
        return render(request, 'register_employer.html')


def candidate_login (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(f"Username: {username}")
        print(f"Password: {password}")

        user= authenticate(username=username,password=password)

        print (f"user= {user}")
        if user is not None:
            auth.login(request,user)
            return redirect('candidate_home')
        
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('candidate_login')
       
    else:    
        return render(request,'candidate_login.html')

def employer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(f"Username: {username}")
        print(f"Password: {password}")

        user= authenticate(username=username,password=password)

        print (f"user= {user}")
        if user is not None:
            auth.login(request,user)
            return redirect('employer_home')
        
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('employer_login')
       
    else:    
        return render(request,'employer_login.html')
@login_required(login_url="employer_login")
def employer_home(request):
    query=None
    posted_job = None
    if request.method == 'POST':
        organization_name = request.POST['organization_name']
        organization_type = request.POST['organization_type']
        job_title = request.POST['job_title']
        job_description = request.POST['job_description']
        openings=request.POST['openings']
        location = request.POST['location']
        
        job= jobs.objects.create(organization_name=organization_name, organization_type=organization_type
                                 ,job_title=job_title,job_description=job_description,
                                 openings=openings,location=location)
        job.save()
        
        posted_job = Posted_job.objects.create(employer=request.user,job=job)
        posted_job.save()
        
        
        messages.success(request, 'Job Posted successfully!!')
        return redirect('employer_home')
    else:
        return render(request, 'employer_home.html',)
    

@login_required(login_url="employer_login")
def posted_job(request):
   
    posted_job=None
    job_applicants = []
    posted_job = Posted_job.objects.filter(employer=request.user)
    query = [job.job for job in posted_job]
    for job in query:
            
            applicants = Application.objects.filter(job=job.id)
            job_applicants.append({'job': job.job_title, 'applicants': applicants})

    return render(request, 'posted_job.html',{'posted_job':query})

@login_required(login_url="employer_login")
def applicants(request,job_id):
   
   job = jobs.objects.get(id=job_id)
   applicants = Application.objects.filter(job=job)

   return render(request, 'posted_job.html', {'applicants': applicants, 'job': job})
    

    
@login_required(login_url="candidate_login")    
def apply_job(request, job_id):
    job = jobs.objects.get(id=job_id)
    application = None
    if request.method == 'POST':
        application = Application.objects.create(candidate=request.user, job=job)
        application.save()
        return redirect('jobs_page')
    return render(request, 'apply_job.html', {'job': job})




# @login_required(login_url="candidate_login")
# def applied_jobs(request):
#     # Get all applications for the current candidate
#     applications = Application.objects.filter(candidate=request.user)

#     # Get the jobs associated with the applications
#     applied_jobs = [app.job for app in applications]

#     return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs})
    
def logout_page(request):
    auth.logout(request)
    return redirect('index')

@login_required(login_url="candidate_login")
def candidate_home (request):
    job= jobs.objects.all()[:3]
    return render(request, 'candidate_home.html',{"jobs":job})

def previous_Year_questions(request):
    PYQ = PYQs.objects.all()
    return render(request,'Previous_Year_questions.html', {"PYQs":PYQ})


def jobs_page(request):
    # applications = Application.objects.filter(candidate=request.user)
    job= jobs.objects.all()
    # return render(request,'jobs_page.html',{"jobs":job,"applications":applications})
    if request.user.is_authenticated:
        applications = Application.objects.filter(candidate=request.user)
        applied_jobs = [app.job for app in applications]
        return render(request,'jobs_page.html',{"jobs":job , "applied_jobs": applied_jobs})
    else:
        return render(request,'jobs_page.html',{"jobs":job })



