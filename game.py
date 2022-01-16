
from collections import deque




class GameMap:
    all_cells={} #Cells
    live_cells= set() # coordinates
    changed_cells = deque() # coordinates
    processed_cells = deque() # coordinates
    def is_end(self):
        return (len(self.live_cells)==0)
    def change_cell(self, px, py, st):
        # st = 0 - dead cell
        #    = 1 - live cell
        #    = 2 - try create new dead cell
        cell = self.all_cells.get((px, py))
        if(cell == None):
            if(st==2):
                st=0
            cell = Cell(self, px, py, st)
        else:
            if(st!=2):
                cell.force_change(st)
        
        return cell
    
    def processed(self):
        self.changed_cells = deque()

        for pp in self.live_cells:
            cl = self.all_cells[pp]
            cl.processed()
            
        for pp in self.changed_cells:
            cl = self.all_cells[pp]
            cl.update()


        while(len(self.processed_cells)!=0):
            pp=self.processed_cells.popleft()
            cl = self.all_cells[pp]
            cl.defroze()


    def __init__(self, coord):
        for pp in coord:
            Cell(self, pp[0], pp[1], 1)
        



class Cell:
    x=0
    y=0
    prev_state = 0
    state=0
    used = 0

    def force_change(self, st):
        if(st!=self.prev_state):
            self.state=st
            self.prev_state=st
            self.gamemap.changed_cells.append((self.x, self.y))

    def change(self, st):
        if(st!=self.prev_state):
            self.state=st
            self.gamemap.changed_cells.append((self.x, self.y))

            

    def update(self):
        self.prev_state=self.state
        if(self.state==1):
            self.activate_near_cells()
            self.gamemap.live_cells.add( (self.x, self.y) )
        else:
            self.gamemap.live_cells.remove( (self.x, self.y) )
        
    def defroze(self):
        self.used=0

    def activate_near_cells(self):
        for xd in range(-1, 2):
                for yd in range(-1, 2):
                    if((xd==0)and(yd==0)):
                        continue
                    self.gamemap.change_cell(self.x+xd, self.y+yd, 2)

    def __init__(self, gm: GameMap, px, py, st):
        #print(f"[Cell.init]: {px} {py} {st}")
        self.gamemap = gm
        self.prev_state=st
        self.used = 0
        self.state= st
        self.x=px
        self.y=py

        self.gamemap.all_cells[(self.x, self.y)]=self

        if(st==1):
            self.gamemap.changed_cells.append((self.x, self.y))
            self.gamemap.live_cells.add((self.x, self.y))
            self.activate_near_cells()
            
            
    def update_state(self):
        res = 0
        for xd in range(-1, 2):
                for yd in range(-1, 2):
                    if((xd==0)and(yd==0)):
                        continue
                    cl= self.gamemap.all_cells.get((self.x+xd, self.y+yd))
                    if(cl!=None):
                        res += cl.prev_state
        
        if((self.prev_state==0)and(res==3)):
            self.change(1)
        elif((self.prev_state==1)and(res!=2)and(res!=3)):
            self.change(0)

    def processed(self):
        #print(f"[Cell.procesed]: {self.x} {self.y} {self.state} {self.prev_state}")
        if(self.used!=1):
            self.used=1
            self.gamemap.processed_cells.append( (self.x, self.y) )
            self.update_state()

            if(self.prev_state==1):
                for xd in range(-1, 2):
                    for yd in range(-1, 2):
                        if((xd==0)and(yd==0)):
                            continue
                        self.gamemap.all_cells[(self.x+xd, self.y+yd)].processed()


                

    
