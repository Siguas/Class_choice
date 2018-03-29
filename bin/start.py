#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:SiWen

import os
import sys
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
#print(sys.path)

from core import main
from config import settings

if __name__ == '__main__':
    obj = main.Main()
    obj.run()
