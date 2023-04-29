import requests, time, urllib.request, re, json, sys
from bs4 import BeautifulSoup


class bilibili_crawl:

    def __init__(self, bv):
        # 视频页地址
        self.url = 'https://www.bilibili.com/video/' + bv
        # 下载开始时间
        self.start_time = time.time()

    def get_vedio_info(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            }

            response = requests.get(url=self.url, headers=headers)
            if response.status_code == 200:
                bs = BeautifulSoup(response.text, 'html.parser')
                # 取视频标题
                video_title = bs.find('h1').get_text()

                # 取视频链接
                pattern = re.compile(r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL)
                script = bs.find("script", text=pattern)
                result = pattern.search(script.next).group(1)

                temp = json.loads(result)
                # 取第一个视频链接
                for item in temp['data']['dash']['video']:
                    if 'baseUrl' in item.keys():
                        video_url = item['baseUrl']
                        break
                for item in temp['data']['dash']['audio']:
                    if 'baseUrl' in item.keys():
                        audio_url = item['baseUrl']
                        break
                return {
                    'title': video_title,
                    'url': video_url,
                    'audio_url': audio_url
                }
        except requests.RequestException:
            print('视频链接错误，请重新更换')

    def download_video(self, video):
        title = re.sub(r'[\/:*?"<>|]', '-', video['title'])
        url = video['url']
        url1 = video['audio_url']
        # print(url)
        # print(url1)
        filename = title + '.mp4'
        filename1 = title + '.mp3'
        opener = urllib.request.build_opener()
        opener.addheaders = [('Origin', 'https://www.bilibili.com'),
                             ('Referer', self.url),
                             ('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url=url, filename=filename, reporthook=self.schedule)
        urllib.request.urlretrieve(url=url1, filename=filename1, reporthook=self.schedule)

    def schedule(self, blocknum, blocksize, totalsize):
        '''
        urllib.urlretrieve 的回调函数
        :param blocknum: 已经下载的数据块
        :param blocksize: 数据块的大小
        :param totalsize: 远程文件的大小
        :return:
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:            percent = 100
        s = ('#' * round(percent)).ljust(100, '-')
        sys.stdout.write("%.2f%%" % percent + '[ ' + s + ']' + '\r')
        sys.stdout.flush()


if __name__ == '__main__':
    bc = bilibili_crawl('BV12t4y167Wd')
    vedio = bc.get_vedio_info()
    bc.download_video(vedio)

# requestUrl
# https://upos-sz-mirrorali.bilivideo.com/upgcxcode/11/08/944170811/944170811_nb3-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1673018598&gen=playurlv2&os=alibv&oi=1880505547&trid=1c306fdafa1a442a803b5ac6c2c94c99u&mid=0&platform=pc&upsig=f93bee4539fb160a391630b6b354b819&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=F6CF0593-8F19-47B8-6915-997F54C8A48798015infoc&build=0&agrr=0&bw=49712&logo=80000000
# 对应的抓包中url
# https://upos-sz-mirrorali.bilivideo.com/upgcxcode/11/08/944170811/944170811-1-30033.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1673019009&gen=playurlv2&os=alibv&oi=1880505547&trid=89ae2f80816a4de0a7a37096501a6e96u&mid=0&platform=pc&upsig=866a8a0189bce6295298ca6578a689e7&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=D496314E-3A50-5624-904C-3AF4DBFC0B5B09299infoc&build=0&agrr=0&bw=25204&logo=80000000
# 抓包中的audiourl
# https://upos-sz-mirrorali.bilivideo.com/upgcxcode/11/08/944170811/944170811_nb3-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1673013032&gen=playurlv2&os=alibv&oi=1880505547&trid=9bc13505bad2499f88881d3ddefd7e54u&mid=0&platform=pc&upsig=3754b0029bbc13e0a0d776cd1315b207&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=32658C16-F51F-2956-48A1-2E1C4B2F8EEC23823infoc&build=0&agrr=0&bw=21030&logo=40000000
#
