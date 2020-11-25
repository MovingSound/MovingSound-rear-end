from django.shortcuts import render
from .__init__ import Http_Response, request_query, send, BASE_URL
from json import loads


def home(request):
    return Http_Response("", "这里是歌曲信息接口", "")


def url(request):
    # 歌曲URL
    query = request_query(request, ["id", "ids"], ["br", {"br": "999000"}])
    query["ids"] = "[" + query["ids"] + "]"
    # data = send({"url": BASE_URL + "api/song/enhance/player/url", "params": query}, "linuxapi").POST("")
    data = send(query).POST("weapi/song/enhance/player/url")
    return Http_Response(request, data.text)
