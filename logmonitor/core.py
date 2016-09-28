import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# file_name = "test.log"
path='.'


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

    # with open(file_name, 'rb') as file:
    #     log_list = Parser().pars(file.read())
    #
    #     for log in log_list:
    #         print(log)
