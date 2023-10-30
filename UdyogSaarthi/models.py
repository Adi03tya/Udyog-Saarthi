from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class CandidateProfile(models.Model):
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mothers_name = models.CharField(max_length=255, blank=True)
    fathers_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    # gender =  models.CharField(max_length=1, choices=GENDER_CHOICES)
    # state =models.TextChoices()
    # city =models.TextChoices()
    pincode = models.IntegerField()
    DOB =models.DateField()
    # qualification = models.TextChoices()
    stream= models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    UDID = models.IntegerField()
    functional_difficulties  = models.TextField(max_length=200)
    assistive_device = models.CharField(max_length=100)
    human_assistance =models.CharField(max_length=100)
    # Add other custom fields here

    def __str__(self):
        return self.user.username
    
class employerProfile(models.Model):
    ORGANIZATION_CHOICES = (
        ( 'Private','Private'),
        ( 'Government','Government'),
        ( 'PSU','PSU'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255, blank=True)
    organization_address = models.TextField(blank=True)
    organization_type =  models.CharField(max_length=10, choices=ORGANIZATION_CHOICES)
    pincode = models.IntegerField()
    DOB =models.DateField()

    def __str__(self):
        return self.user.username


class PYQs(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to="files")

class jobs(models.Model):
   
    ORGANIZATION_CHOICES = (
        ( 'Private','Private'),
        ( 'Government','Government'),
        ( 'PSU','PSU'),
    )
    organization_name=models.CharField(max_length=100)
    organization_type =  models.CharField(max_length=10, choices=ORGANIZATION_CHOICES)
    job_title=models.CharField(max_length=100)
    job_description = models.TextField(max_length=500)
    openings = models.IntegerField()
    location = models.CharField(max_length=100)
    

    def __str__(self):
        return self.job_title

class Posted_job(models.Model):
    employer=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.ForeignKey(jobs,on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.employer.username} posted {self.job.job_title}"

class Application(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(jobs, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} applied for {self.job.job_title}"