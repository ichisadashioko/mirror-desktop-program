import os
import time
import json
import traceback

from PIL import ImageGrab

import numpy as np
import cv2


class Config:
    def __init__(self, top=0, left=0, right=1920, bottom=1080):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

    def __repr__(self):
        return repr(self.__dict__)


config = Config()

config_fpath = 'config.json'
if os.path.exists(config_fpath):
    try:
        with open(config_fpath, mode='r', encoding='utf-8') as infile:
            obj = json.load(infile)
            config = Config(**obj)
    except:
        pass

WINDOW_NAME = 'cv2-window'

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
fullscreen = False


while True:
    try:
        screen = np.array(ImageGrab.grab(
            bbox=(
                config.left,
                config.top,
                config.right,
                config.bottom,
            )
        ))
    except:
        # lock screen while fullscreen
        # or on Linux where ImageGrab is not supported
        traceback.print_exc()
        break

    # print(screen.shape)

    # screen = cv2.resize(
    #     src=screen,
    #     dsize=(1920, 1080),
    #     interpolation=cv2.INTER_NEAREST,
    # )

    screen = cv2.resize(
        src=screen,
        dsize=None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_NEAREST,
    )

    # print(screen.shape)

    # screen = cv2.GaussianBlur(
    #     src=screen,
    #     ksize=(3, 3),
    #     sigmaX=0,
    # )

    screen = cv2.blur(
        src=screen,
        ksize=(2, 2),
    )

    cv2.imshow(WINDOW_NAME, cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))

    key = cv2.waitKey(1) & 0xff

    if key == ord('q'):
        cv2.destroyAllWindows()
        break

    elif key == ord('f'):
        print('toggle fullscreen')
        if fullscreen:
            fullscreen = False
            cv2.setWindowProperty(
                winname=WINDOW_NAME,
                prop_id=cv2.WND_PROP_FULLSCREEN,
                prop_value=cv2.WINDOW_NORMAL,
            )
        else:
            fullscreen = True
            cv2.setWindowProperty(
                winname=WINDOW_NAME,
                prop_id=cv2.WND_PROP_FULLSCREEN,
                prop_value=cv2.WINDOW_FULLSCREEN,
            )
    elif key == ord('t'):
        print(config)
        top_str = input('Enter top position: ')
        try:
            config.top = int(top_str)
            print('set top to', top)
        except:
            pass

    elif key == ord('l'):
        print(config)
        left_str = input('Enter left position: ')
        try:
            config.left = int(left_str)
            print('set left to', left)
        except:
            pass
    elif key == ord('w'):
        print(config)
        right_str = input('Enter right: ')
        try:
            config.right = int(right_str)
            print('set right to', right)
        except:
            pass
    elif key == ord('h'):
        print(config)
        bottom_str = input('Enter bottom: ')
        try:
            config.bottom = int(bottom_str)
            print('set bottom to', bottom)
        except:
            pass

if os.path.exists(config_fpath):
    modified_time = int(os.path.getmtime(config_fpath))
    backup_filename = f'{modified_time}-{config_fpath}'
    os.rename(config_fpath, backup_filename)

with open(config_fpath, mode='w', encoding='utf-8') as outfile:
    json.dump(
        obj=config.__dict__,
        fp=outfile,
        ensure_ascii=False,
        indent=4,
    )
