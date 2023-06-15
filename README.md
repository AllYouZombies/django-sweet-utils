# Django sweet utils.

[![Downloads](https://static.pepy.tech/personalized-badge/django-sweet-utils?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/django-sweet-utils)
  
A little django code sugar.
  
> If you find this package useful, please star it on [GitHub](https://github.com/AllYouZombies/django-sweet-utils).
  
## Quickstart

1. Add `django_sweet_utils` to your `INSTALLED_APPS` setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'django_sweet_utils',
        ...
    ]
    ```

2. Inherit your models from `django_sweet_utils.db.models.Model`:
   ```
   from django_sweet_utils.db.models import Model
   
   
   class MyModel(Model):
      ...
   ```
   
   From now your models has the following fields:
      - `uuid4` as object id;
      - `created_at` as object creation time;
      - `updated_at` as object last update time;
      - `is_deleted` as indicator that object is deleted or not;  
     
     
   Models that inherited from `django_sweet_utils.db.models.Model` can be filtered with simple `existing()` property:
   ```
   from django_sweet_utils.db.models import Model
   
   
   class MyModel(Model):
      ...
   
   
   queryset = MyModel.objects.existing()
   ```
   This returns queryset filtered by `is_deleted=False`

   Also, now you don't need to catch `DoesNotExist` error when attempting to get some object while it does not exist.
   Just use `get_or_none()` instead of `get()` and query returns `None` if there is no object.


## Features

### Models

#### Fake deletion

You can delete your objects without actual database deletion.
Just use `delete()` method on your model instance and it will be marked as deleted with `is_deleted=True`:

To perform actual deletion use `hard_delete()` method instead.

#### UUID4 as object id

Every model instance has `uuid4` field as object id.

#### Created and updated time

Every model instance has `created_at` and `updated_at` fields as object creation and last update time.

#### Existing objects

You can get only existing objects with `existing()` property on your model manager.

```python
queryset = MyModel.objects.existing()
```

#### Get or none

You can get object or `None` if it does not exist with `get_or_none()` method on your model manager.

```python
obj = MyModel.objects.get_or_none(pk=1)
```

### API

#### Views

Inherit your DRF API views from `django_sweet_utils.api.views`:  
  
```
from django_sweet_utils.api.views import UpdateAPIView, DestroyAPIView


class MyUpdateView(UpdateAPIView):
   ...


class MyDestroyView(DestroyAPIView):
   ...
```
  
#### Pagination

There is `PageNumberPagination` class that adds `page_size` query parameter to `PageNumberPagination` class.  
  
```python
REST_FRAMEWORK = {
   ...
   'DEFAULT_PAGINATION_CLASS': 'django_sweet_utils.api.pagination.PageNumberPagination',
   'PAGE_SIZE': 10,
   ...
}
```
  
From now your views supports `POST` request method instead of `PATCH` and `DELETE`
DestroyAPIView does not perform actual database deletion, but only marks file as deleted with `is_deleted=True`
  
### Permissions

#### There is `DjangoModelPermissions` class that adds `view` permission to `DjangoModelPermissions` class on `GET` request method.

### Admin

Hard deletion action for admin panel.

```python
from django_sweet_utils.admin import hard_delete_selected

class MyModelAdmin(admin.ModelAdmin):
    actions = [hard_delete_selected]
```

### Seriliazers

#### Prettier choice field

You can use custom `ChoiceField` instead of `ChoiceField` from `rest_framework` to get prettier choices representation in API.

```python
from django_sweet_utils.api.serializers import ChoiceField

class MySerializer(serializers.ModelSerializer):
    my_field = ChoiceField(choices=MY_CHOICES)
```

#### Prettier multiple choice field

You can use custom `MultipleChoiceField` instead of `MultipleChoiceField` from `rest_framework` to get prettier choices representation in API.

```python
from django_sweet_utils.api.serializers import MultipleChoiceField

class MySerializer(serializers.ModelSerializer):
    my_field = MultipleChoiceField(choices=MY_CHOICES)
```

### Template tags

#### `format_string` template tag

You can use `format_string` template tag to format string with arguments.

```html
{% load django_sweet_utils %}

{{ "Hello, {0}!".format_string("World") }}
```

#### `set_query_string_param` template tag

You can use `set_query_string_param` template tag to set query string parameter.

```html
{% load django_sweet_utils %}

{% set_query_string_param "page" 1 %}
```

More info about this tag you can find [here](django_sweet_utils/templatetags/query_string.py).


### Logging

#### Customised JSON formatter

There is `CustomisedJSONFormatter` class that formats log records as JSON.

```python
from django_sweet_utils.logging import CustomisedJSONFormatter

APP_LABEL = "my_app"
ENVIRONMENT = "production"

formatter = CustomisedJSONFormatter()
```

#### Customised JSON handler

There is `CustomHandler` class that handles log records as JSON.

```python
from django_sweet_utils.logging import CustomHandler

handler = CustomHandler()
```


### Misc

#### Custom JSON encoder

You can use `LazyEncoder` to serialize lazy objects to JSON.

```python
from django_sweet_utils.misc import LazyEncoder

json.dumps({"lazy": lazy_object}, cls=LazyEncoder)
```

