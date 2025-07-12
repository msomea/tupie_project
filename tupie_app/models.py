from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.region.name})"
    
class Ward(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.district.name})"
    
class Street(models.Model):
    name = models.CharField(max_length=100)
    street = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.street.name})"
    
class Place(models.Model):
    name = models.CharField(max_length=100, blank=True)
    place = models.ForeignKey(Street, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.place.name})"

class Item(models.Model):
    tittle = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tittle


