#!/usr/bin/env python3

from sys import argv
from sys import stderr
from pypdf import PdfReader
from pypdf import PdfWriter
from pypdf import PaperSize
from pypdf import PageObject
from pypdf.generic import RectangleObject
from pypdf.papersizes import Dimensions

class PdfCrop:
    source: PdfReader
    dest: PdfWriter


    def __init__(self, sourcefilepath: str, destfilepath: str):
        self.destfilepath = destfilepath
        self.source = PdfReader(sourcefilepath)
        self.dest = PdfWriter()


    def crop_page(self, page: PageObject, cropdelta: RectangleObject):
        page.cropbox.left += cropdelta.left
        page.cropbox.bottom += cropdelta.bottom
        page.cropbox.right += cropdelta.right
        page.cropbox.top += cropdelta.top
        page.mediabox = page.cropbox


    def scale_page(self, page: PageObject, papertype: Dimensions):
        page.scale_to(papertype.width, papertype.height)


    def filter_pages(self, spages: list[PageObject], pagenumsv: list[list[int]]) -> list[PageObject]:
        pages: list[PageObject] = []
        for pagenums in pagenumsv:
            if len(pagenums) <= 0:
                pages = spages
                break
            elif len(pagenums) == 1:
                pages.append(spages[pagenums[0]])
            elif len(pagenums) >= 2 and pagenums[1] <= 0:
                pages.extend(spages[pagenums[0]:len(spages)])
            else:
                pages.extend(spages[pagenums[0]:pagenums[1]])

        return pages


    def crop(self, pagenumsv: list[list[int]], crop: list[float]):
        if len(crop) >= 4:
            pages = self.filter_pages(self.source.pages, pagenumsv)
            cropdelta: RectangleObject = RectangleObject((crop[0], crop[1], crop[2], crop[3]))
            for page in pages:
                self.crop_page(page, cropdelta)


    def scale(self, pagenumsv: list[list[int]], papertype: Dimensions):
        pages = self.filter_pages(self.source.pages, pagenumsv)
        for page in pages:
            self.scale_page(page, papertype)


    def write_page(self, page: PageObject):
        self.dest.add_page(page)


    def write(self):
        for page in self.source.pages:
            self.write_page(page)
            self.dest.write(open(self.destfilepath, "wb"))


def get_crop(cropstr: str) -> list[float]:
    cropstrv: list[str] = argv[4].split(",")
    crop: list[float] = []

    for cropstr in cropstrv:
        try:
            crop.append(float(cropstr))
        except:
            pass

    return crop


def get_pagenums(pagenums_str: str) -> list[list[int]]:
    pagenums_strv: list[str] = pagenums_str.split(",")
    pagenumsv: list[list[int]] = []

    for pagenumsstr in pagenums_strv:
        pagenumstrv: list[str] = pagenumsstr.split(":")
        pagenumv: list[int] = []

        for pagenumstr in pagenumstrv:
            try:
                pagenum: int = int(pagenumstr)
                pagenumv.append(pagenum)
            except:
                pass

        pagenumsv.append(pagenumv)

    return pagenumsv


def get_papersize(papersize_str: str) -> Dimensions:
    papersize: Dimensions = PaperSize.A4

    if "," in papersize_str:
        papersize_strv: list[str] = papersize_str.split(",")
        width: int = 0
        height: int = 0

        try:
            width = int(papersize_strv[0])
            if len(papersize_strv) > 1:
                height = int(papersize_strv[1])
        except:
            pass

        if width <= 0 or height <= 0:
            stderr.write("unknown papersize " + papersize_str + " defaulting to A4")
            papersize = PaperSize.A4
            return papersize

        papersize = Dimensions(width, height)
        return papersize

    match papersize_str:
        case "A0":
            papersize = PaperSize.A0
        case "A1":
            papersize = PaperSize.A1
        case "A2":
            papersize = PaperSize.A2
        case "A3":
            papersize = PaperSize.A3
        case "A4":
            papersize = PaperSize.A4
        case "A5":
            papersize = PaperSize.A5
        case "A6":
            papersize = PaperSize.A6
        case "A7":
            papersize = PaperSize.A7
        case "A8":
            papersize = PaperSize.A8
        case "C4":
            papersize = PaperSize.C4
        case _:
            stderr.write("unknown papersize " + papersize_str + " defaulting to A4")
            papersize = PaperSize.A4

    return papersize


def main():
    if len(argv) < 6:
        stderr.write("[usage]\n\t" + argv[0])
        stderr.write(" inputfile.pdf ")
        stderr.write("outputfile.pdf ")
        stderr.write("startpageidx[:endpageidx][,...] ")
        stderr.write("left-delta,bottom-delta,right-delta,top-delta ")
        stderr.write("papersize\n")
        stderr.write("\n")
        stderr.write("[example]\n\t$ " + argv[0] + " test.pdf test.out.pdf '' '+150, +130, -150, -105' A4\n")
        stderr.write("\tthis commandline will crop all pages of test.pdf by ")
        stderr.write("moving the left margin +150pts towards right margin, ")
        stderr.write("moving bottom margin +130pts towards top margin, ")
        stderr.write("moving right margin -150pts towards left margin, ")
        stderr.write("moving top margin -105pts towards bottom margin ")
        stderr.write("then scale the output to A4 papersize and save the result pdf as test.out.pdf\n")
        stderr.write("\n")
        stderr.write("[example]\n\t$ " + argv[0] + " test.pdf test.out.pdf '0, 1, 7:8' '+150,+130,-150,-105' A3\n")
        stderr.write("\tthis commandline will crop only pages with ")
        stderr.write("page-index 0(1st page), page-index 1(2nd page) and page-index 7(8th page) of test.pdf by ")
        stderr.write("moving the left margin +150pts towards right margin, ")
        stderr.write("moving bottom margin +130pts towards top margin, ")
        stderr.write("moving right margin -150pts towards left margin, ")
        stderr.write("moving top margin -105pts towards bottom margin ")
        stderr.write("then scale the output to A3 papersize and save the result pdf as test.out.pdf\n")
        exit(1)

    pagenumsv: list[list[int]] = get_pagenums(argv[3])
    pc: PdfCrop = PdfCrop(argv[1], argv[2])
    pc.crop(pagenumsv, get_crop(argv[4]))
    pc.scale(pagenumsv, get_papersize(argv[5]))
    pc.write()


if __name__ == "__main__":
    main()
