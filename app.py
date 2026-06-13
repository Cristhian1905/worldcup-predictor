import streamlit as st

from auth import login
from register import register_user

st.set_page_config(
    page_title="World Cup Predictor 2026",
    page_icon="🏆",
    layout="wide"
)

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.title("🏆 World Cup Predictor 2026")

    tab1, tab2 = st.tabs([
        "Iniciar Sesión",
        "Crear Cuenta"
    ])

    with tab1:

        username = st.text_input(
            "Usuario",
            key="login_user"
        )

        password = st.text_input(
            "Contraseña",
            type="password",
            key="login_pass"
        )

        if st.button("Ingresar"):

            user = login(
                username,
                password
            )

            if user:

                st.session_state.user = user

                st.rerun()

            else:

                st.error(
                    "Usuario o contraseña incorrectos"
                )

    with tab2:

        name = st.text_input(
            "Nombre completo"
        )

        username = st.text_input(
            "Usuario"
        )

        password = st.text_input(
            "Contraseña",
            type="password"
        )

        if st.button("Crear cuenta"):

            success = register_user(
                name,
                username,
                password
            )

            if success:

                st.success(
                    "Cuenta creada correctamente"
                )

            else:

                st.error(
                    "Ese usuario ya existe"
                )

else:

    st.title("🏆 World Cup Predictor 2026")

    st.success(
        f"Bienvenido {st.session_state.user['name']}"
    )

    st.info(
        "Seleccione una opción en el menú lateral."
    )

    if st.button("Cerrar sesión"):

        st.session_state.user = None

        st.rerun()
