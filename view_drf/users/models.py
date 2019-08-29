import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

HAIR_TYPE = (
    ('long','Long'),
    ('short','Short'),
    ('semi-long','Semi-long'),
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

class Cat(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=100)
    mass = models.FloatField()
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    hair = models.CharField(choices=HAIR_TYPE, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

    @staticmethod
    def get_object_by_pk_for_user(pk, user_id):
        cat = Cat.objects.get(pk=pk)
        if str(cat.user_id) == str(user_id):
            return cat
        else:
            return '403'
