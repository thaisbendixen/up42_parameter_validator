from pathlib import Path
from dataclasses import dataclass
from typing import Dict
import inspect
from fastapi.testclient import TestClient
import json

import streamlit as st
from main import app

LOCATION = Path(__file__).resolve().parent

# to run this app $ streamlit run app.py

client = TestClient(app)
st.set_page_config(layout="wide")

try:
    import pyperclip
except ImportError:
    pyperclip = None

PIXELS_PER_LINE = 27
INDENT = 8


@st.cache(allow_output_mutation=True)
def state_singleton() -> Dict:
    return {}


STATE = state_singleton()


@dataclass
class JsonInputState:
    value: dict
    default_value: dict
    redraw_counter = 0


class CopyPasteError(Exception):
    pass


def dict_input(label, value, key=None):
    """Display a dictionary or dictionary input widget.
    This implementation is composed of a number of streamlit widgets. It might
    be considered a prototype for a native streamlit widget (perhaps built off
    the existing interactive dictionary widget).
    Json text may be copied in and out of the widget.
    Parameters
    ----------
    label : str
        A short label explaining to the user what this input is for.
    value : dict or func
        The dictionary of values to edit or a function (with only named parameters).
    key : str
        An optional string to use as the unique key for the widget.
        If this is omitted, a key will be generated for the widget
        based on its content. Multiple widgets of the same type may
        not share the same key.
    Returns
    -------
    dict
        The current value of the input widget.
    Example
    -------
    >>> d = st.json_input('parameters', {'a': 1, 'b': 2.0, 'c': 'abc', 'd': {a: 2}})
    >>> st.write('The current parameters are', d)
    """
    try:
        param = inspect.signature(value).parameters
        value = {}
        for p in param.values():
            value[p.name] = p.default
    except TypeError:
        pass  # Assume value is a dict

    # check json can handle input
    value = json.loads(json.dumps(value))

    # Create state on first run
    state_key = f"json_input-{key if key else label}"
    if state_key not in STATE:
        STATE[state_key] = JsonInputState(value, value)
    state: JsonInputState = STATE[state_key]

    # containers
    text_con = st.empty()
    warning_con = st.empty()

    def json_input_text(msg=""):

        if msg:
            state.redraw_counter += 1
            state.default_value = state.value

        # Display warning
        if msg:
            warning_con.warning(msg)
        else:
            warning_con.empty()

        # Read value
        value_s = json.dumps(
            state.default_value, indent=INDENT, sort_keys=True
        )
        input_s = text_con.text_area(
            label,
            value_s,
            height=len(value_s.splitlines()) * PIXELS_PER_LINE,
            key=f"{key if key else label}-{state.redraw_counter}",
            # help="help"
        )

        # Decode
        try:
            new_value = json.loads(input_s)
        except json.decoder.JSONDecodeError:
            return json_input_text(
                "The last edit was invalid json and has been reverted"
            )
        return new_value

    # Input a valid dict
    state.value = json_input_text()

    return state.value


if __name__ == "__main__":
    st.title("UP42 `input parameter` validator")

    st.write(
        """
        This app enables users to validate any input parameters.
        """
    )
    path_json = LOCATION.joinpath("template_input_params.json")
    with open(path_json) as jsonfile:
        json_input_param = json.load(jsonfile)

    col1, col2 = st.columns(2)
    with col1:
        d = dict_input("Edit me!", json_input_param)
    with col2:
        response = client.post("/validate", json=d)
        response_json = response.json()
        st.write("See the response here:")
        st.write(".", response_json)



