#!/usr/bin/env python3

import sys
import os
import datetime
import subprocess
import tempfile

if len(sys.argv) < 4:
    print("usage: " + sys.argv[0] + "<repo_url> <author_name> <author_email>")
    exit()

repo_url = sys.argv[1]
author_name = sys.argv[2]
author_email = sys.argv[3]

file_name = "dummy.txt"

def commit(date, content):
    with open(file_name, "w") as f:
        f.write(content)

    git_env = {
        "GIT_AUTHOR_NAME": author_name,
        "GIT_COMMITTER_NAME": author_name,
        "GIT_AUTHOR_EMAIL": author_email,
        "GIT_COMMITTER_EMAIL": author_email,
        "GIT_AUTHOR_DATE": date.isoformat(),
        "GIT_COMMITTER_DATE": date.isoformat()}
    subprocess.run(
        ["git", "commit", "-m", content, "--", file_name],
        env = git_env)

pixels = """
###  ##       #   #       ##### #                  #
  #  # #     # # # #     #  #   #                  #
  #  # #  #  # # # #     #  #   #      #  # #   #  #
 ######  # # ##  ##  ##   # #  ####   # # ## # # # #
# #  #  ###  #   #  ## #    # # #  # ###  #   ###  #
# #  # # #  ##  ##  #  #    #   #  ## #  ##    #    
 ##  ##   ##  ##  ## ##     #   #  #   ## #     ## #"""
pixels = pixels.replace("\n", "")
if len(pixels) != 52 * 7:
    print("pixels should be 52 * 7 array")
    exit()

with tempfile.TemporaryDirectory() as tmp_dir:
    os.chdir(tmp_dir)
    subprocess.run(["git", "clone", repo_url, "."])
    open(file_name, "w").close()
    subprocess.run(["git", "add", file_name])

    today = datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(13, 37))
    end_of_week = today + datetime.timedelta(
        days = (5 - today.weekday()) % 7)

    commit_date = end_of_week - datetime.timedelta(days = len(pixels) - 1)
    for i in range(len(pixels)):
        j = 52 * (i % 7) + i // 7
        if pixels[j] != " ":
            commit(commit_date, str(i))

        commit_date += datetime.timedelta(days = 1)

    print("input github credentials to push commits")
    subprocess.run(["git", "push", "origin", "master"])
