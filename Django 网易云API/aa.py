class aa:
    def mm(self,name):
        import urllib.request
        from bs4 import UnicodeDammit, BeautifulSoup
        import urllib
        data = name
        data = urllib.parse.quote(data)
        url='http://47.115.149.151:8888/api/search/mxc?value='+data+'&type=1'
        print(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4209.400"}
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req)
        data = data.read()
        dammit = UnicodeDammit(data, ["utf-8", "gbk"])
        data = dammit.unicode_markup
        soup = BeautifulSoup(data, 'html.parser')
        kk=soup.text
        kkk=kk.split(":",6)
        kkkk=kkk[3]
        kkkkk=kkkk.split(",")
        zxx=kkkkk[0]
        return zxx


