from verifier.save_file import SaveFile

class FileParserTestSuite():
    @classmethod
    def getTests(cls):
        return [
            {"runnable": cls.canInit, "name": "Can initialize a FileParser"},
            {"runnable": cls.initWithFS, "name": "Can initialize with a string"},
            {"runnable": cls.emptyParse, "name": "Can create a game from empty file"},
        ]
    
    @staticmethod
    def canInit():
        _ = SaveFile()
        return True
    
    @staticmethod
    def initWithFS():
        _ = SaveFile(path="tests/file_parser/init.txt")
        return True
    
    @staticmethod
    def emptyParse():
        empty = SaveFile(path="tests/file_parser/emptyParse.txt")
        empty.parse()
        return True