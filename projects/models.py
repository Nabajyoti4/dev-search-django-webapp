from django.db import models
import uuid
from users.models import Profile

from django.db.models.deletion import CASCADE

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile,null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    demo_link=models.CharField(max_length=2000, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    source_link=models.CharField(max_length=2000, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-created']


# Review 
class Review(models.Model):
    VOTE_TYPE = (('up', 'Up Vote'), ('down', 'Down Vote'))
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=CASCADE)
    body = models.TextField(null=True, blank=True)
    value=models.CharField(max_length=200, choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.value


# Tag
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.name