from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.core.cache import cache
import requests
# Create your views here.
@api_view(['GET'])
def from_cache(request):
    key = request.GET.get('key')
    if not key:
        return Response('')
    hash = cache.get(key)
    if hash:
        return Response(hash)
    try:
        resp = requests.get(settings.HASH_URL, params={'key': key})
        resp.raise_for_status()
    except:
        return Response('')

    try:
        parse_data = resp.json()
    except ValueError:
        return Response('')

    try:
        hash = parse_data['hash']
    except TypeError:
        return Response('')
    cache.set(key, hash, settings.HASH_TTL)
    return Response(hash)

