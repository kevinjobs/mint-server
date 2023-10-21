import time
import sqlite3
import json
import requests


def strptime_to_stamp(t: str, fmt=r'%Y-%m-%d %H:%M:%S.%f'):
    s_time = time.strptime(t, fmt)
    return int(time.mktime(s_time))


def connect_db():
    conn = sqlite3.connect(r'D:\\Backups\\develop_backup\\mintforge.sqlite')
    return conn.cursor()


def find_pictures(cursor: sqlite3.Cursor):
    sql = 'SELECT * FROM Pictures'
    cursor.execute(sql)
    items = cursor.fetchall()
    rets = []
    for item in items:
        print(item)
        rets.append({
            'createAt': strptime_to_stamp(item[0][:-3]),
            'updateAt': strptime_to_stamp(item[1][:-3]),
            'type': 'photo',
            'title': item[4],
            'author': item[5],
            'content': '',
            'excerpt': item[9],
            'cover': '',
            'status': 'publish' if item[6] == 'public' else 'draft',
            'tags': '',
            'category': 'photo',
            'format': 'jpg',
            'url': item[8],
            'exif': json.dumps({
                'width': item[10],
                'height': item[11],
                'latitude': item[12],
                'longitude': item[13],
                'latitudeRef': item[14],
                'longitudeRef': item[15]
            }, ensure_ascii=False),
            'description': item[9],
        })
    return rets


def find_articles(cursor: sqlite3.Cursor):
    sql = 'SELECT * FROM Articles'
    cursor.execute(sql)
    items = cursor.fetchall()
    rets = []
    for item in items:
        print(item)
        rets.append({
            'createAt': strptime_to_stamp(item[0][:-3], r'%Y-%m-%d %H:%M:%S'),
            'updateAt': strptime_to_stamp(item[1][:-3], r'%Y-%m-%d %H:%M:%S'),
            'type': 'article',
            'title': item[4],
            'author': item[5],
            'content': item[9],
            'excerpt': item[11],
            'cover': item[8],
            'status': 'publish' if item[6] == 'public' else 'draft',
            'tags': item[7],
            'category': 'eassy',
            'format': item[10],
            'url': '',
            'exif': '',
            'description': '',
        })
    return rets


def download_file(url: str):
    filename = url.split(r'/')[-1]
    resp = requests.get(url, stream=True)
    with open('tmp/' + filename, 'wb') as fp:
        for chunk in resp.iter_content(chunk_size=1024):
            fp.write(chunk)


if __name__ == '__main__':
    url = 'http://localhost:5000/upload'
    for i in range(1, 30):
        filename = 'tmp/img (%d).jpg' % i
        files = {
            'file': open(filename, 'rb')
        }
        requests.post(url, files=files)
        time.sleep(1)
