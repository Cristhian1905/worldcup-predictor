import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime

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
# TÍTULO
# -------------------------

st.title(
    "🏆 World Cup Predictor 2026"
)

st.write(
    f"Bienvenido, "
    f"{st.session_state.user['name']}"
)

# -------------------------
# CONEXIÓN
# -------------------------

conn = sqlite3.connect(
    "data/worldcup.db"
)

# -------------------------
# PARTIDOS HOY
# -------------------------

today = datetime.now().date()

matches_today = pd.read_sql_query(
    """
    SELECT *
    FROM matches
    """,
    conn
)

matches_today["match_datetime"] = pd.to_datetime(
    matches_today["match_datetime"]
)

matches_today = matches_today[
    matches_today["match_datetime"].dt.date
    == today
]

# -------------------------
# LÍDER
# -------------------------

leader = pd.read_sql_query(
    """
    SELECT

    u.name,
    COALESCE(
        SUM(s.points),
        0
    ) as total_points

    FROM users u

    LEFT JOIN scores s
    ON u.id = s.user_id

    GROUP BY u.id

    ORDER BY total_points DESC

    LIMIT 1
    """,
    conn
)

# -------------------------
# EXACTOS
# -------------------------

exact_scores = pd.read_sql_query(
    """
    SELECT COUNT(*) as total
    FROM scores
    WHERE points = 6
    """,
    conn
)

# -------------------------
# PRONÓSTICOS
# -------------------------

predictions = pd.read_sql_query(
    """
    SELECT COUNT(*) as total
    FROM predictions
    """,
    conn
)

# -------------------------
# MÉTRICAS
# -------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "⚽ Partidos hoy",
        len(matches_today)
    )

with col2:

    if len(leader):

        st.metric(
            "👑 Líder",
            leader.iloc[0]["name"],
            f"{int(leader.iloc[0]['total_points'])} pts"
        )

with col3:

    st.metric(
        "🎯 Exactos",
        int(
            exact_scores.iloc[0]["total"]
        )
    )

with col4:

    st.metric(
        "📊 Pronósticos",
        int(
            predictions.iloc[0]["total"]
        )
    )

# -------------------------
# PRÓXIMOS PARTIDOS
# -------------------------

st.divider()

st.subheader(
    "📅 Próximos partidos"
)

upcoming = pd.read_sql_query(
    """
    SELECT
    home_team,
    away_team,
    match_datetime
    FROM matches
    WHERE finished = 0
    ORDER BY match_datetime
    LIMIT 10
    """,
    conn
)

conn.close()

for _, match in upcoming.iterrows():

    st.container()

    st.markdown(
        f"**{match['home_team']} vs {match['away_team']}**"
    )

    st.caption(
        match["match_datetime"]
    )
