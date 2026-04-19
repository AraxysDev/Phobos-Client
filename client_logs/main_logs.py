import os
import time

path = '/Applications/PhobosClient/logs'
file = os.path.join(path, 'client.log')
linebreak = '---------------------------------------------------------------\n\n'
linebreak_bold = '===============================================================\n\n'


def log(message, error=False):
    validate()

    # Calculate local time
    t = time.localtime()
    hours = t.tm_hour
    minutes = t.tm_min
    seconds = t.tm_sec
    time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    # Format log
    text = f'Time (hh:mm:ss): {time_str}\nError: {error}\nMessage: {message}\n\n' + linebreak

    with open(file, 'a') as f:
        f.write(text)
        f.close()


def client_opened():
    # Calculate local time
    t = time.localtime()
    hours = t.tm_hour
    minutes = t.tm_min
    seconds = t.tm_sec
    time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}\n\n'

    text = 'CLIENT OPENED - ' + time_str + linebreak_bold

    with open(file, 'a') as f:
        f.write(text)
        f.close()


def page_opened(page):
    # Calculate local time
    t = time.localtime()
    hours = t.tm_hour
    minutes = t.tm_min
    seconds = t.tm_sec
    time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}\n\n'

    text = f'PAGE {page} OPENED - ' + time_str + linebreak_bold

    with open(file, 'a') as f:
        f.write(text)
        f.close()


def clear_logs():
    with open(file, 'w') as f:
        f.write('')
        f.close()


def validate():
    # Ensure folder exists
    if not os.path.exists(path):
        os.makedirs(path)

    # Ensure log file exists
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.close()
