import ast

from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj:
            return {'value': obj, 'display_name': self._choices[obj]}
        return obj


class MultipleChoiceField(serializers.MultipleChoiceField):

    def to_internal_value(self, data):
        if isinstance(data, str) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        return list(
            item for item in data
        )

    def to_representation(self, value):
        try:
            value = ast.literal_eval(str(value))
        except (ValueError, SyntaxError):
            value = [value, ]
        result = list(
            {
                'value': item,
                'display_name': self.get_display_name(item)
            } for item in value
        )
        return result

    def get_display_name(self, item):
        choices = self.choices
        try:
            return next(choices[choice] for choice in choices if choice == item)
        except StopIteration:
            return item

