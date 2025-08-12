import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Carica il CSV FAOSTAT
df = pd.read_csv("FAOSTAT_data_en_8-10-2025.csv")

st.set_page_config(page_title="Gioco Export FAOSTAT", page_icon="🌾")

st.title("🌾 Gioco sugli esportatori - FAOSTAT")

# Selezione parametri
anni = sorted(df["Year"].unique(), reverse=True)
prodotti = sorted(df["Item"].unique())

anno = st.selectbox("Scegli anno", anni)
prodotto = st.selectbox("Scegli prodotto", prodotti)
num_paesi = st.radio("Quanti paesi per giocatore?", [3, 5])

# Inserimento partecipanti
n_partecipanti = st.number_input("Numero di partecipanti", min_value=1, step=1)
partecipanti = {}
for i in range(n_partecipanti):
    nome = st.text_input(f"Nome partecipante {i+1}")
    paesi = st.text_area(f"Elenca {num_paesi} paesi per {nome} (separati da virgola)").split(",")
    paesi = [p.strip() for p in paesi if p.strip()]
    if nome and len(paesi) == num_paesi:
        partecipanti[nome] = paesi

# Avvia gioco
if st.button("Calcola punteggi") and partecipanti:
    df_filtrato = df[
        (df["Item"] == prodotto) &
        (df["Year"] == anno) &
        (df["Element"].str.lower().str.contains("export"))
    ].dropna(subset=["Value"]).sort_values(by="Value", ascending=False)

    totale_mondiale = df_filtrato["Value"].sum()

    punteggi = {}
    for nome, paesi in partecipanti.items():
        totale = 0
        for paese in paesi:
            riga = df_filtrato[df_filtrato["Area"].str.lower() == paese.lower()]
            if not riga.empty:
                totale += riga["Value"].values[0]
        punteggi[nome] = totale

    # Classifica
    classifica = sorted(punteggi.items(), key=lambda x: x[1], reverse=True)
    st.subheader("🏆 Classifica")
    for pos, (nome, punti) in enumerate(classifica, start=1):
        st.write(f"{pos}. **{nome}** → {punti:,.0f} t ({punti/totale_mondiale*100:.2f}%)")

    # Top 5 reale
    top5 = df_filtrato.head(5).copy()
    top5["Percentuale"] = top5["Value"] / totale_mondiale * 100

    st.subheader("🌍 Top 5 reale")
    for _, row in top5.iterrows():
        st.write(f"{row['Area']}: {row['Value']:,.0f} t ({row['Percentuale']:.2f}%)")

    st.write(f"**Totale cumulato Top 5**: {top5['Value'].sum():,.0f} t ({top5['Percentuale'].sum():.2f}%)")

    # Grafico
    fig, ax = plt.subplots()
    ax.bar(top5["Area"], top5["Percentuale"])
    ax.set_ylabel("% sul totale mondiale")
    ax.set_title(f"Top 5 export {prodotto} ({anno})")
    plt.xticks(rotation=45)
    st.pyplot(fig)
