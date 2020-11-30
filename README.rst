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

