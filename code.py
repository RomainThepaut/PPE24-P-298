import streamlit as st
import yfinance as yf
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import base64

# Configuration de la page
st.set_page_config(
    page_title="FinFlation - Simulation d'investissement",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
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

# Menu de navigation simplifié
with st.sidebar:
    st.title("Menu")
    page = st.radio(
        "Navigation",
        ["Présentation", "Vocabulaire financier", "Comprendre les placements", "Simulateur d'investissement" ],
        index=0
    )


if page == "Présentation":
    st.header("🎯 Présentation de FinFlation")

    st.markdown("""
    <div style="background-color: #283593; padding: 30px; border-radius: 15px; color: white;">
        <h2 style="color: #4CAF50;">🔍 C’est quoi FinFlation ?</h2>
        <p style="font-size: 18px;">
            FinFlation est une plateforme éducative et interactive qui aide chacun à <strong>mieux comprendre les placements financiers</strong>, 
            notamment dans un contexte d’inflation.  
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




elif page == "Vocabulaire financier":
    st.header("📚 Vocabulaire financier")

    with st.expander("💸 Qu'est-ce que la volatilité", expanded=True):
        st.markdown("""
        **La volatilité**, c’est une mesure des variations d’un prix dans le temps.  
        Plus un actif est volatil, plus son prix monte ou descend rapidement.  
        C’est un peu comme une mer agitée : plus elle est instable, plus c’est risqué.  
        Mais une forte volatilité peut aussi vouloir dire plus de potentiel de gain.
        """, unsafe_allow_html=True)



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
        
    with st.expander("📊 Qu'est-ce qu'une action ?", expanded=False):
        st.markdown("""
        **Une action**, c’est une petite part d’une entreprise.  
        Quand tu achètes une action, tu deviens en quelque sorte co-propriétaire de cette entreprise.  
        Si l’entreprise fait des bénéfices, tu peux gagner de l’argent (par exemple avec des dividendes ou si le prix de l’action monte).  
        Mais si l’entreprise perd de la valeur, tu peux aussi en perdre.
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



if page == "Comprendre les placements":
    # Page "Comprendre les placements"
    st.header("📚 Comprendre les placements")
    
    with st.expander("💸 Qu'est-ce qu'un ETF?", expanded=True):
        st.markdown("""
        *Un ETF (Exchange-Traded Fund) en bref*  
        Un ETF est un fonds d'investissement coté en bourse qui réplique la performance d'un indice boursier.
        
        *Caractéristiques principales:*
        - Diversification automatique
        - Faibles frais de gestion
        - Transparence sur la composition
        - Liquidité (achat/vente en temps réel)
        - Potentiel de rendement supérieur à long terme
        
        *Avantages face à l'inflation:*
        - Les actions ont historiquement surperformé l'inflation
        - Croissance des entreprises compense l'érosion monétaire
        - Dividendes augmentent souvent avec l'inflation
        
        *Risques:*
        - Volatilité à court terme
        - Performance passée ne garantit pas les résultats futurs
        - Nécessite un horizon d'investissement moyen/long terme
        """)
    
    with st.expander("🏦 Le Livret A", expanded=False):
        st.markdown("""
        *Le Livret A: placement sécurisé*  
        Compte d'épargne réglementé proposé par les banques françaises.
        
        *Caractéristiques:*
        - Taux actuel: 2.4% (2023)
        - Exonéré d'impôts et de prélèvements sociaux
        - Plafond: 22 950€ (hors intérêts)
        - Liquidité immédiate
        
        *Avantages:*
        - Sécurité absolue (garanti par l'État)
        - Disponibilité des fonds à tout moment
        - Pas de frais
        
        *Inconvénients face à l'inflation:*
        - Rendement souvent inférieur à l'inflation
        - Perte de pouvoir d'achat réelle
        - Plafond limitant
        """)
    
    with st.expander("📈 Inflation et épargne", expanded=False):
        st.markdown("""
        *L'impact de l'inflation sur votre épargne*  
        L'inflation réduit progressivement la valeur réelle de votre argent.
        
        *Exemple concret:*
        - Avec 2% d'inflation annuelle, 100€ aujourd'hui ne vaudront que 82€ dans 10 ans en pouvoir d'achat
        - Un livret A à 2.4% avec 2% d'inflation ne rapporte que 0.4% réel
        
        *Stratégies de protection:*
        - Mélange ETF/Livret A comme recommandé par notre simulateur
        - Investissement régulier (lissage des cours)
        - Diversification géographique et sectorielle
        """)

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

            def monte_carlo_simulation(current_price, mean_daily_return, daily_vol, years, simulations=10000):
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
                
                # Graphique de simulation avec titre blanc
                fig2 = go.Figure()
                for i in range(min(100, prices.shape[1])):
                    fig2.add_trace(go.Scatter(
                        y=prices[:, i],
                        mode='lines',
                        line=dict(width=1),
                        name=f"Simulation {i+1}"
                    ))
                fig2.update_layout(
                    title_text="Simulation Monte Carlo des prix de l'ETF",
                    title_font_color="white",
                    xaxis_title="Jours",
                    yaxis_title="Prix de l'ETF (USD)",
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Détails des résultats
                with st.expander("📊 Détails complets des résultats", expanded=True):
                    st.markdown(f"""
                    <div class='result-box'>
                        <h3>Résultats de la simulation sur {years} ans</h3>
                        <p><b>ETF analysé:</b> {etf_ticker}</p>
                        <p><b>Prix actuel:</b> {current_price:.2f} USD</p>
                        <p><b>Prix final moyen simulé:</b> {mean_final_price:.2f} USD</p>
                        <p><b>Rendement total simulé:</b> {total_return:.2%}</p>
                        <p><b>Rendement annualisé:</b> {annualized_etf_return:.2%}</p>
                        
                        <h3>Recommandation d'allocation</h3>
                        <p><b>Part ETF:</b> {proportion_etf:.1f}% (soit {investment_amount * proportion_etf / 100:.2f} USD)</p>
                        <p><b>Part Livret A:</b> {proportion_livret:.1f}% (soit {investment_amount * proportion_livret / 100:.2f} USD)</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Impossible de récupérer le taux d'inflation. Veuillez réessayer plus tard.")
# Pied de page
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>FinFlation - Outil de simulation d'investissement intelligent</p>
    <p>© 2023 Tous droits réservés</p>
</div>
""", unsafe_allow_html=True)
