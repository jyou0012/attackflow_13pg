from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class File(models.Model):
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    content = models.BinaryField()

    def __str__(self):
        return self.filename

class WebsiteInfo(models.Model):
    image = models.BinaryField()
    description = models.TextField()

class IncidentReport(models.Model):
    file = models.FileField(upload_to='incident_reports/')
    
    def __str__(self):
        return self.file.name
