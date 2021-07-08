from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MinLengthValidator, RegexValidator
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
from . import tokens
import datetime


# Create your models here.

ONLINE = 'online'
OFFLINE = 'offline'
PAYMENT_CHOICES = [
    (ONLINE, 'Online'),
    (OFFLINE, 'Offline'),
]


def upload_to(instance, filename):
    return f'static/media/  {instance.id}-{filename}'


class MyUserManager(BaseUserManager):

    def create_user(self, student_id, email, password, date_of_birth, gender, f_name, l_name, phone_number):
        if student_id is None:
            raise TypeError('User must have a username')
        if email is None:
            raise TypeError('User must have an email')
        if password is None:
            raise TypeError('password cannot be empty')
        if date_of_birth is None:
            raise TypeError('Must enter date of birth')
        if gender is None:
            raise TypeError('Must enter gender')
        if f_name is None:
            raise TypeError('Must enter first name')
        if l_name is None:
            raise TypeError('Must enter last name')
        if phone_number is None:
            raise TypeError('Must enter phone number')

        user = self.model(
            student_id=student_id, email=self.normalize_email(email), date_of_birth=date_of_birth, f_name=f_name,
            l_name=l_name, phone_number=phone_number, gender=gender
        )
        # passwd = make_password(password)
        # print(f' without hash {password} with hash {passwd}')
        # user.set_password(passwd)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, student_id, email, password, date_of_birth, gender, f_name, l_name, phone_number):

        user = self.create_user(
            student_id=student_id, email=email, password=password, date_of_birth=date_of_birth, gender=gender,
            f_name=f_name, l_name=l_name, phone_number=phone_number
        )

        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def get_by_natural_key(self, email_):
        return self.get(email=email_)


class MyUser(AbstractBaseUser, PermissionsMixin):
    f_name = models.CharField(max_length=60, verbose_name='First Name')
    l_name = models.CharField(max_length=60, verbose_name='Last Name')
    date_of_birth = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    gender = models.CharField(max_length=10,)
    email = models.EmailField(max_length=245, unique=True)
    password = models.CharField(max_length=100,
                                validators=[
                                    MinLengthValidator(8),
                                    RegexValidator(
                                        r'(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[=+\-#^*@()&])[(@#)=+&\-*^A-Za-z\d]{8,20}',
                                        message='Must contain at least one uppercase, one lowercase,one special char =+-#^*@()& and one digit.'
                                    )
                                ]
    )
    degree = models.CharField(max_length=3)
    section = models.CharField(max_length=1)
    session = models.CharField(max_length=3)
    student_id_number = models.CharField(
        max_length=3, verbose_name='Student ID Number', help_text='For example in case of BCSF17m048 enter 048',
        validators=[RegexValidator(r'[0-9]*', message='Only digits are allowed')]
    )

    student_id = models.CharField(
        max_length=10, unique=True, verbose_name='Student ID', validators=[MinLengthValidator(10)]
    )
    phone_number = models.CharField(
        max_length=11, unique=True,
        validators=[
            MinLengthValidator(11), MinValueValidator('03000000000'),
            RegexValidator(r'[0-9]*', message='Only digits are allowed')
        ]
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    # has_participated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(_('Image'), null=True, blank=True, upload_to=upload_to)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_id', 'phone_number', 'date_of_birth', 'f_name', 'l_name', 'gender']

    objects = MyUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_age(self):
        return datetime.date.today().year - self.date_of_birth.year

    def get_full_name(self):
        return self.f_name+self.l_name

    def get_short_name(self):
        return self.f_name

    def natural_key(self):
        return self.email

    def get_tokens(self):
        access = tokens.generate_access_token(user=self)
        refresh = tokens.generate_refresh_token(user=self)
        return {
            'refresh_token': str(refresh),
            'access_token': str(access),
        }

    def __str__(self):
        return self.student_id


class Event(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Active')  # Archived or active
    payment_account_number = models.CharField(
        max_length=11, verbose_name='Microfinance Account',
        validators=[
            MinLengthValidator(11), MinValueValidator('03000000000'),
            RegexValidator(r'[0-9]*', message='Only digits are allowed')
        ]
    )

    def __str__(self):
        return self.title + " - " + str(self.start_date.year)


class Game(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    time_limit = models.PositiveSmallIntegerField(
                    help_text='Enter time in minutes only. Leave blank in case of no time limit',
                    null=True, blank=True
    )  # time allowed for one round if it is a timed event.
    team_size = models.IntegerField(default=1)  # number of team members allowed
    registration_fee = models.DecimalField(
        max_digits=5, decimal_places=0, verbose_name='Registration Fee per person', default=0
    )
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return self.title + " | " + self.event_id.title + " - " + str(self.event_id.start_date.year)


class GameCoordinator(models.Model):
    game_id = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=MyUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user_id.student_id + ' | ' + self.game_id.title


class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveSmallIntegerField(verbose_name='Total Items')
    allocated = models.PositiveSmallIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cost per item')
    damaged = models.PositiveSmallIntegerField(verbose_name='Items Damaged', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def available_items(self):
        return self.quantity - (self.allocated + self.damaged)


class Payment(models.Model):
    event_id = models.ForeignKey(to=Event, on_delete=models.DO_NOTHING)
    game_id = models.ForeignKey(to=Game, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(to=MyUser, on_delete=models.DO_NOTHING)
    payment_type = models.CharField(max_length=7, choices=PAYMENT_CHOICES, default=OFFLINE)
    amount = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=False, verbose_name='Payment Status', help_text='Tick if verified')
    submission_date = models.DateTimeField(auto_now_add=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    # year = models.PositiveSmallIntegerField(default=datetime.date.year, blank=True, null=True)
    tid = models.CharField(null=True, blank=True, max_length=15)

    @property
    def username(self):
        return self.user_id.student_id

    def __str__(self):
        return self.game_id.title + " | " + self.user_id.student_id


class Team(models.Model):
    team_lead = models.ForeignKey(to=MyUser, on_delete=models.DO_NOTHING)
    team_name = models.CharField(max_length=60, unique=True)
    team_size = models.PositiveSmallIntegerField(verbose_name='Members in Team')

    def __str__(self):
        return self.team_name


class TeamParticipant(models.Model):
    team_id = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    team_member_id = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)


class TeamEnrolment(models.Model):
    team_id = models.ForeignKey(to=Team, on_delete=models.DO_NOTHING)
    game_id = models.ForeignKey(to=Game, on_delete=models.DO_NOTHING)


class RequiredItems(models.Model):
    item_id = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Media(models.Model):
    event_id = models.ForeignKey(to=Event, on_delete=models.DO_NOTHING)
    url = models.TextField(null=True, blank=True)
    image = models.ImageField(_('Image'), null=True, blank=True, upload_to=upload_to)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    skill = models.CharField(max_length=100)
    user_id = models.ForeignKey(to=MyUser, on_delete=models.DO_NOTHING, help_text='Volunteer', verbose_name='Volunteer')
    available = models.BooleanField()

    def __str__(self):
        return self.user_id.student_id


class Expenditure(models.Model):
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=100)
    staff_id = models.ForeignKey(to=MyUser, on_delete=models.DO_NOTHING)


class ItemIssued(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    game_id = models.ForeignKey(to=Game, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField
    game_coordinator_id = models.ForeignKey(to=GameCoordinator, on_delete=models.DO_NOTHING)
    time_of_issue = models.DateTimeField()
    return_time = models.DateTimeField()
    damaged = models.PositiveSmallIntegerField(help_text='Items found damaged on return', verbose_name='Damaged Items')
