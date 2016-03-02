# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

'''
A singleton implementation of a counter
'''
# todo
class counter(object):
    @staticmethod
    def get_instance():
        return counter()

    def __init__(self):
        pass