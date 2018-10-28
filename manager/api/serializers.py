from rest_framework import serializers

from manager.models import Instance, Host, Project, Version

class ProjectSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'url',]
        read_only_fields = ['name', 'url', ]

class VersionSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['name',]
        read_only_fields = ['name',]

class HostSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields=['name', 'ip', 'port',]
        read_only_fields = ['name', 'ip', 'port',]

class InstanceSerializer(serializers.ModelSerializer):
    project = ProjectSerializerGet(required=False)
    project_ver = VersionSerializerGet(required=False)
    host = HostSerializerGet(required=False)

    class Meta:
        model = Instance
        fields = ['name', 'db_name', 'host', 'project', 'project_ver',
                  'usr_deployed', 'latest_deploy',]
        read_only_fields = ['name', 'db_name', 'host',
                            'project', 'project_ver',]
