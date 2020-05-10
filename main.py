from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import os
import shutil
import time
from math import *
import re
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
import mutagen
import tkinter
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

global output
output = []


# from parsimonious.grammar import Grammar #pip install parsimonious




########################################################
class FossVisitor(NodeVisitor):
    def qkOut(self, T, V):
        KV = (T, V)
        ##print(KV)
        output.append(KV)
        return V

    def visit_tab(self, node, visited_children):
        return self.qkOut("Tab", node.text)

    # Selector Types
    def visit_Extension(self, node, visited_children):
        return self.qkOut("Extension", node.text)

    def visit_Date(self, node, visited_children):
        return self.qkOut("Date", node.text)

    def visit_Music(self, node, visited_children):
        return self.qkOut("Music", node.text)

    def visit_op(self, node, visited_children):
        return self.qkOut("OP", node.text)

    def visit_seperator(self, node, visited_children):
        return self.qkOut("Seperator", node.text)

    def visit_filename(self, node, visited_children):
        return self.qkOut("Filename", node.text)

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return node.text


########################################################
class appicationWindow:
    def __init__(self, window):
        # super(appicationWindow,window).__init__()
        # window properties
        self.window = window
        self.window.title("FOSL")
        self.window.minsize(700, 500)
        self.window.configure(background="#1F1F1F")
        self.window.wm_iconbitmap('myicon_6eB_icon.ico')

        # Root: text
        self.window.Label = ttk.Label(self.window, text="Root:")
        self.window.Label.grid(column=0, row=0, sticky="ew")
        self.window.Label.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 24, 'bold'))

        # FOSL Script words
        self.window.Labelfosl = ttk.Label(self.window, text="FOSL Script:")
        self.window.Labelfosl.grid(column=0, row=2, sticky="ew")
        self.window.Labelfosl.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 24, 'bold'))

        # FOSL pick destination words
        self.window.Labelfosl = ttk.Label(self.window, text="Destination:")
        self.window.Labelfosl.grid(column=0, row=3, sticky="ew")
        self.window.Labelfosl.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 24, 'bold'))

        self.window.dirPath = StringVar()  # Root/directory variable to keep track of root.
        self.window.destinationPath = StringVar()  # destination/directory variable to keep track of destination.
        self.window.doNotUpdate = StringVar()
        # self.window.doNotUpdate.set(self.window.destinationPath)#used for checking DO NOT UPDATE THIS VARIABLE
        self.window.filePath = StringVar()  # Fosl file location variable to keep track of root.
        self.window.doNotUpdatealso = StringVar()
        # self.window.doNotUpdatealso.set(self.window.filePath)
        self.window.errorStatusMsg = "All files sorted successfully"
        ##########################################################################################################################
        # rootFileButton
        self.window.rootFileButton = ttk.Button(self.window, text="Pick Root File Directory", command=self.dirPicker)
        self.window.rootFileButton.grid(column=1, row=0, sticky="ew")
        # foslFileButton
        self.window.foslFileButton = ttk.Button(self.window, text="Pick FOSL File", command=self.foslFilePicker)
        self.window.foslFileButton.grid(column=1, row=2, sticky="ew")
        # DestinationButton
        self.window.rootFileButton = ttk.Button(self.window, text="Pick Destination to Place Files",
                                                command=self.destPicker)
        self.window.rootFileButton.grid(column=1, row=3, sticky="ew")
        # text script area
        self.window.myFile = ttk.Label(self.window, text="Make your own script:")
        self.window.myFile.grid(column=0, row=4, sticky="ew", columnspan=2)
        self.window.myFile.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 18, 'bold'))
        self.window.myFileEntry = ScrolledText(self.window, width=25, height=13, wrap=WORD)
        self.window.myFileEntry.grid(column=0, row=5, columnspan=10, sticky="ew")
        self.window.myFileEntry.configure(background="#FFFFFF", foreground="#1F1F1F", font=('Georgia', 11, 'bold'))
        # executeScriptButton
        self.window.foslFileButton = ttk.Button(self.window, text="Organize Root",
                                                command=self.showStatus)  # change command to call status message **
        self.window.foslFileButton.grid(column=0, row=7, sticky="ew")
        # clear fields button
        self.window.clearButton = ttk.Button(self.window, text="Clear everything",
                                             command=self.reset)  # change command to call status message **
        self.window.clearButton.grid(column=0, row=8, sticky="ew")

        def commandWindow():  # help documentation window
            instructions = tk.Tk()
            instructions.wm_title("FOSL Commands")
            instructions.minsize(350, 250)
            instructions.configure(background="#1F1F1F")
            instructions.wm_iconbitmap('myicon_6eB_icon.ico')

            def closeWindow():
                instructions.destroy()

            ##sbar = Scrollbar(instructions)
           ##sbar.pack(side=RIGHT, fill=Y)
            commandsWords = ttk.Label(instructions,text=" General Syntax for Language is as follows:\n\tSelection : foldername\n\tExample: LastModifyDate.month.june : root\n\nFoldername = whatever you want to name the folder for this selection /sorting\n\nSelection: Selection is the metadata that you may want to filter the files by.\n\nChaining Selections: chaining selections is allowed \n\tor=||    , or typing the word or\n\tand=&&, or by typing the word and\nSupported selection object: \n\tLastmodify.month.[actualMonthName]\n\tLastmodify.month.june\n\n Commands:commands are case sensitive\n\tLastModifyDate.month.actualmonth           #actual month= ie January, April …\n\t LastModifyDate.month.actualDay               #actual day = ie Monday, Tuesday…\n\t Extension.actualFileType              #actual file type = ie pdf,docx ….\n\t size.greaterThan.actualSize                           #actual size = done in MB ie 40 , 1\n\t music.artist.flac.actualArtist          #actual artist = ie Boris,The_Beatles \n\t music.album.flac.actualAlbum          #actual album = ie.Desertshore,Pink_Moon\n\t music.genre.flac.actualGenre          #actual genre = ie Deep_House, Pop\n\t music.date.flac.actualDate              #actual date = ie 2015,1992\n\t music.artist.mp3.actualArtist          #actual artist = ie Boris,The_Beatles \n\t music.album.mp3.actualAlbum          #actual album = ie.Desertshore,Pink_Moon\n\t music.genre.mp3.actualGenre          #actual genre = ie Deep_House, Pop\n\t music.date.mp3.actualDate                           #actual date = ie 2015,1992")
            commandsWords.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 12, 'bold'))
            commandsWords.pack(side=TOP, fill=X)
            closeButton = ttk.Button(instructions, text="Exit", command=closeWindow)
            closeButton.pack(side=BOTTOM, fill=X)
            instructions.mainloop()

        # Commands button
        self.window.commandButton = ttk.Button(self.window, text="Commands",
                                               command=commandWindow)  # change command to call status message **
        self.window.commandButton.grid(column=1, row=7, sticky="ew")

    def dirPicker(self):
        directoryName = filedialog.askdirectory()
        self.window.dirPath.set(directoryName)
        self.window.showDir = ttk.Label(text="")
        self.window.showDir.grid(column=2, row=0, sticky="ew")
        self.window.showDir.configure(text=self.window.dirPath.get())
        self.window.showDir.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 18, 'bold'))
        print(self.window.destinationPath.get())
        print(self.window.doNotUpdate.get())
        if (self.window.destinationPath.get() == self.window.doNotUpdate.get()):
            self.window.destinationPath.set(directoryName)
            self.window.showDest = ttk.Label(text="")
            self.window.showDest.grid(column=2, row=3, sticky="ew")
            self.window.showDest.configure(text=self.window.destinationPath.get())
            self.window.showDest.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 18, 'bold'))

    def destPicker(self):
        directoryName = filedialog.askdirectory()
        self.window.destinationPath.set(directoryName)
        self.window.showDest = ttk.Label(text="")
        self.window.showDest.grid(column=2, row=3, sticky="ew")
        self.window.showDest.configure(text=self.window.destinationPath.get())
        self.window.showDest.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 18, 'bold'))

    def foslFilePicker(self):
        self.window.fosldirectoryName = filedialog.askopenfilename(initialdir="/", title="Pick Directory",
                                                                   filetypes=[("FOSL", ".FOSL")])
        self.window.filePath.set(self.window.fosldirectoryName)
        self.window.fFile = ttk.Label(self.window, text="")
        self.window.fFile.configure(text=self.window.filePath.get())
        self.window.fFile.grid(column=2, row=2, sticky="ew")
        self.window.fFile.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 18, 'bold'))

    def reset(self):
        print("resetting")
        self.window.dirPath = StringVar()  # Root/directory variable to keep track of root.
        self.window.destinationPath = StringVar()  # destination/directory variable to keep track of destination.
        self.window.doNotUpdate = StringVar()
        # self.window.doNotUpdate.set(self.window.destinationPath)#used for checking DO NOT UPDATE THIS VARIABLE
        self.window.filePath = StringVar()  # Fosl file location variable to keep track of root.
        self.window.doNotUpdatealso = StringVar()
        # self.window.doNotUpdatealso.set(self.window.filePath)
        self.window.errorStatusMsg = "All files sorted successfully"
        self.window.showDest.configure(text="")
        self.window.showDir.configure(text="")
        self.window.fFile.configure(text="")

    def showStatus(self):
        # parse script
        # self.parse()
        self.window.showmsg = ttk.Label(self.window, text="")  # change command to call status message **
        self.window.showmsg.grid(column=0, row=8, sticky="ew")
        self.window.Label.configure(background="#1F1F1F", foreground='#ffffff', font=('Georgia', 24, 'bold'))
        ##########################
        print("root:" + self.window.dirPath.get())
        print("destination:" + self.window.destinationPath.get())
        print(self.window.filePath.get())
        # self.window.doNotUpdatealso.set("abc")
        print(self.window.doNotUpdatealso.get())

        if ((len(self.window.myFileEntry.get("1.0", "end-1c")) != 0) and (
                self.window.filePath.get() != self.window.doNotUpdatealso.get())):
            self.window.errorStatusMsg = "error-file script and user script"
            print("error user file and fosl file")
        elif ((len(self.window.myFileEntry.get("1.0", "end-1c")) <= 0) and (
                self.window.filePath.get() == self.window.doNotUpdatealso.get())):
            self.window.errorStatusMsg = "error-no fosl file to sort"
            print("error-no fosl file to sort")
        elif (self.window.dirPath.get() == self.window.doNotUpdatealso.get()):
            self.window.errorStatusMsg = "error-no given root"
            print("error-no root to sort")
        elif (self.window.destinationPath.get() == self.window.doNotUpdatealso.get()):
            self.window.errorStatusMsg = "error-no destination"
            print("error-no destination")
        elif (self.window.filePath.get() != self.window.doNotUpdatealso.get()):
            arrayofcommands = []
            file = open(self.window.filePath.get(), 'r')
            for x in file:
                x = x.rstrip()
                x = x.lstrip()
                if (x != '' and x != '\n'):
                    self.parse(x)
                    arrayofcommands.append(x)
                # call function here
        else:
            print("Text input=" + self.window.myFileEntry.get("1.0", "end-1c"))
            print("end input")
            # print("first line: "+self.window.myFileEntry.get("1.0",END)[:self.window.myFileEntry.get("1.0",END).find('\n')])
            seachString = self.window.myFileEntry.get("1.0", "end-1c")
            seachString = seachString.rstrip()
            z = re.split(r'\n', seachString)
            print(z)
            arrayofcommands = []
            for x in z:
                x = x.rstrip()
                x = x.lstrip()
                if (x != '' and x != '\n'):
                    print("line: " + x)
                    self.parse(x)
                    arrayofcommands.append(x)
                # call function here

        root = self.window.dirPath.get()
        root = r"{}".format(root)

        destination = self.window.destinationPath.get()
        destination = r"{}".format(destination)

        originalDestination = destination


        sourceFiles = os.listdir(root)
        inputList = arrayofcommands

        dataList = []
        commandList = []
        operatorList = []

        for inputLine in inputList:
            dataList, operatorList, commandList = self.tokenSeparator(inputLine)
            precodeLine, codeLine, destination = self.codeLinesConstructor(dataList, operatorList, commandList, originalDestination)
            print(precodeLine)
            print(codeLine)
            self.codeExecutor(precodeLine, codeLine, destination,root)
            print(destination)
        
        self.window.showmsg.configure(text=self.window.errorStatusMsg)  # displays final status to user

    def monthConverter(self,month):
        switcher = {
            'Jan': 'January',
            'Feb': 'February',
            'Mar': 'March',
            'Apr': 'April',
            'May': 'May',
            'Jun': 'June',
            'Jul': 'July',
            'Aug': 'August',
            'Sep': 'September',
            'Oct': 'October',
            'Nov': 'November',
            'Dec': 'December',
        }

        return switcher.get(month, 'Invalid Month')

    def dayConverter(self, day):
        switcher = {
            'Mon': 'Monday',
            'Tue': 'Tuesday',
            'Wed': 'Wednesday',
            'Thu': 'Thursday',
            'Fri': 'Friday',
            'Sat': 'Saturday',
            'Sun': 'Sunday',

        }

        return switcher.get(day, 'Invalid day')

    def size(self, fileSize):
        intSize = 1000000 * int(fileSize)
        fileSize = str(intSize)
        codeLine = "os.path.getsize(path) > " + fileSize
        return codeLine

    def month(self, month):
        preCon = "modificationTime = os.path.getmtime(path)\nlocalTime = time.ctime(modificationTime)\nmodTime = localTime.split(' ')[1]\n"
        codeLine = "self.monthConverter(modTime) == " + "'" + month + "'"

        return preCon, codeLine

    def day(self, day):
        preCon = "modificationTimeDay = os.path.getmtime(path)\nlocalTimeDay = time.ctime(modificationTimeDay)\nmodTimeDay = localTimeDay.split(' ')[0]\n"
        codeLine = "dayConverter(modTimeDay) == " + "'" + day + "'"
        return preCon, codeLine

    def typeFile(self,type):
        fileType = '.' + type
        codeLine = "file.endswith('" + fileType + "')"
        return codeLine

    def artistFlac(self, artist, flag):
        preCond = ""
        artist = artist.replace('_', ' ')
        if (not (flag)):
            preCond = 'if(file.endswith(".flac")):\n\taudioFile = FLAC(path)\n\tfileArtist = str(audioFile["artist"])\n\tfileArtist = fileArtist[2:]\n\tfileArtist = fileArtist[:-2]\n'
        else:
            preCond = '\tfileArtist = str(audioFile["artist"])\n\tfileArtist = fileArtist[2:]\n\tfileArtist = fileArtist[:-2]\n\t'

        codeLine = "fileArtist== '" + artist + "' and (os.path.isfile(path) != False)"
        return preCond, codeLine

    def albumFlac(self, album, flag):
        preCond = ""
        album = album.replace('_', ' ')
        if (not (flag)):
            preCond = 'if(file.endswith(".flac")):\n\taudioFile = FLAC(path)\n\tfileAlbum = str(audioFile["album"])\n\tfileAlbum = fileAlbum[2:]\n\tfileAlbum = fileAlbum[:-2]\n'
        else:
            preCond = '\tfileAlbum = str(audioFile["album"])\n\tfileAlbum = fileAlbum[2:]\n\tfileAlbum = fileAlbum[:-2]\n\t'

        codeLine = "fileAlbum == '" + album + "' and (os.path.isfile(path) != False)"

        return preCond, codeLine

    def genreFlac(self, genre, flag):
        preCond = ""
        genre = genre.replace('_', ' ')
        if (not (flag)):
            preCond = 'if(path.endswith(".flac")):\n\taudioFile = FLAC(path)\n\tfileGenre = str(audioFile["genre"])\n\tfileGenre = fileGenre[2:]\n\tfileGenre = fileGenre[:-2]\n'
        else:
            preCond = '\tfileGenre = str(audioFile["genre"])\n\tfileGenre = fileGenre[2:]\n\tfileGenre = fileGenre[:-2]\n'

        codeLine = "fileGenre == '" + genre + "' and (os.path.isfile(path) != False)"
        return preCond, codeLine

    def dateFlac(self, date, flag):
        preCond = ""
        if (not (flag)):
            preCond = 'if(path.endswith(".flac")):\n\taudioFile = FLAC(path)\n\tfileDate = str(audioFile["date"])\n\tfileDate = fileDate[2:]\n\tfileDate = fileDate[:-2]\n'
        else:
            preCond = '\tfileDate = str(audioFile["date"])\n\tfileDate = fileDate[2:]\n\tfileDate = fileDate[:-2]\n'
        codeLine = "fileDate == '" + date + "' and (os.path.isfile(path) != False)"
        return preCond, codeLine

    def artistMP3(self, artist, flag):
        preCond = ""
        artist = artist.replace('_', ' ')
        if (not (flag)):
            preCond = 'if(file.endswith(".mp3")):\n\taudioFile = EasyID3(path)\n\tfileArtist = str(audioFile["artist"])\n\tfileArtist = fileArtist[2:]\n\tfileArtist = fileArtist[:-2]\n'

        else:
            preCond = '\tfileArtist = str(audioFile["artist"])\n\tfileArtist = fileArtist[2:]\n\tfileArtist = fileArtist[:-2]\n'

        codeLine = "fileArtist== '" + artist + "' and (os.path.isfile(path) != False)"
        return preCond, codeLine

    def albumMP3(self, album, flag):
        preCond = ""
        album = album.replace('_', ' ')
        if (not (flag)):
            preCond = 'if(file.endswith(".mp3")):\n\taudioFile = EasyID3(path)\n\tfileAlbum = str(audioFile["album"])\n\tfileAlbum = fileAlbum[2:]\n\tfileAlbum = fileAlbum[:-2]\n'

        else:
            preCond = '\tfileAlbum = str(audioFile["Album"])\n\tfileAlbum = fileAlbum[2:]\n\tfileAlbum = fileAlbum[:-2]\n'

        codeLine = "fileAlbum== '" + album + "' and (os.path.isfile(path) != False)"
        return preCond, codeLine

    def genreMP3(self, genre, flag):
        preCond = ""
        genre = genre.replace('_', ' ')
        if (not (flag)):
            preCond = 'if(file.endswith(".mp3")):\n\taudioFile = EasyID3(path)\n\tfileGenre = str(audioFile["genre"])\n\tfileGenre = fileGenre[2:]\n\tfileGenre = fileGenre[:-2]\n'

        else:
            preCond = '\tfileGenre = str(audioFile["genre"])\n\tfileGenre = fileGenre[2:]\n\tfileGenre = fileGenre[:-2]\n'

        codeLine = "fileGenre== '" + genre + "' and (os.path.isfile(path) != False)"
        return preCond, codeLine

    def dateMP3(self, date, flag):
        preCond = ""
        if (not (flag)):
            preCond = 'if(file.endswith(".mp3")):\n\taudioFile = EasyID3(path)\n\tfileDate = str(audioFile["date"])\n\tfileDate = fileDate[2:]\n\tfileDate = fileDate[:-2]\n'

        else:
            preCond = '\tfileDate = str(audioFile["date"])\n\tfileDate = fileDate[2:]\n\tfileDate = fileDate[:-2]\n'

        codeLine = "fileDate== '" + date + "' and (os.path.isfile(path) != False)"
        return preCond, codeLine

    def tokenSeparator(self, inputLine):
        dataList = [];
        operatorList = [];
        commandList = [];
        inputList = inputLine.split()

        for token in inputList:
            if (token == "||" or token == "or" or token == "&&" or token == "and"):
                operatorList.append(token)
            else:

                if (token == ":"):
                    commandList.append(token)

                else:
                    listToken = token.rsplit(".", 1)
                    dataList.append(listToken[-1])
                    listToken.pop()
                    command = ".".join(listToken)
                    commandList.append(command)

        commandList.pop()
        return dataList, operatorList, commandList

    def codeLinesConstructor(self,dataList, operatorList, commandList, destination):
        codeLine = ""
        preConditionLine = ""
        flagForFlac = False
        flagForMP3 = False
        count = 0

        for command in commandList:

            tempPreConditionLine = ""
            tempCodeLine = ""
            if (command == "LastModifyDate.month"):
                tempPreConditionLine, tempCodeLine = self.month(dataList[0])

            elif (command == "LastModifyDate.day"):
                tempPreConditionLine, tempCodeLine = self.day(dataList[0])

            elif (command == "Extension"):
                tempCodeLine = self.typeFile(dataList[0])

            elif (command == "size.greaterThan"):
                tempCodeLine = self.size(dataList[0])

            elif (command == "music.artist.flac"):

                tempPreConditionLine, tempCodeLine = self.artistFlac(dataList[0], flagForFlac)
                flagForFlac = True
            elif (command == "music.album.flac"):
                tempPreConditionLine, tempCodeLine = self.albumFlac(dataList[0], flagForFlac)
                flagForFlac = True
            elif (command == "music.genre.flac"):
                tempPreConditionLine, tempCodeLine = self.genreFlac(dataList[0], flagForFlac)
                flagForFlac = True
            elif (command == "music.date.flac"):
                tempPreConditionLine, tempCodeLine = self.dateFlac(dataList[0], flagForFlac)
                flagForFlac = True
            elif (command == "music.artist.mp3"):
                tempPreConditionLine, tempCodeLine = self.artistMP3(dataList[0], flagForMP3)
                flagForMP3 = True
            elif (command == "music.album.mp3"):
                tempPreConditionLine, tempCodeLine = self.albumMP3(dataList[0], flagForMP3)
                flagForMP3 = True
            elif (command == "music.genre.mp3"):
                tempPreConditionLine, tempCodeLine = self.genreMP3(dataList[0], flagForMP3)
                flagForMP3 = True
            elif (command == "music.date.mp3"):
                tempPreConditionLine, tempCodeLine = self.dateMP3(dataList[0], flagForMP3)
                flagForMP3 = True
            elif (command == ":"):
                destination = destination + "\\" + dataList[0]
                if not os.path.exists(destination):
                    os.makedirs(destination)

            codeLine = codeLine + tempCodeLine
            preConditionLine = preConditionLine + tempPreConditionLine
            dataList.remove(dataList[0])

            if (len(operatorList) != 0):
                if (operatorList[0] == "||" or operatorList[0] == "or"):
                    codeLine = codeLine + " or "

                elif (operatorList[0] == "&&" or operatorList[0] == "and"):
                    codeLine = codeLine + " and "

                operatorList.remove(operatorList[0])

        codeLine = "if( " + codeLine + "):\n\tshutil.move(path,destination)"
        print(codeLine)
        return preConditionLine, codeLine, destination

    def codeExecutor(self, preCond, codeLine, destination,root):
        for dir, subdirs, files in os.walk(root):
            for file in files:
                path = os.path.join(dir, file)
                try:
                    exec(preCond)
                    exec(codeLine)
                    self.window.errorStatusMsg = "No Error"
                except:
                    self.window.errorStatusMsg = "Syntax Error"
    def parse(self, sourceText):
        # dosent support left recursion
        grammar = Grammar(
            """
            expression =  tab* selection _? seperator _? filename? _?
            selection  =  selector _? ( _? op _? selector)*
            selector   =  kw ("->" args)?
            op         =  or / and / gt / lt
            or         =  "or" / "||" / "|"
            and        =  "and" / "&&" / "&"
            gt         =  ">"
            lt         =  "<"
            kw         =  Extension / Date / Music
            Extension  =  ~"Extension\.[A-Z0-9]*"i
            Date       =  ~"LastModifyDate(\.[A-Z0-9]*)+"i
            Music      =  ~"Music(\.[A-Z0-9]*)+"i
            args       =  "deep"
            seperator  =  ":"
            filename   =  ~"[A-Z0-9]*"i
            tab        =  "\t"
            _          =  ~"( |\t)*"
            """)
        # Use sourceText instead of hardcoded source code line
        try:
            tree = grammar.parse(sourceText)
            Fv = FossVisitor()
            Fv.visit(tree)
            return output
        except:
            self.window.errorStatusMsg = "Syntax Error"





if __name__ == '__main__':
    root_ = Tk()
    appWindow = appicationWindow(root_)
    root_.mainloop()