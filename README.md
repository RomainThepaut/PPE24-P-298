## 🔍 Projet PPE – Optimisation des Rendements Financiers en Contexte d'Inflation

### 🎯 Problématique :
> *Comment optimiser les rendements des investissements financiers tout en minimisant les risques dans un environnement économique inflationniste ?*

Dans un contexte où l’inflation grignote le pouvoir d’achat et où les solutions classiques comme le Livret A ne suffisent plus, les investisseurs doivent se tourner vers des alternatives plus performantes. Ce projet vise à concevoir un outil d’aide à la décision permettant d’analyser différentes options d’investissement selon le profil utilisateur, la conjoncture économique et les indicateurs de risque/volatilité.

---

### 👥 Équipe PPE24-P-298 :
- Victor JOUET  
- Romain THEPAUT  
- Mathis CHATILLON  
- Paul-Adrien THABAULT PARISOT  
- Rémi GAUTUER  
- Corentin PRAT  
- Thomas LE CORRE  

Sujet proposé par : Paul Arnaud Battandier

---

### 💡 Objectifs :
- Proposer un outil simple et pédagogique permettant à chacun de mieux comprendre les opportunités d’investissement face à l’inflation.
- Comparer différents actifs (ETF, SCPI, obligations, épargne réglementée) en fonction de critères de performance comme la volatilité, la VaR, le ratio de Sharpe, ou encore le bêta.
- Fournir des recommandations de répartition capital/investissement selon le profil de risque de l’utilisateur.

---

### 🧠 Domaines mobilisés :
#Big Data et Data Science  
#Finance et Mathématiques  
#Développement Logiciel et Applications  

---

### 🛠️ Solution technique : Python + Streamlit (Solution 1 retenue)
- **Langage** : Python  
- **Interface** : Streamlit  
- **Librairies principales** :
  - `yfinance` pour la récupération de données financières en temps réel
  - `pandas`, `numpy`, `matplotlib` pour l’analyse et la visualisation
  - `scikit-learn` (éventuellement) pour de l’analyse de clusters ou des profils d’utilisateurs

#### ✅ Avantages :
- Déploiement simple (local ou web)
- Interface tout-en-un, sans séparation backend/frontend
- Idéal pour un prototype pédagogique et interactif

#### ❌ Limites :
- Design moins personnalisable
- Moins adapté à des usages très complexes côté front

---

### 🔍 Fonctionnalités prévues :
- Dashboard interactif avec graphiques, indicateurs et comparaisons d’actifs
- Visualisation dynamique des performances passées
- Simulation de répartition de portefeuille selon capital, profil et inflation
- Module éducatif pour expliquer les concepts de base (volatilité, diversification, etc.)

---

### ⚙️ Prérequis techniques (en local sur VS Code ou autre IDE) :

#### 📦 Installation des librairies spécifiques :

Lancer ces commandes dans un terminal ou directement dans VS Code (assurez-vous d’être dans un environnement virtuel) :

```bash
pip install streamlit
pip install yfinance
pip install scikit-learn
pip install plotly
```

> 🔁 Les librairies comme `pandas`, `numpy` ou `matplotlib` sont généralement installées d’office, mais en cas de besoin :

```bash
pip install pandas numpy matplotlib
```

#### 💻 Lancement local de l’interface Streamlit :

Dans le terminal (à la racine du projet) :

```bash
streamlit run app.py
```

> Remplace `app.py` par le nom réel de ton fichier principal.

---
