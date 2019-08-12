import logging
import logging.config
import os
import subprocess
from importlib import import_module

import coloredlogs

import shell_util

FMT = "[%(asctime)s %(filename)s:%(lineno)d %(levelname)s] %(message)s"


class Base(object):
    def __init__(self, lazy_import=[], renames=None):
        self._modules_cache = {}
        self._lazy_import = lazy_import
        self._renames = renames or {}

        self._logger = logging.getLogger(type(self).__name__)
        coloredlogs.install(level="INFO", fmt=FMT)

        self._debugging = False
        if os.environ.get("DEBUG", None):
            self._debugging = True
            coloredlogs.install(level="DEBUG", fmt=FMT)
            self._logger.setLevel(logging.DEBUG)

    def _module(self, m_name):
        if m_name not in self._modules_cache:
            m_name = self._renames.get(m_name, m_name)
            self._logger.debug("Loading:: %s", m_name)

            assert m_name in self._lazy_import, "Import not declared:: `%s`" % m_name

            m = import_module(m_name)
            self._modules_cache[m_name] = m

        return self._modules_cache[m_name]

    def _all_modules(self):
        for m_name in self._lazy_import:
            self._module(m_name)

        return self._modules_cache

    def _debug_mode(self):
        return self._debugging

    def shell(self, cmd, timeout=None, **kwargs):
        self._logger.debug(cmd)
        return shell_util.shell(cmd, timeout=timeout, **kwargs)
