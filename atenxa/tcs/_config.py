# -*- coding: utf-8 -*-
""" ATENXA.TCS Configuration """

from pathlib import Path
from configparser import ConfigParser

import vrmapi

SYSTEM = vrmapi.SYSTEM()

cfgfile_package = Path(__file__).parent / "tcsconfig.ini"
cfgfile_user = Path(SYSTEM.GetLayoutDir()) / "tcsconfig.ini"

encoding = "utf-8"

tcsconfig_defaults = {
    'POST_INIT_TIME': 0.3,  #: init後処理を行う時刻（秒）
}

tcsconfig = ConfigParser(defaults=tcsconfig_defaults)
tcsconfig.read([cfgfile_package, cfgfile_user], encoding=encoding)

vrmapi.LOG(str(tcsconfig))
