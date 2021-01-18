# This file is part of Flatplan.
#
# Flatplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flatplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flatplan.  If not, see <https://www.gnu.org/licenses/>.

import flatplan.logging
import logging
import unittest


class TestLogging(unittest.TestCase):
    def test_setup_logger(self) -> None:
        logger = flatplan.logging.setup_logger("flatplan_test")

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.level, logging.INFO)

    def test_setup_logger_debug(self) -> None:
        logger = flatplan.logging.setup_logger("flatplan_test", True)

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.level, logging.DEBUG)
