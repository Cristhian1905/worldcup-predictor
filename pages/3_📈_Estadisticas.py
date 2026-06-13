import streamlit as st


from utils import require_login

require_login()


st.title("📈 Estadísticas")

st.info(
    "Próximamente estadísticas del torneo."
)
