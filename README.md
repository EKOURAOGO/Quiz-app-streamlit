# Quiz Application - OOP & Streamlit

Application de quiz interactive développée en Python avec une architecture **orientée objet (OOP)** et une interface **Streamlit**.

![Interface principale](IMAGES/Interface_appli.png)

---

## Aperçu

<p align="center">
  <img src="IMAGES/Presentation_des_question_simple.png" width="47%"/>
  <img src="IMAGES/Presentation_des_question_multiple.png" width="47%"/>
</p>
<p align="center">
  <img src="IMAGES/Resultats_detaillées.png" width="47%"/>
  <img src="IMAGES/Performances_par_domaine.png" width="47%"/>
</p>

---

## Fonctionnalités

- Génération de quiz dynamique par domaine (tags)
- Questions à **choix unique** (radio buttons) et **choix multiple** (multiselect)
- Scoring proportionnel pour les questions à choix multiple
- Visualisation des résultats par domaine (Matplotlib/Seaborn)
- Persistance des données via `st.session_state`
- Réinitialisation du quiz

---

## Architecture OOP

```
Quiz-app-streamlit/
│
├── app.py               # Interface Streamlit (QuizView)
├── models.py            # Logique métier (4 classes OOP)
├── quiz_dataset.json    # Dataset de questions en JSON
├── requirments.txt      # Dépendances Python
├── Diagramme_UML.pdf    # Diagramme de classes UML
│
└── IMAGES/              # Captures d'écran de l'application
```

### Classes implémentées (`models.py`)

| Classe | Rôle |
|--------|------|
| `Question` | Représente une question (énoncé, choix, réponse, tags) |
| `QuestionDataset` | Singleton — charge le JSON une seule fois |
| `QuizGenerator` | Génère un quiz aléatoire filtré par domaine |
| `QuizCorrector` | Évalue les réponses et calcule les scores |

### Logique de scoring

**Choix unique** : 1 point si correct, 0 sinon.

**Choix multiple** (score proportionnel) :

$$\text{score} = \max\left(0,\ \frac{|correct \cap selected|}{|correct|} - \frac{|selected \setminus correct|}{|correct|}\right)$$

---

## Installation & lancement

```bash
# Cloner le dépôt
git clone https://github.com/EKOURAOGO/Quiz-app-streamlit.git
cd Quiz-app-streamlit

# Installer les dépendances
pip install -r requirments.txt

# Lancer l'application
streamlit run app.py
```

---

## Utilisation

1. Sélectionner un ou plusieurs **domaines** dans la sidebar
2. Cliquer sur **"Générer le quiz"**
3. Répondre aux questions (radio ou multiselect)
4. Soumettre pour voir le **score détaillé par question**
5. Visualiser les **performances par domaine** en graphique

---

## Stack technique

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![OOP](https://img.shields.io/badge/Design-OOP%20%2B%20Singleton-purple?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-charts-blue?style=flat-square)

---

## Auteur

**Emmanuel KOURAOGO** 
[GitHub](https://github.com/EKOURAOGO) · [Email](mailto:ekouraogo73@gmail.com)
