from string import Template

header: str = """
#!/usr/bin/env python
import pytest
from aws_cdk.core import App, Environment # CDKv1
from aws_cdk import App, Environment # CDKv2
from aws_cdk.assertions import Match, Template

"""

class_template = Template(
    """
class Test$class_name:
    @pytest.fixture
    def stack_environment(self):
        return Environment(
            account=...,
            region=...,
        )

    @pytest.fixture
    def stack_config(self):
        return {}

    @pytest.fixture
    def stack_template(self, stack_config):
        return Template.from_stack(
            MyStack(
                App()
                "MyStack",
                stack_config,
            )
        )

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
