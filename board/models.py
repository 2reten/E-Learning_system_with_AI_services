from django.db import models
from django.conf import settings
from django.utils import timezone



class Board(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # 수정됨
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 기존 Question 모델에 Board 연결
class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_question')

    def __str__(self):
        return self.subject

# 기존 Answer 모델에 Board 연결 (선택적)
class Answer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_answer')

# 기존 Comment 모델에 Board 연결 (선택적)
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

# Board_Manage 클래스
class Board_Manage:
    @staticmethod
    def create_board(name, description):
        board = Board(name=name, description=description)
        board.save()
        return board

    @staticmethod
    def delete_board(board_id):
        try:
            board = Board.objects.get(id=board_id)
            board.delete()
            return True
        except Board.DoesNotExist:
            return False


    @staticmethod
    def update_board(board_id, new_name=None, new_description=None):
        try:
            board = Board.objects.get(id=board_id)
            if new_name:
                board.name = new_name
            if new_description:
                board.description = new_description
            board.save()
            return board
        except Board.DoesNotExist:
            return None