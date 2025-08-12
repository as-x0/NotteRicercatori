import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Carica il CSV FAOSTAT
df = pd.read_csv("FAOSTAT_data_en_8-10-2025.csv")

st.set_page_config(page_title="Gioco Export FAOSTAT", page_icon="🌾")

st.title("🌾 Gioco sugli esportatori - FAOSTAT")

# --- Dizionario prodotti inglese -> italiano (espandi a piacere) ---
traduzioni_prodotti = {
    "Coffee, green": "Caffè",
    "Maize (corn)": "Mais",
    "Rice, paddy (rice milled equivalent)": "Riso",
    "Tomatoes": "Pomodori",
    "Soya beans": "Fagioli di soia",
    "Wheat": "Grano",
    "Cocoa beans": "Cacao",
    "Bananas": "Banane",
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
    "Afghanistan": "Afghanistan",
    "Albania": "Albania",
    "Algeria": "Algeria",
    "Angola": "Angola",
    "Antigua and Barbuda": "Antigua e Barbuda",
    "Argentina": "Argentina",
    "Armenia": "Armenia",
    "Australia": "Australia",
    "Austria": "Austria",
    "Azerbaijan": "Azerbaigian",
    "Bahamas": "Bahamas",
    "Bahrain": "Bahrein",
    "Bangladesh": "Bangladesh",
    "Barbados": "Barbados",
    "Belarus": "Bielorussia",
    "Belgium": "Belgio",
    "Belize": "Belize",
    "Benin": "Benin",
    "Bhutan": "Bhutan",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Bosnia and Herzegovina": "Bosnia-Erzegovina",
    "Botswana": "Botswana",
    "Brazil": "Brasile",
    "Brunei Darussalam": "Brunei",
    "Bulgaria": "Bulgaria",
    "Burkina Faso": "Burkina Faso",
    "Burundi": "Burundi",
    "Cabo Verde": "Capo Verde",
    "Cambodia": "Cambogia",
    "Cameroon": "Camerun",
    "Canada": "Canada",
    "Central African Republic": "Repubblica Centrafricana",
    "Chile": "Cile",
    "China": "Cina",
    "China, Hong Kong SAR": "Honk Kong",
    "China, Macao SAR": "Macao",
    "China, mainland": "",
    "China, Taiwan Province of": "Taiwan",
    "Colombia": "Colombia",
    "Comoros": "Comore",
    "Congo": "Congo",
    "Costa Rica": "Costa Rica",
    "Côte d'Ivoire": "Costa d'Avorio",
    "Croatia": "Croazia",
    "Cuba": "Cuba",
    "Cyprus": "Cipro",
    "Czechia": "Repubblica Ceca",
    "Democratic People's Republic of Korea": "Corea del Nord",
    "Democratic Republic of the Congo": "Repubblica Democratica del Congo",
    "Denmark": "Danimarca",
    "Djibouti": "Gibuti",
    "Dominica": "Dominica",
    "Dominican Republic": "Repubblica Dominicana",
    "Ecuador": "Ecuador",
    "Egypt": "Egitto",
    "El Salvador": "El Salvador",
    "Equatorial Guinea": "Guinea Equatoriale",
    "Eritrea": "Eritrea",
    "Estonia": "Estonia",
    "Eswatini": "Eswatini",
    "Ethiopia": "Etiopia",
    "Fiji": "Fiji",
    "Finland": "Finlandia",
    "France": "Francia",
    "French Polynesia": "Polinesia Francese",
    "Gabon": "Gabon",
    "Gambia": "Gambia",
    "Georgia": "Georgia",
    "Germany": "Germania",
    "Ghana": "Ghana",
    "Greece": "Grecia",
    "Grenada": "Grenada",
    "Guatemala": "Guatemala",
    "Guinea": "Guinea",
    "Guyana": "Guyana",
    "Haiti": "Haiti",
    "Honduras": "Honduras",
    "Hungary": "Ungheria",
    "Iceland": "Islanda",
    "India": "India",
    "Indonesia": "Indonesia",
    "Iran (Islamic Republic of)": "Iran",
    "Iraq": "Iraq",
    "Ireland": "Irlanda",
    "Israel": "Israele",
    "Italy": "Italia",
    "Jamaica": "Giamaica",
    "Japan": "Giapone",
    "Jordan": "Giordania",
    "Kazakhstan": "Kazakistan",
    "Kenya": "Kenya",
    "Kuwait": "Kuwait",
    "Kyrgyzstan": "Kirghizistan",
    "Lao People's Democratic Republic": "Lao",
    "Latvia": "Lettonia",
    "Lebanon": "Libano",
    "Lesotho": "Lesotho",
    "Liberia": "Liberia",
    "Libya": "Libia",
    "Lithuania": "Lituania",
    "Luxembourg": "Lussemburgo",
    "Madagascar": "Madagascar",
    "Malawi": "Malawi",
    "Malaysia": "Malaysia",
    "Mali": "Mali",
    "Malta": "Malta",
    "Mauritius": "Mauritius",
    "Mexico": "Messico",
    "Montenegro": "Montenegro",
    "Morocco": "Marocco",
    "Mozambique": "Mozambico",
    "Myanmar": "Myanmar",
    "Namibia": "Namibia",
    "Nepal": "Nepal",
    "Netherlands (Kingdom of the)": "Paesi Bassi",
    "New Caledonia": "Nuova Caledonia",
    "New Zealand": "Nuova Zelanda",
    "Nicaragua": "Nicaragua",
    "Niger": "Niger",
    "Nigeria": "Nigeria",
    "North Macedonia": "Macedonia del Nord",
    "Norway": "Norvegia",
    "Oman": "Oman",
    "Pakistan": "Pakistan",
    "Palestine": "Palestina",
    "Panama": "Panama",
    "Papua New Guinea": "Papua Nuova Guinea",
    "Paraguay": "Paraguay",
    "Peru": "Perù",
    "Philippines": "Filippine",
    "Poland": "Polonia",
    "Portugal": "Portogallo",
    "Qatar": "Qatar",
    "Republic of Korea": "Corea del Sud",
    "Republic of Moldova": "Moldavia",
    "Romania": "Romania",
    "Russian Federation": "Russia",
    "Rwanda": "Ruanda",
    "Saint Kitts and Nevis": "Saint Kitts and Nevis",
    "Saint Lucia": "Saint Lucia",
    "Saint Vincent and the Grenadines": "Saint Vincent e Grenadines",
    "Samoa": "Samoa",
    "Sao Tome and Principe": "Sao Tomé e Príncipe",
    "Saudi Arabia": "Arabia Saudita",
    "Senegal": "Senegal",
    "Serbia": "Serbia",
    "Seychelles": "Seychelles",
    "Sierra Leone": "Sierra Leone",
    "Singapore": "Singapore",
    "Slovakia": "Slovacchia",
    "Slovenia": "Slovenia",
    "Solomon Islands": "Isole Salomone",
    "South Africa": "Sudafrica",
    "South Sudan": "Sudan del Sud",
    "Spain": "Spagna",
    "Sri Lanka": "Sri Lanka",
    "Sudan": "Sudan",
    "Suriname": "Suriname",
    "Sweden": "Svezia",
    "Switzerland": "Svizzera",
    "Syrian Arab Republic": "Siria",
    "Tajikistan": "Tagikistan",
    "Thailand": "Thailandia",
    "Timor-Leste": "Timor Est",
    "Togo": "Togo",
    "Tonga": "Tonga",
    "Trinidad and Tobago": "Trinidad e Tobago",
    "Tunisia": "Tunisia",
    "Türkiye": "Turchia",
    "Turkmenistan": "Turkmenistan",
    "Uganda": "Uganda",
    "Ukraine": "Ucraina",
    "United Arab Emirates": "Emirati Arabi Uniti",
    "United Kingdom of Great Britain and Northern Ireland": "Regno Unito",
    "United Republic of Tanzania": "Tanzania",
    "United States of America": "Stati Uniti",
    "Uruguay": "Uruguay",
    "Uzbekistan": "Uzbekistan",
    "Vanuatu": "Vanuatu",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Viet Nam": "Vietnam",
    "Yemen": "Yemen",
    "Zambia": "Zambia",
    "Zimbabwe": "Zimbabwe",
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

