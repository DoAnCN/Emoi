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
        fields = ['version',]

class HostSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['name', 'ip', 'port', 'os', 'monitor', 'date_add',
                  'last_alive', 'id_agent']
        read_only_fields = ['name', 'port', 'ip']

class InstanceSerializer(serializers.ModelSerializer):
    project = ProjectSerializerGet(required=False)
    project_ver = VersionSerializerGet(required=False)
    host = HostSerializerGet(required=False)

    class Meta:
        model = Instance
        fields = ['name', 'db_name', 'host', 'project', 'project_ver',
                  'usr_deployed', 'latest_deploy', 'type']
        read_only_fields = ['name', 'db_name', 'host', 'project',
                            'project_ver', 'type']
