import streamlit as st


def require_login():

    if (
        "user" not in st.session_state
        or
        st.session_state.user is None
    ):

        st.warning(
            "Debe iniciar sesión."
        )

        st.stop()
