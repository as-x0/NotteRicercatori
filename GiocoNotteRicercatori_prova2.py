import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Carica il CSV FAOSTAT
df = pd.read_csv("FAOSTAT_data_en_8-10-2025.csv")

st.set_page_config(page_title="Gioco Export FAOSTAT", page_icon="🌾")

st.title("🌾 Gioco sugli esportatori - FAOSTAT")

# --- Dizionario prodotti inglese -> italiano (espandi a piacere) ---
traduzioni_prodotti = {
    "Soya beans": "Fagioli di soia",
    "Corn": "Mais",
    "Wheat": "Grano",
    # aggiungi qui i prodotti che vuoi tradurre
}

# Lista prodotti originali
prodotti_inglese = sorted(df["Item"].unique())

# Lista prodotti tradotti (se non c'è traduzione, lascia inglese)
prodotti_italiano = [traduzioni_prodotti.get(p, p) for p in prodotti_inglese]

# Seleziona anno
anni = sorted(df["Year"].unique(), reverse=True)
anno = st.selectbox("Scegli anno", anni)

# Seleziona prodotto in italiano
prodotto_italiano = st.selectbox("Scegli prodotto", prodotti_italiano)

# Trova il prodotto inglese corrispondente
indice_prodotto = prodotti_italiano.index(prodotto_italiano)
prodotto = prodotti_inglese[indice_prodotto]

num_paesi = st.radio("Quanti paesi per giocatore?", [3, 5])

# --- Lista Paesi in italiano e mappa a inglese ---
# Ricava lista Paesi unici dal df (inglese)
paesi_inglese = sorted(df["Area"].unique())

# Mappa Paesi inglese -> italiano (esempio, espandi a piacere)
mappa_paesi = {
    "Italy": "Italia",
    "France": "Francia",
    "Germany": "Germania",
    "Spain": "Spagna",
    # aggiungi tutti i paesi necessari qui
}

# Inversa: italiano -> inglese
mappa_paesi_inv = {v: k for k, v in mappa_paesi.items()}

# Lista Paesi in italiano da mostrare (prendi quelli in mappa, altrimenti lascia inglese)
paesi_italiano = [mappa_paesi.get(p, p) for p in paesi_inglese]

# Inserimento partecipanti
n_partecipanti = st.number_input("Numero di partecipanti", min_value=1, step=1)
partecipanti = {}

for i in range(n_partecipanti):
    nome = st.text_input(f"Nome partecipante {i+1}")
    # Usa multiselect per scegliere i paesi in italiano con autocomplete integrato
    paesi_scelti_italiano = st.multiselect(
        f"Scegli {num_paesi} paesi per {nome}", paesi_italiano, key=f"paesi_{i}"
    )
    if nome and len(paesi_scelti_italiano) == num_paesi:
        # Converti i paesi scelti in inglese per il filtro
        paesi_scelti_inglese = []
        for p in paesi_scelti_italiano:
            p_en = mappa_paesi_inv.get(p, p)  # se non in mappa, usa nome così com'è
            paesi_scelti_inglese.append(p_en)
        partecipanti[nome] = paesi_scelti_inglese

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
        # Se possibile mostra nome paese in italiano
        paese_it = mappa_paesi.get(row["Area"], row["Area"])
        st.write(f"{paese_it}: {row['Value']:,.0f} t ({row['Percentuale']:.2f}%)")

    st.write(f"**Totale cumulato Top 5**: {top5['Value'].sum():,.0f} t ({top5['Percentuale'].sum():.2f}%)")

    # Grafico
    fig, ax = plt.subplots()
    top5_paesi_it = [mappa_paesi.get(p, p) for p in top5["Area"]]
    ax.bar(top5_paesi_it, top5["Percentuale"])
    ax.set_ylabel("% sul totale mondiale")
    ax.set_title(f"Top 5 export {prodotto_italiano} ({anno})")
    plt.xticks(rotation=45)
    st.pyplot(fig)
