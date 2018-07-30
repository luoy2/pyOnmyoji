
from controller import click
from combat import Combat, CombatResult
from findimg import wait_for_state, click_to_leaving_state, findimg
import img
import parties
import time


def main_yaoqi(times, target_monster):
    count = 0
    while count < times:
        yaoqi_loc = wait_for_state(img.party_img.YAOQIFENGYIN)
        click(yaoqi_loc)

        refresh_location = wait_for_state(img.party_img.REFRESH)
        parties.yaoqifengyin.find_monster(target_monster, refresh_location)

        combat = Combat('妖气封印')
        combat_result = combat.start()

        party_loc = wait_for_state(img.party_img.MAIN_PARTY, 15)
        time.sleep(1)
        click_to_leaving_state(img.party_img.MAIN_PARTY, rand_offset=10, location=party_loc)

        count += 1

# findimg(img.party_img.YAOQIFENGYIN)

if __name__ == '__main__':
    target_monster = img.ss_img.RIHEFANG
    count = 30
    main_yaoqi(12, img.ss_img.RIHEFANG)