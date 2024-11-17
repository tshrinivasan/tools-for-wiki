#!/usr/bin/env python3
from io import TextIOWrapper
from sys import stderr, argv

class ColumnCombine:
    """
    combines two files horizontally with tilde
    file1.txt:
    1111
    2222
    3333

    file2.txt:
    4444
    5555

    $ python3 columncombine.py file1.txt file2.txt
    1111~4444
    2222~5555
    3333
    """
    def __init__(self, *args: str, **kwargs: str):
        """
        *args, **kwargs - filenames to combine
        """
        self.seperator: str = '~'
        self.files: list[TextIOWrapper] = []
        filenames: list[str] = []

        for filename in args:
            filenames.append(filename)

        for (_, filename) in kwargs.items():
            filenames.append(filename)

        for filename in filenames:
            try:
                file = open(filename)
                self.files.append(file)
            except:
                print('failed to open {}'.format(filename), file=stderr)

    def set_seperator(self, seperator: str):
        """
        seperator - seperator to use while joining lines
        """
        self.seperator = seperator

    def combine(self):
        """
        generator function returns one combined line per call
        """
        stop: bool = False

        while not stop:
            line: str = ''

            if len(self.files) <= 0:
                stop = True
                continue

            for file in self.files:
                try:
                    newline = file.readline()
                    # readline() returns empty string
                    # to indicate End Of File
                    if len(newline) <= 0:
                        raise EOFError('EOF reached')
                    
                    newline = newline.strip()
                    if len(newline) > 0:
                        if len(line) > 0:
                            line += self.seperator
                        line += newline

                except Exception as exception:
                    print('exception during processing {}: {}'.format(file.name, exception), file=stderr)
                    file.close()
                    self.files.remove(file)

            if len(line) > 0:
                yield line


def main():
    columncombine = ColumnCombine(*argv[1:])
    line: str = ''
    for line in columncombine.combine():
        print(line)

if __name__ == "__main__":
    main()
