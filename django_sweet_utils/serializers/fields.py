from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj:
            return {'value': obj, 'display_name': self._choices[obj]}
        return obj
