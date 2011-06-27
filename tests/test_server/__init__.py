#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
import os
import locale
locale.setlocale(locale.LC_ALL, os.environ["LANG"])

import const

#    Set up translations
import gettext
gettext.bindtextdomain(const.AppTitle, const.LocaleDir)
gettext.textdomain(const.AppTitle)
_ = gettext.gettext
gettext.install(const.AppTitle)

from test_server import *
from test_verify import *


if __name__ == "__main__":
    unittest.main()
