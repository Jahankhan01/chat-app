import uuid
from django.db import models
from django.contrib.auth.models import User



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class Conversation(BaseModel):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    class Meta:
        db_table = 'Conversation'
    
    def __str__(self):
        return self.name


class ConversationMessage(BaseModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    tagged_message = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='tagged_messages')

    class Meta:
        db_table = 'ConversationMessage'

