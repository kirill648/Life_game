from game import GameMap 
import front
import sys
import time

def how_use():
    print('Using: python main.py path/to/config/file')
    print('Config file should contain in start positions of live cells [ \'*\' == live cell ]')

def parse_config(filename):
    res = []
    f = open(filename, "r")
    c = 1
    for l in f:
        inds = [ind for ind, ch in enumerate(l) if ch == "*" ]
        for i in inds:
            res.append((i+1, c))
        c+=1
    return res

def parse_config_old(filename):
    res = []
    f = open(filename, "r")
    for l in f:
        pp = list(map(int, l.split(' ')[:2]))
        if(len(pp)==2):
            res.append((pp[0], pp[1]))
        else:
            print("[Panic]: Wrong config format\n")
            exit(0)
    return res
     
def main():
    if(len(sys.argv)!=2):
        return how_use()
    else:
        coord= parse_config(sys.argv[1])
        front.clear_console()
        gm = GameMap(coord)
        front.change_printed_map(gm)

        while(not gm.is_end()):
            time.sleep(0.2)
            gm.processed()
            front.change_printed_map(gm)



if(__name__== "__main__"):
    main()