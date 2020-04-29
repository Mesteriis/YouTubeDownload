import progressbar

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from component import itemDownloads
from pytube import Playlist
# import general
# import oauth2client
# import httplib2

import os
import requests
def callBack(string):
    print ( "CallBack " + string )

class ytd:
    ShowDocumentation = True
    config = None
    fileSettings = 'res/settings.plist'
    isFirstStart = True
    forcedNeedSyncDataBase = False
    headersForRequest = {
        'Login': 'втойящик@mail.ru',
        'Password': 'твой пароль',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11.6; rv:51.0.1) Gecko/20100101 Firefox/51.0.1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://mail.ru/',
        'remember': 1,
    }
    VideoList = list
    VideoListAll = list
    previouslyProcessedSheet = dict()



    playListYouTube = Playlist
    #
    def defaultSettings(self, fileSettings = 'res/settings.plist'):
        """
        We configure the work and create the settings file and environment, to change the settings, change the file
        ROOT_Project/res/settings.plist, or use the API
        :param fileSettings: Path to settings file
        """
        if self.ShowDocumentation:
            print(self.defaultSettings.__doc__)
        self.config.add_section ( "Settings" )
        self.config.set ( 'Settings', 'defPLAYLIST', 'https://www.youtube.com/playlist?list=FLhJ4IOQrs63Y5_Rx5aqolZw')
        self.config.set ( 'Settings', 'pathToNASDir', '' )
        self.config.set ( 'Settings', 'nameDirLibrary', 'res/YouTubeDownloads/' )
        self.config.set ( 'Settings', 'defaultVideoDir', '{}{}Video/'
                            .format(self.config.get('Settings', 'pathToNASDir'),
                                    self.config.get('Settings', 'nameDirLibrary')) )
        self.config.set ( 'Settings', 'defaultMP3Dir', '{}{}MP3/'
                          .format(self.config.get('Settings', 'pathToNASDir'),
                                  self.config.get('Settings', 'nameDirLibrary')) )
        self.config.add_section ( "Settings_DB_File" )
        self.config.set ( 'Settings_DB_File', 'path', 'res/item.dby' )
        self.config.set ( 'Settings_DB_File', 'sep', '#')
        self.config.add_section ( "Settings_DB_SQLite" )
        self.config.set ( 'Settings_DB_SQLite', 'None', 'None' )
        self.config.add_section ( "Downland_Settings" )
        self.config.set ( 'Downland_Settings', 'defaultFormatVideo', 'video/mp4' )
        self.config.set ( 'Downland_Settings', 'defaultFormatMP3', '320')
        config_file = open ( self.fileSettings, "w" )
        self.config.write (config_file)

    def readSettings(self):
        self.config.read ( self.fileSettings )

    def saveSettings (self):
        with open ( self.fileSettings, "w" ) as config_file:
            self.config.write (config_file)

    def prepareEnvironment(self):
        self.defaultSettings ()
        os.mkdir ( self.config.get('Settings', 'nameDirLibrary') )
        os.mkdir ( self.config.get('Settings', 'defaultVideoDir') )
        os.mkdir ( self.config.get('Settings', 'defaultMP3Dir') )
        self.readSettings()

    def __init__(self, urlVideo = None, urlPl = None):
        # print('init')
        if not os.path.exists('res'):
            os.mkdir ( 'res' )
            self.isFirstStart = False

        self.config = configparser.ConfigParser()
        if not os.path.exists ( self.fileSettings ):
            self.prepareEnvironment()
        else:
            self.readSettings()

    def readBD(self):
        if not os.path.exists(self.config.get('Settings_DB_File', 'path') ):
            f = open(self.config.get('Settings_DB_File', 'path') ,'w')
            f.write('test#1\ntest2#0')
            f.close()

        with open ( self.config.get('Settings_DB_File', 'path') ) as f:
            content = f.read()
        try:
            lines = content.split ( '\n' )
            for line in lines:
                sepIndex = line.rfind('#')
                self.previouslyProcessedSheet.update({line[:sepIndex]:line[sepIndex+1:]}) # отсортировать true false
        except:
            print('database file signature not recognized')

    def addItemsToBase(self, nameItem, statusItem = 1):
        self.previouslyProcessedSheet.update ( {nameItem: statusItem} )

    def markItemDownloadComplite(self, nameItem):
        self.previouslyProcessedSheet.update ( {nameItem: 1} )

    def syncDB(self):
        f = open ( self.config.get ( 'Settings_DB_File', 'path' ), 'r' )
        line = f.readlines ()
        f.close ()
        if len ( line ) < len ( self.previouslyProcessedSheet ):
            f = open ( self.config.get ( 'Settings_DB_File', 'path' ), 'w' )
            for el in self.previouslyProcessedSheet:
                tmpString = el + '#' + self.previouslyProcessedSheet[el]
                f.write(tmpString)
            f.close()
            print ('DB sync Done! Items in data base {}'.format(len(line)))
        else:
            print('Database does not need updating')

        if self.forcedNeedSyncDataBase:
            f = open ( self.config.get ( 'Settings_DB_File', 'path' ), 'w' )
            for el in self.previouslyProcessedSheet:
                tmpString = el + '#' + self.previouslyProcessedSheet[el]
                f.write ( tmpString )
            f.close ()
            print ( 'DB sync Done! Items in data base {}'.format ( len ( line ) ) )
        self.forcedNeedSyncDataBase = False

    def __str__(self):
        return "YouTube Video and Audio downloads\n" + self.__doc__

    def __repr__(self):
        return "YouTube Video and Audio downloads\n" + self.__doc__

    def listVideos(self):
        self.playListYouTube = Playlist(self.config.get('Settings', 'defPLAYLIST'))
        for indexList in self.playListYouTube:
            print ('Проверка:', indexList, end = ' ')
            if self.checkUrlToItem(indexList):
                item = itemDownloads.itemYouTube(indexList,'')
                print ( item.title, end=' ')
                # with progressbar.ProgressBar ( max_value=10 ) as bar: подумать процесс бар
                #         bar.update ( i )
                item.downloadItem()
            # self.youtube = pytube.YouTube(indexList)

    def checkUrlToItem(self,url):
        if not url:
            return False

        else:
            try:
                responds = requests.get(url)
            except:
                print ('Something went wrong, the link is not available')
            if responds.status_code == 200:
                return True
            return False

    def dddd(self):
        print( " d ")





# ytd('-q \'ds\' w e r t y u', '213123')
y = ytd()
y.listVideos()


# y.listVideos()
# print(y.previouslyProcessedSheet)
# from os import path
# _PLAYLIST = Playlist("https://www.youtube.com/playlist?list=FLhJ4IOQrs63Y5_Rx5aqolZw")


url = "https://www.youtube.com/watch?v=iP5JQq3eUJ8&list=FLhJ4IOQrs63Y5_Rx5aqolZw&index=2&t=0s"

# f= itemDownloads.itemYouTube( url, callBack )
# f.downloadItem()

# response = requests.get(url)
# print(response.content)

# print(playlist.title)
# i = 1
# yt = None
# for el in playlist:
    # print (i,el)
    # yt = YouTube(el)
    # print(yt.title)
    # break
        # i+=1

# https://www.youtube.com/watch?v=D6-qZUX7DfY    скачать потом