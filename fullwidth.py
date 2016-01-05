# !/usr/bin/env python
# Copyright (c) 2016 Porter Smith
#
# Some rights reserved.
#
# Redistribution and use in source and binary forms of the software as well
# as documentation, with or without modification, are permitted provided
# that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
#
# THIS SOFTWARE AND DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE AND DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

import sys

# I'm sorry.
try:
    import weechat
except ImportError:
    print("This is a WeeChat Script - http://www.weechat.org")
    print("It makes no sense to run it on its own.")
    sys.exit(1)


# Global / Static script values
SCRIPT_NAME = "fullwidth"
SCRIPT_AUTHOR = "Porter Smith <flowbish@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "BSD"
SCRIPT_DESCRIPTION = "Translates latin characters to their fullwidth equivalents."

FW_TABLE = dict()


def decode(s):
    """ Decode utf-8 to ascii """
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s


def encode(u):
    """ Encode ascii as utf-8 """
    if isinstance(u, unicode):
        u = u.encode('utf-8')
    return u


def fw_cb(data, bufferptr, args):
    # args is given to us as an ascii string, must decode it to utf-8.
    line_unicode = decode(args)
    # Simple character translation.
    line_fullwidth = line_unicode.translate(FW_TABLE)
    # Send transformed line to buffer as text, encoding it back into bytes.
    weechat.command(bufferptr, encode(line_fullwidth))
    return weechat.WEECHAT_RC_OK


def main():
    """ Entry point, initializes everything  """

    # Setup the translation table, mapping latin characters to their Unicode
    #  fullwidth equivalents.
    global FW_TABLE
    FW_TABLE = dict(zip(range(0x21, 0x7F),
                        range(0xFF01, 0xFF5F)))
    # Handle space specially.
    FW_TABLE[0x20] = 0x3000

    weechat.register(
        SCRIPT_NAME,
        SCRIPT_AUTHOR,
        SCRIPT_VERSION,
        SCRIPT_LICENSE,
        SCRIPT_DESCRIPTION,
        "", # Shutdown callback function
        "", # Charset (blank for utf-8)
    )

    # Command callbacks
    weechat.hook_command(  # command name
                           "fw",
                           # description
                           "Translates latin characters to their fullwidth equivalents.",
                           # arguments
                           "text",
                           # description of arguments
                           " text: text to be full-width'd",
                           # completions
                           "",
                           "fw_cb", "")


if __name__ == '__main__':
    main()
