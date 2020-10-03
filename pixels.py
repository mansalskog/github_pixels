#!/usr/bin/env python3

import subprocess
import datetime
import math

FILE_NAME = "timestamp.txt"
PIXELS = """
###  ##       #   #       ##### #                  #
  #  # #     # # # #     #  #   #                  #
  #  # #  #  # # # #     #  #   #      #  # #   #  #
 ######  # # ##  ##  ##   # #  ####   # # ## # # # #
# #  #  ###  #   #  ## #    # # #  # ###  #   ###  #
# #  # # #  ##  ##  #  #    #   #  ## #  ##    #    
 ##  ##   ##  ##  ## ##     #   #  #   ## #     ## #"""
PIXELS = PIXELS.replace("\n", "")
if len(PIXELS) != 52 * 7:
    print("Invalid pixels!")
    exit()

def commit(date, content):
    with open(FILE_NAME, "w") as f:
        f.write(content)
    git_env = {
        "GIT_AUTHOR_DATE": date.isoformat(),
        "GIT_COMMITTER_DATE": date.isoformat()}
    subprocess.run(
        ["git", "commit", "-m", "'" + content + "'", "--", FILE_NAME],
        env = git_env)


today = datetime.datetime.combine(
    datetime.date.today(),
    datetime.time(13, 37))
end_of_week = today + datetime.timedelta(
    days = (5 - today.weekday()) % 7)

commit_date = end_of_week - datetime.timedelta(days = len(PIXELS) - 1)

for i in range(len(PIXELS)):
    j = 52 * (i % 7) + i // 7
    if PIXELS[j] != " ":
        commit(commit_date, str(i))
    commit_date += datetime.timedelta(days = 1)
