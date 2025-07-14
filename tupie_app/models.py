from django.db import models

# Create your models here.
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    iso = models.CharField(max_length=2, null=False)
    name = models.TextField(max_length=100, null=False)
    nicename = models.TextField(max_length=100, null=False)
    iso3 = models.CharField(max_length=3, null=True)
    numcode = models.IntegerField(null=True)
    phonecode = models.IntegerField(null=False)

    class Meta:
        db_table = 'countries'
        managed = False

    def __str__(self):
        return self.name

class Region(models.Model):
    region_name = models.TextField(max_length=100, unique=True)
    region_code = models.IntegerField(primary_key=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='country_id', null=True)

    class Meta:
        db_table = 'regions'
        managed = False

    def __str__(self):
        return self.region_name

class District(models.Model):
    district_name = models.TextField(max_length=100)
    district_code = models.IntegerField(primary_key=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id', to_field='region_code', null=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='country_id', null=True)

    class Meta:
        db_table = 'districts'
        managed = False

    def __str__(self):
        return self.district_name
    
class Ward(models.Model):
    ward_name = models.TextField(max_length=100)
    ward_code = models.IntegerField(primary_key=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, db_column='district_id', to_field='district_code', null=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id', to_field='region_code', null=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE,db_column='country_id', null=True)

    class Meta:
        db_table = 'wards'
        managed = False

    def __str__(self):
        return self.ward_name
    
class Place(models.Model):
    id = models.AutoField(primary_key=True)
    place_name = models.TextField(max_length=100)
    ward_id = models.ForeignKey(Ward, on_delete=models.CASCADE, db_column='ward_id', to_field='ward_code', null=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, db_column='district_id', to_field='district_code', null=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id', to_field='region_code', null=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='country_id', null=True)

    class Meta:
        db_table = 'places'
        managed = False

    def __str__(self):
        return self.place_name
    
class General(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    region = models.TextField(max_length=100, null=True)
    regioncode = models.IntegerField(null=True)
    district = models.TextField(max_length=100, null=True)
    districtcode = models.IntegerField(null=True)
    ward = models.TextField(max_length=100, null=True)
    wardcode = models.IntegerField(null=True)
    street = models.TextField(max_length=100, null=True)
    place = models.TextField(max_length=100, null=True)

    class Meta:
        db_table = 'general'
        managed = False


    def __str__(self):
        return f"{self.region} - {self.district}"
    
class Street(models.Model):
    name = models.TextField(max_length=100, blank=True, null=True)
    general_locations = models.ForeignKey(General, on_delete=models.CASCADE, null=True, related_name='streets')

    def __str__(self):
        return self.name or "No Street"
    


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


