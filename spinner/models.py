from django.db import models


class SlugContent(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=200)
    content = models.TextField()
    area_type = models.CharField(max_length=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    postcode = models.CharField(max_length=15)
    parent_country = models.IntegerField()
    parent_county = models.IntegerField()
    spinned = models.IntegerField()
    batch = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'slug_content'


class Article(models.Model):
    name = models.CharField(max_length=255, null=True)
    content = models.TextField(null=True)


class Batch(models.Model):
    name = models.CharField(max_length=255, null=True)
    kwargs = models.TextField(null=True)
    number = models.IntegerField( null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    started = models.BooleanField(default=False)
    generated = models.IntegerField( null=True)
