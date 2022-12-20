import logging
import sys
import traceback

from json_log_formatter import VerboseJSONFormatter
from logstash_async.handler import AsynchronousLogstashHandler
from django.conf import settings


class CustomisedJSONFormatter(VerboseJSONFormatter):
    def json_record(self, message: str, extra: dict, record):
        context = self.extra_from_record(record)
        try:
            context.pop('request')
        except KeyError:
            pass

        return {
            'message': message,
            'level': record.levelname,
            'app': settings.APP_LABEL + '_' + settings.RUNNING_BRANCH,
            **context
        }


class CustomFilter(logging.Filter):

    def filter(self, record):
        def _get_trace():
            trace = None
            if record.levelname in ['ERROR', 'CRITICAL']:
                type_, value_, traceback_ = sys.exc_info()
                trace = "".join(traceback.format_exception(type_, value_, traceback_))
            return trace if trace else None

        record.trace = _get_trace()
        if self.nlen == 0:
            return True
        elif self.name == record.name:
            return True
        elif record.name.find(self.name, 0, self.nlen) != 0:
            return False
        return record.name[self.nlen] == "."


class CustomHandler(AsynchronousLogstashHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addFilter(CustomFilter())
