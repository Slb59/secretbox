from crispy_forms.layout import HTML, Div, Submit
from django.urls import reverse_lazy


def action_buttons(
    submit_label="Valider", back_url_name=None, back_label="Retour", back_css_class=None
):
    """
    Generate a crispy-forms Div with a Submit button and a link button.

    Args:
        submit_label (str): Label of the submit button.
        back_url_name (str): URL name to reverse for the back link.
        back_label (str): Label of the back link.

    Returns:
        Div: A crispy-forms layout Div.
    """
    back_url = reverse_lazy(back_url_name) if back_url_name else "#"
    back_classes = (
        "block w-full focus:outline-none text-black bg-gray-500 hover:bg-gray-800 "
        "focus:ring-4 focus:ring-gray-300 font-medium rounded-lg "
        "text-sm px-5 py-2.5 mb-2 "
        "dark:focus:ring-gray-900"
    )
    submit_classe = (
        "block w-full rounded-xl bg-rose-500 hover:bg-rose-800 focus:outline-none "
        "focus:ring-4 focus:ring-rose-300 font-medium rounded-lg "
        "text-sm px-5 py-2.5 mb-2 "
        "dark:focus:ring-rose-900"
    )

    return Div(
        Submit("submit", submit_label, css_class=submit_classe),
        HTML(f'<a href="{back_url}" class="{back_classes}">{back_label}</a>'),
        css_class="flex gap-4",
    )
