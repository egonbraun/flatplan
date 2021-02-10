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
from json import loads
from os import remove
from os.path import abspath, dirname, join
from tempfile import gettempdir


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.example_plan_path = join(dirname(abspath(__file__)), "assets/plan.json")
        self.example_state_path = join(dirname(abspath(__file__)), "assets/state.json")
        self.output_plan_path = join(gettempdir(), "output_plan.json")
        self.output_state_path = join(gettempdir(), "output_state.json")

    def test_run_with_plan(self) -> None:
        flatplan.run(
            debug=True,
            output=self.output_plan_path,
            path=self.example_plan_path,
            remove="remove=true",
            state=False,
        )

        with open(self.output_plan_path) as f:
            flattened_plan = loads(f.read())

        remove(self.output_plan_path)

        self.assertIsNotNone(flattened_plan)
        self.assertIn("providers", flattened_plan.keys())
        self.assertIn("resources", flattened_plan.keys())

        self.assertEqual(len(flattened_plan["resources"]), 36)
        self.assertEqual(len(flattened_plan["providers"]), 1)

        addresses = [r["address"] for r in flattened_plan["resources"]]

        self.assertNotIn("module.eks-example-01.data.aws_ami.eks_worker", addresses)
        self.assertNotIn(
            "module.eks-example-01.aws_security_group.cluster[0]", addresses
        )

    def test_run_with_state(self) -> None:
        flatplan.run(
            debug=True,
            output=self.output_state_path,
            path=self.example_state_path,
            remove="remove=true",
            state=True,
        )

        with open(self.output_state_path) as f:
            flattened_plan = loads(f.read())

        remove(self.output_state_path)

        self.assertIsNotNone(flattened_plan)
        self.assertIn("resources", flattened_plan.keys())

        self.assertEqual(len(flattened_plan["resources"]), 5)

        addresses = [r["address"] for r in flattened_plan["resources"]]

        self.assertNotIn("aws_kms_key.kms01", addresses)
