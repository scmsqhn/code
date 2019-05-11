#!/usr/bin/python
#coding:utf8
"""
Strategy
In most of other languages Strategy pattern is implemented via creating some base strategy interface/abstract class and
subclassing it with a number of concrete strategies (as we can see at http://en.wikipedia.org/wiki/Strategy_pattern),
however Python supports higher-order functions and allows us to have only one class and inject functions into it's
instances, as shown in this example.
"""
import types

class StrategyMatch:

    def __init__(self, func=None):
        self.name = 'Strategy of address match'
        if func is not None:
            self.execute = types.MethodType(func, self)

    def execute(self):
        print(self.name)

def execute_replacement1(self):
    print(self.name + ' from execute 1')

def execute_replacement2(self):
    print(self.name + ' from execute 2')

if __name__ == '__main__':
    strat0 = StrategyMatch()

    strat1 = StrategyMatch(execute_replacement1)
    strat1.name = 'Strategy Example 1'

    strat2 = StrategyMatch(execute_replacement2)
    strat2.name = 'Strategy Example 2'

    strat0.execute()
    strat1.execute()
    strat2.execute()
