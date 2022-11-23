import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Manager(models.Manager):
    """ Base manager with the following additions:
        - 'existing()' method that filters queryset by 'is_deleted=False'
    """
    def get_queryset(self):
        return super(Manager, self).get_queryset()

    def existing(self):
        return self.filter(is_deleted=False)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Model(models.Model):
    """ Base model with the following additions:
        - uuid4 as object id;
        - created_at as object creation time;
        - updated_at as object last update time;
        - is_deleted as indicator that object is deleted or not;
     """

    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    objects = Manager()

    class Meta:
        abstract = True

