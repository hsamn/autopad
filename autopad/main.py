from autopad.api.posts import POSTS
from autopad.uia.notepad import open_notepad, paste_and_save
from autopad.utils.helpers import close_mss

def try_paste_and_save(content, name, ext):
    for _ in range(3):
        time.sleep(3)
        app, window = open_notepad()
        if paste_to_notepad(window, content, name, ext):
            return
    close_mss()
    raise TimeoutError("Pasting and Saving timeout")

def main():
    for post in POSTS:
        content, name, ext = post["content"], post["name"], post["ext"]
        try_paste_and_save(content, name, ext)
    close_mss()

if __name__ == "__main__":
    main()

