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

        with open(self.example_plan_path, "r") as f:
            plan = f.read()
            self.flattened_plan = flatplan.Flattener(plan).flatten()

    def test_remove_resource_by_tag_hook(self) -> None:
        context = flatplan.HookContext(
            debug=False,
            path=self.example_plan_path,
            plan=self.flattened_plan,
            remove="remove=true",
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
