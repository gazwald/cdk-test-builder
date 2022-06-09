import json

import yaml
from finder import \
    Finder  # pip install git+https://github.com/gazwald/finder.git

from builder.templates import class_template, function_template, header

resource_exclusions: list[str] = ["AWS::CDK::Metadata"]


def process_template(template, output_filename: str = "test.py"):
    resources = template.get("Resources", None)
    metadata = resources["CDKMetadata"]["Metadata"]

    with open(output_filename, "w") as handle:
        handle.write(header)

        class_name = metadata["aws:cdk:path"].split("/")[0].replace("-", "_")
        class_definition = class_template.substitute(class_name=class_name)
        handle.write(class_definition)

        find = Finder(resources.keys())
        for resource_name, resource_details in resources.items():
            resource_type = resource_details["Type"]
            if resource_type not in resource_exclusions:
                resource_properties = resource_details["Properties"]

                resource_properties = find.replace(
                    resource_properties,
                    "Match.any_value()",
                )

                function_definition = function_template.substitute(
                    function_name=resource_name,
                    resource_type=resource_type,
                    resource_properties=resource_properties,
                )

                handle.write(function_definition)


def builder(filename: str):
    with open(filename) as handle:
        if filename.endswith("json"):
            template = json.load(handle)
        elif filename.endswith("yaml"):
            template = yaml.safe_load(handle)
        elif filename.endswith("yml"):
            template = yaml.safe_load(handle)
        else:
            template = None

    if template:
        process_template(template)
