import streamlit as st
import sqlite3
import pandas as pd

from recalculate_scores import (
    recalculate_scores
)

from update_results import (
    update_results
)

from auto_update import (
    should_update,
    mark_updated
)
# ---------------------------------
# VALIDAR SESIÓN
# ---------------------------------

if "user" not in st.session_state:

    st.warning(
        "Debe iniciar sesión."
    )

    st.stop()

# ---------------------------------
# RECALCULAR AUTOMÁTICAMENTE
# ---------------------------------

if should_update(1):

    try:

        update_results()

        recalculate_scores()

        mark_updated()

    except Exception as e:

        print(
            "Error actualización:",
            e
        )

# ---------------------------------
# TÍTULO
# ---------------------------------

st.title(
    "📊 Clasificación Mundial 2026"
)

# ---------------------------------
# CONSULTA
# ---------------------------------

conn = sqlite3.connect(
    "data/worldcup.db"
)

query = """
SELECT

u.name,

COALESCE(
    SUM(s.points),
    0
) as total_points,

SUM(
    CASE
        WHEN s.points >= 4
        THEN 1
        ELSE 0
    END
) as exact_scores,

SUM(
    CASE
        WHEN s.points > 0
        THEN 1
        ELSE 0
    END
) as correct_predictions

FROM users u

LEFT JOIN scores s
ON u.id = s.user_id

WHERE u.role <> 'admin'

GROUP BY u.id

ORDER BY total_points DESC
"""

df = pd.read_sql_query(
    query,
    conn
)

conn.close()

# ---------------------------------
# SIN DATOS
# ---------------------------------

if len(df) == 0:

    st.info(
        "No hay clasificación disponible."
    )

    st.stop()

# ---------------------------------
# PODIO
# ---------------------------------

st.subheader(
    "🏆 Clasificación General"
)

medals = [
    "🥇",
    "🥈",
    "🥉"
]

for i, row in df.head(3).iterrows():

    medal = ""

    if i < len(medals):

        medal = medals[i]

    st.markdown(
        f"### {medal} "
        f"{row['name']} "
        f"— "
        f"{int(row['total_points'])} pts"
    )

# ---------------------------------
# MÉTRICAS
# ---------------------------------

st.divider()

leader_points = int(
    df.iloc[0]["total_points"]
)

st.metric(
    "👑 Líder actual",
    df.iloc[0]["name"],
    f"{leader_points} pts"
)

# ---------------------------------
# TABLA COMPLETA
# ---------------------------------

st.divider()

df_display = df.copy()

df_display.columns = [
    "Usuario",
    "Puntos",
    "Marcadores Exactos",
    "Aciertos"
]

df_display.index = (
    df_display.index + 1
)

st.dataframe(
    df_display,
    width="stretch"
)

# ---------------------------------
# ESTADÍSTICAS
# ---------------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Usuarios",
        len(df)
    )

with col2:

    st.metric(
        "Puntos Totales",
        int(
            df["total_points"].sum()
        )
    )

with col3:

    st.metric(
        "Marcadores Exactos",
        int(
            df["exact_scores"].sum()
        )
    )
