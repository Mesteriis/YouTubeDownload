import progressbar
import pytube

class itemYouTube:
    url = str
    sizeV = 0
    sizeA = 0
    title = str
    author = str
    youtube = pytube.YouTube
    video = None
    audio = None
    info = str
    resolution = None
    stringForDB = str
    cb_done = None
    cb_procesing = None
    pathToSave = str
    bar = None
    titleVideoBar = '\t[Video] '
    titleAudioBar = '\t[Audio] '
    titleRequest  = ''

    def __init__(self, _urlToItem, _pathToSave, _cd_done, sep = '#'):

        self.url = _urlToItem
        self.cb_done = _cd_done
        self.pathToSave = _pathToSave
        def complete(stream, file_handle):
            if self.cb_done:
                self.done(self.url,self.title)
                print("\u001b[32m",'\tDONE','\u001b[39m')

            else:
                print ( "\u001b[31mDownload not marked up in the database, error" )
        ytV = self.youtube (self.url, on_progress_callback=self.progress_function_video,on_complete_callback=complete)
        ytA = self.youtube (self.url, on_progress_callback=self.progress_function_audio, on_complete_callback=complete )
        self.video = ytV.streams.get_highest_resolution()
        self.audio = ytA.streams.get_audio_only ()
        self.title = self.video.title
        self.sizeV = self.video.filesize
        self.sizeA = self.audio.filesize
        self.resolution = self.video.resolution
        self.author = ytV.author
        self.info = self.video.title, 'resolution:', self.resolution, 'size:', round(self.sizeV//1024/1024, 2) , 'Mb'
        self.stringForDB = self.title + 'sep'



    def downloadItem(self, pathToSaveVideo = None, pathToSaveAudio = None, _items=None):
        # print('pathToSaveVideo ' , pathToSaveVideo, '\n', 'pathToSaveAudio ', pathToSaveAudio )
        print(self.title)
        if _items is None:
            _items = dict ( {'VIDEO': False, 'AUDIO': True} )
        if _items['VIDEO']:
            self.video.download(pathToSaveVideo)
        else:
            print(self.titleVideoBar, 'Download video strangled!')
        if _items['AUDIO']:
            self.audio.download(pathToSaveAudio)
        else:
            print (self.titleAudioBar, 'Download audio strangled!' )

    def progress_function_video(self, chunk, file_handle, bytes_remaining):
        self.bar = progressbar.ProgressBar(maxval=round(self.sizeV/1024/1024, 2), widgets=[
                    self.titleVideoBar, # Статический текст
                    progressbar.Bar(left='[', marker='#', right='] Mb: '), # Прогресс
                    # progressbar.ReverseBar(left='NE', marker='=', right='] '), # Регресс
                    progressbar.SimpleProgress(), # Надпись "6 из 10"
                    ]).start()
        self.bar.update(round((self.sizeV - bytes_remaining)/1024/1024,2),True)

    def progress_function_audio(self, chunk, file_handle, bytes_remaining):
        self.bar = progressbar.ProgressBar(maxval=round(self.sizeA/1024/1024, 2), widgets=[
                    self.titleAudioBar, # Статический текст
                    progressbar.Bar(left='[', marker='#', right='] Mb: '), # Прогресс
                    # progressbar.ReverseBar(left='NE', marker='=', right='] '), # Регресс
                    progressbar.SimpleProgress(), # Надпись "6 из 10"
                    ]).start()
        self.bar.update(round((self.sizeA - bytes_remaining)/1024/1024,2),True)

    def done(self,string,title):
        if self.cb_done:
            self.cb_done(string , title)
        else:
            print(self.cb_done)

def getTitle(urlToYT):
    try:
        answen = {pytube.YouTube(urlToYT).title,
                    pytube.YouTube(urlToYT).streams.get_highest_resolution().filesize,
                    pytube.YouTube ( urlToYT ).streams.get_audio_only().filesize}
    except:
        answen = None
    return answen
