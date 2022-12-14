import logging
import os
import subprocess
from threading import Thread
from tkinter import filedialog
from tkinter import *
from ffprobe import FFProbe
from queue import Queue


def main():
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory(initialdir="/", title="Select Audio Files Folder")
    filelist = os.listdir(path)
    newfilelist = [file for file in filelist if ".mp3" in file]

    # Calculate chapters
    def worker():
        while True:
            file = q.get()
            order = file[0]
            file = file[1]
            metadata = FFProbe(f"{path}/{file}")
            for stream in metadata.streams:
                print(f"Order: {order} | Duration: {stream.duration_seconds()}")
            q.task_done()

    q = Queue()
    for i in range(16):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for x, item in enumerate(newfilelist):
        q.put([x, item])

    q.join()  # block until all tasks are done

    input("end of threading")

    output_filename = "test.mp3"
    ffmpeg_input_string = f"ffmpeg -i {' -i '.join(filelist)} -i {metadata} {output_filename}"
    subprocess.Popen(f"ffmpeg {ffmpeg_input_string}").communicate()


if __name__ == '__main__':
    main()
