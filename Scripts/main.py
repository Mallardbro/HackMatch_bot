import time

import Grid
import Intelligence
import Movement
import Settings
import Tile
import cv2
import numpy as np
from PIL import ImageGrab

player = Movement.Player()
block_fail_count = 0
out_of_synce_count = 0
colours = {'red': (0, 0, 255), 'green': (0, 255, 0), 'orange': (0, 172, 255), 'pink': (172, 0, 255),
           'violet': (255, 0, 172)}

frames = -2

if Settings.SCREENSHOT_NUMBER == 0:
    frames = 0
    for count in range(3, 0, -1):
        print(count)
        time.sleep(1)

while frames != -1:
    frames += 1

    # Load image, select region, convert to grayscale.
    if Settings.SCREENSHOT_NUMBER == 0:
        full_img_bgr = np.array(ImageGrab.grab())
        full_img_rgb = cv2.cvtColor(full_img_bgr, cv2.COLOR_BGR2RGB)

        # cv2.imwrite("../Images/Screenshots/ImageGrab.jpg", full_img_rgb)

    else:
        full_img_rgb = cv2.imread(f"..\Images\Screenshots\Screenshot {Settings.SCREENSHOT_NUMBER}.jpg")

    # Uncomment if resolution is not 1440p (That's a lot of pixels!)
    # full_img_rgb = cv2.resize(full_img_rgb, (2560, 1440))
    # [Debug purposes] cv2.imwrite("../Images/Screenshots/Rescaled.jpg", full_img_rgb)
    # res_x = full_img_rgb.shape[1]
    # res_y = full_img_rgb.shape[0]

    img_rgb = full_img_rgb[180:1070, 580:1270]
    # cv2.imwrite("../Images/Screenshots/ROI.jpg", img_rgb)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    grid = Grid.Grid()

    # Get player position
    player_slice_rgb = full_img_rgb[1170:1200, 580:1265]
    player_slice_gray = cv2.cvtColor(player_slice_rgb, cv2.COLOR_BGR2GRAY)

    template_player = cv2.imread("../Images/Templates/player.jpg", 0)
    res = cv2.matchTemplate(player_slice_gray, template_player, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.92)

    try:
        x = loc[1][0]
    except IndexError:
        block_fail_count += 1
        print(f"Holding a block?? {block_fail_count}")
        player.grab()
        player.execute()
        continue

    x = loc[1][0]
    _w = player_slice_gray.shape[1]
    position = int(round((x - _w / 14) / 100))
    # print(f"Pos = {position}.")
    if player.pos != position:
        print(f"Player out of sync -{out_of_synce_count}.")
    # Out of sync. Re-sync
    player.pos = position


    for col in colours:
        # Loop through all templates, colours and pips, and append to the grid's list of tiles.
        for pip in [True, False]:
            if pip:
                template = cv2.imread(f"../Images/Templates/{col}-pip.jpg", 0)
            else:
                template = cv2.imread(f"../Images/Templates/{col}.jpg", 0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.92
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                # Over-matching fix: Only add/draw tiles that are far enough away from already found tiles.
                for t in grid.pre_tiles[::-1]:
                    dx = abs(pt[0] - t.ix)
                    dy = abs(pt[1] - t.iy)
                    if dx < 10 and dy < 10:
                        break
                else:  # I'm so happy that I used this! :)
                    grid.pre_tiles.append(Tile.Tile(_ix=pt[0], _iy=pt[1], _colour=col, _pip=pip))


    grid.setup_tiles()
    AI = Intelligence.Intelligence(grid, player)

    try:
        winner = AI.analyse()
    except:
        print("AI.analyse broke. Next frame...")
        continue

    for t in grid.tiles:
        if t:
            t.text = str(t.index) + "|" + str(t.chained)
    grid.draw(img_rgb)
    # print(grid)
    if not winner:
        print("no winner for this frame,. sleep!")
        time.sleep(0.017)
        continue

    try:
        AI.move(winner)
    except ValueError:
        print("AI.move gave valueError, sleep")
        time.sleep(0.017)
        continue

    if Settings.SHOW_WINDOW:
        cv2.imshow('Result', img_rgb)
        cv2.waitKey()
    cv2.destroyAllWindows()

    print(f"Done with frame {frames}")

