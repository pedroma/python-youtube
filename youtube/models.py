class YTUser(object):

    def __init__(self, item):
        self.username = item['author']
        self.user_id = item['id']
        self.thumbnail = item['media_thumbnail'][0]['url']
        self.first_name = item['yt_firstname']
        self.last_name = item['yt_lastname']
        self.location = item['yt_location']
        self.tags = [t['label'] for t in item['tags'] if t['label'] is not None]
        self.age = item['yt_age']
        self.gender = item['yt_gender']
        self.last_access = item['yt_statistics']['lastwebaccess']
        self.subscribers_count = item['yt_statistics']['subscribercount']
        self.total_uploads_views = item['yt_statistics']['totaluploadviews']


class YTVideo(object):
    def __init__(self, item):
        self.author_thumbnail = item['media_thumbnail'][0]['url']
        self.publish_date = item['published_parsed']
        self.author_username = item['author']
        self.tags = [t['label'] for t in item['tags'] if t['label'] is not None]
        self.url = item['content'][0]['src']
        self.num_views = item['gd_feedlink'].get('counthint',None)
        self.rating_avg = item['gd_rating']['average']
        self.rating_min = item['gd_rating']['min']
        self.rating_max = item['gd_rating']['max']
        self.rating_count = item['gd_rating']['numraters']
        self.id = item['id']
        self.video_web_url = item['media_player']['url']
        self.published = item['published_parsed']
        self.title = item['title']
        self.duration = item['yt_duration']['seconds']
        self.n_likes = item['yt_rating']['numlikes']
        self.n_dislikes = item['yt_rating']['numdislikes']

