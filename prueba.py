import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Te amo", page_icon="💗", layout="centered")

# Oculta el header/footer/menú de Streamlit para que quede bien estético
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 1rem;}
        body {background-color: #000000;}
    </style>
    """,
    unsafe_allow_html=True,
)

corazon_html = """
<div style="display:flex; justify-content:center; align-items:center; background:#000000; border-radius:16px; padding:10px;">
  <canvas id="heart" width="600" height="520"></canvas>
</div>

<script>
const canvas = document.getElementById("heart");
const ctx = canvas.getContext("2d");

const cx = canvas.width / 2;
const cy = canvas.height / 2 + 30;
const scale = 15;

let t = 0;
const step = 0.05;
const twoPi = Math.PI * 2;

let phase = "draw";   // "draw" -> "hold" -> "fade"
let holdFrames = 0;
let fadeAlpha = 1;

function heartPoint(angle) {
    const x = 16 * Math.pow(Math.sin(angle), 3);
    const y = 13 * Math.cos(angle) - 5 * Math.cos(2 * angle) - 2 * Math.cos(3 * angle) - Math.cos(4 * angle);
    return { x: cx + x * scale, y: cy - y * scale };
}

function drawFrame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // fondo negro con glow sutil
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.globalAlpha = fadeAlpha;

    // trazo del corazón
    ctx.beginPath();
    ctx.strokeStyle = "#ffb6c1";
    ctx.lineWidth = 3;
    ctx.shadowColor = "#ff69b4";
    ctx.shadowBlur = 15;

    let first = true;
    for (let a = 0; a <= t; a += 0.02) {
        const p = heartPoint(a);
        if (first) {
            ctx.moveTo(p.x, p.y);
            first = false;
        } else {
            ctx.lineTo(p.x, p.y);
        }
    }
    ctx.stroke();

    // relleno una vez completo
    if (t >= twoPi) {
        ctx.beginPath();
        for (let a = 0; a <= twoPi; a += 0.02) {
            const p = heartPoint(a);
            if (a === 0) ctx.moveTo(p.x, p.y);
            else ctx.lineTo(p.x, p.y);
        }
        ctx.closePath();
        ctx.fillStyle = "rgba(255,105,180,0.15)";
        ctx.fill();

        // texto "Te amo" pulsante
        const pulse = 1 + 0.08 * Math.sin(holdFrames * 0.15);
        ctx.save();
        ctx.translate(cx, cy);
        ctx.scale(pulse, pulse);
        ctx.font = "bold 42px Arial";
        ctx.fillStyle = "#ffffff";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.shadowColor = "#ff1493";
        ctx.shadowBlur = 20;
        ctx.fillText("Te amo", 0, 0);
        ctx.restore();
    }

    ctx.restore();
}

function loop() {
    if (phase === "draw") {
        t += step;
        if (t >= twoPi) {
            t = twoPi;
            phase = "hold";
        }
    } else if (phase === "hold") {
        holdFrames += 1;
        if (holdFrames > 130) {
            phase = "fade";
        }
    } else if (phase === "fade") {
        fadeAlpha -= 0.03;
        if (fadeAlpha <= 0) {
            fadeAlpha = 0;
            t = 0;
            holdFrames = 0;
            fadeAlpha = 1;
            phase = "draw";
        }
    }

    drawFrame();
    requestAnimationFrame(loop);
}

loop();
</script>
"""

components.html(corazon_html, height=560)