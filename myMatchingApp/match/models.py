from django.db import models


class Red(models.Model):

    name =  models.CharField(max_length=50)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    pairing = models.ForeignKey('Pairing', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = (("community", "name"),)

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.name



class Blue(models.Model):
    name = models.CharField(max_length=50)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    pairing = models.ForeignKey('Pairing', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = (("community", "name"),)


    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.name

class Ranking(models.Model):
    red_to_blue_score = models.IntegerField(null=True)
    blue_to_red_score = models.IntegerField(null=True)
    red = models.ForeignKey('Red', on_delete=models.CASCADE)
    blue = models.ForeignKey('Blue', on_delete=models.CASCADE )
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.name

class Pairing(models.Model):
    matching = models.ForeignKey('Matching', on_delete=models.CASCADE)
    # def __str__(self):
    #     """
    #     String for representing the MyModelName object (in Admin site etc.)
    #     """
    #     return self.matching.community

class Matching(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    SG_BLUE_PROPOSE = 'SGBP'
    SG_RED_PROPOSE = 'SGRP'
    ALGORITHM_CHOICES = (
        (SG_BLUE_PROPOSE, 'Shapley Gale Blue Propose'),
        (SG_RED_PROPOSE, 'Shapley Gale Red Propose'),
    )
    algorithm = models.CharField(max_length=10,
    choices=ALGORITHM_CHOICES,
    default=SG_BLUE_PROPOSE
    )
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.name
# TODO poner un status ready para ver si todas las personas ya pusieron el ranking


class Community(models.Model):
    name = models.CharField(max_length=20, unique = True)
    number_couples = models.IntegerField()


    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.name
