========
Flatplan
========

.. image:: https://github.com/egonbraun/flatplan/workflows/CI/badge.svg

Flatplan is a command line tool that can be used to *flatten* the resources and providers found inside a terraform plan.
You can obtain a JSON version of the plan by running:

.. sourcecode::

    $ terraform plan -out=planfile
    $ terraform show -json planfile > plan.json

Now, we can feed our exported JSON plan to flatplan:

.. sourcecode::

    $ flatplan --jsonplan=plan.json --output=flattened_plan.json --debug

The problem we are trying to solve with flatplan is that, when you export the plan to JSON the resources might be in
different locations which makes it hard for other tools to find them. Therefore, flatplan will extract all resources and
providers for you and return a much simpler JSON structure.

For example, let's say we have a complex terraform project that uses many modules and submodules. When we create the
plan file for this project and then export it to JSON we might end up with something like this:

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

As you can see this recursive nature of the plan can get quite ugly if you use a lot of modules and submodules. After,
flatplan process this file we will get:

.. sourcecode::

    {
        "resources": [ ... all resources here ... ],
        "providers": [ ... all providers here ... ]
    }


This makes it easy for tools like Open Policy Agent to process our file since it has no way to recursively traverse a
raw terraform plan.

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

