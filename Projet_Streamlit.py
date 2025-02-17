import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

st.set_page_config(page_title="Scraper App", layout="wide")

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Scraper en temps réel", "Télécharger les données", "Formulaire KoboToolbox", "Formulaire Google Forms"])

# Fonction de scraping
def scrape_shoes(pages, category):
    data = []
    base_url = "https://sn.coinafrique.com/categorie/chaussures-"
    url = base_url + ("homme" if category == "hommes" else "enfants")
    
    for page in range(1, pages + 1):
        res = requests.get(f"{url}?page={page}")
        soup = BeautifulSoup(res.text, "html.parser")
        containers = soup.find_all("div", class_="col s6 m4 l3")
        
        for container in containers:
            try:
                price = container.find("p", class_="ad__card-price").text.replace("CFA", "").strip()
                type_ = container.find("p", class_="ad__card-description").text.strip()
                location = container.find("p", class_="ad__card-location").span.text.strip()
                img_url = container.find("img", class_="ad__card-img")["src"]
                data.append({"Prix": price, "Type": type_, "Localisation": location, "Image": img_url})
            except:
                pass
    return pd.DataFrame(data)

if menu == "Scraper en temps réel":
    st.title("📌 Scraping en temps réel")
    pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=10, value=2)
    category = st.radio("Choisissez la catégorie :", ["hommes", "enfants"], horizontal=True)
    if st.button("Lancer le scraping"):
        with st.spinner("Scraping en cours..."):
            df = scrape_shoes(pages, category)
            st.success("Scraping terminé !")
            st.dataframe(df)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(f"📥 Télécharger les données ({category})", csv, f"scraped_data_{category}.csv", "text/csv")
            


elif menu == "Télécharger les données":
    st.title("📂 Télécharger un fichier CSV")
    category_download = st.radio("Télécharger les données pour :", ["hommes", "enfants"], horizontal=True)
    file_path = "data/chaussures_hommes_ws.csv" if category_download == "hommes" else "data/chaussures_enfants_ws.csv"
    
    if st.button("Afficher les données"):
        df_download = pd.read_csv(file_path)
        st.dataframe(df_download)
        csv_download = df_download.to_csv(index=False).encode('utf-8')
        st.download_button(f"📥 Télécharger les données ({category_download})", csv_download, file_path, "text/csv")


elif menu == "Formulaire KoboToolbox":
    st.title("📝 Formulaire KoboToolbox")
    st.markdown("[Remplir le formulaire KoboToolbox]")
    components.html(""" <iframe src="https://ee.kobotoolbox.org/x/KB1xDzPa" width="800" height="1100"></iframe>
    """,height=1100,width=800)

elif menu == "Formulaire Google Forms":
    st.title("📝 Formulaire Google Forms")
    st.markdown("[Remplir le formulaire Google Forms]")
    components.html(""" <iframe src="https://forms.gle/CJvrNLFWgyCJZTBg6" width="800" height="1100"></iframe>
    """,height=1100,width=800)
