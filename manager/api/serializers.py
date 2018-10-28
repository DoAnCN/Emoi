from rest_framework import serializers

from manager.models import Instance, Host, Project, Version
# from rest_framework.serializers import HyperlinkedModelSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'url',
            ]

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = [
            'name',
            ]

class InstanceSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(required=True)
    project_ver = VersionSerializer(required=True)
    class Meta:
        model = Instance
        fields = [
            'name',
            'db_name',
            'host',
            'project',
            'project_ver',
        ]

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields=[
            'name',
            'ip',
            'port',
            'os',
            'num_of_inst',
        ]