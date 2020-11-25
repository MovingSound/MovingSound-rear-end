from django.shortcuts import render
from .__init__ import *


# def user_playlist(uid, cookies, offset=0, limit=50):
#     return send(dict(uid=uid, offset=offset, limit=limit, csrf_token=cookies["__csrf"])).post("weapi/user/playlist")


def home(request):
    return Http_Response("", "这是API", "")
