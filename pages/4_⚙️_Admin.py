import streamlit as st
import sqlite3
import pandas as pd

from import_matches import import_matches

from recalculate_scores import (
    recalculate_scores
)

from update_results import (
    update_results
)

# -------------------------
# VALIDAR SESIÓN
# -------------------------

if (
    "user" not in st.session_state
    or
    st.session_state.user is None
):

    st.warning(
        "Debe iniciar sesión."
    )

    st.stop()
# -------------------------
# VALIDAR ADMIN
# -------------------------

user = st.session_state.get(
    "user"
)

if user["role"] != "admin":

    st.error(
        "Acceso restringido."
    )

    st.stop()
# -------------------------
# TÍTULO
# -------------------------

st.title("⚙️ Administración")

# -------------------------
# CONTADOR DE PARTIDOS
# -------------------------

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM matches"
)

total_matches = cursor.fetchone()[0]

conn.close()

st.info(
    f"Partidos cargados: {total_matches}"
)

# -------------------------
# BORRAR PARTIDOS
# -------------------------

if st.button(
    "🗑️ Borrar todos los partidos"
):

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM matches"
    )

    conn.commit()
    conn.close()

    st.success(
        "Todos los partidos fueron eliminados"
    )

    st.rerun()

# -------------------------
# IMPORTAR CSV
# -------------------------

st.subheader(
    "📁 Importar partidos desde CSV"
)

uploaded_file = st.file_uploader(
    "Seleccione archivo CSV",
    type=["csv"]
)

if uploaded_file:

    if st.button(
        "Importar partidos"
    ):

        total = import_matches(
            uploaded_file
        )

        st.success(
            f"{total} partidos importados correctamente"
        )

        st.rerun()

# -------------------------
# MOSTRAR PARTIDOS
# -------------------------

st.subheader(
    "📋 Partidos cargados"
)

if st.button(
    "🔄 Actualizar resultados desde API"
):

    update_results()

    recalculate_scores()

    st.success(
        "Resultados actualizados"
    )

    st.rerun()

conn = sqlite3.connect(
    "data/worldcup.db"
)

df = pd.read_sql_query(
    """
    SELECT
        id,
        home_team,
        away_team,
        match_datetime,
        stage
    FROM matches
    ORDER BY match_datetime
    """,
    conn
)

conn.close()

if len(df) > 0:

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No hay partidos cargados."
    )
    
# -------------------------
# GESTIONAR RESULTADOS
# -------------------------

st.divider()

st.subheader(
    "⚽ Gestionar resultados"
)

conn = sqlite3.connect(
    "data/worldcup.db"
)

matches_df = pd.read_sql_query(
    """
    SELECT
        id,
        home_team,
        away_team,
        match_datetime,
        home_score,
        away_score,
        finished
    FROM matches
    ORDER BY match_datetime
    """,
    conn
)

conn.close()

if len(matches_df) > 0:

    match_options = {
        f"{row['id']} - {row['home_team']} vs {row['away_team']}":
        row["id"]
        for _, row in matches_df.iterrows()
    }

    selected_match = st.selectbox(
        "Seleccione un partido",
        options=list(match_options.keys())
    )

    match_id = match_options[
        selected_match
    ]

    selected_row = matches_df[
        matches_df["id"] == match_id
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        home_score = st.number_input(
            selected_row["home_team"],
            min_value=0,
            max_value=20,
            value=int(
                selected_row["home_score"]
            )
            if pd.notna(
                selected_row["home_score"]
            )
            else 0
        )

    with col2:

        away_score = st.number_input(
            selected_row["away_team"],
            min_value=0,
            max_value=20,
            value=int(
                selected_row["away_score"]
            )
            if pd.notna(
                selected_row["away_score"]
            )
            else 0
        )

    finished = st.checkbox(
        "Partido finalizado",
        value=bool(
            selected_row["finished"]
        )
    )

    if st.button(
        "💾 Guardar resultado"
    ):

        conn = sqlite3.connect(
            "data/worldcup.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE matches
            SET
                home_score=?,
                away_score=?,
                finished=?
            WHERE id=?
            """,
            (
                home_score,
                away_score,
                int(finished),
                match_id
            )
        )

        conn.commit()
        conn.close()

        # Recalcular clasificación
        recalculate_scores()

        st.success(
            "Resultado guardado correctamente"
        )

        st.rerun()

# -------------------------
# CARGAR PRONÓSTICOS
# -------------------------

st.divider()

st.subheader(
    "📝 Cargar pronósticos históricos"
)

conn = sqlite3.connect(
    "data/worldcup.db"
)

users_df = pd.read_sql_query(
    """
    SELECT
        id,
        name
    FROM users
    WHERE role='user'
    ORDER BY name
    """,
    conn
)

matches_df = pd.read_sql_query(
    """
    SELECT
        id,
        home_team,
        away_team,
        match_datetime
    FROM matches
    ORDER BY match_datetime
    """,
    conn
)

conn.close()

if len(users_df) > 0 and len(matches_df) > 0:

    user_options = {
        row["name"]: row["id"]
        for _, row in users_df.iterrows()
    }

    selected_user = st.selectbox(
        "Usuario",
        options=list(user_options.keys()),
        key="prediction_user"
    )

    user_id = user_options[
        selected_user
    ]

    match_options = {
        f"{row['home_team']} vs {row['away_team']} ({row['match_datetime']})":
        row["id"]
        for _, row in matches_df.iterrows()
    }

    selected_match = st.selectbox(
        "Partido",
        options=list(match_options.keys()),
        key="prediction_match"
    )

    match_id = match_options[
        selected_match
    ]

    selected_row = matches_df[
        matches_df["id"] == match_id
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        pred_home = st.number_input(
            selected_row["home_team"],
            min_value=0,
            max_value=20,
            value=0,
            key="pred_home"
        )

    with col2:

        pred_away = st.number_input(
            selected_row["away_team"],
            min_value=0,
            max_value=20,
            value=0,
            key="pred_away"
        )
        

    if st.button(
        "💾 Guardar pronóstico histórico"
    ):



        st.info(
            f"Guardando: "
            f"usuario={user_id}, "
            f"partido={match_id}, "
            f"pronóstico={pred_home}-{pred_away}"
        )

        conn = sqlite3.connect(
            "data/worldcup.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO predictions
            (
                user_id,
                match_id,
                pred_home,
                pred_away,
                created_at
            )
            VALUES
            (
                ?,?,?,?,
                datetime('now')
            )
            """,
            (
                user_id,
                match_id,
                pred_home,
                pred_away
            )
        )

        conn.commit()



        conn.close()

        recalculate_scores()

        st.success(
            "Pronóstico guardado correctamente"
        )

        st.rerun()
