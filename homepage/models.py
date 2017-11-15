from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

# https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser

# 1st keyword argument is the verbose_name which is human readable name, marked for translation with ugettext_lazy
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True, primary_key=True)
    email = models.EmailField(_('email address'), unique=True) #required & unique
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True) #set field to when object is created
    is_active = models.BooleanField(_('active'), default=True)
    trips = models.ManyToManyField('Trip', verbose_name="user's trips") #many-to-many relationship. Use name of model since it is not yet defined
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False, verbose_name="user follows")

    objects = UserManager()

    USERNAME_FIELD = 'username' #telling Django that email field will be used for username
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email'] #remove e-mail from required fields for superusers since it is automatically included as the username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def __str__(self):
        return "username: {}, name: {} {}, email: {}".format(self.username, self.first_name, self.last_name, self.email)

class Trip(models.Model):

    IN_PROGRESS = 'I'
    UPCOMING = 'U'
    COMPLETED = 'C'
    STATUS_CHOICES = (
        (IN_PROGRESS, "In Progress"),
        (UPCOMING, "Upcoming"),
        (COMPLETED, "Completed"),
    )

    name = models.CharField(_('name'), max_length=30, default='Untitled Trip')
    transports = models.ManyToManyField('Transport', verbose_name='transport on trip') #many-to-many relationship
    stops = models.ManyToManyField('Stop', verbose_name='stops on trip') #many-to-many relationship
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default=UPCOMING)
    start_date = models.DateTimeField(_('start date'), blank=True)
    end_date = models.DateTimeField(_('end date'), blank=True)

    def __str__(self):
        return "name: {}, dates: {} - {}".format(self.name, self.start_date, self.end_date)

class Transport(models.Model):

    name = models.CharField(_('name'), max_length=30, blank=True)
    from_address = models.CharField(_('address'), max_length=100, blank=True)
    to_address = models.CharField(_('address'), max_length=100, blank=True)
    start_date = models.DateTimeField(_('start date'), blank=True)
    end_date = models.DateTimeField(_('end date'), blank=True)

    def __str__(self):
        return "name: {}, from: {} to: {}".format(self.name, self.from_address,
            self.to_address)

class Stop(models.Model):
    address = models.CharField(_('address'), max_length=100)
    start_date = models.DateTimeField(_('start date'), blank=True)
    end_date = models.DateTimeField(_('end date'), blank=True)

    def __str__(self):
        return "address: {}, dates: {} - {}".format(self.address, self.start_date, self.end_date)

class Place(models.Model):
    stop = models.ForeignKey('Stop', on_delete=models.CASCADE, verbose_name="related stop") #many-to-one relationship. Each stop has many places, but each place corresponds to 1 stop.
    name = models.TextField(_('name'))
    address = models.CharField(_('address'), max_length=100, blank=True) #allow blank addresses for custom/add later
    info =  models.TextField(_('info'), blank=True)
    # review =

    def __str__(self):
        return "name: {}, address: {}".format(self.name, self.address)


# class PlaceReview(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     place = models.ForeignKey(Place, on_delete=models.CASCADE)
#     review = models.TextField(max_length=500)
#     timestamp = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return "name: {}, place: {}, review: {}".format(self.user, self.place, self.review)




# """
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     trips = models.ManyToManyField(Trip) #many-to-many relationship
#     follows = models.ManyToManyField(self, related_name='followers', symmetrical=False)
#
# # Signals to update Profile automatically when User is updated
# # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# # https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
# """
