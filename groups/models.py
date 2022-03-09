from django.db import models
from django.conf import settings
from datetime import datetime


User = settings.AUTH_USER_MODEL

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=12)
    members = models.ManyToManyField(User, related_name='groups', blank=True)
    admins = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_user_in_group(self, request, pk):
        group = Group.objects.get(id=pk)
        if group.members.filter(id=request.user.id).exists():
            return True
        return False

    def is_token_valid(self, pk, token):
        group = Group.objects.get(id=pk)
        try:
            token = group.invitation_tokens.get(token=token)
            if (datetime.now() - token.created_at).days >= 1:
                return False
            return True
        except:
            return False


class GroupInvitationToken(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitation_tokens')
    token = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)