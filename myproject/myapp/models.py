from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    selected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если тема уже выбрана другим пользователем, не позволяем её выбрать
        if self.selected_by:
            existing_topic = Topic.objects.filter(selected_by=self.selected_by).exclude(id=self.id)
            if existing_topic.exists():
                raise ValueError("Вы уже выбрали тему.")
        super().save(*args, **kwargs)

class Document(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic.name} - {self.user.username}"