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
import unittest
from os.path import abspath, dirname, join


class TestFlatplan(unittest.TestCase):
    def setUp(self) -> None:
        self.example_plan_path = join(dirname(abspath(__file__)), "assets/plan.json")
        self.example_state_path = join(dirname(abspath(__file__)), "assets/state.json")

    def test_plan_flattener(self) -> None:
        with open(self.example_plan_path, "r") as f:
            plan = f.read()

        flattener = flatplan.PlanFlattener(plan)
        flattened_plan = flattener.flatten()

        self.assertIsNotNone(flattened_plan)
        self.assertIn("providers", flattened_plan.keys())
        self.assertIn("resources", flattened_plan.keys())

        resources = flattened_plan["resources"]

        self.assertEqual(len(resources), 38)
        self.assertEqual(len([r for r in resources if r["mode"] == "managed"]), 29)
        self.assertEqual(len([r for r in resources if r["mode"] == "data"]), 9)

        providers = flattened_plan["providers"]

        self.assertEqual(len(providers), 1)

    def test_state_flattener(self) -> None:
        with open(self.example_state_path, "r") as f:
            plan = f.read()

        flattener = flatplan.StateFlattener(plan)
        flattened_plan = flattener.flatten()

        self.assertIsNotNone(flattened_plan)
        self.assertIn("resources", flattened_plan.keys())

        resources = flattened_plan["resources"]

        self.assertEqual(len(resources), 6)
        self.assertEqual(len([r for r in resources if r["mode"] == "managed"]), 5)
        self.assertEqual(len([r for r in resources if r["mode"] == "data"]), 1)
