from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_link = models.CharField(max_length=255, unique=True, null=True, blank=True)
    pseudo = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


    @staticmethod
    def generate_unique_link():
        from uuid import uuid4
        unique_link = str(uuid4())[:32]
        while Profile.objects.filter(unique_link=unique_link).exists():
            unique_link = str(uuid4())[:32]
        return unique_link
    

    def save(self, *args, **kwargs):
        if not self.unique_link:
            self.unique_link = Profile.generate_unique_link()
        if not self.pseudo:
            self.pseudo = self.user.username
        super().save(*args, **kwargs)


    

class AnonymousMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    readden = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"Message to {self.profile.user.username}"
