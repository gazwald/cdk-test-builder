import json
import subprocess

import yaml
from finder import \
    Finder  # pip install git+https://github.com/gazwald/finder.git

from builder.templates import class_template, function_template, header

resource_exclusions: list[str] = ["AWS::CDK::Metadata"]
method_references: dict[str, str] = {"MATCH_ANY_VALUE": "Match.any_value()"}


def process_template(template, output_filename: str):
    resources = template.get("Resources", None)
    app_name: str
    class_name: str

    if "CDKMetadata" in resources:
        metadata = resources["CDKMetadata"]["Metadata"]
        app_name = metadata["aws:cdk:path"].split("/")[0]
        class_name = app_name.title().replace("-", "")
    else:
        class_name = "TestMyStack"

    with open(output_filename, "w") as handle:
        handle.write(header)

        class_definition = class_template.substitute(class_name=class_name)
        handle.write(class_definition)

        find = Finder(resources.keys())
        for resource_name, resource_details in resources.items():
            resource_type = resource_details["Type"]
            if resource_type not in resource_exclusions:
                resource_properties = resource_details["Properties"]

                resource_properties = find.replace(
                    resource_properties,
                    "MATCH_ANY_VALUE",
                )

                function_definition = function_template.substitute(
                    function_name=resource_name,
                    resource_type=resource_type,
                    resource_properties=resource_properties,
                )

                handle.write(function_definition)


def cleanup_references(output_filename: str):
    for key, value in method_references.items():
        subprocess.run(
            ["sed", "-i", f"s/'{key}'/{value}/g", output_filename], check=True
        )


def builder(input_template: str, output_filename: str = "test.py"):
    with open(input_template) as handle:
        if input_template.endswith("json"):
            template = json.load(handle)
        elif input_template.endswith("yaml"):
            template = yaml.safe_load(handle)
        elif input_template.endswith("yml"):
            template = yaml.safe_load(handle)
        else:
            template = None

    if template:
        process_template(template, output_filename)
        cleanup_references(output_filename)
