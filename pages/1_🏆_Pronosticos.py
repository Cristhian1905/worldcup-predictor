import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime

from scoring import (
    save_prediction,
    get_prediction,
    get_points_for_prediction
)

# ---------------------------------
# BANDERAS
# ---------------------------------

FLAGS = {
    "Mexico": "🇲🇽",
    "South Africa": "🇿🇦",
    "Korea Republic": "🇰🇷",
    "Czechia": "🇨🇿",
    "Canada": "🇨🇦",
    "Bosnia and Herzegovina": "🇧🇦",
    "Qatar": "🇶🇦",
    "Switzerland": "🇨🇭",
    "Brazil": "🇧🇷",
    "Morocco": "🇲🇦",
    "Haiti": "🇭🇹",
    "Scotland": "🏴",
    "USA": "🇺🇸",
    "United States": "🇺🇸",
    "Paraguay": "🇵🇾",
    "Australia": "🇦🇺",
    "Turkiye": "🇹🇷",
    "Germany": "🇩🇪",
    "Curacao": "🇨🇼",
    "Cote d'Ivoire": "🇨🇮",
    "Ecuador": "🇪🇨",
    "Netherlands": "🇳🇱",
    "Japan": "🇯🇵",
    "Sweden": "🇸🇪",
    "Tunisia": "🇹🇳",
    "Belgium": "🇧🇪",
    "Egypt": "🇪🇬",
    "IR Iran": "🇮🇷",
    "Iran": "🇮🇷",
    "New Zealand": "🇳🇿",
    "Spain": "🇪🇸",
    "Cabo Verde": "🇨🇻",
    "Saudi Arabia": "🇸🇦",
    "Uruguay": "🇺🇾",
    "France": "🇫🇷",
    "Senegal": "🇸🇳",
    "Iraq": "🇮🇶",
    "Norway": "🇳🇴",
    "Argentina": "🇦🇷",
    "Algeria": "🇩🇿",
    "Austria": "🇦🇹",
    "Jordan": "🇯🇴",
    "Portugal": "🇵🇹",
    "Congo DR": "🇨🇩",
    "Uzbekistan": "🇺🇿",
    "Colombia": "🇨🇴",
    "England": "🏴",
    "Croatia": "🇭🇷",
    "Ghana": "🇬🇭",
    "Panama": "🇵🇦"
}

# ---------------------------------
# VALIDAR SESIÓN
# ---------------------------------

if (
    "user" not in st.session_state
    or
    st.session_state.user is None
):
    st.warning(
        "Debe iniciar sesión."
    )
    st.stop()

# ---------------------------------
# TÍTULO
# ---------------------------------

st.title("🏆 Pronósticos Mundial 2026")

st.write(
    f"Bienvenido, "
    f"{st.session_state.user['name']}"
)

# ---------------------------------
# MODO ADMINISTRADOR
# ---------------------------------

is_admin = (
    st.session_state.user["role"]
    == "admin"
)

allow_historical_edit = False

if is_admin:

    st.warning(
        "⚠️ MODO ADMINISTRADOR ACTIVADO\n\n"
        "Puedes editar pronósticos incluso después del inicio del partido."
    )

    allow_historical_edit = st.toggle(
        "🕒 Permitir edición de partidos ya iniciados",
        value=True
    )

# ---------------------------------
# CARGAR PARTIDOS
# ---------------------------------

conn = sqlite3.connect(
    "data/worldcup.db"
)

matches = pd.read_sql_query(
    """
    SELECT *
    FROM matches
    ORDER BY stage,
             match_datetime
    """,
    conn
)

conn.close()

if len(matches) == 0:

    st.info(
        "No hay partidos cargados."
    )

    st.stop()

# ---------------------------------
# FILTRO FECHA
# ---------------------------------

st.divider()

selected_date = st.date_input(
    "📅 Seleccione fecha",
    value=datetime.now().date()
)

matches["match_datetime"] = pd.to_datetime(
    matches["match_datetime"],
    errors="coerce"
)

matches = matches[
    matches["match_datetime"].dt.date
    == selected_date
]

st.info(
    f"⚽ Partidos encontrados: {len(matches)}"
)

if len(matches) == 0:

    st.warning(
        "No hay partidos para esta fecha."
    )

    st.stop()

# ---------------------------------
# RECORRER PARTIDOS
# ---------------------------------

for stage in matches["stage"].unique():

    st.header(f"🏆 {stage}")

    stage_matches = matches[
        matches["stage"] == stage
    ]

    for _, match in stage_matches.iterrows():

        with st.container(border=True):

            home_flag = FLAGS.get(
                match["home_team"],
                "🏳️"
            )

            away_flag = FLAGS.get(
                match["away_team"],
                "🏳️"
            )

            st.subheader(
                f"{home_flag} {match['home_team']}  vs  "
                f"{away_flag} {match['away_team']}"
            )

            # -------------------------
            # FECHA
            # -------------------------

            if pd.notna(
                match["match_datetime"]
            ):

                st.caption(
                    "📅 "
                    + match[
                        "match_datetime"
                    ].strftime(
                        "%d/%m/%Y %H:%M"
                    )
                )

            # -------------------------
            # BLOQUEO
            # -------------------------

            match_started = False

            if pd.notna(
                match["match_datetime"]
            ):

                match_started = (
                    datetime.now()
                    >=
                    match["match_datetime"]
                )

            if match_started:

                if is_admin:

                    st.info(
                        "⚙️ Partido iniciado. Edición permitida para administrador."
                    )

                else:

                    st.error(
                        "🔒 Este partido ya comenzó."
                    )

            if is_admin:

                locked = False

                if not allow_historical_edit:

                    locked = match_started

            else:

                locked = match_started

            # -------------------------
            # PRONÓSTICO GUARDADO
            # -------------------------

            saved_prediction = get_prediction(
                st.session_state.user["id"],
                match["id"]
            )

            default_home = 0
            default_away = 0

            if saved_prediction:

                default_home = saved_prediction[0]
                default_away = saved_prediction[1]

                st.success(
                    f"Pronóstico actual: "
                    f"{default_home} - {default_away}"
                )
            # -------------------------
            # RESULTADO FINAL
            # -------------------------

            if match["finished"] == 1:

                st.divider()

                st.markdown(
                    f"### Resultado oficial: "
                    f"{match['home_score']} - "
                    f"{match['away_score']}"
                )

                points = get_points_for_prediction(
                    st.session_state.user["id"],
                    match["id"]
                )

                if points == 6:

                    st.success(
                        f"🏆 Marcador exacto (+{points} puntos)"
                    )

                elif points > 0:

                    st.info(
                        f"✅ Acertaste el resultado (+{points} puntos)"
                    )

                else:

                    st.error(
                        "❌ Sin puntos"
                    )

            # -------------------------
            # INPUTS
            # -------------------------

            col1, col2 = st.columns(2)

            with col1:

                pred_home = st.number_input(
                    match["home_team"],
                    min_value=0,
                    max_value=20,
                    value=int(default_home),
                    disabled=locked,
                    key=f"home_{match['id']}"
                )

            with col2:

                pred_away = st.number_input(
                    match["away_team"],
                    min_value=0,
                    max_value=20,
                    value=int(default_away),
                    disabled=locked,
                    key=f"away_{match['id']}"
                )

            # -------------------------
            # BOTÓN
            # -------------------------

            button_text = (
                "💾 Guardar pronóstico"
            )

            if saved_prediction:

                button_text = (
                    "✏️ Actualizar pronóstico"
                )

            if st.button(
                button_text,
                key=f"save_{match['id']}",
                disabled=locked,
                width="stretch"
            ):

                save_prediction(
                    st.session_state.user["id"],
                    match["id"],
                    pred_home,
                    pred_away
                )

                st.success(
                    "✅ Pronóstico guardado correctamente"
                )

                st.rerun()
