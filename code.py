import streamlit as st
import yfinance as yf
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import base64

from streamlit.components.v1 import html

# Configuration de la page
st.set_page_config(
    page_title="FinFlation - Simulation d'investissement",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"  # ← ça va la masquer au démarrage
)


# Style CSS personnalisé
st.markdown("""
    <style>
    /* Suppression de la barre blanche par défaut */
    header {
        background-color: #1a237e !important;
        border-bottom: none !important;
    }
    
    /* Style principal bleu foncé */
    .main {
        background-color: #1a237e;
    }
    
    /* Tous les textes en blanc */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: white !important;
    }
    
    /* Sidebar bleu plus clair */
    [data-testid=stSidebar] {
        background-color: #3949ab !important;
    }
    
    /* En-tête personnalisé */
    .custom-header {
        background-color: #1a237e;
        padding: 1rem 0;
        margin: -1rem 0 1rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 2px solid #4CAF50;
    }
    
    /* Logo et titre */
    .logo-title {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    /* Boutons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
    }
    
    /* Slider */
    .stSlider>div>div>div>div {
        background-color: #4CAF50;
    }
    
    /* Tableaux */
    table {
        color: white !important;
    }
    
    /* Boîtes de résultats */
    .result-box {
        background-color: #283593;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        border-left: 5px solid #4CAF50;
    }
    
    /* Correction des titres des graphiques Plotly */
    .gtitle {
        color: white !important;
        font-size: 16px !important;
    }
    
    /* Style du disclaimer */
    .disclaimer-box {
        background-color: #d32f2f;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 14px;
    }
    /* Centrer le titre Menu dans la sidebar */
    [data-testid="stSidebar"] h1 {
        text-align: center !important;
    }
    /* Centrer le titre Menu dans la sidebar */
    [data-testid="stSidebar"] h1 {
        text-align: center !important;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Boîtes de résultats */
    .result-box {
        background-color: #283593;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        border-left: 5px solid #4CAF50;
    }

    /* Boîte pour les résultats financiers */
    .financial-box {
        background-color: #283593;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        border-left: 5px solid #4CAF50;
        font-size: 18px;
        color: white;
    }
    /* Boîte pour les taux */
    .rate-box {
        background-color: #283593;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        border-left: 5px solid #4CAF50;
        font-size: 18px;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)



# En-tête personnalisé avec logo
st.markdown(f"""
    <div class="custom-header">
        <div class="logo-title">
            <img src="data:image/png;base64,{base64.b64encode(open('logo.png', 'rb').read()).decode()}" 
                 alt="Logo FinFlation" width="80">
            <div>
                <h1 style="margin:0; font-size:2.5rem;">FinFlation</h1>
                <p style="margin:0; font-size:1.2rem;">Optimisez vos investissements face à l'inflation</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Initialisation du state
if "page" not in st.session_state:
    st.session_state.page = "Accueil"


with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <h1 style="margin: 0; color: white;">Menu</h1>
            <img src="data:image/png;base64,{}" alt="Logo" width="40" style="margin-left: 10px;"/>
        </div>
        <hr style="border-top: 2px solid white; margin-top: 5px; margin-bottom: 20px;">
    """.format(base64.b64encode(open("logo.png", "rb").read()).decode()), unsafe_allow_html=True)

    # RADIO + changement de page sans double clic
    new_page = st.radio(
        "Navigation",
        ["Accueil", "Présentation", "Vocabulaire financier", "Comprendre les placements", "Testez vos connaissances fiancières", "Simulateur d'investissement"],
        index=["Accueil", "Présentation", "Vocabulaire financier", "Comprendre les placements", "Testez vos connaissances fiancières", "Simulateur d'investissement"].index(st.session_state.page)
    )

    if new_page != st.session_state.page:
        st.session_state.page = new_page
        st.experimental_rerun()


page = st.session_state.page




if page == "Accueil":
    st.markdown("""
        <style>
        /* Style général boutons */
        div.stButton > button {
            background-color: #42a5f5;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8em 1.5em;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
            width: 280px;
        }
        div.stButton > button:hover {
            background-color: #1e88e5;
            transform: scale(1.05);
        }
    
        /* Conteneur central */
        .centered-buttons {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2rem;
            max-width: 900px;
            margin: auto;
            padding-top: 30px;
        }
        
        /* Style rouge uniquement pour le bouton "simulateur_btn" */
        div[data-testid="stButton"][data-button-key="simulateur_btn"] > button {
            background-color: #e53935 !important;
        }
        div[data-testid="stButton"][data-button-key="simulateur_btn"] > button:hover {
            background-color: #c62828 !important;
        }
        </style>
    """, unsafe_allow_html=True)


    # Titre centré
    st.markdown("<h1 style='text-align: center; color: white;'>Bienvenue sur FinFlation</h1>", unsafe_allow_html=True)

    # Texte d’introduction centré
    

    # Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        ⚠ <strong>Disclaimer :</strong> Notre simulation est fournie à titre informatif uniquement et ne constitue pas 
        un conseil en investissement. Les résultats sont basés sur des hypothèses et des données historiques qui ne 
        garantissent pas les performances futures. Consultez un conseiller financier avant toute décision d'investissement.
    </div>
    """, unsafe_allow_html=True)
    
    # Fonction pour convertir une image en base64
    def img_to_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    # Charger les images
    img1 = img_to_base64("livret.png")
    img2 = img_to_base64("capbourse.png")
    img3 = img_to_base64("fin.png")
    img4 = img_to_base64("graphe.png")
    img5 = img_to_base64("etf.png")
    
    # Deux colonnes : texte à gauche, carrousel à droite
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="background-color: #283593; padding: 27px; border-radius: 15px; color: white; width: 90%;">
            <h2 style="color: #4CAF50;">Contexte économique</h2>
            <p style="font-size: 18px;">
                En France, l’inflation a fortement augmenté depuis 2021, portée par la hausse des prix de l’énergie, de l’alimentation et des matières premières.  
                Après un pic à plus de 6 % en 2022, elle reste élevée, réduisant le pouvoir d’achat des ménages et pesant sur leur capacité à épargner.
            </p>
        </div>
        """, unsafe_allow_html=True)


    
    with col2:
        html(f"""
        <div style="width: 100%; height: 300px; overflow: hidden; border-radius: 20px;">
            <img id="carousel" 
                 src="data:image/png;base64,{img1}" 
                 style="width: 100%; height: 100%; object-fit: contain; transition: opacity 1s;">
        </div>
    
        <script>
        const images = [
            "data:image/png;base64,{img1}",
            "data:image/png;base64,{img2}",
            "data:image/png;base64,{img3}",
            "data:image/png;base64,{img4}",
            "data:image/png;base64,{img5}"
        ];

        let index = 0;
        setInterval(() => {{
            const carousel = document.getElementById("carousel");
            carousel.style.opacity = 0;
            setTimeout(() => {{
                index = (index + 1) % images.length;
                carousel.src = images[index];
                carousel.style.opacity = 1;
            }}, 500);
        }}, 3000);
        </script>
        """, height=320)
        
    st.markdown("""
    <hr style="height: 3px; background-color: #4CAF50; border: none; margin-top: 30px; margin-bottom: 30px;">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="text-align: center; font-size:18px; color: white;">
        Explorez les rubriques pour découvrir les bases de la finance, comprendre les principaux placements, 
        enrichir votre vocabulaire et mettre vos connaissances à l’épreuve grâce à un quiz interactif.
    </p>
    """, unsafe_allow_html=True)


    
    # Conteneur des boutons centrés
    st.markdown('<div class="centered-buttons">', unsafe_allow_html=True)

    # Espacement
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LIGNE 1 : Présentation (gauche) & Vocabulaire (droite)
    col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 3, 2])
    with col2:
        if st.button("📘 Présentation"):
            st.session_state.page = "Présentation"
            st.experimental_rerun()
    with col4:
        if st.button("📚 Vocabulaire financier"):
            st.session_state.page = "Vocabulaire financier"
            st.experimental_rerun()
    
    # Espacement
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LIGNE 2 : Comprendre (gauche) & Simulateur (droite)
    col6, col7, col8, col9, col10 = st.columns([2, 3, 1, 3, 2])
    with col7:
        if st.button("📈 Comprendre les placements"):
            st.session_state.page = "Comprendre les placements"
            st.experimental_rerun()
    with col9:
        if st.button("🧠 Testez vos connaissances fiancières"):
            st.session_state.page = "Testez vos connaissances fiancières"
            st.experimental_rerun()

    st.markdown("""
    <hr style="height: 3px; background-color: #4CAF50; border: none; margin-top: 30px; margin-bottom: 30px;">
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <p style="font-size: 18px; color: white; text-align: center;">
        Explorer notre simulateur qui vous permet de comparer l’évolution potentielle d’un placement en ETF face au Livret A, 
        en tenant compte de la durée de l’investissement, du montant investi et de l'inflation actuelle. 
        
        
    </p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size: 18px; color: white; text-align: center;">
        Visualisez en un clic l’impact de vos choix d’allocation.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size: 18px; color: white; text-align: center;">
     </p>
    """, unsafe_allow_html=True)
    
    
    # Crée 7 colonnes pour un centrage très précis
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])  # col4 est la plus large et au centre
    
    with col4:
        if st.button("📈 Simuler votre capital", key="simulateur_btn"):
            st.session_state.page = "Simulateur d'investissement"
            st.experimental_rerun()
    
    
    
elif page == "Présentation":

    st.markdown("""
    <div style="background-color: #283593; padding: 30px; border-radius: 15px; color: white;">
        <h2 style="color: #4CAF50;">🔍 C’est quoi FinFlation ?</h2>
        <p style="font-size: 18px;">
            FinFlation est une plateforme éducative et interactive qui aide chacun à <strong>mieux comprendre les placements financiers</strong>, 
            spécialement dans un contexte d’inflation.  
            L’objectif est simple : rendre la finance <strong>accessible, claire et utile</strong> pour toutes les générations, que vous soyez débutant ou curieux d’en savoir plus.
        </p>

    <h2 style="color: #4CAF50;">📌 Que propose FinFlation ?</h2>
        <ul style="font-size: 17px;">
            <li><strong>Un simulateur</strong> pour tester différents scénarios d'investissement entre ETF et Livret A.</li>
            <li><strong>Un vocabulaire clair</strong> pour mieux comprendre les mots compliqués de la finance.</li>
            <li><strong>Des fiches explicatives</strong> sur les placements comme les ETF ou les livrets d’épargne.</li>
        </ul>

    <h2 style="color: #4CAF50;">🧠 Pourquoi c’est important ?</h2>
        <p style="font-size: 18px;">
            Dans un monde où <strong>l’inflation impacte le pouvoir d’achat</strong>, il est essentiel de savoir où et comment investir intelligemment.  
            FinFlation vous donne les clés pour prendre vos décisions en toute connaissance de cause, sans jargon ni complexité.
        </p>

    <h2 style="color: #4CAF50;">🚀 Prêt à commencer ?</h2>
        <p style="font-size: 18px;">
            Explorez le menu à gauche pour tester le simulateur, enrichir votre vocabulaire ou découvrir les bases de l’investissement.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Style du bouton bleu
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #42a5f5;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8em 1.5em;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #1e88e5;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Colonne principale à gauche + vide à droite
    col1, col2 = st.columns([1, 3])  # bouton à gauche
    with col1:
        if st.button("Retourner à l'accueil"):
            st.session_state.page = "Accueil"
            st.experimental_rerun()
    
    
    
    
    
    
    
elif page == "Vocabulaire financier":

    st.header("📚 Vocabulaire financier")
    
    st.markdown("""
    <div style="background-color: #283593; padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px;">
        <p style="font-size: 18px;">
            Comprendre les <span style="font-weight: 900;">mots de la finance</span> est une première étape essentielle pour prendre des 
            <span style="font-weight: 900;">décisions éclairées</span>.  
            Que vous soyez <span style="font-weight: 900;">débutant</span> ou que vous souhaitiez rafraîchir vos connaissances, cette section vous permet de découvrir les 
            <span style="font-weight: 900;">notions clés</span> comme la <span style="font-weight: 900;">volatilité</span>, la 
            <span style="font-weight: 900;">liquidité</span> ou encore les <span style="font-weight: 900;">actions</span>. 
        </p>
        <p style="font-size: 18px;">
            Chaque terme est expliqué simplement, avec des <span style="font-weight: 900;">analogies du quotidien</span>, pour rendre la finance plus 
            <span style="font-weight: 900;">accessible</span> et moins <span style="font-weight: 900;">intimidante</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)



    with st.expander("💸 Qu'est-ce que la volatilité ?", expanded=False):
        st.markdown("""
        **La volatilité**, c’est une mesure des variations d’un prix dans le temps. 
        
        Plus un actif est volatil, plus son prix monte ou descend rapidement.  
        C’est un peu comme une mer agitée : plus elle est instable, plus c’est risqué. 
        
        Mais une forte volatilité peut aussi vouloir dire plus de potentiel de gain.
        """, unsafe_allow_html=True)

        st.image("volatilite.png", caption="Illustration de la volatilite", width=700)
        
        st.markdown("""
        **🧭 Comment lire ce schéma ?**
        
        Sur **la gauche**, la courbe bouge doucement : c’est une **volatilité faible**.  
        Les variations de prix sont petites, donc le risque est plus faible.
        
        Sur **la droite**, la courbe monte et descend rapidement et fortement : c’est une **volatilité élevée**.  
        Les variations de prix sont grandes, donc le risque est plus élevé.
        
        👉 En résumé : **plus la courbe est agitée, plus la volatilité est forte**.
        """)



        
    with st.expander("🏦 Qu'est-ce que la liquidité ?", expanded=False):
        st.markdown("""
        **La liquidité**, c’est la facilité avec laquelle on peut acheter ou vendre un produit financier.  
        
        Par exemple, un livret A est très liquide car on peut retirer l’argent à tout moment.  
        Une maison est peu liquide car cela prend du temps pour la vendre.  
        
        En finance, plus c’est liquide, plus c’est simple d’acheter ou de revendre rapidement.
        """)

    with st.expander("📈 Qu'est-ce qu'un indice boursier ?", expanded=False):
        st.markdown("""
        **Un indice boursier**, c’est un chiffre qui reflète l’évolution d’un groupe d’entreprises en Bourse.  
        
        Par exemple, le CAC 40 regroupe les 40 plus grandes entreprises françaises.  
        Si l’indice monte, cela veut dire que globalement ces entreprises vont bien.  
        
        C’est un bon moyen de suivre la santé d’un marché sans regarder chaque entreprise individuellement.
        """)
        
        st.image("indices.jpg", caption="Evolution des grands indices boursiers", width=400)

        st.markdown("""
        **📊 Voici une liste des principaux indices boursiers mondiaux :**
        
        Ce schéma présente les performances de différents indices sur une période de 25 ans :
        
        - **Nasdaq (🇺🇸)** : Regroupe principalement les grandes entreprises technologiques américaines (Apple, Amazon, Microsoft...).
        - **Dow Jones (🇺🇸)** : Composé de 30 grandes entreprises américaines traditionnelles (comme Coca-Cola ou McDonald’s).
        - **S&P 500 (🇺🇸)** : Représente les 500 plus grandes entreprises cotées aux États-Unis.
        - **Toronto Stock Exchange (🇨🇦)** : Principal indice du marché canadien.
        - **Shanghai Composite (🇨🇳)** : Indice regroupant les entreprises cotées à la Bourse de Shanghai.
        - **CAC 40 (🇫🇷)** : Indice phare de la Bourse de Paris, avec 40 grandes entreprises françaises.
        - **Eurostoxx 50 (🇪🇺)** : Représente les 50 plus grandes entreprises de la zone euro.
        - **Nikkei 225 (🇯🇵)** : Principale référence de la Bourse de Tokyo, avec les grandes entreprises japonaises.
        
        👉 En résumé : ces indices permettent de suivre l’évolution des marchés dans chaque région. Le **Nasdaq** domine largement en termes de performance sur cette période, tiré par la croissance du secteur technologique.
        """)



    with st.expander("💼 Qu'est-ce qu'un fonds d'investissement ?", expanded=False):
        st.markdown("""
        **Un fonds d’investissement**, c’est un “panier” d’actifs (actions, obligations, etc.) géré par des professionnels.  
        
        Quand tu investis dans un fonds, ton argent est mélangé avec celui d’autres investisseurs, puis investi selon une stratégie.  
        L’idée est de diversifier les placements et de confier la gestion à des experts.  
        
        Les ETF sont un type de fonds, mais ils sont cotés en Bourse.
        """)

    with st.expander("🏢 Qu'est-ce que la capitalisation boursière ?", expanded=False):
        st.markdown("""
        **La capitalisation boursière**, c’est la valeur totale d’une entreprise en Bourse.  
        
        On la calcule en multipliant le prix d’une action par le nombre total d’actions.  
        Par exemple, si une action vaut 100€ et qu’il y a 1 million d’actions, la capitalisation est de 100 millions d’euros.  
        
        C’est un bon indicateur de la taille d’une entreprise cotée.
        """)
        
        st.image("capbourse.png", caption="Illustration de la capitalisation boursière", width=400)

    with st.expander("💡 Qu'est-ce que le rendement ?", expanded=False):
            st.markdown("""
            Le **rendement** est le **gain financier** que vous obtenez en investissant de l’argent, généralement exprimé en **pourcentage du capital investi**.
        
            Par exemple, si vous placez **1 000 €** et que vous gagnez **50 €** au bout d’un an, le rendement est de **5 %**.
        
            Il existe deux types de rendement :
            - Le **rendement courant** : ce que vous touchez chaque année (ex : intérêts, dividendes).
            - Le **rendement global** : inclut aussi les éventuelles plus-values (hausse de valeur de l’actif).
        
            👉 **Plus le rendement est élevé**, plus le placement est **potentiellement rentable**… mais cela va souvent **de pair avec un risque plus important**.
            """)
        
    with st.expander("📉 Qu'est-ce que le risque de perte en capital ?", expanded=False):
            st.markdown("""
            Le **risque de perte en capital**, c’est la **possibilité que vous ne récupériez pas tout l’argent que vous avez investi**.
        
            C’est un risque présent dans des produits comme :
            - Les **actions**
            - Les **ETF**
            - Les **obligations d’entreprise**
            - Les **SCPI**
            - Les **cryptomonnaies**
        
            Contrairement aux **livrets réglementés** (comme le Livret A), où le capital est **garanti par l’État**, ces placements peuvent **baisser en valeur**.
        
            👉 En résumé : vous pouvez **perdre de l’argent**, notamment en cas de crise économique ou de mauvaise gestion.
            """)
    with st.expander("🎯 Qu'est-ce que la diversification ?", expanded=False):
            st.markdown("""
            La **diversification** est une **stratégie de gestion du risque** qui consiste à **répartir vos investissements sur différents types de placements**.
        
            L’idée est simple :
            - Si un placement chute, les autres peuvent compenser.
            - Vous n’êtes pas dépendant d’un seul actif ou secteur.
        
            Exemple : au lieu d’investir 10 000 € uniquement en actions, vous pouvez répartir :
            - 4 000 € en ETF
            - 3 000 € en Livret A
            - 2 000 € en SCPI
            - 1 000 € en obligations
        
            👉 En diversifiant, vous **limitez les pertes potentielles** et **équilibrez les performances** de votre portefeuille.
            """)
        
    with st.expander("💸 Qu'est-ce qu’un dividende ?", expanded=False):
            st.markdown("""
            Un **dividende** est une **part des bénéfices** qu'une entreprise verse à ses **actionnaires**.  
            C’est une **récompense** pour avoir investi dans l’entreprise.
        
            Vous pouvez recevoir des dividendes si vous détenez :
            - Des **actions**
            - Certains **ETF** qui distribuent les revenus
        
            Tous les titres ne versent pas de dividendes.  
            Certaines entreprises préfèrent **réinvestir leurs bénéfices** pour se développer plutôt que les distribuer.
        
            👉 Le dividende est une **source de revenu passif**, souvent versée **chaque trimestre ou une fois par an**.
            """)
            
    with st.expander("📊 Qu’est-ce que le taux d’intérêt ?", expanded=False):
        st.markdown("""
        Le **taux d’intérêt**, c’est le **coût de l’argent emprunté** ou le **rendement d’un placement**.  
        C’est un pourcentage qui indique combien vous gagnez (ou payez) **chaque année** sur un montant donné.
    
        Deux cas :
        - Si vous **empruntez** (prêt immobilier, crédit à la consommation…) → vous **payez** un taux d’intérêt à la banque.
        - Si vous **placez** de l’argent (livret, obligation…) → vous **touchez** un taux d’intérêt.
    
        **Exemple simple :**  
        Si vous placez 1 000 € à un taux de 3 % pendant 1 an, vous gagnez 30 € d’intérêts.
    
        👉 Le taux d’intérêt peut être **fixe** (ne bouge pas) ou **variable** (change avec le temps).
        """)
        
    with st.expander("🌐 Qu’est-ce que décentralisé veut dire ?", expanded=False):
        st.markdown("""
        En finance, **décentralisé** veut dire **qu’il n’y a pas d’autorité centrale** (comme une banque, un gouvernement ou une entreprise) qui contrôle le système.
    
        Dans le cas des **cryptomonnaies** :
        - Pas de banque centrale.
        - Les transactions sont vérifiées par un **réseau d’utilisateurs**, grâce à la technologie **blockchain**.
        - Les données sont **réparties** (copies sur de nombreux ordinateurs) → c’est ce qu’on appelle un **réseau décentralisé**.
    
        👉 Cela rend le système plus **transparent**, plus **résilient**… mais parfois **plus risqué** ou moins réglementé.
        """)
    
    with st.expander("⚠️ Quels sont les différents types de risques ?", expanded=False):
        st.markdown("""
        En finance, tout investissement comporte des **risques**. Voici les principaux à connaître :
    
        - **Risque de marché** : vos actifs peuvent **perdre de la valeur** à cause des variations des marchés (ex : chute de la Bourse).
        - **Risque de taux** : si les **taux d’intérêt augmentent**, la valeur des obligations baisse.
        - **Risque de liquidité** : vous pouvez avoir **du mal à vendre** rapidement un actif sans perte (ex : immobilier, SCPI).
        - **Risque de crédit** : l’émetteur (entreprise, État...) **ne rembourse pas** (ex : défaut d’une obligation).
        - **Risque de change** : si vous investissez dans une **devise étrangère**, son évolution peut impacter vos gains.
        - **Risque réglementaire** : changement de loi ou de fiscalité qui affecte votre investissement (ex : taxation des crypto-actifs).
    
        👉 La **diversification** permet de limiter certains de ces risques.
        """)

    # Style du bouton bleu
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #42a5f5;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8em 1.5em;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #1e88e5;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Colonne principale à gauche + vide à droite
    col1, col2 = st.columns([1, 3])  # bouton à gauche
    with col1:
        if st.button("Retourner à l'accueil"):
            st.session_state.page = "Accueil"
            st.experimental_rerun()








    
    
    
if page == "Comprendre les placements":

    # Page "Comprendre les placements"
    st.header("📚 Comprendre les placements")
    
    st.markdown("""
    <div style="background-color: #283593; padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px;">
        <p style="font-size: 18px;">
            Comprendre les <span style="font-weight: 900;">différents types de placements</span> est essentiel pour bâtir une stratégie d’épargne efficace.  
            Que vous cherchiez à <span style="font-weight: 900;">sécuriser</span> votre capital ou à <span style="font-weight: 900;">le faire fructifier</span>, cette section vous présente les principales solutions disponibles.
        </p>
        <p style="font-size: 18px;">
            Chaque produit d’investissement (actions, ETF, obligations, SCPI, cryptomonnaies...) est expliqué de façon claire et structurée, avec ses 
            <span style="font-weight: 900;">caractéristiques</span>, <span style="font-weight: 900;">avantages</span> et <span style="font-weight: 900;">inconvénients</span>.  
            L’objectif est de vous permettre de mieux <span style="font-weight: 900;">comparer les options</span> et de <span style="font-weight: 900;">faire des choix adaptés</span> à votre profil.
        </p>
    </div>
    """, unsafe_allow_html=True)


    with st.expander("📊 Qu'est-ce qu'une action ?", expanded=False):
        st.markdown("""
        *Une action représente une part du capital d'une entreprise cotée en bourse.*

        En achetant une action, vous devenez actionnaire et donc copropriétaire de l’entreprise. Vous pouvez bénéficier de la croissance de l’entreprise via les dividendes et la valorisation du titre.

        *Caractéristiques :*
        - Droit de vote à l'assemblée générale
        - Éligibilité à des dividendes
        - Cours variable selon l’offre et la demande
        - Cotation en bourse

        *Avantages :*
        - Potentiel de gain élevé à long terme
        - Participation aux bénéfices de l’entreprise (dividendes)
        - Facilité d’achat/vente (liquidité)

        *Inconvénients :*
        - Risque de perte en capital
        - Volatilité importante
        - Pas de garantie de revenus réguliers
        """)

    with st.expander("💸 Qu'est-ce qu'un ETF ?", expanded=False):
        st.markdown("""
        *Un ETF (Exchange-Traded Fund) en bref*  
        Un ETF est un fonds d'investissement coté en bourse qui réplique la performance d'un indice boursier.

        *Caractéristiques principales :*
        - Diversification automatique
        - Faibles frais de gestion
        - Transparence sur la composition
        - Liquidité (achat/vente en temps réel)
        - Potentiel de rendement supérieur à long terme

        *Avantages face à l'inflation :*
        - Les actions ont historiquement surperformé l'inflation
        - Croissance des entreprises compense l'érosion monétaire
        - Dividendes augmentent souvent avec l'inflation

        *Risques :*
        - Volatilité à court terme
        - Performance passée ne garantit pas les résultats futurs
        - Nécessite un horizon d'investissement moyen/long terme
        """)

    with st.expander("💸 Qu'est-ce qu'une obligation ?", expanded=False):
        st.markdown("""
        *Une obligation, c’est un emprunt que vous faites à une entreprise ou à un État.*  
        En achetant une obligation, vous prêtez votre argent, et en échange vous recevez des intérêts pendant une durée définie.

        *Caractéristiques principales :*
        - Revenu fixe (les intérêts ou "coupons")
        - Échéance connue à l’avance
        - Moins risqué que les actions en général
        - Peut être revendu sur le marché secondaire

        *Avantages :*
        - Revenus stables et prévisibles
        - Bonne visibilité sur l’investissement
        - Moins de volatilité que les actions

        *Risques :*
        - Risque de défaut (l’émetteur peut ne pas rembourser)
        - Rendement parfois inférieur à l’inflation
        - Sensibilité aux taux d’intérêt (si les taux montent, le prix des obligations baisse)
        """)

    with st.expander("🏦 Qu'est-ce qu'un livret d'épargne ?", expanded=False):
        st.markdown("""
        *Un livret d’épargne est un compte bancaire qui permet de placer de l’argent tout en générant des intérêts.*  
        Il est sécurisé et souvent réglementé par l’État (comme le Livret A).

        *Caractéristiques :*
        - Taux fixe défini par l’État (ex : 2,4% pour le Livret A en 2023)
        - Intérêts exonérés d’impôt (pour les livrets réglementés)
        - Plafond de dépôt
        - Accès à l’argent à tout moment (liquidité)

        *Avantages :*
        - Sécurité totale (capital garanti)
        - Aucun risque de perte
        - Simplicité d’utilisation

        *Inconvénients :*
        - Rendement faible
        - Rendement souvent inférieur à l’inflation
        - Plafond qui limite l’épargne
        """)

    with st.expander("🏢 Qu'est-ce qu'une SCPI ?", expanded=False):
        st.markdown("""
        *Une SCPI (Société Civile de Placement Immobilier) vous permet d’investir dans l’immobilier sans acheter directement un bien.*

        *Caractéristiques :*
        - Vous achetez des parts de la SCPI
        - Elle investit dans des immeubles (bureaux, commerces, logements)
        - Les loyers perçus sont redistribués aux porteurs de parts

        *Avantages :*
        - Revenus réguliers (loyers)
        - Mutualisation du risque
        - Accessibilité (ticket d’entrée plus faible qu’un achat immobilier direct)

        *Inconvénients :*
        - Capital non garanti
        - Liquidité limitée (revente des parts pas toujours immédiate)
        - Frais d’entrée parfois élevés
        """)

    with st.expander("🪙 Qu'est-ce qu'une cryptomonnaie ?", expanded=False):
        st.markdown("""
        *Une cryptomonnaie est une monnaie numérique, décentralisée, et souvent basée sur la technologie blockchain.*

        *Caractéristiques :*
        - Aucune autorité centrale (banque ou gouvernement)
        - Transactions anonymes et sécurisées via blockchain
        - Volatilité très élevée

        *Avantages :*
        - Potentiel de rendement très élevé
        - Accessibilité mondiale
        - Innovation technologique

        *Inconvénients :*
        - Risque élevé de perte
        - Réglementation floue ou absente
        - Pas de revenus passifs (pas de dividende ni coupon)
        """)



    
    # Style du bouton bleu
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #42a5f5;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8em 1.5em;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #1e88e5;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Colonne principale à gauche + vide à droite
    col1, col2 = st.columns([1, 3])  # bouton à gauche
    with col1:
        if st.button("Retourner à l'accueil"):
            st.session_state.page = "Accueil"
            st.experimental_rerun()









if page == "Testez vos connaissances fiancières":
    
    st.header("🧠 Testez vos connaissances financières avec FinFlation")
    
    st.markdown("""
    <div style="background-color: #283593; padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px;">
        <p style="font-size: 18px;">
            Ce test est conçu pour évaluer vos <span style="font-weight: 900;">connaissances financières</span> de manière ludique. 
            Il couvre les notions essentielles abordées dans les sections <span style="font-weight: 900;">Vocabulaire financier</span> 
            et <span style="font-weight: 900;">Comprendre les placements</span>.
        </p>
        <p style="font-size: 18px;">
            Cliquez sur <span style="font-weight: 900;">"Lancer le test"</span> pour débuter. Vous verrez une série de questions à choix unique. 
            Une fois terminé, appuyez sur <span style="font-weight: 900;">"Valider mes réponses"</span> pour afficher la correction, 
            où les bonnes réponses auront l'émoji ✅ et les mauvaises auront l'émoji ❌ avec une correction en dessous. 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Questions de la base
    questions = [
        {
            "question": "Quel est l’avantage principal d’un ETF ?",
            "options": [
                "Garantit un rendement fixe",
                "Réplique la performance d’un indice",
                "Offre une protection contre la déflation",
                "Permet d’éviter tout risque de marché"
            ],
            "answer": 1
        },
        {
            "question": "Qu’est-ce que la volatilité en finance ?",
            "options": [
                "La vitesse d'achat ou de vente d'un actif",
                "La fréquence et l’amplitude des variations de prix",
                "Le rendement garanti d’un actif",
                "Le taux d’intérêt appliqué aux emprunts"
            ],
            "answer": 1
        },
        {
            "question": "Qu’est-ce qu’un indice boursier ?",
            "options": [
                "Une mesure du taux d’intérêt bancaire",
                "Un groupe d’entreprises cotées représenté par un chiffre",
                "Un outil pour fixer le prix d’une action",
                "Un fonds d’investissement à haut risque"
            ],
            "answer": 1
        },
        {
            "question": "Qu’est-ce qu’une action ?",
            "options": [
                "Une obligation d’État",
                "Un produit d’épargne garanti",
                "Une part de propriété dans une entreprise",
                "Un indice boursier"
            ],
            "answer": 2
        },
        {
            "question": "Qu’est-ce que la liquidité d’un actif ?",
            "options": [
                "Sa rentabilité garantie",
                "La facilité avec laquelle il peut être acheté ou vendu",
                "Le risque qu’il représente",
                "Son rendement annuel moyen"
            ],
            "answer": 1
        },
        {
            "question": "Quelle est la caractéristique principale d’un Livret A ?",
            "options": [
                "Risque élevé",
                "Rendement supérieur à l’inflation",
                "Fonds investis dans des actions",
                "Placement sécurisé et liquide"
            ],
            "answer": 3
        },
        {
            "question": "Pourquoi diversifier ses placements ?",
            "options": [
                "Pour maximiser les pertes",
                "Pour réduire les risques",
                "Pour augmenter les frais bancaires",
                "Pour investir uniquement dans des actions"
            ],
            "answer": 1
        },
        {
            "question": "Quel placement permet une disponibilité immédiate des fonds ?",
            "options": [
                "L'immobilier locatif",
                "Le Livret A",
                "Les obligations d'État",
                "Les actions"
            ],
            "answer": 1
        },
        {
            "question": "Que reflète un indice boursier comme le CAC 40 ?",
            "options": [
                "La performance moyenne de plusieurs entreprises",
                "La rentabilité des obligations",
                "Le taux d’épargne moyen des ménages",
                "La valeur de l’or sur le marché international"
            ],
            "answer": 0
        },
        {
            "question": "Quel est le principal risque d’un ETF ?",
            "options": [
                "Aucun, c’est garanti par l’État",
                "Il peut être difficile à vendre",
                "Il peut varier fortement avec le marché",
                "Il offre peu de diversification"
            ],
            "answer": 2
        },
        {
        "question": "Que représente la capitalisation boursière d'une entreprise ?",
        "options": [
            "Le montant de ses bénéfices annuels",
            "La valeur totale de ses actifs immobiliers",
            "Le prix d’une action multiplié par le nombre d’actions",
            "Son chiffre d'affaires"
        ],
        "answer": 2
    },
    {
        "question": "Quel est l’un des principaux avantages d’un ETF ?",
        "options": [
            "Il est exonéré d'impôts",
            "Il permet une diversification automatique",
            "Il garantit un rendement fixe",
            "Il est géré activement au quotidien"
        ],
        "answer": 1
    },
    {
        "question": "Quel terme désigne la rapidité avec laquelle un actif peut être vendu sans perte significative de valeur ?",
        "options": [
            "Rendement",
            "Inflation",
            "Volatilité",
            "Liquidité"
        ],
        "answer": 3
    },
    {
        "question": "Pourquoi le Livret A est-il considéré comme un placement sécurisé ?",
        "options": [
            "Il rapporte plus que les actions",
            "Il est garanti par l’État",
            "Il est indexé sur l’or",
            "Il est toujours supérieur à l’inflation"
        ],
        "answer": 1
    },
    {
        "question": "Qu'est-ce qu’un fonds d’investissement ?",
        "options": [
            "Un prêt entre particuliers",
            "Un panier de plusieurs actifs géré par des professionnels",
            "Une obligation d’État",
            "Un compte bancaire à taux fixe"
        ],
        "answer": 1
    },
    {
        "question": "Quelle affirmation est vraie concernant les actions ?",
        "options": [
            "Elles garantissent un rendement annuel fixe",
            "Elles sont des produits d’épargne réglementés",
            "Elles représentent une part de propriété d’une entreprise",
            "Elles ne sont accessibles qu’aux professionnels"
        ],
        "answer": 2
    },
    {
        "question": "À quoi sert un indice boursier comme le CAC 40 ?",
        "options": [
            "À fixer le prix des produits alimentaires",
            "À mesurer la performance moyenne d’un groupe d’entreprises",
            "À calculer le taux d’imposition sur les revenus",
            "À suivre la croissance démographique"
        ],
        "answer": 1
    },
    {
        "question": "Quelle est une caractéristique essentielle d’un ETF ?",
        "options": [
            "Il se négocie uniquement en fin de journée",
            "Il réplique un indice de marché",
            "Il est plafonné à 10 000 €",
            "Il ne peut pas être vendu avant 5 ans"
        ],
        "answer": 1
    },
    {
        "question": "Comment l’inflation affecte-t-elle votre épargne ?",
        "options": [
            "Elle augmente automatiquement votre capital",
            "Elle réduit le pouvoir d’achat de votre argent",
            "Elle garantit un taux d’intérêt plus élevé",
            "Elle annule tous les rendements"
        ],
        "answer": 1
    },
    {
        "question": "Quel placement est le plus liquide parmi les suivants ?",
        "options": [
            "L’achat d’un appartement",
            "Un Livret A",
            "Un contrat d’assurance-vie bloqué",
            "Un ETF avec un préavis de vente"
        ],
        "answer": 1
    }
    ]

    import random
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []
    if "quiz_validated" not in st.session_state:
        st.session_state.quiz_validated = False
    
    if not st.session_state.quiz_started:
        if st.button("🚀 Lancer le test"):
            st.session_state.quiz_started = True
            st.session_state.quiz_validated = False
            st.session_state.quiz_data = random.sample(questions, k=min(10, len(questions)))
            st.session_state.quiz_answers = [None] * len(st.session_state.quiz_data)
            st.experimental_rerun()
            
    else:
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**{i+1}. {q['question']}**")
        
            selected = st.radio(
                label="", 
                options=q["options"], 
                key=f"q_{i}"
            )
        
            # Si une sélection est faite, on l'enregistre
            if selected is not None:
                st.session_state.quiz_answers[i] = q["options"].index(selected)


        if not st.session_state.quiz_validated:
            if st.button("✅ Valider mes réponses"):
                st.session_state.quiz_validated = True
                st.experimental_rerun()
        else:
            st.markdown("""
            <hr style="height: 3px; background-color: #4CAF50; border: none; margin-top: 30px; margin-bottom: 30px;">
            """, unsafe_allow_html=True)
            st.markdown("""
            <h2 style='color: #4CAF50; margin-top: 40px;'>📋 Correction de votre test</h2>
            """, unsafe_allow_html=True)
            score = 0
            for i, q in enumerate(st.session_state.quiz_data):
                user_answer = st.session_state.quiz_answers[i]
                correct_answer = q["answer"]
                st.markdown(f"**{i+1}. {q['question']}**")
                if user_answer == correct_answer:
                    st.markdown(f"<span style='color: limegreen; font-weight: bold;'>✅ {q['options'][user_answer]}</span>", unsafe_allow_html=True)
                    score += 1
                else:
                    st.markdown(f"<span style='color: red;'>❌ {q['options'][user_answer]}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: limegreen;'>✔ Bonne réponse : {q['options'][correct_answer]}</span>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="margin-top: 20px; padding: 10px; background-color: #0d47a1; color: white; border-radius: 10px;">
                <strong>Score final :</strong> {score} / {len(st.session_state.quiz_data)}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <hr style="height: 3px; background-color: #4CAF50; border: none; margin-top: 30px; margin-bottom: 30px;">
            """, unsafe_allow_html=True)
            if st.button("❌ Fermer le QCM"):
                st.session_state.quiz_started = False
                st.experimental_rerun()

    
    
    # Style du bouton bleu
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #42a5f5;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8em 1.5em;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #1e88e5;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Affiche le bouton retour uniquement si le test n'est PAS lancé
    if not st.session_state.quiz_started:
        col1, col2 = st.columns([1, 3])  # bouton à gauche
        with col1:
            if st.button("Retourner à l'accueil"):
                st.session_state.page = "Accueil"
                st.experimental_rerun()

    
    
    
    
    
    
    
if page == "Simulateur d'investissement":
    
    st.header("📊 Simulateur d'investissement intelligent")
    
    # Ajout du disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        ⚠ <strong>Disclaimer :</strong> Cette simulation est fournie à titre informatif uniquement et ne constitue pas 
        un conseil en investissement. Les résultats sont basés sur des hypothèses et des données historiques qui ne 
        garantissent pas les performances futures. Consultez un conseiller financier avant toute décision d'investissement.
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("⚙ Paramètres de simulation", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            etf_ticker = st.selectbox(
                "FINANCIAGE",
                ("SPY", "QQQ", "VTI", "VT", "ARKK"),
                index=0
            )
        with col2:
            years = st.slider(
                "Nombre d'années d'investissement",
                min_value=1, max_value=30, value=10, step=1
            )
        with col3:
            investment_amount = st.number_input(
                "Montant à investir (en USD)",
                min_value=100, max_value=1000000, value=10000, step=1000
            )
    
    if st.button("Lancer la simulation"):
        with st.spinner('Calcul en cours...'):
            # Fonctions de calcul
            def get_etf_data(ticker):
                etf = yf.Ticker(ticker)
                hist = etf.history(period="5y")
                hist['Daily Return'] = hist['Close'].pct_change()
                mean_return = hist['Daily Return'].mean()
                daily_vol = hist['Daily Return'].std()
                return hist['Close'].iloc[-1], mean_return, daily_vol

            def get_inflation_rate():
                inflation_ticker = "^IRX"
                inflation_data = yf.Ticker(inflation_ticker)
                hist = inflation_data.history(period="1mo")
                if not hist.empty:
                    return hist['Close'].iloc[-1] / 100
                return None

            def monte_carlo_simulation(current_price, mean_daily_return, daily_vol, years, simulations=1000):
                days = years * 252
                np.random.seed(42)
                daily_returns = np.random.normal(loc=mean_daily_return, scale=daily_vol, size=(days, simulations))
                price_paths = current_price * np.exp(np.cumsum(daily_returns, axis=0))
                return price_paths

            beta = 0.5
            current_price, mean_daily_return, daily_vol = get_etf_data(etf_ticker)
            inflation_rate = get_inflation_rate()
            livret_a_rate = 0.024

            if inflation_rate is not None:
                # Simulation Monte Carlo
                prices = monte_carlo_simulation(current_price, mean_daily_return, daily_vol, years)
                final_prices = prices[-1]
                mean_final_price = np.mean(final_prices)
                total_return = (mean_final_price - current_price) / current_price
                simulated_annual_return = (1 + total_return) ** (1 / years) - 1

                historical_annual_return = (1 + mean_daily_return) ** 252 - 1
                annualized_etf_return = beta * historical_annual_return + (1 - beta) * simulated_annual_return

                proportion_etf = 0
                proportion_livret = 100
                target_value_livret_a = investment_amount * (1 + livret_a_rate)**years

                while True:
                    etf_investment = investment_amount * proportion_etf / 100
                    livret_a_investment = investment_amount * proportion_livret / 100

                    vf_etf = etf_investment * ((1 + annualized_etf_return) / (1 + inflation_rate)) ** years
                    vf_livret = livret_a_investment * ((1 + livret_a_rate) / (1 + inflation_rate)) ** years
                    total_value = vf_etf + vf_livret

                    if total_value >= target_value_livret_a:
                        break

                    proportion_etf += 0.5
                    proportion_livret -= 0.5

                # Affichage des résultats
                st.success("Simulation terminée avec succès!")
                
                # Métriques
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rendement ETF annualisé", f"{annualized_etf_return:.2%}")
                with col2:
                    st.metric("Taux d'inflation", f"{inflation_rate:.2%}")
                with col3:
                    st.metric("Taux Livret A", f"{livret_a_rate:.2%}")
                
                # Graphique de répartition avec titre blanc
                fig1 = go.Figure(go.Pie(
                    labels=['ETF', 'Livret A'],
                    values=[proportion_etf, proportion_livret],
                    hole=.4,
                    marker_colors=['#4CAF50', '#2196F3']
                ))
                fig1.update_layout(
                    title_text="Répartition optimale de votre portefeuille",
                    title_font_color="white",
                    title_x=0.5,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig1, use_container_width=True)
                
                
                
                
    
            
# Pied de page
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>FinFlation - Outil de simulation d'investissement intelligent</p>
    <p>© 2025 Tous droits réservés</p>
</div>
""", unsafe_allow_html=True)



