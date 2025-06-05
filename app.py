import streamlit as st
import random
import pandas as pd

vermelhos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
pretos = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
colunas = {
    1: set(range(1, 37, 3)),
    2: set(range(2, 37, 3)),
    3: set(range(3, 37, 3))
}
duzias = {
    1: set(range(1, 13)),
    2: set(range(13, 25)),
    3: set(range(25, 37))
}

st.set_page_config(page_title="Simulador de Roleta", layout="centered")
st.title("🎰 Simulador de Roleta - Apostas Reais")
st.caption("Desenvolvido para uso em celular 📱")

saldo_inicial = st.number_input("Saldo inicial (R$)", value=1000, step=50)
n_rodadas = st.slider("Número de rodadas", 10, 300, 100)

st.subheader("🎯 Selecione suas apostas")
col1, col2 = st.columns(2)
with col1:
    aposta_vermelho = st.checkbox("Vermelho")
    aposta_impar = st.checkbox("Ímpar")
    aposta_baixo = st.checkbox("1 a 18")
with col2:
    aposta_preto = st.checkbox("Preto")
    aposta_par = st.checkbox("Par")
    aposta_alto = st.checkbox("19 a 36")

duzia = st.selectbox("Dúzia", ["Nenhuma", "1ª (1–12)", "2ª (13–24)", "3ª (25–36)"])
coluna = st.selectbox("Coluna", ["Nenhuma", "1ª", "2ª", "3ª"])
numero_escolhido = st.multiselect("Escolha número(s) direto (0–36)", list(range(37)))
valor_aposta = st.number_input("Valor por aposta (R$)", value=10, step=5)

if st.button("🎲 Rodar Simulação"):
    saldo = saldo_inicial
    historico = []

    for i in range(n_rodadas):
        numero = random.randint(0, 36)
        ganho = 0
        perdeu = 0

        if aposta_vermelho and numero in vermelhos:
            ganho += valor_aposta
        elif aposta_vermelho:
            perdeu += valor_aposta

        if aposta_preto and numero in pretos:
            ganho += valor_aposta
        elif aposta_preto:
            perdeu += valor_aposta

        if aposta_impar and numero != 0 and numero % 2 == 1:
            ganho += valor_aposta
        elif aposta_impar:
            perdeu += valor_aposta

        if aposta_par and numero != 0 and numero % 2 == 0:
            ganho += valor_aposta
        elif aposta_par:
            perdeu += valor_aposta

        if aposta_baixo and 1 <= numero <= 18:
            ganho += valor_aposta
        elif aposta_baixo:
            perdeu += valor_aposta

        if aposta_alto and 19 <= numero <= 36:
            ganho += valor_aposta
        elif aposta_alto:
            perdeu += valor_aposta

        if duzia.startswith("1") and numero in duzias[1]:
            ganho += 2 * valor_aposta
        elif duzia.startswith("2") and numero in duzias[2]:
            ganho += 2 * valor_aposta
        elif duzia.startswith("3") and numero in duzias[3]:
            ganho += 2 * valor_aposta
        elif duzia != "Nenhuma":
            perdeu += valor_aposta

        if coluna.startswith("1") and numero in colunas[1]:
            ganho += 2 * valor_aposta
        elif coluna.startswith("2") and numero in colunas[2]:
            ganho += 2 * valor_aposta
        elif coluna.startswith("3") and numero in colunas[3]:
            ganho += 2 * valor_aposta
        elif coluna != "Nenhuma":
            perdeu += valor_aposta

        for n in numero_escolhido:
            if numero == n:
                ganho += 35 * valor_aposta
            else:
                perdeu += valor_aposta

        saldo += ganho - perdeu
        historico.append((i + 1, numero, saldo))

    df = pd.DataFrame(historico, columns=["Rodada", "Número", "Saldo"])
    st.line_chart(df.set_index("Rodada")["Saldo"], use_container_width=True)
    st.metric("💰 Saldo Final", f"R${saldo:.2f}")
    st.download_button("⬇️ Baixar resultados em CSV", data=df.to_csv(index=False), file_name="resultados_roleta.csv")
    st.dataframe(df.tail(10), use_container_width=True)
