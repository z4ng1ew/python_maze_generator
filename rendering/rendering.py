from rendering.render_main.rendermain import RenderMain
from rendering.render_maze.rendermaze import RenderMaze

class Render:
    def __init__(self):
        self.window = None



    def showMain(self):
        if not self.window:
            self.window = RenderMain(app=self)
        self.window.render()
        self.window.root.mainloop() 

    def showMaze(self, size):
        RenderMaze(app=self, root=self.window.root, size = int(size), file = None).render()

    def loadMaze(self, file):
        RenderMaze(app=self, root=self.window.root, size = None, file = file).render()        




