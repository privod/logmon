import time
import os.path
from .log import Parser
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

path = os.path.join('.' 'logmonitor', 'testdata')           # TODO Переопределить


class Handler(FileSystemEventHandler):
    def on_modified(self, event):

        print(event)


def main():

    observer = Observer()
    observer.schedule(Handler(), path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
