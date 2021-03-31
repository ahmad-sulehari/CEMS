from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, RegexValidator

# linux sha 8e5af78e93424336f787d4dd0fdd89b429675d5ae67b1c1634ea1b53c5650677
# Create your models here.
MALE = 'male'
FEMALE = 'female'
OTHER = 'other'
GENDER_CHOICES = [
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
]


class Person(models.Model):
    f_name = models.CharField(max_length=60)
    l_name = models.CharField(max_length=60)
    age = models.DateField(verbose_name='Date of Birth')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    email = models.EmailField(max_length=245, unique=True)
    password = models.CharField(max_length=20,
                                validators=[
                                    MinLengthValidator(8),
                                    RegexValidator(r'(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[=+\-#^*@()&])[(@#)=+&\-*^A-Za-z\d]{8,20}',
                                    message='Must contain at least one uppercase, one lowercase,one special char =+-#^*@()& and one digit.')
                                ]
                                )
    degree = models.CharField(max_length=3, default='BCS')
    section = models.CharField(max_length=1)
    session = models.CharField(max_length=3)
    student_id_number = models.CharField(max_length=3,
                                         validators=[
                                             RegexValidator(r'[0-9]*', message='Only digits are allowed')
                                         ]
                                         )
    phone_number = models.CharField(
        max_length=11, unique=True,
        validators=[
            MinLengthValidator(11), MinValueValidator('03000000000'),
            RegexValidator(r'[0-9]*', message='Only digits are allowed')
        ]
    )
    username = models.CharField(max_length=10, unique=True,
                                validators=[
                                    MinLengthValidator(10),
                                ]
                                )
    verification_status = models.BooleanField(default=False)
    participation_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Team(models.Model):
    team_lead = models.ForeignKey(Person, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=60)


class TeamParticipant(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    team_member_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    team_size = models.IntegerField(verbose_name='Members in Team')


class EventBody(models.Model):
    participant_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=60)
    position = models.CharField(max_length=60)


class Chairperson(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11), MinValueValidator('03000000000'),
            RegexValidator(r'[0-9]*', message='only digits are allowed')
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
    status = models.BooleanField()  # active or retired from chairperson role


class Event(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=256)
    description = models.TextField()
    status = models.BooleanField()  # Archived or active


class Category(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    time_limit = models.TimeField(blank=True)  # time allowed for one round if it is a timed event.
    team_size = models.IntegerField()  # number of team members allowed
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)


class CategoryCoordinator(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    event_body_member_id = models.ForeignKey(EventBody, on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    available = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    damaged = models.IntegerField()


class RequiredItems(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Funds(models.Model):
    total_fund = models.DecimalField(max_digits=10, decimal_places=2)
    funds_remaining = models.DecimalField(max_digits=10, decimal_places=2)


class Expenditure(models.Model):
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=100)
    eventBody_id = models.ForeignKey(EventBody, on_delete=models.CASCADE)


class Volunteer(models.Model):
    skill = models.CharField(max_length=100)
    participant_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    eventBody_id = models.ForeignKey(EventBody, on_delete=models.CASCADE)
    available = models.BooleanField()


class Timeslot(models.Model):
    day = models.CharField(max_length=100)
    date = models.DateField()
    timeslot = models.TimeField()


class BookedSlots(models.Model):
    participant_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    timeslot_id = models.ForeignKey(Timeslot, on_delete=models.CASCADE)


class ItemIssued(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    category_coordinator_id = models.ForeignKey(CategoryCoordinator, on_delete=models.CASCADE)
    time_of_issue = models.DateTimeField()
    return_time = models.DateTimeField()
