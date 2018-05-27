import sys
from Tkinter import *
from ttk import *
import csv


class Post(object):
    def __init__(self, ID, user, text, ups, downs, parent):
        self.ID = ID
        self.user = user
        self.text = text
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

    def saveCsvString(self):
        #ID,user,ups,downs,parentName
        writer = csv.writer(open('test.csv', 'wb'))
        writer.writerow([str(self.ID), str(self.user), self.text, str(self.ups), str(self.downs), str(self.getParentID())])

    def saveCsvString(self, writer):
        writer.writerow([str(self.ID), str(self.user), self.text, str(self.ups), str(self.downs), str(self.getParentID())])

    def orderChildren(self):
        self.bestDescendant = None
        for child in self.children:
            if (self.bestDescendant == None) or (child.calcScore() > self.bestDescendant.calcScore()):
                self.bestDescendant = child



class votingPopUp(Toplevel):
    def __init__(self, master, treeclear, node):
        Toplevel.__init__(self, master)
        self.node = node
        self.treeclear = treeclear
        self.label = Label(self, text=node.ID)
        self.label.grid()
        self.upVote = Button(self, command=self.voteUp, text="Up")
        self.upVote.grid(row=1, column=0)
        self.downVote = Button(self, command=self.voteDown, text="Down")
        self.downVote.grid(row=1, column=1)
    def voteUp(self):
        self.node.ups += 1
        self.treeclear()
    def voteDown(self):
        self.node.downs += 1
        self.treeclear()
class PostElement():
    def __init__(self, master, post, refresh):
        self.post = post
        self.master = master
        self.refresh = refresh
        #I have no idea why we need this frame. it won't indent if I don't
        self.mainFrame = Frame(self.master, borderwidth=2, relief=RIDGE)
        self.makeInfoFrame(self.mainFrame)
        self.makeContentFrame(self.mainFrame)
        self.makeButtonFrame(self.mainFrame)

    def makeInfoFrame(self, master):
        self.infoFrame = Frame(master, borderwidth=2, relief=RIDGE)
        self.userLabel = Label(self.infoFrame, text=self.post.user)
        self.userLabel.grid(row=0, column=0)
        self.idLabel = Label(self.infoFrame, text=self.post.ID, justify=RIGHT)
        self.idLabel.grid(row=0, column=1, sticky=E+W)
    def makeContentFrame(self, master):
        self.contentFrame = Frame(master)
        tmpLabel = Label(self.contentFrame, text=self.post.text)
        tmpLabel.grid()
    def makeButtonFrame(self, master):
        self.buttonFrame = Frame(master)
        likeButton = Button(self.buttonFrame, text="Like")
        dislikeButton = Button(self.buttonFrame, text="Dislike")
        replyButton = Button(self.buttonFrame, text="Reply", command=self.addReply)
        likeButton.grid(row=1, column=0)
        dislikeButton.grid(row=1, column=1)
        replyButton.grid(row=1, column=2)

    def addReply(self):
        replyPost = Post(-1,"Alice", '', 0, 0, self.post)
        self.refresh()
    
    def _grid(self):
        self.infoFrame.grid(sticky=W+E)
        self.contentFrame.grid()
        self.buttonFrame.grid()
        self.mainFrame.grid()

class NewPostElement(PostElement):
    def __init__(self, master, post, refresh):
        PostElement.__init__(self, master, post, refresh)
    def makeContentFrame(self, master):
        self.contentFrame = Frame(master)
        self.textArea = Text(self.contentFrame, height=4)
        self.textArea.grid()
    def makeButtonFrame(self, master):
        self.buttonFrame = Frame(master)
        cancelButton = Button(self.buttonFrame, text="cancel", command=self.cancel)
        postButton = Button(self.buttonFrame, text="post", command=self.makePost)
        cancelButton.grid(row=0,column=0)
        postButton.grid(row=0,column=1)
    def cancel(self):
        self.post.parent.children.remove(self.post)
        self.refresh()
        del self
    def makePost(self):
        self.post.ID = 10
        self.post.text = self.textArea.get("1.0", END)
        self.refresh()

def gridPostAndChildren(master, post, refresh, indent=0):
    pFrame = Frame(master, borderwidth=5, relief=RIDGE)
    if post.ID == -1:
        #make temp element
        pElement = NewPostElement(pFrame, post, refresh)
    else:
        pElement = PostElement(pFrame, post, refresh)
    pElement._grid()
    pFrame.grid(sticky=W+E, padx=(40*indent,15))
    for child in post.children:
        gridPostAndChildren(master, child, refresh, indent + 1)


class board():
    def __init__(self, rootPost):
        #make the window
        self.tkRoot = Tk()
        self.rootPost = rootPost
        self.posts = []
        self.addPostToPosts(self.rootPost)
        self.sortPosts()
        self.mainFrame = Frame(self.tkRoot)
        self.makeMainArea()
        self.mainFrame.grid()
        self.makeSecondaryArea()
        self.makeButtonArea()
        self.tkRoot.mainloop()

    def makeMainArea(self):
        self.postArea = Frame(self.mainFrame)
        gridPostAndChildren(self.postArea, self.posts[0], self.refresh)
        self.postArea.grid(row=0, column=0)
    def makeSecondaryArea(self):
        self.sideFrame = Frame(self.tkRoot)
        for post in self.posts[::-1]:
            Label(self.sideFrame, text=post.text).grid()
        self.sideFrame.grid(row=0, column=1)


    def makeButtonArea(self):
        self.buttonFrame = Frame(self.tkRoot)
        self.saveButton = Button(self.buttonFrame, text="save", command=self.savePosts)
        self.saveButton.grid()
        self.loadButton = Button(self.buttonFrame, text="load", command=self.loadPosts)
        self.loadButton.grid()
        self.buttonFrame.grid()

    def addPostToPosts(self, post):
        self.posts.append(post)
        for child in post.children:
            self.addPostToPosts(child)

    def sortPosts(self):
        self.posts.sort(key=lambda post:post.calcScore())

    def savePosts(self):
        writer = csv.writer(open('test.csv', 'wb'))
        self.savePostsHelper(self.posts[0], writer)
    def loadPosts(self):
        self.posts = []
        reader = csv.reader(open('test.csv', 'rb'))
        for row in reader:
            print(row)
            self.loadPostHelper(row)
        self.refresh()

    def loadPostHelper(self, row):
        parent = None
        print("in helper")
        for post in self.posts:
            if post.ID == int(row[5]):
                parent = post
                break
        print (parent)
        newPost = Post(int(row[0]), row[1], row[2], int(row[3]), int(row[4]), parent)
        self.posts.append(newPost)


    def savePostsHelper(self, post, writer):
        post.saveCsvString(writer)
        for child in post.children:
            self.savePostsHelper(child, writer)
    
    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        post = None
        for candidate in self.posts:
            if candidate.ID == item:
                post = candidate
        votingPopUp(self.tkRoot, self.refresh, post)

    def refresh(self):
        for child in self.mainFrame.winfo_children():
            child.destroy()
        print("destroyed stuff, now I make stuff")
        for child in self.sideFrame.winfo_children():
            child.destroy()
        self.posts = []
        self.addPostToPosts(self.rootPost)
        self.sortPosts()
        self.makeMainArea()
        self.makeSecondaryArea()


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
    newPost = Post(1,"Bob", 'what i said', 2, 7, None)
    replyPost = Post(2,"Alice", 'what she said', 100, 2, newPost)
    SisterPost = Post(3,"Carrol",'a thing', 8, 2, newPost)
    SisterPost = Post(4,"Carrol", 'another thing', 215, 2, replyPost)
    newBoard = board(newPost)


def getCommand():
    return raw_input("Give me a command: ")

def doHelp():
    print("post    prints a default box")
    print("tree    prints a tree")

def doExit():
    print("we are exiting!")

if __name__ == "__main__":
    menu()
