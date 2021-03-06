# -*- coding: utf-8 -*-
#
# Copyright 2004-2006 Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Convert plain text (.txt) files to Gettext PO localization files.

See: http://docs.translatehouse.org/projects/translate-toolkit/en/latest/commands/txt2po.html
for examples and usage instructions.
"""

from translate.storage import po, txt


class txt2po(object):

    def __init__(self, duplicatestyle="msgctxt"):
        self.duplicatestyle = duplicatestyle

    def convertstore(self, thetxtfile):
        """converts a file to .po format"""
        thetargetfile = po.pofile()
        targetheader = thetargetfile.header()
        targetheader.addnote("extracted from %s" % thetxtfile.filename,
                             "developer")

        for txtunit in thetxtfile.units:
            newunit = thetargetfile.addsourceunit(txtunit.source)
            newunit.addlocations(txtunit.getlocations())
        thetargetfile.removeduplicates(self.duplicatestyle)
        return thetargetfile


def converttxt(inputfile, outputfile, templates, duplicatestyle="msgctxt",
               encoding="utf-8", flavour=None):
    """reads in stdin using fromfileclass, converts using convertorclass,
    writes to stdout
    """
    inputstore = txt.TxtFile(inputfile, encoding=encoding, flavour=flavour)
    convertor = txt2po(duplicatestyle=duplicatestyle)
    outputstore = convertor.convertstore(inputstore)
    if outputstore.isempty():
        return 0
    outputstore.serialize(outputfile)
    return 1


def main(argv=None):
    from translate.convert import convert
    formats = {"txt": ("po", converttxt), "*": ("po", converttxt)}
    parser = convert.ConvertOptionParser(formats, usepots=True,
                                         description=__doc__)
    parser.add_option("", "--encoding", dest="encoding", default='utf-8',
                      type="string",
                      help="The encoding of the input file (default: UTF-8)")
    parser.passthrough.append("encoding")
    parser.add_option("", "--flavour", dest="flavour", default="plain",
                      type="choice",
                      choices=["plain", "dokuwiki", "mediawiki"],
                      help="The flavour of text file: plain (default), dokuwiki, mediawiki",
                      metavar="FLAVOUR")
    parser.passthrough.append("flavour")
    parser.add_duplicates_option()
    parser.run(argv)
