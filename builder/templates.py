from string import Template

header: str = """
import pytest
from aws_cdk.assertions import Match, Template

"""

class_template = Template(
    """
class Test$class_name:
    @pytest.fixture(scope="class")
    def stack_config(self):
        return {}

    @pytest.fixture(scope="class")
    def stack_template(self, stack_app, stack_environment, stack_config):
        return Template.from_stack(
            MyStack(
                stack_app,
                "MyStack",
                stack_config,
                env=stack_environment,
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
