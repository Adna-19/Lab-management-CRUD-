from django.db import models
from django.template.defaultfilters import slugify

class MalePatientsManager(models.Manager):
    def get_queryset(self):
        return super(MalePatientsManager, self).get_queryset().filter(gender='Male')

class FemalePateintsManager(models.Manager):
    def get_queryset(self):
        return Patient.objects.filter(gender='Female')

class Patient(models.Model):

    GENDER_CHOICES = (
        ('Male', 'MALE'), 
        ('Female', 'FEMALE')
    )

    MARITAL_STATUS_CHOICES = (
        ('Married', 'MARRIED'),
        ('Divorced', 'DIVORCED'),
        ('Single', 'SINGLE'),
        ('Engaged', 'ENGAGED')
    )

    objects = models.Manager()        # default manager
    males   = MalePatientsManager()   # manage male patients
    females = FemalePateintsManager() # manage female patients

    slug            = models.SlugField(max_length=70, db_index=True)
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    cnic            = models.CharField(max_length=14, unique=True)
    image           = models.ImageField(upload_to='images/', blank=True, null=True)
    address         = models.CharField(max_length=200)
    contact         = models.CharField(max_length=12, unique=True)
    email           = models.EmailField(null=True)
    marital_status  = models.CharField(choices=MARITAL_STATUS_CHOICES, max_length=100) 
    gender          = models.CharField(choices=GENDER_CHOICES, max_length=6)
    date_of_birth   = models.DateField()
    surgery_date    = models.DateField()
    recovery_date   = models.DateField()
    surgery         = models.CharField(max_length=100, blank=True, null=True)
    surgery_details = models.TextField()
    
    class Meta:
        ordering = ('-surgery_date',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name) + slugify(self.cnic)
        super(Patient, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return self.first_name