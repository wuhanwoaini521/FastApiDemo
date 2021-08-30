import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
moudle_path = os.path.join(os.path.dirname(BASE_DIR))
cur_path = os.path.dirname(os.path.realpath(__file__))
screen_path_bug = os.path.join(os.path.dirname("."))

print(os.path.realpath(__file__))
print(os.path.dirname(os.path.realpath(__file__)))
print("Base_DIR : %s" % BASE_DIR)
print("_" * 50)

print(os.path.exists("D:hjhas.txt"))

print("_" * 50)

print("moudle_path : %s" % moudle_path)
print("cur_path : %s" % cur_path)
print("screen_path_bug : %s" % screen_path_bug)
