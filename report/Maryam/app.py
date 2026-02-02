import streamlit as st
import math
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import io

# Configuration de la page
st.set_page_config(
    page_title="Advanced Option Pricing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec les couleurs demandées
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .header-box {
        background: linear-gradient(135deg, #800020, #DC143C);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(128, 0, 32, 0.3);
    }
    .parameter-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #800020;
    }
    .result-card {
        background: linear-gradient(135deg, #32CD32, #228B22);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(50, 205, 50, 0.3);
        margin: 1rem 0;
    }
    .model-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-top: 4px solid #800020;
    }
    .info-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #32CD32;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .calculate-btn {
        background-color: #32CD32 !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1.1rem !important;
    }
    .calculate-btn:hover {
        background-color: #228B22 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(34, 139, 34, 0.3);
    }
    .nav-btn {
        background-color: #800020 !important;
        color: white !important;
        border: none !important;
        margin: 0.2rem;
    }
    .nav-btn:hover {
        background-color: #DC143C !important;
    }
    .section-title {
        color: #800020;
        font-weight: bold;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    .subsection-title {
        color: #DC143C;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
        font-size: 1.1rem;
    }
    .quick-adjust-btn {
        background-color: #f8f9fa !important;
        color: #800020 !important;
        border: 1px solid #800020 !important;
        margin: 0.1rem;
    }
    .tab-content {
        padding: 1rem 0;
    }
    .greek-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
        margin: 0.2rem;
    }
    .convergence-plot {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Fonction Black-Scholes avec Grecques
def black_scholes(S, K, T, r, sigma, option_type, dividend=0):
    """Calcule le prix d'une option européenne avec le modèle Black-Scholes et ses Grecques"""
    if T <= 0:
        return 0, {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
    
    d1 = (math.log(S / K) + (r - dividend + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == 'call':
        price = S * math.exp(-dividend * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        delta = math.exp(-dividend * T) * norm.cdf(d1)
        theta = (-(S * math.exp(-dividend * T) * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) 
                 + dividend * S * math.exp(-dividend * T) * norm.cdf(d1)
                 - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100
    else:  # put
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-dividend * T) * norm.cdf(-d1)
        delta = math.exp(-dividend * T) * (norm.cdf(d1) - 1)
        theta = (-(S * math.exp(-dividend * T) * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) 
                 - dividend * S * math.exp(-dividend * T) * norm.cdf(-d1)
                 + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100
    
    gamma = (math.exp(-dividend * T) * norm.pdf(d1)) / (S * sigma * math.sqrt(T))
    vega = S * math.exp(-dividend * T) * norm.pdf(d1) * math.sqrt(T) / 100
    
    greeks = {
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega,
        'rho': rho
    }
    
    return max(price, 0), greeks

# Fonction Binomial
def binomial_tree(S, K, T, r, sigma, n, option_type, option_style='european', dividend=0):
    """Calcule le prix d'une option avec le modèle binomial"""
    if T <= 0:
        return 0
    
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((r - dividend) * dt) - d) / (u - d)
    
    # Initialiser les prix à l'échéance
    prices = [0] * (n + 1)
    for i in range(n + 1):
        if option_type == 'call':
            prices[i] = max(S * (u ** i) * (d ** (n - i)) - K, 0)
        else:
            prices[i] = max(K - S * (u ** i) * (d ** (n - i)), 0)
    
    # Calculer les prix en remontant dans l'arbre
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            prices[i] = (p * prices[i + 1] + (1 - p) * prices[i]) * math.exp(-r * dt)
            
            # Exercice anticipé pour les options américaines
            if option_style == 'american':
                current_price = S * (u ** i) * (d ** (j - i))
                if option_type == 'call':
                    exercise_value = max(current_price - K, 0)
                else:
                    exercise_value = max(K - current_price, 0)
                prices[i] = max(prices[i], exercise_value)
    
    return prices[0]

# Fonction Trinomial
def trinomial_tree(S, K, T, r, sigma, n, option_type, option_style='european', dividend=0):
    """Calcule le prix d'une option avec le modèle trinomial"""
    if T <= 0:
        return 0
    
    dt = T / n
    u = math.exp(sigma * math.sqrt(2 * dt))
    d = 1 / u
    m = 1
    
    pu = ((math.exp((r - dividend) * dt / 2) - math.exp(-sigma * math.sqrt(dt / 2))) / 
          (math.exp(sigma * math.sqrt(dt / 2)) - math.exp(-sigma * math.sqrt(dt / 2)))) ** 2
    pd = ((math.exp(sigma * math.sqrt(dt / 2)) - math.exp((r - dividend) * dt / 2)) / 
          (math.exp(sigma * math.sqrt(dt / 2)) - math.exp(-sigma * math.sqrt(dt / 2)))) ** 2
    pm = 1 - pu - pd
    
    # Initialiser les prix à l'échéance
    prices = [0] * (2 * n + 1)
    for i in range(2 * n + 1):
        stock_price = S * (u ** max(i - n, 0)) * (d ** max(n - i, 0))
        if option_type == 'call':
            prices[i] = max(stock_price - K, 0)
        else:
            prices[i] = max(K - stock_price, 0)
    
    # Calculer les prix en remontant dans l'arbre
    for j in range(n - 1, -1, -1):
        for i in range(2 * j + 1):
            up_idx = i + 2
            mid_idx = i + 1
            down_idx = i
            
            prices[i] = (pu * prices[up_idx] + pm * prices[mid_idx] + pd * prices[down_idx]) * math.exp(-r * dt)
            
            # Exercice anticipé pour les options américaines
            if option_style == 'american':
                stock_price = S * (u ** max(i - j, 0)) * (d ** max(j - i, 0))
                if option_type == 'call':
                    exercise_value = max(stock_price - K, 0)
                else:
                    exercise_value = max(K - stock_price, 0)
                prices[i] = max(prices[i], exercise_value)
    
    return prices[0]

def calculate_greeks(S, K, T, r, sigma, option_type, model_type, steps=100, dividend=0):
    """Calcule les Grecques par différences finies pour les modèles d'arbres"""
    epsilon = 0.01
    
    if model_type == "Binomial":
        model_func = binomial_tree
    else:  # Trinomial
        model_func = trinomial_tree
    
    # Prix actuel
    current_price = model_func(S, K, T, r, sigma, steps, option_type, 'european', dividend)
    
    # Delta
    price_up = model_func(S * (1 + epsilon), K, T, r, sigma, steps, option_type, 'european', dividend)
    price_down = model_func(S * (1 - epsilon), K, T, r, sigma, steps, option_type, 'european', dividend)
    delta = (price_up - price_down) / (2 * S * epsilon)
    
    # Gamma
    gamma = (price_up - 2 * current_price + price_down) / ((S * epsilon) ** 2)
    
    # Theta (variation sur 1 jour)
    price_time = model_func(S, K, T + 1/365, r, sigma, steps, option_type, 'european', dividend)
    theta = (price_time - current_price)  # Pour 1 jour
    
    # Vega
    price_vega = model_func(S, K, T, r, sigma + epsilon, steps, option_type, 'european', dividend)
    vega = (price_vega - current_price) / (100 * epsilon)  # Pour 1% de changement
    
    # Rho
    price_rho = model_func(S, K, T, r + epsilon, sigma, steps, option_type, 'european', dividend)
    rho = (price_rho - current_price) / (100 * epsilon)  # Pour 1% de changement
    
    return {
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega,
        'rho': rho
    }

import plotly.graph_objects as go

# --- Helpers figures ---------------------------------------------------------
def _binomial_tree_fig(n=5, title="Arbre binomial (n périodes)"):
    # positions: niveau t (0..n), noeud i (0..t)
    xs, ys = [], []
    edges_x, edges_y = [], []
    for t in range(n + 1):
        for i in range(t + 1):
            xs.append(t)
            ys.append(i - t/2)  # centre vertical pour un look équilibré

    # map (t,i) -> index
    def idx(t, i): return t*(t+1)//2 + i

    # edges: (t,i)->(t+1,i) (down) et (t+1,i+1) (up)
    for t in range(n):
        for i in range(t + 1):
            x0, y0 = t, (i - t/2)
            # down
            x1, y1 = t+1, (i - (t+1)/2)
            edges_x += [x0, x1, None]
            edges_y += [y0, y1, None]
            # up
            x2, y2 = t+1, (i+1 - (t+1)/2)
            edges_x += [x0, x2, None]
            edges_y += [y0, y2, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode="lines",
                             line=dict(width=1.2), name="Transitions"))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers+text",
                             marker=dict(size=9),
                             text=[f"{t},{i}" for t in range(n+1) for i in range(t+1)],
                             textposition="top center", name="Nœuds"))
    fig.update_layout(template="plotly_white",
                      title=f"{title}".replace("n", str(n)),
                      xaxis_title="t (périodes)", yaxis_title="états",
                      showlegend=False, height=420,
                      margin=dict(l=20, r=20, t=50, b=10))
    fig.update_xaxes(dtick=1, range=[-0.2, n+0.2])
    return fig

def _trinomial_tree_fig(n=4, title="Arbre trinomial (n périodes)"):
    # niveaux t (0..n), index d’état k dans [-t..t]
    # positions: x=t, y=k ; on centre verticalement
    xs, ys = [], []
    edges_x, edges_y = [], []
    for t in range(n + 1):
        for k in range(-t, t+1):
            xs.append(t)
            ys.append(k)

    # edges: (t,k)->(t+1,k+1),(t+1,k),(t+1,k-1)
    for t in range(n):
        for k in range(-t, t+1):
            x0, y0 = t, k
            for dk in (+1, 0, -1):
                x1, y1 = t+1, k+dk
                edges_x += [x0, x1, None]
                edges_y += [y0, y1, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode="lines",
                             line=dict(width=1.2), name="Transitions"))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers+text",
                             marker=dict(size=9),
                             text=[f"{t},{k}" for t in range(n+1) for k in range(-t, t+1)],
                             textposition="top center", name="Nœuds"))
    fig.update_layout(template="plotly_white",
                      title=f"{title}".replace("n", str(n)),
                      xaxis_title="t (périodes)", yaxis_title="états",
                      showlegend=False, height=420,
                      margin=dict(l=20, r=20, t=50, b=10))
    fig.update_xaxes(dtick=1, range=[-0.2, n+0.2])
    return fig

# --- Home page ---------------------------------------------------------------
import plotly.graph_objects as go

# ==== Helpers pour les schémas (représentatifs) ====
def _binomial_tree_fig(n=5, title="Schéma représentatif — Arbre binomial"):
    xs, ys, edges_x, edges_y = [], [], [], []
    # positions des noeuds (t,i) centrées verticalement
    for t in range(n + 1):
        for i in range(t + 1):
            xs.append(t)
            ys.append(i - t/2)

    # arêtes (t,i)->(t+1,i) et (t,i)->(t+1,i+1)
    for t in range(n):
        for i in range(t + 1):
            x0, y0 = t, (i - t/2)
            x1, y1 = t+1, (i - (t+1)/2)       # down
            x2, y2 = t+1, (i+1 - (t+1)/2)     # up
            edges_x += [x0, x1, None, x0, x2, None]
            edges_y += [y0, y1, None, y0, y2, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode="lines",
                             line=dict(width=1.2), name="Transitions"))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers",
                             marker=dict(size=8), name="Nœuds"))
    fig.update_layout(template="plotly_white", title=title,
                      xaxis_title="t (étapes)", yaxis_title="états",
                      showlegend=False, height=360,
                      margin=dict(l=20, r=20, t=50, b=10))
    fig.update_xaxes(dtick=1, range=[-0.2, n+0.2])
    return fig

def _trinomial_tree_fig(n=5, title="Schéma représentatif — Arbre trinomial"):
    xs, ys, edges_x, edges_y = [], [], [], []
    # noeuds (t,k) avec k ∈ [-t, …, t]
    for t in range(n + 1):
        for k in range(-t, t+1):
            xs.append(t)
            ys.append(k)
    # arêtes (t,k)->(t+1,k+1),(t+1,k),(t+1,k-1)
    for t in range(n):
        for k in range(-t, t+1):
            x0, y0 = t, k
            for dk in (+1, 0, -1):
                x1, y1 = t+1, k+dk
                edges_x += [x0, x1, None]
                edges_y += [y0, y1, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode="lines",
                             line=dict(width=1.2), name="Transitions"))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers",
                             marker=dict(size=8), name="Nœuds"))
    fig.update_layout(template="plotly_white", title=title,
                      xaxis_title="t (étapes)", yaxis_title="états",
                      showlegend=False, height=360,
                      margin=dict(l=20, r=20, t=50, b=10))
    fig.update_xaxes(dtick=1, range=[-0.2, n+0.2])
    return fig

# ==== Home page homogène ====


def show_home_page():
    """Affiche la page d'accueil (boxes titrées, schémas fixes, colonnes homogènes)"""

    # ===== En-tête =====
    st.markdown("""
    <div class="header-box">
        <h1 style="margin:0;font-size:2.5rem;">📊 Option Pricing</h1>
        <p style="margin:0;font-size:1.1rem;opacity:.9;">Guide Complet des Modèles de Pricing d'Options</p>
    </div>
    """, unsafe_allow_html=True)

    # ===== Introduction =====
    st.markdown("<div class='info-card'><div class='section-title'>🎯 Introduction au Pricing d'Options</div>", unsafe_allow_html=True)
    st.write("""
    Cette application calcule le prix théorique d’options avec **Black–Scholes**, **Binomial** et **Trinomial**.
    Elle illustre les hypothèses, paramètres et sensibilités (Greeks) pour mieux comparer les méthodes.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Black–Scholes =====
    st.markdown("<div class='info-card'><div class='section-title'>📈 Modèle Black–Scholes</div>", unsafe_allow_html=True)
    
    st.markdown("**Définition :** Formule fermée pour options **européennes** (1973).")
    st.markdown("**Formule (Call) :**")
    st.latex(r"C = S_0 e^{-qT} N(d_1) - K e^{-rT} N(d_2)")
    st.latex(r"d_1 = \frac{\ln(S_0/K) + (r - q + \tfrac{1}{2}\sigma^2)T}{\sigma\sqrt{T}},\quad d_2 = d_1 - \sigma\sqrt{T}")
    st.markdown("**Hypothèses clés :**")
    st.markdown("- Volatilité et taux **constants**\n- Marché frictionless, **pas d’arbitrage**\n- **Log-normalité** des prix sous risque-neutre")


    # ===== Binomial =====
    st.markdown("<div class='info-card'><div class='section-title'>🌳 Modèle Binomial</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        # suppose que _binomial_tree_fig(n) existe déjà dans ton code
        st.plotly_chart(_binomial_tree_fig(n=5), use_container_width=True)
    with c2:
        st.markdown("**Définition :** Arbre à deux branches (hausse **u** / baisse **d**) avec probabilité risque-neutre **p**.")
        st.markdown("**Paramètres clés (CRR) :**")
        st.latex(r"u = e^{\sigma\sqrt{\Delta t}},\quad d = e^{-\sigma\sqrt{\Delta t}}=\frac{1}{u}")
        st.latex(r"p = \frac{e^{(r-q)\Delta t} - d}{u - d}")
        st.markdown("**Atouts :** gère l’**exercice anticipé** (américaines), **flexible** (dividendes, barrières), **converge** vers BS quand \(n\to\infty\).")
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Trinomial =====
    st.markdown("<div class='info-card'><div class='section-title'>🌲 Modèle Trinomial</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        **Définition :**  
        Arbre à **trois issues** (hausse, **stable**, baisse) — souvent une **convergence plus rapide** et plus stable.
        
        **Applications :**
        - Options américaines complexes, barrières  
        - Exotiques nécessitant une meilleure granularité
        """)
    with c2:
        st.plotly_chart(_trinomial_tree_fig(n=5), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    # ===== Greeks (aperçu avec popovers LaTeX) =====
    st.markdown("<div class='info-card'><div class='section-title'>📊 Les Grecques </div>", unsafe_allow_html=True)
    st.markdown("Clique sur chaque pastille pour voir la formule (modèle Black–Scholes, dividende continu \(q\)).")

    cols = st.columns(5, gap="large")

    # Δ
    with cols[0]:
        st.markdown(
            "<div style='background:#800020;color:#fff;padding:12px;border-radius:10px;text-align:center;font-weight:700;'>"
            "Δ<br><small style='font-weight:400;'>Prix du sous-jacent</small></div>",
            unsafe_allow_html=True
        )
        with st.popover("Formule"):
            st.latex(r"\Delta_{\text{call}} = e^{-qT}\,N(d_1)")
            st.latex(r"\Delta_{\text{put}}  = e^{-qT}\,N(d_1) - e^{-qT}")
            st.markdown("---")
            st.latex(r"d_1=\frac{\ln(S_0/K) + (r-q+\tfrac12\sigma^2)T}{\sigma\sqrt{T}}")

    # Γ
    with cols[1]:
        st.markdown(
            "<div style='background:#DC143C;color:#fff;padding:12px;border-radius:10px;text-align:center;font-weight:700;'>"
            "Γ<br><small style='font-weight:400;'>Variation du Δ</small></div>",
            unsafe_allow_html=True
        )
        with st.popover("Formule"):
            st.latex(r"\Gamma=\frac{e^{-qT}\,\varphi(d_1)}{S_0\,\sigma\,\sqrt{T}}")
            st.caption("Avec \( \varphi \) la densité normale standard.")

    # Θ
    with cols[2]:
        st.markdown(
            "<div style='background:#32CD32;color:#0b240b;padding:12px;border-radius:10px;text-align:center;font-weight:700;'>"
            "Θ<br><small style='font-weight:400;'>Décroissance temporelle</small></div>",
            unsafe_allow_html=True
        )
        with st.popover("Formule"):
            st.latex(
                r"\Theta_{\text{call}} = -\frac{S_0 e^{-qT}\varphi(d_1)\sigma}{2\sqrt{T}}"
                r" - rK e^{-rT} N(d_2) + q S_0 e^{-qT} N(d_1)"
            )
            st.latex(r"\Theta_{\text{put}} = -\frac{S_0 e^{-qT}\varphi(d_1)\sigma}{2\sqrt{T}} + rK e^{-rT} N(-d_2) - q S_0 e^{-qT} N(-d_1)")
            st.latex(r"d_2 = d_1 - \sigma\sqrt{T}")

    # ν (Vega)
    with cols[3]:
        st.markdown(
            "<div style='background:#FF8C00;color:#fff;padding:12px;border-radius:10px;text-align:center;font-weight:700;'>"
            "ν<br><small style='font-weight:400;'>Volatilité</small></div>",
            unsafe_allow_html=True
        )
        with st.popover("Formule"):
            st.latex(r"\text{Vega} = S_0 e^{-qT} \sqrt{T}\,\varphi(d_1)")
            st.caption("Identique pour call et put.")

    # ρ
    with cols[4]:
        st.markdown(
            "<div style='background:#4169E1;color:#fff;padding:12px;border-radius:10px;text-align:center;font-weight:700;'>"
            "ρ<br><small style='font-weight:400;'>Taux sans risque</small></div>",
            unsafe_allow_html=True
        )
        with st.popover("Formule"):
            st.latex(r"\rho_{\text{call}} = K T e^{-rT} N(d_2)")
            st.latex(r"\rho_{\text{put}}  = -K T e^{-rT} N(-d_2)")

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Paramètres =====
    st.markdown("<div class='info-card'><div class='section-title'>⚙️ Paramètres des Options</div>", unsafe_allow_html=True)
    param_cols = st.columns(3, gap="large")
    with param_cols[0]:
        st.markdown("**Paramètres de Base :**")
        st.write("- **Sous-jacent (S)** : Prix actuel de l'actif")
        st.write("- **Strike (K)** : Prix d'exercice")
        st.write("- **Maturité (T)** : Temps jusqu'à l'échéance")
    with param_cols[1]:
        st.markdown("**Paramètres de Marché :**")
        st.write("- **Taux (r)** : Sans risque")
        st.write("- **Volatilité (σ)** : Du sous-jacent")
        st.write("- **Dividende (q)** : Taux de dividende")
    with param_cols[2]:
        st.markdown("**Types d'Options :**")
        st.write("- **Call** : Droit d'acheter")
        st.write("- **Put** : Droit de vendre")
        st.write("- **Européenne** : Exercice à l'échéance")
        st.write("- **Américaine** : Exercice à tout moment")
    st.markdown("</div>", unsafe_allow_html=True)

def show_pricing_page():
    """Pricing en 2 colonnes (Paramètres actifs | Marché d'entrée) + résultats en dessous"""
    st.markdown("""
    <div class="header-box" style="margin-bottom:1rem">
      <h1 style="margin:0; font-size:2.2rem">💰 Option Pricing</h1>
      <p style="margin:0; opacity:.9">Black–Scholes • Binomial • Trinomial</p>
    </div>
    """, unsafe_allow_html=True)

    # ====== 2 COLONNES HORIZONTALES : PARAMÈTRES ======
    colA, colB = st.columns(2, gap="large")

    # ---- Colonne A : Paramètres actifs (modèle) ----
    with colA:
        st.markdown("<div class='model-card'><div class='section-title'>⚙️ Paramètres actifs</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            model_type = st.selectbox("Modèle", ["Black-Scholes", "Binomial", "Trinomial"])
        with c2:
            option_type = st.radio("Type", ["Call", "Put"], horizontal=True)
        if model_type == "Black-Scholes":
            option_style = "Européenne"
            steps = 200
            st.caption("Style fixé : Européenne (BS)")
        else:
            c3, c4 = st.columns(2)
            with c3:
                option_style = st.selectbox("Style", ["Européenne", "Américaine"])
            with c4:
                steps = st.slider("Étapes (N)", 20, 800, 200, step=20)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Colonne B : Marché d'entrée ----
    with colB:
        st.markdown("<div class='parameter-card'><div class='section-title'>📈 Marché d'entrée</div>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            S = st.number_input("Sous-jacent S", min_value=0.01, value=100.0, step=1.0)
        with b2:
            K = st.number_input("Strike K", min_value=0.01, value=100.0, step=1.0)
        with b3:
            T = st.number_input("Maturité T", min_value=0.01, value=1.0, step=0.1)

        b4, b5, b6 = st.columns(3)
        with b4:
            r = st.number_input("Taux r (%)", min_value=0.0, value=5.0, step=0.1)
        with b5:
            sigma = st.number_input("Volatilité σ (%)", min_value=0.1, value=20.0, step=0.5)
        with b6:
            q = st.number_input("Dividende q (%)", min_value=0.0, value=0.0, step=0.1)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Bouton d'action centré ----
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    calc_col = st.columns([1, 1, 1])[1]
    with calc_col:
        run = st.button("🚀 Calculer", use_container_width=True, type="primary")

    # ========= CALCUL & PERSISTENCE =========
    if run:
        r_dec, sigma_dec, q_dec = r/100.0, sigma/100.0, q/100.0
        if model_type == "Black-Scholes":
            price, greeks = black_scholes(S, K, T, r_dec, sigma_dec, option_type.lower(), q_dec)
            model_used = "Black-Scholes"
        elif model_type == "Binomial":
            price = binomial_tree(S, K, T, r_dec, sigma_dec, steps, option_type.lower(), option_style.lower(), q_dec)
            greeks = calculate_greeks(S, K, T, r_dec, sigma_dec, option_type.lower(), "Binomial", steps, q_dec)
            model_used = f"Binomial (N={steps})"
        else:
            price = trinomial_tree(S, K, T, r_dec, sigma_dec, steps, option_type.lower(), option_style.lower(), q_dec)
            greeks = calculate_greeks(S, K, T, r_dec, sigma_dec, option_type.lower(), "Trinomial", steps, q_dec)
            model_used = f"Trinomial (N={steps})"

        st.session_state["pricing_done"] = True
        st.session_state["pricing_payload"] = dict(
            model_type=model_type, option_style=option_style, option_type=option_type,
            S=S, K=K, T=T, r_dec=r_dec, sigma_dec=sigma_dec, q_dec=q_dec,
            steps=steps if model_type != "Black-Scholes" else 200,
            price=float(price), greeks={k: float(v) for k, v in greeks.items()},
            model_used=model_used,
        )

    # ========= AFFICHAGE (réutilise la session si besoin) =========
    show_results = run or st.session_state.get("pricing_done", False)
    if show_results:
        if not run:
            P = st.session_state["pricing_payload"]
            model_type   = P["model_type"]
            option_style = P["option_style"]
            option_type  = P["option_type"]
            S, K, T      = P["S"], P["K"], P["T"]
            r_dec, sigma_dec, q_dec = P["r_dec"], P["sigma_dec"], P["q_dec"]
            steps        = P["steps"]
            price        = P["price"]
            greeks       = P["greeks"]
            model_used   = P["model_used"]

        # ---- Carte résultat
        st.markdown(f"""
        <div class="result-card" style="padding:1.2rem; margin-top:.5rem">
          <div style="font-weight:800; font-size:1rem; opacity:.95">Résultat</div>
          <div style="display:flex; align-items:end; gap:1rem">
            <div style="font-size:3rem; font-weight:900">{price:.6f}</div>
            <div style="opacity:.9">• {model_used} • {option_style}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ---- Grecques
        g1, g2, g3, g4, g5 = st.columns(5)
        chips = [
            ("Δ Delta", greeks["delta"]),
            ("Γ Gamma", greeks["gamma"]),
            ("Θ Theta (j)", greeks["theta"]),
            ("ν Vega (1%)", greeks["vega"]),
            ("ρ Rho (1%)", greeks["rho"]),
        ]
        for col, (lab, val) in zip([g1, g2, g3, g4, g5], chips):
            with col:
                st.markdown(
                    f"<div class='greek-card' style='text-align:center'>"
                    f"<div style='font-weight:800'>{lab}</div>"
                    f"<div class='metric-value'>{val:.6f}</div>"
                    f"</div>", unsafe_allow_html=True
                )

        # ---- P&L Scénarios (Δ, Γ, Vega) — UNIQUEMENT BS
        if model_type == "Black-Scholes":
            st.markdown("### 📊 P&L Scénarios")

            # Cas "une seule option/unité" :
            qty, mult = 1, 1
            ESP = greeks["delta"] * S * qty * mult
            dollar_gamma = 0.5 * (greeks["gamma"] * qty * mult) * (S ** 2)
            vega_per_pt = greeks["vega"] * qty * mult  # vega déjà par 1% dans ta fonction

            c1x, c2x, c3x = st.columns(3)
            c1x.metric("ESP (Dollar-Δ)", f"{ESP:,.0f} $")
            c2x.metric("$-Gamma (½·Γ·S²)", f"{dollar_gamma:,.0f} $")
            c3x.metric("Vega / pt de vol", f"{vega_per_pt:,.0f} $")

            with st.form("scenarios_bs"):
                st.caption("Formule : P&L ≈ ESP×Return + $-Gamma×Return² + Vega×Δσ")
                cc1, cc2 = st.columns(2)
                u_stress_str = cc1.text_input("Stress sous-jacent (%)", "-20,-10,-5,-2,-1,0,1,2,5,10,20")
                vol_stress_str = cc2.text_input("Stress volatilité (points de vol)", "-10,-5,-2,-1,0,1,2,5,10")
                submit_scenarios = st.form_submit_button("Calculer le tableau")

            if submit_scenarios:
                try:
                    u_stress = [float(x.strip()) for x in u_stress_str.split(",") if x.strip()]
                    vol_stress = [float(x.strip()) for x in vol_stress_str.split(",") if x.strip()]
                except Exception:
                    st.error("Vérifie les listes de stress : nombres séparés par des virgules.")
                    st.stop()

                R = np.array(u_stress) / 100.0
                dSigma_pts = np.array(vol_stress)

                pnls = np.zeros((len(R), len(dSigma_pts)))
                for i, r_ in enumerate(R):
                    for j, ds_pt in enumerate(dSigma_pts):
                        pnls[i, j] = ESP * r_ + dollar_gamma * (r_ ** 2) + vega_per_pt * ds_pt

                df = pd.DataFrame(
                    pnls,
                    index=[f"{u:+g}%" for u in u_stress],
                    columns=[f"{v:+g} pts" for v in vol_stress]
                )
                df.index.name = "Underlying Stress"
                df.columns.name = "Vol Stress"

                df_pivot = df.copy()
                df_pivot["Row Total"] = df.sum(axis=1)
                totals_row = pd.DataFrame([list(df.sum(axis=0)) + [df.values.sum()]],
                                          index=["Grand Total"], columns=df_pivot.columns)
                df_pivot = pd.concat([df_pivot, totals_row])

                styled = df_pivot.style.format("{:,.0f}") \
                    .background_gradient(cmap="RdYlGn", axis=None) \
                    .set_properties(**{"text-align": "right"}) \
                    .set_table_styles([{ "selector": "th.col_heading, th.row_heading",
                                         "props": "text-align: center; font-weight: 600;" }])
                st.dataframe(styled, use_container_width=True)

                cdl, xdl = st.columns(2)
                cdl.download_button("⬇️ CSV", df_pivot.round(0).to_csv().encode("utf-8"),
                                    file_name="scenario_pivot.csv", mime="text/csv")

                excel_buf = io.BytesIO()
                with pd.ExcelWriter(excel_buf, engine="xlsxwriter") as writer:
                    df_pivot.round(0).to_excel(writer, sheet_name="Scenario Pivot")
                    ws = writer.sheets["Scenario Pivot"]
                    numf = writer.book.add_format({"num_format": "#,##0", "align": "right"})
                    nrows, ncols = df_pivot.shape
                    ws.set_column(1, ncols, 14, numf)
                    ws.conditional_format(1, 1, nrows, ncols-1, {
                        "type": "3_color_scale",
                        "min_color": "#F4CCCC", "mid_color": "#FFFFFF", "max_color": "#D9EAD3"
                    })
                excel_buf.seek(0)
                xdl.download_button("⬇️ Excel", excel_buf.getvalue(),
                                    file_name="scenario_pivot.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # ---- Sensibilité (reste visible grâce à la persistance)
        with st.expander("🎯 Sensibilité (un paramètre)"):
            target = st.selectbox("Paramètre", ["S", "K", "T", "r", "sigma"], index=0, key="sensib_target")
            grid = {
                "S": np.linspace(max(1, S*0.6), S*1.4, 80),
                "K": np.linspace(max(1, K*0.6), K*1.4, 80),
                "T": np.linspace(0.05, T*2, 80),
                "r": np.linspace(0.0, max(0.0001, r_dec*2), 80),
                "sigma": np.linspace(0.01, max(0.02, sigma_dec*2), 80)
            }[target]

            vals = []
            if model_type == "Black-Scholes":
                for x in grid:
                    args = dict(S=S, K=K, T=T, r=r_dec, sigma=sigma_dec, option_type=option_type.lower(), dividend=q_dec)
                    args[{"S":"S","K":"K","T":"T","r":"r","sigma":"sigma"}[target]] = x
                    v, _ = black_scholes(**args)
                    vals.append(v)
            else:
                engine = binomial_tree if model_type == "Binomial" else trinomial_tree
                for x in grid:
                    args = dict(S=S, K=K, T=T, r=r_dec, sigma=sigma_dec, n=steps,
                                option_type=option_type.lower(), option_style=option_style.lower(), dividend=q_dec)
                    if target == "S": args["S"] = x
                    elif target == "K": args["K"] = x
                    elif target == "T": args["T"] = x
                    elif target == "r": args["r"] = x
                    elif target == "sigma": args["sigma"] = x
                    vals.append(engine(**args))

            fig = px.line(x=grid, y=vals, labels={"x": target, "y": "Prix"}, title=f"Sensibilité — {target}")
            fig.add_vline(x={"S": S, "K": K, "T": T, "r": r_dec, "sigma": sigma_dec}[target], line_dash="dash")
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Renseignez les paramètres ci-dessus puis cliquez **Calculer**.")



def show_convergence_page():
    """Affiche la page d'analyse de convergence — paramètres en ligne, 2 graphes en colonnes, stats en dessous"""
    # En-tête
    st.markdown("""
    <div class="header-box">
        <h1 style="margin: 0; font-size: 2.5rem;">📈 Convergence Analysis</h1>
        <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">
            Analyse de la convergence des modèles Binomial et Trinomial
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # Paramètres (3 rangées horizontales)
    # =========================
    st.markdown("<div class='parameter-card'><div class='section-title'>⚙️ Paramètres de Convergence</div>", unsafe_allow_html=True)

    # Rangée 1 : S, K, T
    r1c1, r1c2, r1c3 = st.columns([1, 1, 1], gap="medium")
    with r1c1:
        S_conv = st.number_input(
            "Sous-jacent S", min_value=0.01, max_value=100000.0,
            value=100.0, step=1.0, key="conv_S"
        )
    with r1c2:
        K_conv = st.number_input(
            "Strike K", min_value=0.01, max_value=100000.0,
            value=100.0, step=1.0, key="conv_K"
        )
    with r1c3:
        T_conv = st.number_input(
            "Maturité T (années)", min_value=0.01, max_value=50.0,
            value=1.0, step=0.1, key="conv_T"
        )

    # Rangée 2 : r (%), sigma (%), q (%)
    r2c1, r2c2, r2c3 = st.columns([1, 1, 1], gap="medium")
    with r2c1:
        r_conv = st.number_input(
            "Taux r (%)", min_value=0.0, max_value=100.0,
            value=5.0, step=0.1, key="conv_r"
        )
    with r2c2:
        sigma_conv = st.number_input(
            "Volatilité σ (%)", min_value=0.01, max_value=300.0,
            value=20.0, step=0.5, key="conv_sigma"
        )
    with r2c3:
        q_conv = st.number_input(
            "Dividende q (%)", min_value=0.0, max_value=50.0,
            value=0.0, step=0.1, key="conv_q"
        )

    # Rangée 3 : Type, N max, Bouton
    r3c1, r3c2, r3c3 = st.columns([1, 1, 1], gap="medium")
    with r3c1:
        option_type_conv = st.radio(
            "Type d'option", ["Call", "Put"], horizontal=True, key="conv_option_type"
        )
    with r3c2:
        max_steps = st.slider(
            "N max (étapes)", min_value=10, max_value=1000,
            value=200, step=10, help="Nombre maximum d'étapes pour l'analyse"
        )
    with r3c3:
        st.markdown("<div style='height:1.55rem'></div>", unsafe_allow_html=True)  # espace au-dessus du bouton
        analyze_btn = st.button("🔍 Analyser la Convergence", use_container_width=True, type="primary")

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # Calcul + Graphes (2 colonnes)
    # =========================
    if analyze_btn or 'convergence_data' in st.session_state:
        # Conversions en décimal
        r_dec = r_conv / 100.0
        sigma_dec = sigma_conv / 100.0
        q_dec = q_conv / 100.0

        # Black–Scholes de référence
        bs_price, _ = black_scholes(
            S_conv, K_conv, T_conv, r_dec, sigma_dec, option_type_conv.lower(), q_dec
        )

        # N = 1..max_steps
        step_sizes = list(range(1, max_steps + 1))
        binomial_prices, trinomial_prices = [], []
        binomial_errors, trinomial_errors = [], []

        for steps in step_sizes:
            bin_price = binomial_tree(
                S_conv, K_conv, T_conv, r_dec, sigma_dec,
                steps, option_type_conv.lower(), 'european', q_dec
            )
            tri_price = trinomial_tree(
                S_conv, K_conv, T_conv, r_dec, sigma_dec,
                steps, option_type_conv.lower(), 'european', q_dec
            )
            binomial_prices.append(bin_price)
            trinomial_prices.append(tri_price)
            binomial_errors.append(abs(bin_price - bs_price))
            trinomial_errors.append(abs(tri_price - bs_price))

        # (optionnel) Sauvegarde pour export
        st.session_state["last_convergence"] = {
            "N": step_sizes,
            "crr": binomial_prices,
            "tri": trinomial_prices,
            "bs": float(bs_price)
        }

        # Deux colonnes : Prix | Erreur
        g_left, g_right = st.columns(2, gap="large")

        # Graphique de convergence des prix
        with g_left:
            st.markdown("<div class='convergence-plot'>", unsafe_allow_html=True)
            st.subheader("Convergence des Prix")
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=step_sizes, y=binomial_prices, mode='lines', name='Binomial'))
            fig1.add_trace(go.Scatter(x=step_sizes, y=trinomial_prices, mode='lines', name='Trinomial'))
            fig1.add_hline(y=bs_price, line_dash="dash", line_color="blue", annotation_text="Black-Scholes")
            fig1.update_layout(
                title="Convergence des modèles d'arbres vers Black-Scholes",
                xaxis_title="Nombre d'étapes",
                yaxis_title="Prix de l'option",
                template="plotly_white"
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Graphique des erreurs (log)
        with g_right:
            st.markdown("<div class='convergence-plot'>", unsafe_allow_html=True)
            st.subheader("Erreur de Convergence")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=step_sizes, y=binomial_errors, mode='lines', name='Binomial'))
            fig2.add_trace(go.Scatter(x=step_sizes, y=trinomial_errors, mode='lines', name='Trinomial'))
            fig2.update_layout(
                title="Erreur absolue par rapport à Black-Scholes",
                xaxis_title="Nombre d'étapes",
                yaxis_title="Erreur absolue",
                template="plotly_white",
                yaxis_type="log"
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # Statistiques (ligne en dessous)
        # =========================


        st.markdown("<div class='parameter-card'><div class='section-title'>📊 Statistiques de Convergence", unsafe_allow_html=True)


        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            st.metric("Prix Black-Scholes", f"{bs_price:.4f}")
        with c2:
            last_bin_error = binomial_errors[-1] if binomial_errors else 0.0
            st.metric("Erreur Binomiale Finale", f"{last_bin_error:.6f}")
        with c3:
            last_tri_error = trinomial_errors[-1] if trinomial_errors else 0.0
            st.metric("Erreur Trinomiale Finale", f"{last_tri_error:.6f}")

        # Taux de convergence (inchangé)
        if len(binomial_errors) > 1 and len(trinomial_errors) > 1:
            bin_convergence_rate = binomial_errors[-2] / binomial_errors[-1] if binomial_errors[-1] != 0 else 0
            tri_convergence_rate = trinomial_errors[-2] / trinomial_errors[-1] if trinomial_errors[-1] != 0 else 0

            st.write(f"**Taux de convergence Binomial :** {bin_convergence_rate:.2f}")
            st.write(f"**Taux de convergence Trinomial :** {tri_convergence_rate:.2f}")

            if tri_convergence_rate > bin_convergence_rate:
                st.success("Le modèle trinomial converge plus rapidement que le modèle binomial")
            else:
                st.info("Le modèle binomial converge à un taux similaire ou meilleur")

        st.markdown("</div>", unsafe_allow_html=True)




# --- NAVIGATION "STYLE CARTE" CLAIRE (maryam) --------------------------------
# --- NAVIGATION "STYLE CARTE" CLAIRE (maryam) --------------------------------
def fancy_sidebar_nav_v2(
    title=("OPTION", "PRICING", "PRO"),
    colors=dict(
        primary="#800020",   # bordeaux
        accent="#DC143C",    # carmin
        bg="#FFFFFF",
        pill="#F3F4F6",
        text="#0F172A"
    )
):
    # ---------- STYLE ----------
    st.markdown(f"""
    <style>
      [data-testid="stSidebar"] > div:first-child {{
        position: relative; overflow: hidden;
        padding: 18px 14px 22px 14px; border-right: 1px solid #EEF2F7;
        background: linear-gradient(180deg, {colors["bg"]} 0%,
                   rgba(220,20,60,.05) 40%, rgba(128,0,32,.06) 100%);
      }}
      [data-testid="stSidebar"] > div:first-child::before {{
        content:""; position:absolute; inset:0;
        background: repeating-linear-gradient(135deg,
                    rgba(128,0,32,.03) 0 6px, rgba(128,0,32,0) 6px 12px);
        mix-blend-mode:multiply; pointer-events:none;
      }}
      [data-testid="stSidebar"] > div:first-child::after {{
        content:""; position:absolute; inset:-10% -20%;
        background:
          radial-gradient(420px 320px at 110% -10%, rgba(128,0,32,.15), transparent 60%),
          radial-gradient(380px 360px at -10% 20%, rgba(220,20,60,.14), transparent 60%),
          radial-gradient(300px 260px at 60% 120%, rgba(128,0,32,.12), transparent 60%);
        filter: blur(6px); pointer-events:none;
      }}

      .nav-hero {{
        background: rgba(255,255,255,.78); backdrop-filter: blur(6px);
        border:1px solid rgba(128,0,32,.18); border-radius:18px;
        padding:14px 16px; box-shadow:0 10px 24px rgba(16,24,40,.08);
        display:flex; align-items:center; gap:12px; margin-bottom:14px;
      }}
      .nav-hero .t1 {{ font-weight:900; letter-spacing:.6px; color:{colors["primary"]}; line-height:1; }}
      .nav-hero .t2 {{ font-weight:900; letter-spacing:.6px; color:{colors["accent"]}; line-height:1; }}
      .nav-hero .t3 {{ font-weight:800; color:#64748B; font-size:.85rem; letter-spacing:.4px; }}

      .nav-menu {{ background: rgba(255,255,255,.86); backdrop-filter: blur(6px);
                   border:1px solid rgba(128,0,32,.16); border-radius:16px; padding:10px; }}
      .nav-menu .stRadio > div {{ display:flex; flex-direction:column; gap:10px; }}
      .nav-menu label {{
        background:{colors["pill"]}; border:1px solid #E5E7EB; border-radius:16px;
        padding:12px 14px; color:{colors["text"]}; font-weight:800; width:100%;
        box-shadow:0 2px 0 rgba(15,23,42,.03) inset;
        display:flex; align-items:center; gap:.65rem;
        transition: all .15s ease;
      }}
      .nav-menu label:hover {{ border-color:{colors["primary"]}77; transform: translateY(-1px); }}

      .nav-menu input:checked + div {{
        background: linear-gradient(135deg, rgba(128,0,32,.13), rgba(220,20,60,.11));
        border-color:{colors["primary"]}77;
      }}
      .nav-dot {{ width:8px; height:8px; border-radius:999px; background:transparent; }}
      .nav-menu input:checked + div .nav-dot {{ background:{colors["accent"]}; }}

      .nav-footer {{ margin-top:12px; text-align:center; font-size:.85rem; color:#64748B; }}
    </style>
    """, unsafe_allow_html=True)

    # ---------- EN-TÊTE ----------
    st.markdown(f"""
    <div class="nav-hero">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
        <rect x="3" y="2" width="18" height="20" rx="4" stroke="#1E293B" stroke-width="1.6"/>
        <rect x="7" y="5" width="10" height="3" rx="1.2" fill="#1E293B"/>
        <rect x="7" y="10" width="3" height="3" rx="0.8" fill="#2563EB"/>
        <rect x="11" y="10" width="3" height="3" rx="0.8" fill="#10B981"/>
        <rect x="15" y="10" width="3" height="3" rx="0.8" fill="#F59E0B"/>
        <rect x="7" y="14" width="3" height="3" rx="0.8" fill="#EF4444"/>
        <rect x="11" y="14" width="7" height="3" rx="0.8" fill="#94A3B8"/>
      </svg>
      <div>
        <div class="t1">{title[0]}</div>
        <div class="t2">{title[1]}</div>
        <div class="t3">{title[2]}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- NAV ----------
    st.markdown('<div class="nav-menu">', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["🏠 Home", "💰 Pricing", "📈 Convergence"],
        label_visibility="collapsed",
        key="nav_palette_vertical"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- FOOTER ----------

    return page



def main():
    with st.sidebar:
        page = fancy_sidebar_nav_v2(
            title=("OPTION", "PRICE", "CALCULATOR"),
            colors=dict(
                primary="#800020",
                accent="#DC143C",
                bg="#FFFFFF",
                pill="#F3F4F6",
                text="#0F172A"
            )
        )

    if page == "🏠 Home":
        show_home_page()
    elif page == "💰 Pricing":
        show_pricing_page()
    elif page == "📈 Convergence":
        show_convergence_page()




if __name__ == "__main__":
    main()