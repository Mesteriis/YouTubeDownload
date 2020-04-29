import time
import progressbar
import logging

# for i in progressbar.progressbar(range(100)):
#     time.sleep(0.02)



# progressbar.streams.wrap_stderr ()
# logging.basicConfig ()
#
# for i in progressbar.progressbar ( range ( 10 ) ):
#     logging.error ( 'Got %d', i )
#     time.sleep ( 0.2 )
#
with progressbar.ProgressBar ( max_value=10 ) as bar:
    for i in range ( 10 ):
        time.sleep ( 0.1 )
        bar.update ( i )
#
# for i in progressbar.progressbar(range(100), redirect_stdout=False):
#     print('Some text', i)
#     time.sleep(0.1)

# bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
# for i in range(20):
#     time.sleep(0.1)
#     bar.update(i)

widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
]
# for i in progressbar.progressbar(range(20), widgets=widgets):
#     time.sleep(0.1)


# def custom_len(value):
#     # These characters take up more space
#     characters = {
#         '进': 2,
#         '度': 2,
#     }
#
#     total = 0
#     for c in value:
#         total += characters.get(c, 1)
#
#     return total


# bar = progressbar.ProgressBar(
#     widgets=[
#         '进度: ',
#         progressbar.Bar(),
#         ' ',
#         progressbar.Counter(format='%(value)02d/%(max_value)d'),
#     ],
#     len_func=custom_len,
# )
# for i in bar(range(10)):
#     time.sleep(0.1)

# bar = progressbar.ProgressBar ( maxval=10.0, widgets=[
#     'Just a progress bar test: ',  # Статический текст
#     progressbar.Bar ( left='[', marker='=', right=']' ),  # Прогресс
#     progressbar.ReverseBar ( left='[', marker='*', right=']' ),  # Регресс
    # progressbar.SimpleProgress (),  # Надпись "6 из 10"
# ] ).start ()
#
# t = 0.0
# while t <= 10.0:
#     bar.update ( t )
#     time.sleep ( 0.01 )
#     t += 0.1
# bar.finish ()