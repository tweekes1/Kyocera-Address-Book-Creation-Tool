import os, sys

curr_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(curr_path, "utils"))

from utils.term import Terminal

cli = Terminal()
cli.cmdloop()
