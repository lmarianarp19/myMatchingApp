from django.db import models

class Community(models.Model):
    number_couples: models.IntegerField()

class Woman(models.Model):
    name =  models.CharField(max_length=50)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    pairing = models.ForeignKey('Pairing', on_delete=models.CASCADE)

class Man(models.Model):
    name = models.CharField(max_length=50)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    pairing = models.ForeignKey('Pairing', on_delete=models.CASCADE)

class Ranking(models.Model):
    woman_score = models.IntegerField()
    man_score = models.IntegerField()
    woman = models.ForeignKey('Woman', on_delete=models.CASCADE)
    man = models.ForeignKey('Man', on_delete=models.CASCADE)

class Pairing(models.Model):
    matching = models.ForeignKey('Matching', on_delete=models.CASCADE)

class Matching(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    algorithm = models.CharField(max_length=20)
