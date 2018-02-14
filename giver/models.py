from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Email(models.Model):
    '''Emails on email list'''
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ['email']

class Charge(models.Model):
    '''The senior we are giving care to.'''
    full_name = models.CharField(max_length=100)
    casual_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Aide(models.Model):
    '''The person operating Fern and giving care to the charge.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname

class PrimaryCaregiver(models.Model):
    '''The person, usually a family member, who has primary responsibility
    for the charge.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    charge = models.OneToOneField(Charge, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.full_name

class Status(models.Model):
    '''A periodic report on what and how the charge is doing.'''
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)
    summary = models.CharField(max_length=240)
    notes = models.TextField(blank=True)
    extras = models.TextField(blank=True)
    timestamp = models.DateTimeField('timestamp', auto_now_add=True)

    def __str__(self):
        return self.summary

class Shift(models.Model):
    '''A period of time when Fern is active for a particular charge.'''
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)
    aide = models.ForeignKey(Aide, on_delete=models.SET_NULL, blank=True, null=True)
    start = models.TimeField('start')
    end = models.TimeField('end')
    repeat = models.CharField(max_length=100)

    def humanize_repeat(self):
        if self.repeat == 'SMTWHFS':
            return 'every day'
        elif self.repeat == 'MTWHF':
            return 'weekdays'
        else:
            return self.repeat

    def __str__(self):
        return '{} from {} to {} {}'.format(self.charge,
            self.start.strftime('%H:%M'),
            self.end.strftime('%H:%M'),
            self.humanize_repeat())
