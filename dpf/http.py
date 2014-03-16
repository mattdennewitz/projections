import decimal
import json

from django.http import HttpResponse

from projections.models import PlayerContainer


class JsonEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, decimal.Decimal):
            return round(float(value), 2)
        if isinstance(value, (tuple, PlayerContainer)):
            raise Exception, value._asdict()
        return value



class JsonResponse(HttpResponse):

    def __init__(self, content='', status=None):
        super(JsonResponse, self).__init__(
            content=json.dumps(content, cls=JsonEncoder),
            status=status,
            content_type='application/json')
