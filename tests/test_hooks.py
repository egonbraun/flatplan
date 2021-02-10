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


class TestHooks(unittest.TestCase):
    def setUp(self) -> None:
        self.example_plan_path = join(dirname(abspath(__file__)), "assets/plan.json")
        self.example_state_path = join(dirname(abspath(__file__)), "assets/state.json")

    def test_remove_resource_from_plan_by_tag_hook(self) -> None:
        with open(self.example_plan_path, "r") as f:
            plan = f.read()

        flattener = flatplan.PlanFlattener(plan)
        flattened_plan = flattener.flatten()

        context = flatplan.HookContext(
            debug=False,
            path=self.example_plan_path,
            flat=flattened_plan,
            remove="remove=true",
            state=False,
        )

        hook = flatplan.RemoveResourceByTagHook(context)
        plan = hook.run()

        self.assertIsNotNone(plan)
        self.assertIn("providers", plan.keys())
        self.assertIn("resources", plan.keys())

        addresses = [r["address"] for r in plan["resources"]]

        self.assertNotIn("module.eks-example-01.data.aws_ami.eks_worker", addresses)
        self.assertNotIn(
            "module.eks-example-01.aws_security_group.cluster[0]", addresses
        )

    def test_remove_resource_from_state_by_tag_hook(self) -> None:
        with open(self.example_state_path, "r") as f:
            plan = f.read()

        flattener = flatplan.StateFlattener(plan)
        flattened_plan = flattener.flatten()

        context = flatplan.HookContext(
            debug=False,
            path=self.example_plan_path,
            flat=flattened_plan,
            remove="remove=true",
            state=True,
        )

        hook = flatplan.RemoveResourceByTagHook(context)
        plan = hook.run()

        self.assertIsNotNone(plan)
        self.assertIn("resources", plan.keys())

        addresses = [r["address"] for r in plan["resources"]]

        self.assertNotIn("aws_kms_key.kms01", addresses)
