import os
import sys
from game import GameMap



#stdscr = curses.initscr()

def print_char(x, y, char):
    #print("{x} {y}")
    print("\033["+str(y)+";"+str(x)+"H"+char)

def clear_console():
    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    elif sys.platform.startswith('darwin'):
        os.system("clear")
    else:
        print("Unable to clear terminal. Your operating system is not supported.\n\r")


def change_printed_map(gm: GameMap):
    
    while(len(gm.changed_cells)!=0):
        pp = gm.changed_cells.popleft()
        
        c=' '
        if(gm.all_cells[pp[0], pp[1]].state==1):
            c='*'
        print_char(pp[0], pp[1], c)





