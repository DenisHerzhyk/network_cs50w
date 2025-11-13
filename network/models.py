from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_text

class Like(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def __str__(self):
        return f"{self.creator.username} liked {self.post.id}"

class UserFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_curr")
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")

    def __str__(self):
        return f"{self.user.username} followed {self.user_following.username}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment