
from board import Board
from notation_parser import NotationParser


class NotationParserTestSuite():
    @classmethod
    def getTests(cls):
        return [
            {"runnable": cls.parseABongcloud, "name": "Parse a bongcloud FEN position (1.e4 e5 2. Ke2 Ke7)"},
        ]

    @staticmethod
    def parseABongcloud():
        bongcloud = "rnbq1bnr/ppppkppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR w - - 2 3"
        position = NotationParser.parsePosition(bongcloud)
        assert(position.board == Board.fromFEN("rnbq1bnr/ppppkppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR"))
        return True