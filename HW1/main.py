import sys
from zipfile import ZipFile
import os
import re

class CLI:
    def __init__(self, archiveName):
        self.currentPath = ""
        self.directory = ZipFile(archiveName)
        self.exec()

    def ls(self, absPath=""):
        path = self.currentPath
        if absPath != "":
            path = absPath

        if (len(path) != 0):
            path += '/'

        name = ""
        for fullName in self.directory.namelist():
            if fullName.startswith(path):
                name = fullName.replace(path, "")
                if (name != "" and 
                    ((len(name.split("/")) == 1) or 
                    (
                        len(name.split("/")) == 2 and 
                        name.endswith("/")
                    ))):
                    print(name)

    def isFile(self, path):
        for name in self.directory.namelist():
            if (name == path):
                return True
        return False

    def isDir(self, path):
        path += "/"
        for name in self.directory.namelist():
            if (name == path):
                return True
        return False

    def normalizePath(self, path):
        if (path.startswith("/")):
            path = path[1:]
        if (path.endswith("/")):
            path = path[:-1]

        return os.path.join(self.currentPath, path).replace("\\", "/")

    def cd(self, to):
        if (to == "~" or to == "/"): 
            self.currentPath = ""

        elif ((to == ".." or to == "../") and len(self.currentPath)):
            matches = re.findall("^(.+)\/", self.currentPath)
            if (len(matches)):
                self.currentPath = matches[0]
            else:
                self.currentPath = ""

        else:
            tempPath = self.normalizePath(to)

            if self.isDir(tempPath):
                self.currentPath = tempPath
            else:
                print(f"No such directory: {to}")

    def cat(self, filePath):
        filePath = self.normalizePath(filePath)

        if (not self.isFile(filePath)):
            print(f"No such file: {filePath}")
        else:
            for line in self.directory.open(filePath).readlines():
                print(line.decode('utf-8'))

    def pwd(self):
        if (len(self.currentPath)):
            print(f"/{self.currentPath}")
        else:
            print(self.currentPath)

    def enterCommands(self):
        slash = ""
        if (len(self.currentPath)):
            slash = "/"
        return input(f"[root ~{slash}{self.currentPath}]# ").split()

    def checkSecondElem(self, arr, smth=""):
        if (len(arr) == 1):
            print(f"You forgot to enter a {smth}")
            return False
        else:
            return True

    def exec(self):
        commands = []
        while True:
            commands = self.enterCommands()

            if (commands[0] == "ls"):
                if (len(commands) == 1): 
                    self.ls()
                else: 
                    self.ls(commands[1])

            elif commands[0] == "cd":
                if (self.checkSecondElem(commands, "directory")):
                    self.cd(commands[1])
                else: 
                    continue

            elif commands[0] == "cat":
                if (self.checkSecondElem(commands, "file")):
                    self.cat(commands[1])
                else: 
                    continue

            elif commands[0] == "pwd":
                self.pwd()

            elif commands[0] == "exit":
                break

            else:
                print(f"Command: {commands[0]} not found")

# cli = CLI(sys.argv[1])
cli = CLI("dir1.zip")