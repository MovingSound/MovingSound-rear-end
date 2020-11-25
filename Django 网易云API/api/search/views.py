from django.shortcuts import render
from .__init__ import *


def home(request):
    # type:  1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单, 1002: 用户, 1004: MV, 1006: 歌词, 1009: 电台, 1014: 视频
    query = request_query(request,
                          ["value", "s"],
                          ["type", {"type": 1}],
                          ["limit", {"limit": 10}],
                          ["offset", {"offset": 0}])
    if query["s"]:
        data = send(query).POST("weapi/search/get")
        return Http_Response(request, data.text)
    return Http_Response("", "这里是搜索API", "")