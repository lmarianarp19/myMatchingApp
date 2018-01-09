from django.db import models


class Woman(models.Model):

    # blue = 'blue',
    # red = 'red'
    #
    # colors = (
    #     (blue, 'Blue'),
    #     (red, 'Red'),
    # )
    # color = models.CharField(
    #     max_length=4,
    #     choices=colors
    #     default=blue,
    # )

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



class Man(models.Model):
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
    woman_score = models.IntegerField()
    man_score = models.IntegerField()
    woman = models.ForeignKey('Woman', on_delete=models.CASCADE)
    man = models.ForeignKey('Man', on_delete=models.CASCADE)

class Pairing(models.Model):
    matching = models.ForeignKey('Matching', on_delete=models.CASCADE)

class Matching(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    algorithm = models.CharField(max_length=20)

class Community(models.Model):
    name = models.CharField(max_length=20, unique = True)
    number_couples = models.IntegerField()


    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.name
