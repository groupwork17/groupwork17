#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple program on automatically finding all commits of a range starting at a git revision.
Educational purpose only, do not use for other purpose please!
"""

__author__ = "Group 17, CS 212, Lanzhou University"
__copyright__ = "Copyright (c) 2020, Study Project in Lanzhou University , China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = "ShenJiacheng"
__email__ = "shenjch18@lzu.edu.cn"
__status__ = "Experimental"

import re
import pandas as pd
from subprocess import Popen, PIPE, DEVNULL


class Rev:
    """
    One revision as an instance
    """
    def __init__(self, rev, revrange):
        """
        revision name and the range should be provided of an instance
        :param rev:
        :param revrange:
        """
        self.rev = rev
        self.revrange = revrange
        self.repo = 'D:\git repository\linux-stable'

    def get_commit_cnt(self, next_rev):
        """
        return the length of commits log from base revision to the target revision
        :param next_rev:
        :return:
        """
        tagrange = self.rev + ".." + next_rev
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + tagrange
        git_rev_list = Popen(gitcnt, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if len(cnt) == 0:
            pass
            # raise TagNotExistError("No such revision range: {0}..{1}, please check tag again!"
            #                        .format(self.rev, self.rev + str(self.revrange)))
        return len(cnt)

    def get_tag_days(self, rev):
        """
        return the days between the target revision to the base
        :param rev:
        :return:
        """
        SecPerHour = 3600
        HourPerDay = 24
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev
        git_tag_date = Popen(gittag, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds = int(git_tag_date.communicate()[0])
        day = seconds // (SecPerHour * HourPerDay)
        return day

    def get_log(self, rev2):
        """
        return the days and commit log, return False if no revision exist.
        :param rev2:
        :return:
        """
        commit_cnt = self.get_commit_cnt(rev2)
        if commit_cnt:
            current = self.get_tag_days(rev2)
            base = self.get_tag_days(self.rev)
            days = current - base
            return days, commit_cnt
        else:
            return False

    def log_print(self):
        """
        print out the result in a pretty way, and load it into a file.
        :return:
        """
        count = 0
        data = []
        for sl in range(1, self.revrange+1):
            rev2 = self.rev + "." + str(sl)
            days, commit_cnt = self.get_log(rev2)
            if commit_cnt:
                print(sl, days, commit_cnt, days-count)
                data.append([days, commit_cnt, days-count])
            else:
                break
            count = days
        header = ["days", "bugs", "diff"]
        tb = pd.DataFrame(columns=header, data=data)
        tb.to_csv('{0}.csv'.format(self.rev))


class TagError(Exception):
    def __init__(self, msg):
        self.msg = msg


class TagNotExistError(TagError):
    pass


def main():
    try:
        rev_in = input("Type the tag(e.g. 'v4.4'):")
        range_in = input("Type the patchlevel range(e.g. '100'):")
        rev = Rev(rev_in, int(range_in))
        rev.log_print()
    except TypeError:
        print('argument type wrong: the first arg should be like"v4.1", and the second should be an int.')


if __name__ == "__main__":
    main()
