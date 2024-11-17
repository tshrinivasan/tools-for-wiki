#!/usr/bin/env python3
from io import TextIOWrapper
from sys import argv

class PreviousPagenoGenerator:
    """
    generate previous page number and join it in the previous line
    input:
    chapterno~title~startpage~endpage
    1~something1~1
    2~something2~10
    3~something3~15

    output:
    chapterno~title~startpage~endpage
    1~something1~1~9
    2~something2~10~14
    3~something3~15
    """
    def __init__(self, file: TextIOWrapper):
        "file: opened File object to process"
        self.seperator: str = '~'
        self.file: TextIOWrapper = file

    def set_seperator(self, seperator: str):
        """
        seperator - seperator to use while joining lines
        """
        self.seperator = seperator

    def get_pageno(self, line: str):
        cols = line.split(self.seperator)
        return int(cols[len(cols) - 1])

    def generate_previous_pageno(self):
        pline = ""
        while True:
            nline = self.file.readline()
            if len(nline) <= 0:
                if len(pline) > 0:
                    print(pline)
                break

            nline = nline.strip()
            if len(pline) <= 0:
                pline = nline
                continue

            ppageno = self.get_pageno(nline)
            ppageno = (ppageno - 1) if ppageno > 0 else 0
            if ppageno > 0:
                pline = pline + self.seperator + str(ppageno)

            print(pline)
            pline = nline

def main():
    filename = "/proc/self/fd/0"
    if len(argv) > 1 and len(argv[1]) > 0:
        filename = argv[1]

    file = open(filename)
    gpp = PreviousPagenoGenerator(file)
    gpp.generate_previous_pageno()

if __name__ == "__main__":
    main()
