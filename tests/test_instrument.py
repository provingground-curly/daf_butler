# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest

from lsst.daf.butler.core import Registry
from lsst.daf.butler.core.butlerConfig import ButlerConfig

from lsst.daf.butler.instrument import Instrument

"""Tests for Instrument.
"""


class DummyCam(Instrument):

    @classmethod
    def getName(cls):
        return "DummyCam"

    def register(self, registry):
        """Insert Instrument, PhysicalFilter, and Detector entries into a
        `Registry`.
        """
        dataId = {"instrument": self.getName()}
        registry.addDimensionEntry("Instrument", dataId)
        for f in ("dummy_g", "dummy_u"):
            registry.addDimensionEntry("PhysicalFilter", dataId, physical_filter=f)
        for d in (1, 2):
            registry.addDimensionEntry("Detector", dataId, detector=d)

    def getRawFormatter(self, dataId):
        """Return the Formatter class that should be used to read a particular
        raw file.

        Parameters
        ----------
        dataId : `DataId`
            Dimension-link identifier for the raw file or files being ingested.

        Returns
        -------
        formatter : `Formatter`
            Object that reads the file into an `lsst.afw.image.Exposure`
            instance.
        """
        return None


class InstrumentTestCase(unittest.TestCase):
    """Test for Instrument.
    """

    def setUp(self):
        self.testDir = os.path.dirname(__file__)
        self.configFile = os.path.join(self.testDir, "config/basic/butler.yaml")

    def testRegister(self):
        registry = Registry.fromConfig(ButlerConfig(self.configFile))
        dummyCam = DummyCam()
        dummyCam.register(registry)


if __name__ == "__main__":
    unittest.main()
