import math
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Valuador de Derivados Financieros",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Calculadora de Valuación de Opciones")
st.markdown(
    "Valuación de Opciones Financieras mediante el **Modelo Binomial de Cox-Ross-Rubinstein**."
)

# ==========================================
# BARRA LATERAL: PARÁMETROS DE ENTRADA
# ==========================================
st.sidebar.header("⚙️ Parámetros del Modelo")

nombre = st.sidebar.text_input("Tu Nombre", value="Inversionista")
st.sidebar.markdown(f"**¡Bienvenid@, {nombre}!** 👋")

tipo_opcion = st.sidebar.selectbox(
    "Selecciona el Tipo de Opción",
    [
        "1. Call Europea",
        "2. Put Europea",
        "3. Call Americana",
        "4. Put Americana",
        "5. Lookback Call (Floating Strike)",
        "6. Opción Asiática (Promedio aritmético)",
        "7. Call Up and Out",
    ],
)

st.sidebar.subheader("Valores del Activo y Mercado")
S0 = st.sidebar.number_input(
    "Precio Inicial del Activo ($S_0$)", value=100.0, step=1.0, min_value=0.01
)
K = st.sidebar.number_input(
    "Precio de Ejercicio ($K$)", value=100.0, step=1.0, min_value=0.00
)

B = None
rebate = 0.0
if "Up and Out" in tipo_opcion:
    B = st.sidebar.number_input(
        "Barrera ($B$)", value=120.0, step=1.0, min_value=0.01
    )
    rebate = st.sidebar.number_input(
        "Rebate", value=0.0, step=1.0, min_value=0.00
    )

r = st.sidebar.number_input(
    "Tasa Libre de Riesgo Anual ($r$)",
    value=0.05,
    step=0.01,
    format="%.4f",
)
dt = st.sidebar.number_input(
    "Paso de Tiempo en Años ($\Delta t$)",
    value=1.0,
    step=0.1,
    format="%.2f",
    min_value=0.01,
)
N = st.sidebar.slider("Número de Periodos ($N$)", min_value=1, max_value=10, value=3)

# Selección de parámetros u y d o Volatilidad sigma
usar_sigma = st.sidebar.checkbox("Calcular u y d desde Volatilidad (σ)", value=False)

if usar_sigma:
    sigma = st.sidebar.number_input(
        "Volatilidad Anual (σ)", value=0.20, step=0.01, format="%.2f"
    )
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    st.sidebar.info(f"**u calculado:** {u:.4f} | **d calculado:** {d:.4f}")
else:
    u = st.sidebar.number_input(
        "Factor de Subida ($u$)", value=1.10, step=0.01, format="%.4f"
    )
    d = st.sidebar.number_input(
        "Factor de Bajada ($d$)", value=0.90, step=0.01, format="%.4f"
    )

# ==========================================
# CÁLCULOS Y LÓGICA DE VALUACIÓN
# ==========================================
R = math.exp(r * dt)

if not (d < R < u):
    st.error(
        f"⚠️ **Error de Arbitraje:** No se cumple la condición $d < e^{{r \Delta t}} < u$ "
        f"({d:.4f} < {R:.4f} < {u:.4f}). Ajusta los factores $u$, $d$ o la tasa $r$."
    )
    st.stop()

p = (R - d) / (u - d)
q = 1 - p


def calcular_opcion(tipo, S0, K, u, d, R, p, q, N, B=None, rebate=0.0):
    """Calcula la matriz/árbol de precios del activo y valores de la opción."""
    # Matriz del subyacente: S[paso][i]
    S = [[0.0] * (i + 1) for i in range(N + 1)]
    for paso in range(N + 1):
        for i in range(paso + 1):
            S[paso][i] = S0 * (u ** (paso - i)) * (d**i)

    # Matriz del valor del derivado: V[paso][i]
    V = [[0.0] * (i + 1) for i in range(N + 1)]

    # Condición terminal (vencimiento)
    for i in range(N + 1):
        if "Up and Out" in tipo:
            V[N][i] = rebate if S[N][i] >= B else max(S[N][i] - K, 0.0)
        elif "Call" in tipo and "Lookback" not in tipo:
            V[N][i] = max(S[N][i] - K, 0.0)
        elif "Put" in tipo:
            V[N][i] = max(K - S[N][i], 0.0)

    # Inducción hacia atrás
    if "Europea" in tipo:
        for paso in range(N - 1, -1, -1):
            for i in range(paso + 1):
                V[paso][i] = (p * V[paso + 1][i] + q * V[paso + 1][i + 1]) / R

    elif "Americana" in tipo:
        for paso in range(N - 1, -1, -1):
            for i in range(paso + 1):
                esperado = (p * V[paso + 1][i] + q * V[paso + 1][i + 1]) / R
                if "Call" in tipo:
                    ejercicio_temprano = max(S[paso][i] - K, 0.0)
                else:
                    ejercicio_temprano = max(K - S[paso][i], 0.0)
                V[paso][i] = max(esperado, ejercicio_temprano)

    elif "Up and Out" in tipo:
        for paso in range(N - 1, -1, -1):
            for i in range(paso + 1):
                if S[paso][i] >= B:
                    V[paso][i] = rebate
                else:
                    V[paso][i] = (p * V[paso + 1][i] + q * V[paso + 1][i + 1]) / R

    elif "Lookback" in tipo:
        # Algoritmo recursivo para Lookback basada en el PRECIO MÁXIMO histórico (S_max)
        memo = {}

        def evaluar_lookback(paso, S_act, S_max):
            # Condición terminal: el payoff es directamente el precio máximo alcanzado
            if paso == N:
                return S_max

            # Estado actual redondeado para la tabla de memoización
            estado = (paso, round(S_act, 5), round(S_max, 5))
            if estado in memo:
                return memo[estado]

            # Movimientos al alza y a la baja actualizando el máximo registrado
            v_up = evaluar_lookback(paso + 1, S_act * u, max(S_max, S_act * u))
            v_dn = evaluar_lookback(paso + 1, S_act * d, max(S_max, S_act * d))

            # Esperanza neutral al riesgo descontada un período
            val = (p * v_up + q * v_dn) / R
            memo[estado] = val
            return val

        # Evaluación en el período 0 partiendo de S0
        precio_lookback = evaluar_lookback(0, S0, S0)
        V[0][0] = precio_lookback

    elif "Asiática" in tipo:
        # Algoritmo recursivo para Asiática Call (Payoff: max(Promedio - K, 0))
        memo = {}

        def evaluar_asiatica(paso, S_act, suma_precios):
            if paso == N:
                promedio = (suma_precios + S_act) / (N + 1)
                return max(promedio - K, 0.0)
            estado = (paso, round(S_act, 5), round(suma_precios, 5))
            if estado in memo:
                return memo[estado]

            v_up = evaluar_asiatica(
                paso + 1, S_act * u, suma_precios + S_act
            )
            v_dn = evaluar_asiatica(
                paso + 1, S_act * d, suma_precios + S_act
            )
            val = (p * v_up + q * v_dn) / R
            memo[estado] = val
            return val

        V[0][0] = evaluar_asiatica(0, S0, 0.0)

    return S, V


S_tree, V_tree = calcular_opcion(tipo_opcion, S0, K, u, d, R, p, q, N, B, rebate)

# ==========================================
# FUNCIÓN PARA DIBUJAR EL ÁRBOL BINOMIAL
# ==========================================
def graficar_arbol(S, V, N, titulo):
    G = nx.DiGraph()
    pos = {}
    labels = {}

    for paso in range(N + 1):
        for i in range(paso + 1):
            node_id = f"{paso}_{i}"
            G.add_node(node_id)
            pos[node_id] = (paso, paso - 2 * i)
            labels[node_id] = f"S: {S[paso][i]:.2f}\nV: {V[paso][i]:.2f}"

            if paso < N:
                G.add_edge(node_id, f"{paso+1}_{i}")
                G.add_edge(node_id, f"{paso+1}_{i+1}")

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_color="#4A90E2", node_size=2500, ax=ax)
    nx.draw_networkx_edges(
        G, pos, edge_color="#888888", arrowstyle="->", arrowsize=15, ax=ax
    )
    nx.draw_networkx_labels(
        G, pos, labels=labels, font_color="white", font_size=8, font_weight="bold", ax=ax
    )

    plt.title(titulo, fontsize=14, fontweight="bold")
    plt.axis("off")
    st.pyplot(fig)


# ==========================================
# MOSTRAR RESULTADOS EN LA INTERFAZ
# ==========================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Factor R ($e^{r \Delta t}$)", f"{R:.4f}")
col2.metric("Probabilidad p (Subida)", f"{p:.4f}")
col3.metric("Probabilidad q (Bajada)", f"{q:.4f}")
col4.metric(
    f"Precio {tipo_opcion.split('.')[1]}",
    f"${V_tree[0][0]:.4f}",
)

st.markdown("---")
st.subheader("Visualización del Árbol Binomial")
st.caption(
    "En cada nodo se muestra: **S** = Precio del Activo Subyacente, **V** = Valor del Derivado."
)

graficar_arbol(S_tree, V_tree, N, f"Árbol Binomial - {tipo_opcion}")
