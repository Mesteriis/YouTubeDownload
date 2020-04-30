import progressbar

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from component import itemDownloads
from colorsConsoleTextUTF8 import colorText
from pytube import Playlist, YouTube
# import general
# import oauth2client
from datetime import datetime
# import datetime

import os
import requests





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
    VideoList = list()
    VideoListAll = list()
    previouslyProcessedSheet = dict()

    dictIntoDataBase = dict ()
    playListYouTube = Playlist
    listForDownloads = list()

    titleRequestWork = '\u001b[34mRequest\u001b[39m'


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
        self.config.set ( 'Settings', 'nameDirLibrary', 'Library/YouTubeDownloads/' )
        self.config.set ( 'Settings', 'defaultVideoDir', '{}{}Video/'
                            .format(self.config.get('Settings', 'pathToNASDir'),
                                    self.config.get('Settings', 'nameDirLibrary')) )
        self.config.set ( 'Settings', 'defaultMP3Dir', '{}{}Audio/'
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
        self.config.set ( 'Downland_Settings', 'checkBeforeDownloading', '0' )
        config_file = open ( self.fileSettings, "w" )
        self.config.write (config_file)

    def readSettings(self):
        self.config.read ( self.fileSettings )

    def saveSettings (self):
        with open ( self.fileSettings, "w" ) as config_file:
            self.config.write (config_file)

    def prepareEnvironment(self):
        self.defaultSettings ()
        if not os.path.exists ( 'Library' ):
            os.mkdir ( 'Library' )
        os.mkdir ( self.config.get('Settings', 'nameDirLibrary') )
        os.mkdir ( self.config.get('Settings', 'defaultVideoDir') )
        os.mkdir ( self.config.get('Settings', 'defaultMP3Dir') )
        self.readSettings()

    def __init__(self, urlVideo = None, urlPl = None):
        if not os.path.exists('res'):
            os.mkdir ( 'res' )
            self.isFirstStart = False
        if not os.path.exists('Library'):
            os.mkdir ( 'Library' )
        self.config = configparser.ConfigParser()
        if not os.path.exists ( self.fileSettings ):
            self.prepareEnvironment()
        else:
            self.readSettings()

    def readBD(self):
        if not os.path.exists(self.config.get('Settings_DB_File', 'path') ):
            f = open(self.config.get('Settings_DB_File', 'path') ,'w')
            f.write('-Created By {}'.format(datetime.now()) + '\n-url # title \n')
            f.close()

        with open ( self.config.get('Settings_DB_File', 'path') ) as f:
            content = f.read()
        try:
            lines = content.split ( '\n' )
            # line = url # title
            for line in lines:
                if line[0] == '-':
                    continue
                sepIndex = line.rfind('#')
                self.dictIntoDataBase.update({line[:sepIndex]:line[sepIndex+1:]}) # отсортировать true false
        except:
            print('database file signature not recognized')

    def addItemsToBase(self, urlToItem = None, title = None):
        if urlToItem is None or title is None:
            return
        self.previouslyProcessedSheet.update ( {urlToItem: title} )
        f = open ( self.config.get ( 'Settings_DB_File', 'path' ), 'a' )
        f.write(urlToItem + self.config.get('Settings_DB_File', 'sep') + title + '\n')
        f.close()


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

    def listVideos(self):
        print (self.titleRequestWork, "Create a video sheet to upload... " )
        self.playListYouTube = Playlist(self.config.get('Settings', 'defPLAYLIST'))
        time = round(len( self.playListYouTube)*20/60/60)
        time = str(time) + ' hour'
        answer = input( "Found {} video, get the title? (this operation may take a long time, \n"
                      "but the local base will be taken into account( {} elements ), this may take {} ) ( y/n ): "
                      .format( len( self.playListYouTube ) , len( self.dictIntoDataBase ),time ))
        # answer = 'n' # TODO del
        if answer == 'y' or answer == 'н':
            for indexList in self.playListYouTube:
                if self.dictIntoDataBase.get(indexList):

                    print(self.dictIntoDataBase.get(indexList))
                else:
                    titleItem =  itemDownloads.getTitle ( indexList )
                    self.listForDownloads.append(indexList)

        elif answer == 'n' or answer == 'n':
            print ( 'Putting together a download list...' )
            self.listForDownloads = self.playListYouTube
            # for indexList in self.playListYouTube:
            #     self.listForDownloads.append ( indexList )
            # break #TODO del
        # answer = 'y'  # TODO del
        answer = input('Prepared to load {} items, upload? (y/n): '.format(len(self.listForDownloads)))
        if answer == 'y' or answer == 'н':
            self.downloadBySheet()

    def downloadBySheet(self):
        _items = dict ( {'VIDEO': False, 'AUDIO': False} )
        answer = input( 'Will we download the video? (y/n): ' )
        if answer == 'y':
            _items['VIDEO'] = True
            print ( "I’ll then put the video in {}".format ( self.config.get ( 'Settings', 'defaultVideoDir' ) ) )
        answer = input ( 'And the music? (y/n): ' )
        if answer == 'y':
            print ( "And the music will be in {}".format ( self.config.get ( 'Settings', 'defaultMP3Dir' ) ) )
            _items['AUDIO'] = True

        if not _items['AUDIO'] and  not _items['VIDEO']:
            print('Then another time... Bye-bye')
            return

        time =str(round(len(self.listForDownloads)*300/1024)) + ' Gb'

        print (
            "Ok, about {} need to be loaded, we’ll download the last one, it’s about {}".format (
                len ( self.listForDownloads ),
                time ) )
        input('letSStart?')
        print('And I would start anyway %-)')
        print(self.titleRequestWork, 'Download, you can pet the cat %-)...')
        print(len(self.listForDownloads))
        # 'downloads list item'
        for indexList in self.listForDownloads:
            if self.config.get ( 'Downland_Settings', 'checkBeforeDownloading' ) == '1':
                print ( 'Verification URL:', indexList, end=' ' )
                if self.checkUrlToItem ( indexList ):
                    item = itemDownloads.itemYouTube \
                        ( indexList, self.config.get('Settings', 'nameDirLibrary'), self.addItemsToBase ( self.config.get ( 'Settings_DB_File', 'path' )))
                    print ( item.title )
                    item.downloadItem ( self.config.get ( 'Settings', 'defaultVideoDir' ),
                                        self.config.get ( 'Settings', 'defaultMP3Dir' ) )
            else:
                print ( self.config.get ( 'Settings_DB_File', 'path' ) )

                item = itemDownloads.itemYouTube ( indexList, '', self.addItemsToBase )
                print ( item.title )
                item.downloadItem (self.config.get('Settings', 'defaultVideoDir'), self.config.get('Settings', 'defaultMP3Dir') )


    def tryFindItemInDB(self, item_urlToItem):
        if self.dictIntoDataBase.get( item_urlToItem ):
            return True
        else:
            return False

    def checkUrlToItem(self,url):
        responds = None
        if not url:
            return False
        else:
            try:
                responds = requests.get(url)
            except : #TODO handle all exceptions
                print ('Something went wrong, the link is not available')
            if responds.status_code == 200:
                return True
            return False



y = ytd()
y.readBD()
y.listVideos()



# https://www.youtube.com/watch?v=D6-qZUX7DfY    скачать потом