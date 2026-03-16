from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):

    COMPANY_CHOICES = [
        ('TCS', 'TCS'),
        ('WIPRO', 'Wipro'),
        ('INFOSYS', 'Infosys'),
        ('ACCENTURE', 'Accenture'),
    ]

    SECTION_CHOICES = [
        ('QUANT', 'Quantitative'),
        ('REASON', 'Reasoning'),
        ('VERBAL', 'Verbal')
    ]

    company = models.CharField(max_length=50, choices=COMPANY_CHOICES, default='TCS')
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)

    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.company} - {self.section} - {self.question}"


class Score(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username