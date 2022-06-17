import json
import subprocess
from pathlib import Path

import yaml

from builder.templates import class_template, function_template, header
from finder.finder import Finder

resource_exclusions: list[str] = ["AWS::CDK::Metadata"]
method_references: dict[str, str] = {"MATCH_ANY_VALUE": "Match.any_value()"}


def load_template(input_template: str):
    template = None
    if not Path(input_template).exists():
        return template

    with open(input_template) as handle:
        if input_template.endswith("json"):
            template = json.load(handle)
        elif input_template.endswith("yaml") or input_template.endswith("yml"):
            template = yaml.safe_load(handle)

    return template


def generate_output_filename(input_filename: str) -> str:
    """
    Generate a filename based on the input template name, for example:
    input: template.json
    output: test_template.py

    If 'test_template.py' already exists:
    output: test_template_1.py
    """
    output_filename: str = Path(input_filename).stem.replace("-", "_").replace(".", "_")
    if not output_filename.startswith("test_"):
        output_filename = "test_" + output_filename

    if Path(output_filename + ".py").exists():
        # Could generate test_template_1_1_1_1_1.py
        generate_output_filename(output_filename + "_1")

    output_filename = output_filename + ".py"

    return output_filename


def process_template(template, input_filename: str, output_filename: str):
    resources = template.get("Resources", None)
    app_name: str
    class_name: str

    if not resources:
        print(f"No resources found in {input_filename} - skipping")
        return

    if "CDKMetadata" in resources:
        metadata = resources["CDKMetadata"]["Metadata"]
        app_name = metadata["aws:cdk:path"].split("/")[0]
        class_name = app_name.title().replace("-", "")
    else:
        class_name = "TestMyStack"
        print(
            f"No CDKMetadata found in {input_filename} - using default classname {class_name}"
        )

    with open(output_filename, "w") as handle:
        handle.write(header)

        class_definition = class_template.substitute(class_name=class_name)
        handle.write(class_definition)

        find = Finder(resources.keys())
        for resource_name, resource_details in resources.items():
            resource_type = resource_details["Type"]
            if resource_type not in resource_exclusions:
                resource_properties = resource_details.get("Properties", None)
                if resource_properties:
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


def post_processing(output_filename: str):
    for key, value in method_references.items():
        subprocess.run(
            ["sed", "-i", f"s/'{key}'/{value}/g", output_filename], check=True
        )


def builder(input_templates: list[str]):
    for input_template in input_templates:
        template = load_template(input_template)

        if template:
            output_filename: str = generate_output_filename(input_template)
            process_template(template, input_template, output_filename)
            if Path(output_filename).exists():
                post_processing(output_filename)
