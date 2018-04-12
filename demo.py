import sys
from Tkinter import *
from ttk import *


class Post(object):
    def __init__(self, ID, user, ups, downs, parent):
        self.ID = ID
        self.user = user
        self.ups = ups
        self.downs = downs
        self.parent = parent
        self.children = []
        self.bestDescendant = None

        if (self.parent != None):
            self.parent.addChild(self)

    def __str__(self):
        #find the sub strings
        topLine = "-"*23 + "\n"
        userLine = "|User: {:^15}|\n".format(self.user)
        scoreLine = "|Score: {:>14}|\n".format(self.calcScore())
        descendantLine = "|Best: {:>15}|\n".format(self.printBestDescendant())
        return topLine + userLine + scoreLine + descendantLine + topLine

    def calcScore(self):
        return self.ups - self.downs

    def printBestDescendant(self):
        if self.bestDescendant == None:
            return "N/A"
        else:
            return self.bestDescendant.user
    
    def getParentID(self):
        if self.parent == None:
            return ""
        else:
            return self.parent.ID

    def addChild(self, child):
        self.children.append(child)
        if (self.bestDescendant == None) or (child.calcScore() > self.bestDescendant.calcScore()):
            self.bestDescendant = child

    def toCsvString(self):
        #ID,user,ups,downs,parentName
        return str(self.ID) + "," + str(self.user) + "," + str(self.ups) + "," + str(self.downs) + "," + str(self.getParentID())

class votingPopUp(Toplevel):
    def __init__(self, master, tree, node):
        Toplevel.__init__(self, master)
        self.label = Label(self, text=node.ID)
        self.label.grid()
        self.upVote = Button(self, command=self.voteUp)
        self.upVote.grid(row=1, column=0)
        self.downVote = Button(self, command=self.voteDown)
        self.downVote.grid(row=1, column=1)
    def voteUp(self):
        pass
    def voteDown(self):
        pass

class board():
    def __init__(self, postList):
        #make the window
        self.tkRoot = Tk()
        self.posts = postList
        self.tree = Treeview(self.tkRoot)
        self.tree["columns"] = ["User", "Score"]
        for post in self.posts:
            self.tree.insert(post.getParentID(), "end", iid=post.ID, text=post.ID, values=(post.user, post.calcScore()))
        self.tree.pack()
        print ("Off to the races!")
	self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tkRoot.mainloop()

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        post = None
        for candidate in self.posts:
            if candidate.ID == item:
                post = candidate
        votingPopUp(self.tkRoot, self.tree, post)


#make default menu
def menu():
    if (len(sys.argv) > 1):
        command = sys.argv[1]
    else:
        command = "Help"
    doCommand(command)
    #the command was exit
    doExit()

def doCommand(command):
    if (command == "Help"):
        doHelp()
    elif (command == "post"):
        doPrint()
    elif (command == "tree"):
        doTree()
    elif (command == "CSV"):
        printCSV()
    elif (command == "board"):
        doBoard()
    else:
        print ("I don't know that command")
        doCommand("Help")

def doPrint():
    newPost = Post(1,"Bob", 7, 2, None)
    replyPost = Post(2,"Alice", "Noting", 7, 2, newPost)
    print(newPost)

def doTree():
    newPost = Post(1,"Bob", 7, 2, None)
    replyPost = Post(2,"Alice",  7, 2, newPost)
    SisterPost = Post(3,"Carrol", 8, 2, newPost)
    printTree(newPost,0)

def printCSV():
    newPost = Post(1,"Bob", 7, 2, None)
    replyPost = Post(2,"Alice",  7, 2, newPost)
    SisterPost = Post(3,"Carrol", 8, 2, newPost)
    print(SisterPost.toCsvString())
    print(newPost.toCsvString())

def printTree(root, indentLevel):
    indent = " "*13*indentLevel
    for line in str(root).splitlines():
        print (indent + line)
    for child in root.children:
        printTree(child, indentLevel + 1)

def doBoard():
    newPost = Post("1","Bob", 7, 2, None)
    replyPost = Post("2","Alice",  7, 2, newPost)
    SisterPost = Post("3","Carrol", 8, 2, newPost)
    newBoard = board([newPost,replyPost,SisterPost])


def getCommand():
    return raw_input("Give me a command: ")

def doHelp():
    print("post    prints a default box")
    print("tree    prints a tree")

def doExit():
    print("we are exiting!")

if __name__ == "__main__":
    menu()
