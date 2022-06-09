#!/usr/bin/env python
import json
from string import Template

import yaml
# https://github.com/gazwald/finder.git
from finder import Finder

header: str = """
#!/usr/bin/env python
import pytest
from aws_cdk.assertions import Match, Template

"""

class_template = Template(
    """
class test_$class_name:
    def __init__(self):
        pass

"""
)

function_template = Template(
    """
    def test_$function_name(self, stack_template):
        stack_template.has_resource_properties(
            "$resource_type",
            $resource_properties
        )

"""
)


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


def main(filename: str):
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


if __name__ == "__main__":
    main("template.json")
