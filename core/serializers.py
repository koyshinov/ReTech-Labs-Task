from django.http import Http404
from core.models import Task
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=True, allow_null=True)
    assignee = serializers.PrimaryKeyRelatedField(read_only=True)
    organization = serializers.PrimaryKeyRelatedField(read_only=True)
    deadline = serializers.DateTimeField(allow_null=True)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)

    def create(self, validated_data):
        request = self.context['request']
        assignee = request.user.profile
        organization = assignee.organiz_login
        validated_data.update({"assignee": assignee, "organization": organization})
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']
        assignee = request.user.profile
        organization = assignee.organiz_login
        if instance.assignee != assignee or instance.organization != organization:
            raise Http404
        else:
            instance.name = validated_data.get("name", instance.name)
            instance.description = validated_data.get("description", instance.description)
            instance.deadline = validated_data.get("deadline", instance.deadline)
            instance.status = validated_data.get("status", instance.status)
            instance.priority = validated_data.get("priority", instance.priority)
            instance.save()
        return instance

    class Meta:
        model = Task
        fields = ("id", "name", "description", "assignee", "organization", "deadline", "status", "priority")
