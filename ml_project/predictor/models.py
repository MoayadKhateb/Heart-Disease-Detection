from django.db import models

class Prediction(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    cp = models.CharField(max_length=50)
    trestbps = models.IntegerField()
    chol = models.IntegerField()
    fbs = models.CharField(max_length=5)
    restecg = models.CharField(max_length=50)
    thalch = models.IntegerField()
    exang = models.CharField(max_length=5)
    oldpeak = models.FloatField()
    slope = models.CharField(max_length=20)
    ca = models.IntegerField()
    thal = models.CharField(max_length=50)
    result = models.CharField(max_length=20)
    probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Positive' if self.result == 'Positive' else 'Negative'} - {self.created_at}"
