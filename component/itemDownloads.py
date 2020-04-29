import pytube
from component import cli_grafiks

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

    def __init__(self, _urlToItem, _pathToSave = '' , _cd_done = None, _cb_procesing = None, sep = '#'):
        self.cb_done = _cd_done
        self.cb_procesing = _cb_procesing
        self.pathToSave = _pathToSave
        def complete(stream, file_handle):
            print ( file_handle, "DONE" )
            self.done()


        yt = self.youtube (_urlToItem, on_progress_callback=self.progress_function,on_complete_callback=complete)
        self.video = yt.streams.get_highest_resolution()
        self.audio = yt.streams.get_audio_only ()
        self.title = self.video.title
        self.sizeV = self.video.filesize
        self.sizeA = self.audio.filesize
        self.resolution = self.video.resolution
        self.author = yt.author
        self.info = self.video.title, 'resolution:', self.resolution, 'size:', round(self.sizeV//1024/1024, 2) , 'Mb'
        self.stringForDB = self.title + 'sep'



    def downloadItem(self,pathToSave = None):
        self.video.download(pathToSave)

    def progress_function(self, chunk, file_handle, bytes_remaining):
        # print ( round ( (1 - bytes_remaining / self.sizeV) * 100, 3 ), '% done...' )
        # self.cb_finish((1 - bytes_remaining / self.sizeV) * 100, 3 )
        prb = cli_grafiks.progressbar.progressbar (((1 - bytes_remaining / self.sizeV) * 100, 3 ), widgets=cli_grafiks.widgets )
        # print ( prb. )

    def done(self):
        print( 'done in class')
        # return self.cb_done('test')