# Quiz Application — OOP & Streamlit

Application de quiz interactive développée en Python avec une architecture **orientée objet (OOP)** et une interface **Streamlit**.

![Interface principale](IMAGES/Interface_appli.png)

## Fonctionnalités
- Génération de quiz dynamique par domaine (tags)
- Questions à choix unique (radio) et choix multiple (multiselect)
- Scoring proportionnel pour les questions à choix multiple
- Visualisation des résultats par domaine
- Persistance via st.session_state

## Classes OOP (models.py)
| Classe | Rôle |
|--------|------|
| Question | Représente une question |
| QuestionDataset | Singleton — charge le JSON une seule fois |
| QuizGenerator | Génère un quiz filtré par domaine |
| QuizCorrector | Évalue les réponses et calcule les scores |

## Installation
```bash
pip install -r requirments.txt
streamlit run app.py
```

## Auteur
**Emmanuel KOURAOGO** 
