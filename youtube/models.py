from datetime import datetime

class YTUser(object):

    def __init__(self, item):
        try:
            age = int(item['yt_age'])
        except:
            age = 0
        try:
            last_access = datetime.strptime(item['yt_statistics']['lastwebaccess'],'%Y-%m-%dT%H:%M:%S.000Z')
        except:
            last_access = datetime.now()
        try:
            subscribers_count = int(item['yt_statistics']['subscribercount'])
        except:
            subscribers_count = 0
        try:
            total_uploads_views = int(item['yt_statistics']['totaluploadviews'])
        except:
            total_uploads_views = 0
        self.username = item['author']
        self.user_id = item['id']
        self.thumbnail = item['media_thumbnail'][0]['url']
        self.first_name = item.get('yt_firstname',item['author'])
        self.last_name = item.get('yt_lastname','')
        self.location = item['yt_location']
        self.tags = [t['label'] for t in item['tags'] if t['label'] is not None]
        self.age = age
        self.gender = item.get('yt_gender','')
        self.last_access = last_access
        self.subscribers_count = subscribers_count
        self.total_uploads_views = total_uploads_views


class YTVideo(object):
    def __init__(self, item):
        try:
            num_views = int(item['yt_statistics'].get('viewcount',None))
            rating_count = item['gd_rating']['numraters']
        except:
            num_views = 0
            rating_count = 0
        try:
            rating_avg = float(item['gd_rating']['average'])
            rating_min = float(item['gd_rating']['min'])
            rating_max = float(item['gd_rating']['max'])
        except:
            rating_avg = 0
            rating_min = 0
            rating_max = 0
        self.author_thumbnail = item['media_thumbnail'][0]['url']
        self.publish_date = datetime(*item['published_parsed'][:6])
        self.author_username = item['author']
        self.tags = [t['label'] for t in item['tags'] if t['label'] is not None]
        self.url = item['content'][0]['src']
        self.num_views = num_views
        self.rating_avg = rating_avg
        self.rating_min = rating_min
        self.rating_max = rating_max
        self.rating_count = rating_count
        self.id = item['id']
        self.video_web_url = item['media_player']['url']
        self.title = item['title']
        try:
            self.duration = int(item['yt_duration']['seconds'])
        except:
            self.duration = 0
        try:
            self.n_likes = int(item['yt_rating']['numlikes'])
        except:
            self.n_likes = 0
        try:
            self.n_dislikes = int(item['yt_rating']['numdislikes'])
        except:
            self.n_dislikes = 0

