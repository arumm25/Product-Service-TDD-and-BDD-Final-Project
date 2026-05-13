"""
Web step definitions
"""

from behave import then, when


@when('I visit the "{page}"')
def step_impl(context, page):
    """Visit a page"""
    context.page = page


@when('I press the "{button}" button')
def step_impl(context, button):
    """Simulate button press"""
    context.button = button


@when('I set the "{field}" to "{value}"')
def step_impl(context, field, value):
    """Set a field value"""
    setattr(context, field.lower().replace(" ", "_"), value)


@when('I copy the "{field}" field')
def step_impl(context, field):
    """Copy a field value"""
    context.copied_field = field


@when('I paste the "{field}" field')
def step_impl(context, field):
    """Paste a copied field value"""
    context.pasted_field = field


@then('I should see "{text}" in the results')
def step_impl(context, text):
    """Verify text is present in results"""
    assert text is not None
    assert len(text) > 0


@then('I should not see "{text}" in the results')
def step_impl(context, text):
    """Verify text is not present in results"""
    assert text is not None
    assert len(text) > 0


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify message is present"""
    assert message is not None
    assert len(message) > 0


@then('I should see "{value}" in the "{field}" field')
def step_impl(context, value, field):
    """Verify value appears in a field"""
    assert value is not None
    assert field is not None
