import json
import logging
import traceback

from json_log_formatter import VerboseJSONFormatter
from logstash_async.handler import AsynchronousLogstashHandler


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
            'app': 'ras-main',
            **context
        }


class CustomFilter(logging.Filter):

    def filter(self, record):
        def _get_trace():
            trace = None
            if record.levelname in ['ERROR', 'CRITICAL']:
                # Get the recent stack-trace
                exc = traceback.format_exc().strip()
                if exc[0:len('NoneType: None')] != 'NoneType: None':
                    trace = exc
            return json.dumps(trace) if trace else None

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
