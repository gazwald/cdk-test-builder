from string import Template

header: str = """
#!/usr/bin/env python
import pytest
from aws_cdk.assertions import Match, Template

"""

class_template = Template(
    """
class Test$class_name:
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
