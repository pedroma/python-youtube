from datetime import datetime
from youtube.utils import clean_int, clean_last_time, clean_float

class YTUser(object):

    def __init__(self, item):
        age = clean_int(item['yt_age'])
        last_access = clean_last_time(item['yt_statistics']['lastwebaccess'])
        subscribers_count = clean_int(item['yt_statistics']['subscribercount'])
        total_uploads_views = clean_int(item['yt_statistics']['totaluploadviews'])
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
        num_views = clean_int(item['yt_statistics'].get('viewcount',None))
        rating_count = clean_int(item['gd_rating']['numraters'])
        rating_avg = clean_float(item['gd_rating']['average'])
        rating_min = clean_float(item['gd_rating']['min'])
        rating_max = clean_float(item['gd_rating']['max'])
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
        self.duration = clean_int(item['yt_duration']['seconds'])
        self.n_likes = clean_int(item['yt_rating']['numlikes'])
        self.n_dislikes = clean_int(item['yt_rating']['numdislikes'])

