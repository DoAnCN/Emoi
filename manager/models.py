# -*- codding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.http import Http404

# STATUS_CHOICES = (
#     ('a', 'Active'),
#     ('p', 'Pending'),
#     ('i', 'Inactive'),
# )
STATUS_CHOICES = (
    ('a', 'Active'),
    ('p', 'Pending'),
    ('n', 'Never Connected'),
)
INSTANCE_TYPES = (
    ('i', 'Integration'),
    ('s', 'Staging'),
    ('p', 'Production'),
)
# Create your models here.
class Host(models.Model):
    name = models.CharField('Host Name', max_length=200, unique=True)
    ip = models.GenericIPAddressField('IP Address', unique=True)
    port = models.CharField('Port SSH', max_length=10)
    os = models.CharField('Operating System', max_length=200, null=True)
    num_of_inst = models.IntegerField('Number of Instance', default=0)
    monitor = models.CharField('Status', max_length=20, choices=STATUS_CHOICES,
                               default='n')
    date_add = models.DateTimeField('Date add', null=True)
    last_alive = models.DateTimeField('Last Keep Alive', null=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField('Project Name', max_length=200, unique=True)
    url = models.TextField('Remote URL')
    def __str__(self):
        return self.name

class Version(models.Model):
    name = models.CharField('Version Name', max_length=100, blank=True)
    version = models.CharField('Project Version', max_length=10)
    project = models.ForeignKey('Project', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = '{0}/{1}'.format(self.version, self.project)
        super(Version, self).save(*args, **kwargs)

class Instance(models.Model):
    name = models.CharField('Instance Name',max_length=200, unique=True)
    db_name = models.CharField('Database Name', max_length=200)
    domain = models.CharField('Domain Name', max_length=200)
    usr_deployed = models.CharField('User Deployed',
                                    max_length=200, blank=True)
    status = models.BooleanField('Status', default=False)
    latest_deploy =  models.DateTimeField('Latest Deploy', null=True,)
    project = models.ForeignKey('Project', default=None,
                                on_delete=models.PROTECT)
    host = models.ForeignKey('Host', on_delete=models.PROTECT)
    project_ver = models.ForeignKey('Version',
                                on_delete=models.PROTECT)
    type = models.CharField('Type', max_length=200, choices=INSTANCE_TYPES)
    def __str__(self):
        return self.name

    def get_proj_id(self):
        try:
            project = Project.objects.get(name = self.project)
            return project.id
        except Project.DoesNotExist:
            raise Http404("Project does not exist")

    def _count_instance(self):
        try:
            host = Host.objects.get(name = self.host)
            host.num_of_inst = Instance.objects.filter(host = host.id).count()
            host.save()
        except Host.DoesNotExist:
            raise Http404("Host does not exist")

    def save(self, *args, **kwargs):
        super(Instance, self).save(*args, **kwargs)
        self._count_instance()
