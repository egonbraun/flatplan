========
Flatplan
========

.. image:: https://github.com/egonbraun/flatplan/workflows/CI/badge.svg

Flatplan is a command line tool that can be used to *flatten* the resources and
providers found in a terraform plan in JSON format. You can obtain it by first
export your plan file by running:

``$ terraform plan -out=planfile``

And then:

``$ terraform show -json planfile > plan.json``

Now, we can feed flatplan with the exported plan:

``$ flatplan --jsonplan=plan.json --output=flattened_plan.json --debug``

The problem we are trying to solve with this tool is that, when you export the plan
to JSON the resources might be in different locations which makes it hard for other
tools to find them. Therefor, flatplan will extract all resources and providers and
return a simpler JSON structure for you.

For example, the usual structure of a terraform plan that uses modules and perhaps
those modules use submodules would be something like this:

.. sourcecode::

    {
        ...
        "planned_values": {
            "root_module": {
                "resources": [
                    ... a lot of resources here ...
                ],
                "child_modules": [{
                    "resources": [
                        ... a lot of resources here ...
                    ],
                    "child_modules": [{
                        "resources": [
                            ... a lot of resources here ...
                        ],
                        "child_modules": [{
                            ... and so on ...
                        }]
                    }]
                }, {
                    "resources": [
                        ... a lot of resources here ...
                    ],
                    "child_modules": [{
                        "resources": [
                            ... a lot of resources here ...
                        ],
                        "child_modules": [{
                            ... and so on ...
                        }]
                    }]
                }]
            }
        },
        ...
        "configuration": {
            "provider_config": {
                "aws": {
                    "name": "aws",
                    "expressions": {
                        "region": {
                            "constant_value": "us-east-1"
                        }
                    }
                }
            }
        }
    }

As you can see this recursive nature of the plan can get quite ugly if you use
a lot of modules and submodules. When you run flatplan will then extract all
resources and providers and output something like this:

.. sourcecode::

    {
        "resources": [ ... all resources here ... ],
        "providers": [ ... all providers here ... ]
    }


This makes it easy for tools like Open Policy Agent that have no way to recursively
traverse a JSON file.

-------
Install
-------

If you use pip:

``$ pip install flatplan``

If you use pipx:

``$ pipx install flatplan``

-----
Usage
-----

Flatplan accepts the following command line parameters:

``--jsonplan="path"``: Reads JSON plan from the specified path, default: STDIN.

``--output="path"``: Writes flattened plan to the specified path, default: STDOUT.

``--debug``: Sets log level to debug, default: False.

Example:

``$ flatplan --jsonplan=plan.json --output=flattened.json --debug``

