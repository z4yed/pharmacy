from django.db import models


class Setting(models.Model):
    company_title = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    logo = models.ImageField(upload_to='logo', null=True, blank=True)
    login_background = models.ImageField(upload_to='login_background', null=True, blank=True)
    footer_text = models.TextField(default='Copyright@2021')

    def __str__(self):
        return self.company_title

    @property
    def logo_url(self):
        url = ''
        if self.logo:
            url = self.logo.url
        return url

    @property
    def login_background_url(self):
        url = ''
        if self.login_background:
            url = self.login_background.url
        return url
