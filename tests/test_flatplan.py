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

import flatplan
import json
import unittest
from os.path import abspath, dirname, join


class TestFlatplan(unittest.TestCase):
    def setUp(self) -> None:
        example_plan_path = join(dirname(abspath(__file__)), "assets/plan.json")

        with open(example_plan_path, "r") as plan:
            json_plan = plan.read()
            self.flattener = flatplan.Flattener(json_plan)

    def test_plan_flattener(self) -> None:
        json_output = self.flattener.flatten()

        self.assertIsNotNone(json_output)
        self.assertIsNot(json_output, "")

        dict_output = json.loads(json_output)

        self.assertIn("providers", dict_output.keys())
        self.assertIn("resources", dict_output.keys())

        resources = dict_output["resources"]

        self.assertEqual(len(resources), 38)
        self.assertEqual(len([r for r in resources if r["mode"] == "managed"]), 29)
        self.assertEqual(len([r for r in resources if r["mode"] == "data"]), 9)

        providers = dict_output["providers"]

        self.assertEqual(len(providers), 1)
