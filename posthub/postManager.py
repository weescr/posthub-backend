from datetime import timedelta, datetime, timezone
import time
import requests
from random import randint



class ManagerPost(object):
    "класс для управленеия постановкой постов"

    def __init__(self, ConfigVK: dict):
        self.ACCESS_TOKEN = ConfigVK.get('ACCESS_TOKEN')
        self.GROUP_ID = ConfigVK.get('GROUP_ID')
        self.VERSION = ConfigVK.get('VERSION')

    def CommitPost(self, Comment: str, Day: str, Time: str):
        Date = self._getDate(Day, Time)
        BoxWithPhotoPath = []

        unixtime = time.mktime(Date.timetuple())
        self._LoadVkСontent(BoxWithPhotoPath, unixtime, Comment)

        return

    def _LoadVkСontent(self, PhotoPath, Date, Comment):

        PhotoLink = "I:/photo_2019-12-09_13-34-08.jpg"

        # # Формируем параметры для размещения картинки в группе и публикуем её
        if Comment != 'NULL':
            params = {'access_token': self.ACCESS_TOKEN,
                      'owner_id': self.GROUP_ID,
                      'from_group': 1,
                      'message': Comment,
                      'attachments': PhotoLink,
                      'publish_date': Date,
                      'v': self.VERSION}
        else:
            params = {'access_token': self.ACCESS_TOKEN,
                      'owner_id': self.GROUP_ID,
                      'from_group': 1,
                      'attachments': PhotoLink,
                      'publish_date': Date,
                      'v': self.VERSION}

        requests.get('https://api.vk.com/method/wall.post', params)

    def _getDate(self, Day: str, Time: str):
        if Day is not None or Time is not None:
            day = Day.split(".")
            time = Time.split(":")
            Date = datetime(int(day[0]), int(day[1]), int(day[2]), int(time[0]), int(time[1]))
         #   print(f"Date: {Date.day}.{Date.month}.{Date.year}, Day time {Date.hour}:{Date.minute}")
            return Date
        else:
            today = datetime.now()
            minute = today.minute + 5
            Date = datetime(today.year, today.month, today.day, today.hour, minute)
         #   print(f"Date: {today.day}.{today.month}.{today.year}, Day time {today.hour}:{today.minute}")
            return Date

    def LoadVkСontentWithPhoto(self, PhotoPath, Date, Comment):
        response = requests.get('https://api.vk.com/method/photos.getWallUploadServer',
                                params={'access_token': self.ACCESS_TOKEN,
                                        'group_id': self.GROUP_ID,
                                        'v': self.VERSION})
        print(response.json())
        upload_url = response.json()['response']['upload_url']

        BoxPhotoLink = []

        for i in range(len(PhotoPath)):
            # Формируем данные параметров для сохранения картинки на сервере
            request = requests.post(upload_url, files={'photo': open(PhotoPath[i], "rb")})

            # Сохраняем картинку на сервере и получаем её идентификатор
            photo_id = requests.get('https://api.vk.com/method/photos.saveWallPhoto',
                                    params={'access_token': self.ACCESS_TOKEN,
                                            'group_id': self.GROUP_ID,
                                            'photo': request.json()["photo"],
                                            'server': request.json()['server'],
                                            'hash': request.json()['hash'],
                                            'v': self.VERSION}
                                    )
            a = 'photo' + str(photo_id.json()['response'][0]['owner_id']) + '_' + str(
                photo_id.json()['response'][0]['id'])
            BoxPhotoLink.append(a)

        PhotoLink = ",".join(BoxPhotoLink)

        # # Формируем параметры для размещения картинки в группе и публикуем её
        if Comment != 'NULL':
            params = {'access_token': self.ACCESS_TOKEN,
                      'owner_id': -self.GROUP_ID,
                      'from_group': 1,
                      'message': Comment,
                      'attachments': PhotoLink,
                      'publish_date': Date,
                      'v': self.VERSION}
        else:
            params = {'access_token': self.ACCESS_TOKEN,
                      'owner_id': -self.GROUP_ID,
                      'from_group': 1,
                      'attachments': PhotoLink,
                      'publish_date': Date,
                      'v': self.VERSION}

        requests.get('https://api.vk.com/method/wall.post', params)
