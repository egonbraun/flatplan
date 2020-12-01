Flatplan
========

Flatplan is a command line tool that can be used to *flatten* the resources and
providers found in a terraform plan in JSON format. You can obtain it by first
export your plan file by running:

``$ terraform plan -out=planfile``

And then:

``$ terraform show -json planfile > plan.json``

Now, we can feed flatplan with the exported plan:

``$ flatplan --jsonplan=plan.json --output=flattened_plan.json --debug``

Install
-------

If you use pip:

``$ pip install flatplan``

If you use pipx:

``$ pipx install flatplan``

Usage
-----

Flatplan accepts the following command line parameters:

``--jsonplan="path"``: Reads JSON plan from the specified path, default: STDIN.

``--output="path"``: Writes flattened plan to the specified path, default: STDOUT.

``--debug``: Sets log level to debug, default: False.

Example:

``$ flatplan --jsonplan=~/plan.json --output=~/flattened.json --debug``

