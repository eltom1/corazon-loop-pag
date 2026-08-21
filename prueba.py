import os
import tempfile

import matplotlib
matplotlib.use("Agg")

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="❤️",
    page_icon="❤️",
    layout="centered"
)

USUARIO = "Lu"
CONTRASENA = "amor123"


# ============================================================
# ESTADO
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "loves_me" not in st.session_state:
    st.session_state.loves_me = None


# ============================================================
# GENERAR GIF DEL CORAZÓN
# ============================================================

@st.cache_data
def generar_gif_corazon():

    scale = 15

    # Menos puntos = GIF más liviano
    n_points = 60

    angles = np.linspace(
        0,
        2 * np.pi,
        n_points
    )

    xs = (
        16
        * np.sin(angles) ** 3
        * scale
    )

    ys = (
        13 * np.cos(angles)
        - 5 * np.cos(2 * angles)
        - 2 * np.cos(3 * angles)
        - np.cos(4 * angles)
    ) * scale


    # --------------------------------------------------------
    # FIGURA
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(5, 5)
    )

    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    ax.set_xlim(
        xs.min() - 30,
        xs.max() + 30
    )

    ax.set_ylim(
        ys.min() - 30,
        ys.max() + 30
    )

    ax.axis("off")


    # --------------------------------------------------------
    # ANIMACIÓN
    # --------------------------------------------------------

    texts = []


    def update(frame):

        # Borrar el frame anterior
        for txt in texts:
            txt.remove()

        texts.clear()


        # Dibujar el corazón progresivamente
        for i in range(frame + 1):

            txt = ax.text(
                xs[i],
                ys[i],
                "I love you",
                color="#ff8cde",
                fontsize=8,
                fontweight="bold",
                ha="center",
                va="center"
            )

            texts.append(txt)

        return texts


    anim = animation.FuncAnimation(
        fig,
        update,
        frames=n_points,
        interval=40,
        blit=False
    )


    # --------------------------------------------------------
    # GUARDAR GIF TEMPORAL
    # --------------------------------------------------------

    with tempfile.NamedTemporaryFile(
        suffix=".gif",
        delete=False
    ) as tmp:

        tmp_path = tmp.name


    try:

        anim.save(
            tmp_path,
            writer="pillow",
            fps=25
        )

        plt.close(fig)

        with open(
            tmp_path,
            "rb"
        ) as f:

            gif_bytes = f.read()

    finally:

        if os.path.exists(tmp_path):
            os.remove(tmp_path)


    return gif_bytes


# ============================================================
# LOGIN
# ============================================================

def pantalla_login():

    st.title("🔒 Iniciar sesión")

    usuario = st.text_input(
        "Usuario"
    )

    contrasena = st.text_input(
        "Contraseña",
        type="password"
    )


    if st.button(
        "Ingresar",
        use_container_width=True
    ):

        if (
            usuario == USUARIO
            and contrasena == CONTRASENA
        ):

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error(
                "Usuario o contraseña incorrectos"
            )


# ============================================================
# PREGUNTA
# ============================================================

def pantalla_pregunta():

    st.markdown(
        """
        <h1 style="
            text-align:center;
        ">
            ¿Me amas? 🥺
        </h1>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # SÍ
    # --------------------------------------------------------

    with col1:

        if st.button(
            "Sí 💖",
            use_container_width=True
        ):

            st.session_state.loves_me = True

            st.rerun()


    # --------------------------------------------------------
    # NO
    # --------------------------------------------------------

    with col2:

        if st.button(
            "No 💔",
            use_container_width=True
        ):

            st.session_state.loves_me = False

            st.rerun()


# ============================================================
# CORAZÓN
# ============================================================

def pantalla_corazon():

    st.markdown(
        """
        <h2 style="
            text-align:center;
            color:#ff8cde;
        ">
            Sabía que sí 💕
        </h2>
        """,
        unsafe_allow_html=True
    )


    # Celebración
    st.balloons()


    # El GIF se genera solamente la primera vez.
    # Después Streamlit usa el caché.
    gif_bytes = generar_gif_corazon()


    st.image(
        gif_bytes,
        use_container_width=True
    )


# ============================================================
# NO
# ============================================================

def pantalla_no():

    st.markdown(
        """
        <h2 style="
            text-align:center;
        ">
            Está bien... 😢
        </h2>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "Esperá, me equivoqué 🥹",
        use_container_width=True
    ):

        st.session_state.loves_me = True

        st.rerun()


# ============================================================
# ROUTING
# ============================================================

if not st.session_state.logged_in:

    pantalla_login()

elif st.session_state.loves_me is None:

    pantalla_pregunta()

elif st.session_state.loves_me:

    pantalla_corazon()

else:

    pantalla_no()
