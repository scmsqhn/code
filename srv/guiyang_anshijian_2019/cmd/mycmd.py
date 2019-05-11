"""
author   : qin hai ning
datetime : 2019/4/15 下午6:45
file     : test.py
project  : guiyang_anshijian_2019
"""

import fire

class Calculator(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number

if __name__ == '__main__':
  fire.Fire(Calculator)