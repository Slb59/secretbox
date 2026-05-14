from crispy_forms.layout import HTML, Div, Submit
from django.urls import reverse


def action_buttons(
    submit_label="Valider", back_url_name=None, back_label="Retour", back_css_class=None
):
    """
    Generate a crispy-forms Div with a Submit button and a link button.

    Args:
        submit_label (str): Label of the submit button.
        back_url_name (str): URL name to reverse for the back link.
        back_label (str): Label of the back link.
        back_css_class (str): Optional CSS class for the back link.

    Returns:
        Div: A crispy-forms layout Div.
    """
    back_url = reverse(back_url_name) if back_url_name else "#"
    back_classes = back_css_class or (
        "inline-block mt-4 focus:outline-none text-white bg-gray-500 hover:bg-gray-700 "
        "focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 "
        "dark:focus:ring-gray-900"
    )

    return Div(
        Submit("submit", submit_label, css_class="button-valider"),
        HTML(f'<a href="{back_url}" class="{back_classes}">{back_label}</a>'),
        css_class="flex space-x-4",
    )