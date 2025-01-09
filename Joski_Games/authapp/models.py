from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string

def generate_unique_code():
    length = 10
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(char) for x in range(length))

class User(AbstractUser):
    phone = models.CharField(max_length=12, unique=True)
    code_add_friends = models.CharField(max_length=10, unique=True, null=True, blank=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='friends_set')

    def save(self, *args, **kwargs):
        if not self.code_add_friends:
            self.code_add_friends = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        length = 10
        char = string.ascii_uppercase + string.digits + string.ascii_lowercase
        while True:
            code = ''.join(random.choice(char) for x in range(length))
            if not User.objects.filter(code_add_friends=code).exists():
                break
        return code


class Friendship(models.Model):

    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f'{self.user.username} is friends with {self.friend.username}'