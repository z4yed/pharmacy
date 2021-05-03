from django.db import models

RATE_TYPE = (
    (1, 'Hourly'),
    (2, 'Salary'),
)


class Designation(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    rate_type = models.IntegerField(choices=RATE_TYPE, null=True, blank=True)
    salary = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    blood_group = models.CharField(max_length=200, null=True, blank=True)
    first_address = models.CharField(max_length=200, null=True, blank=True)
    second_address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='employees', max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def image_url(self):
        url = ''
        if self.image:
            url = self.image.url
        return url

    @property
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

