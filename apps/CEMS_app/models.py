from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, RegexValidator
from django.TIME_ZONE import DateTimeField
# Create your models here.
MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]


class Participant(models.Model):
    f_name = models.CharField()
    l_name = models.CharField()
    age = models.DateField(verbose_name=('Date of Birth'))
    gender = models.CharField(choices=GENDER_CHOICES, default=MALE)
    email = models.EmailField(max_length=245, unique=True)
    password = models.CharField(max_length=20)
    section = models.CharField(max_length=3)
    session = models.CharField(max_length=3)
    student_id_number = models.IntegerField()
    phone_number = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11), MinValueValidator('03000000000'), RegexValidator(r'[0-9]*', message='only digits are allowed')
        ]
    )
    participation_status = models.CharField()
    student_id = models.CharField(max_length=10)
    username = models.CharField(max_length=12,
        validators==[
            MinLengthValidator(5),
        ]
    )
    status = models.BooleanField()

    def __str__(self):
        return self.email

class Team(models.Model):
    team_lead = models.ForeignKey(Participant, on_delete=models.CASCADE)

class Team_participant(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)

class EventBody(models.Model):
    participant_id = models.ForeignKey(Participant, on_delete= models.CASCADE)
    role = models.CharField()
    position = models.CharField()

class Chairperson(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    gender = models.CharField(choices=GENDER_CHOICES, default=MALE)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11), MinValueValidator('03000000000'), RegexValidator(r'[0-9]*', message='only digits are allowed')
        ]
    )
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=12,
    validators=[
        MinLengthValidator(5)
    ]
    )
    designation = models.CharField(max_length=20)
    status = models.BooleanField() # active or retired from chairperson role


class Event(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField()
    description = models.CharField()
    status = models.CharField() # Archived or active


class Catagory(models.Model):
    title = models.CharField()
    description = models.CharField()
    time_limit =  models.TimeField(blank=True) # time allowed for one round if it is a timed event.
    team_size = models.IntegerField() # number of team members allowed
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)


class Catagory_cordinator(models.Model):
    catagory_id = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)

class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    available = models.IntegerField()
    cost = models.DecimalField()
    damaged = models.IntegerField()

class Requied_items(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
#mahnoor
class Funds(models.Model):
    total_fund = models.DecimalField()
    funds_remaining = models.DecimalField()

class Expenditure(models.Model):
    amount_spent = models.DecimalField()
    purpose = models.CharField(max_length=100)
    eventBody_id = models.ForeignKey(EventBody, on_delete=models.CASCADE)

class Volunteer(models.Model):
    skill = models.CharField(max_length=100)
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)
    eventBody_id = models.ForeignKey(EventBody, on_delete=models.CASCADE)
    available = models.BooleanField()

class Timeslot(models.Model):
    day = models.CharField(max_length=100)
    date = models.DateField()
    timeslot = models.TimeField()

class Available_slots(models.Model):
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)
    timeslot_id = models.ForeignKey(Timeslot, on_delete=models.CASCADE)

class Item_issued(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    catagory_id = models.ForeignKey(Catagory, on_delete=models.CASCADE)quantity = models.IntegerField()
    Catagory_cordinator_id = models.ForeignKey(Catagory_cordinator, on_delete=models.CASCADE)
    time_of_issue = models.DateTimeField()
    return_time = models.DateTimeField()