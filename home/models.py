from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    job = models.CharField(max_length=50)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True, null=True, related_name='employees')
    
    def __str__(self) -> str:
        return self.name
    
class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_leader = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='team_leader')
    
    def __str__(self) -> str:
        return self.team_name
    
