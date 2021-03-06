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

import unittest
from datetime import datetime

from lsst.daf.butler.core.datasets import DatasetType, DatasetRef
from lsst.daf.butler.core.quantum import Quantum
from lsst.daf.butler.core.storageClass import StorageClass

"""Tests for Quantum.
"""


class QuantumTestCase(unittest.TestCase):
    """Test for Quantum.
    """

    def testConstructor(self):
        """Test of constructor.
        """
        # Quantum specific arguments
        run = None  # TODO add Run
        task = "some.task.object"  # TODO Add a `SuperTask`?
        # Base class arguments
        startTime = datetime(2018, 1, 1)
        endTime = datetime(2018, 1, 2)
        host = "localhost"
        quantum = Quantum(task, run, startTime, endTime, host)
        self.assertEqual(quantum.task, task)
        self.assertEqual(quantum.run, run)
        self.assertEqual(quantum.predictedInputs, dict())
        self.assertEqual(quantum.actualInputs, dict())
        self.assertIsNone(quantum.id)
        self.assertEqual(quantum.startTime, startTime)
        self.assertEqual(quantum.endTime, endTime)
        self.assertEqual(quantum.host, host)

    def testAddInputsOutputs(self):
        """Test of addPredictedInput() method.
        """
        quantum = Quantum(task="some.task.object", run=None)

        # start with empty
        self.assertEqual(quantum.predictedInputs, dict())

        instrument = "DummyCam"
        datasetTypeName = "test_ds"
        storageClass = StorageClass("testref_StructuredData")
        datasetType = DatasetType(datasetTypeName, ("instrument", "visit"), storageClass)

        # add one ref
        ref = DatasetRef(datasetType, dict(instrument=instrument, visit=42))
        quantum.addPredictedInput(ref)
        self.assertIn(datasetTypeName, quantum.predictedInputs)
        self.assertEqual(len(quantum.predictedInputs[datasetTypeName]), 1)
        # add second ref
        ref = DatasetRef(datasetType, dict(instrument=instrument, visit=43))
        quantum.addPredictedInput(ref)
        self.assertEqual(len(quantum.predictedInputs[datasetTypeName]), 2)

        # mark last ref as actually used
        self.assertEqual(quantum.actualInputs, dict())
        quantum._markInputUsed(ref)
        self.assertIn(datasetTypeName, quantum.actualInputs)
        self.assertEqual(len(quantum.actualInputs[datasetTypeName]), 1)

        # add couple of outputs too
        self.assertEqual(quantum.outputs, dict())
        ref = DatasetRef(datasetType, dict(instrument=instrument, visit=42))
        quantum.addOutput(ref)
        self.assertIn(datasetTypeName, quantum.outputs)
        self.assertEqual(len(quantum.outputs[datasetTypeName]), 1)

        ref = DatasetRef(datasetType, dict(instrument=instrument, visit=43))
        quantum.addOutput(ref)
        self.assertEqual(len(quantum.outputs[datasetTypeName]), 2)


if __name__ == "__main__":
    unittest.main()
