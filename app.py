import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from models import QuestionDataset, QuizGenerator, QuizCorrector, Question

# Définitions des classes DUMMY pour la sécurité
class DummyDataset:
    def get_unique_tags(self): return ["Python", "SQL", "Statistique"]
class DummyQuestion:
    def __init__(self, q="", choices=[], correct=[], tags=[], mode="single"):
        self.question = q
        self.choices = choices
        self.correct = correct
        self.tags = tags
        self.mode = mode
class DummyQuizCorrector:
    @staticmethod
    def calculate_score(question, user_answers): return 0.5
class DummyQuizGenerator:
    def __init__(self, dataset): pass
    def generate_quiz(self, fields, num): 
        return [DummyQuestion(f"Question {i+1} de {f}", ["Vrai", "Faux"], ["Vrai"], [f]) for i, f in enumerate(fields)]

# Importation des modèles réels (tentative)
try:
    from models import QuestionDataset, QuizGenerator, QuizCorrector, Question
except ImportError as e:
    QuestionDataset = DummyDataset
    QuizGenerator = DummyQuizGenerator
    QuizCorrector = DummyQuizCorrector
    Question = DummyQuestion


# ==============================
# CONFIG GLOBALE
# ==============================
st.set_page_config(
    page_title="APPLICATION GENERATEUR DE QUIZ",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        #'Report a bug': "ekouraogo73@gmail.com",
        'About': "Cette application permet de générer et corriger des quiz interactifs, en utilisant Python, OOP et Streamlit. Elle gère les questions à choix unique et multiple, calcule les scores et affiche les résultats en temps réel."
    }
)
sns.set_theme(context="notebook", style="whitegrid")

# ---------- STYLES (cartes + sidebar) ----------
STYLES = """
<style>
/* Fond global transparent sauf la barre de navigation */
body, .main, .block-container { 
    background-color: transparent;  /* Arrière-plan transparent pour l'ensemble de l'application */
    color: #e2e8f0;  /* Texte en gris clair */
}

/* La barre de navigation (header) avec un fond bleu foncé */
header {
    background-color: #1e293b;  /* Fond bleu foncé pour la barre de navigation */
}

/* Conteneur et rythme */
.block-container {padding-top: 1.2rem; max-width: 1200px;}
hr { border-color: rgba(255,255,255,0.06); }

/* Cartes question (transparent) */
.q-card {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 0;
    overflow: hidden;
    background: transparent;  /* Rendre les cartes transparentes */
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    margin-bottom: 18px;
}

.q-card:hover {
    transform: scale(1.05);  /* Zoom léger sur la carte */
    box-shadow: 0 8px 18px rgba(0,0,0,0.35);  /* Ombre plus marquée */
}

/* En-tête de chaque carte */
.q-card__head {
    background: linear-gradient(90deg, #1e293b, #0f172a);  /* Conserver le dégradé bleu foncé dans l'en-tête des cartes */
    color: white;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,0.12);
}

/* Contenu des cartes */
.q-card__body { padding: 14px 16px; color: #e2e8f0; }
.q-card__head-title{ flex: 1; font-weight: 700; white-space: normal; word-break: break-word; letter-spacing:.1px; }
.q-card__head-title span{ font-weight: 500; }

/* Badge mode */
.q-chip {
    font-size: 12px; font-weight: 700;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 6px 12px; border-radius: 999px;
    backdrop-filter: blur(2px);
}

/* Bloc "réponse attendue" */
.q-answer {
    border-left: 4px solid #1e293b;
    padding: 10px 12px; border-radius: 10px;
    background: transparent; color: #e2e8f0; /* Rendre l'arrière-plan des réponses transparent */
}

/* Renforcer la lisibilité des états Streamlit */
div.stAlert { border-radius: 12px; }
div.stAlert[data-baseweb="notification"] { border: 1px solid rgba(255,255,255,0.08); }
div.stAlert:has(svg[aria-label="error"]) { background: linear-gradient(180deg, #3a1f23, #2b171a); }
div.stAlert:has(svg[aria-label="warning"]) { background: linear-gradient(180deg, #3a301f, #2b2317); }
div.stAlert:has(svg[aria-label="check-circle-fill"]) { background: linear-gradient(180deg, #1f3a2b, #172b21); }

/* === SIDEBAR : cartes via expanders stylés === */
section[data-testid="stSidebar"] details {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 14px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.25);
    background: rgba(255,255,255,0.03);
}

section[data-testid="stSidebar"] details > summary {
    list-style: none;
    background: linear-gradient(90deg, #1e293b, #0f172a);  /* Conserver le fond dégradé bleu dans la sidebar */
    color: #fff;
    font-weight: 800;
    letter-spacing: .2px;
    padding: 12px 14px;
    cursor: default;
    user-select: none;
    border-bottom: 1px solid rgba(255,255,255,0.12);
}

section[data-testid="stSidebar"] details > summary::-webkit-details-marker { display:none; }

section[data-testid="stSidebar"] details[open] > div {
    padding: 12px 14px 16px 14px;
    background: rgba(255,255,255,0.03);
}

section[data-testid="stSidebar"] label { color:#e2e8f0 !important; }

/* === HERO BANNER (plein largeur contenu) === */
.hero {
    background: linear-gradient(135deg, #1e293b, #0f172a);  /* Laissez cette barre avec le dégradé bleu */
    padding: 32px 40px;
    border-radius: 18px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 22px rgba(0,0,0,0.15);
    width: 100%;
    margin: 30px 0 35px 0;
}

@media (max-width: 640px){
    .hero { padding: 24px; border-radius: 14px; }
}

/* Dock d'action collant */
.st-dock {
    position: sticky; bottom: 12px; z-index: 50;
    margin-top: 16px;
}
.st-dock-inner{
    backdrop-filter: blur(6px);
    background: transparent;  /* Rendre le fond du dock transparent */
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 10px;
    display:flex; justify-content:center;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# === Celebration après rerun (toujours) ===
if st.session_state.get('just_submitted'):
    st.balloons()  # 🎈
    total = float(st.session_state.get('total_score', 0.0))
    n = len(st.session_state.get('quiz_questions', [])) or 1
    st.toast(f"🎉 Quiz corrigé — note {(total/n)*10:.2f}/10", icon="✅")
    st.session_state.just_submitted = False

# ==============================
# CLASSE VUE
# ==============================
class QuizView:
    def __init__(self, dataset: QuestionDataset): # type: ignore
        self.dataset = dataset
        self.all_tags = dataset.get_unique_tags() or []

        if 'quiz_generated' not in st.session_state:
            self.reset_quiz(initial_load=True)
        if 'quiz_history' not in st.session_state:
            st.session_state.quiz_history = []
        # Initialisation de l'ID de course si manquant
        if 'quiz_run_id' not in st.session_state:
            st.session_state.quiz_run_id = str(datetime.now().timestamp())

    def reset_quiz(self, initial_load: bool = False):
        st.session_state.quiz_questions = []
        st.session_state.quiz_generated = False
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        st.session_state.scores = {}
        st.session_state.total_score = 0.0
        st.session_state.num_questions = st.session_state.get('num_questions', 10)
        st.session_state.last_selected_fields = []
        # Mise à jour de l'ID de course
        st.session_state.quiz_run_id = str(datetime.now().timestamp()) 
        if not initial_load:
            st.rerun()

    # Génère le quiz et prépare l'état
    def generate_quiz(self, selected_fields: list, num_questions: int = 10):
        if not selected_fields:
            st.warning("Sélectionne au moins un domaine.")
            return

        if st.session_state.get('quiz_generated', False) and not st.session_state.get('quiz_submitted', False):
            st.warning("Un quiz est déjà en cours. Soumets-le ou réinitialise.")
            return

        generator = QuizGenerator(self.dataset)
        try:
            questions = generator.generate_quiz(selected_fields, num_questions=num_questions)
        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")
            return

        if not questions:
            st.error("Aucune question trouvée pour les domaines sélectionnés.")
            return

        if st.session_state.get("shuffle_choices", True):
            for q in questions:
                if hasattr(q, "choices") and isinstance(q.choices, list):
                    random.shuffle(q.choices)

        st.session_state.quiz_questions = questions
        st.session_state.quiz_generated = True
        st.session_state.quiz_submitted = False
        
        # MISE À JOUR DE L'ID DE COURSE ET RÉINITIALISATION DES RÉPONSES
        st.session_state.quiz_run_id = str(datetime.now().timestamp()) 
        st.session_state.user_answers = {i: [] for i in range(len(questions))}
        
        st.session_state.scores = {}
        st.session_state.total_score = 0.0
        st.session_state.last_selected_fields = selected_fields

        st.success(f"✅ Quiz de {len(questions)} questions généré !")
        st.rerun()

    # -------- Résumé métriques (Affichage classique)
    def _display_summary_and_score(self):
        num_questions = len(st.session_state.quiz_questions)
        total_score = float(st.session_state.total_score)
        max_score = float(num_questions) if num_questions else 1.0
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0.0
        note_sur10 = (total_score / max_score) * 10 if max_score > 0 else 0.0

        # Message d'encouragement
        if percentage >= 80:
            encouragement = "🎉 Excellent travail! Continue comme ça!"
        elif percentage >= 50:
            encouragement = "Bien joué! Mais il y a encore des progrès à faire."
        else:
            encouragement = "Pas de panique! Tu peux le faire. Un peu plus d'effort!"

        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px; padding: 24px 32px;
            margin-top: 12px; margin-bottom: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.25);
        ">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <h3 style="margin:0; font-size:20px; color:#e2e8f0;">Synthèse de la correction</h3>
          </div>
          <p style="color:#94a3b8; font-size:13px; margin:0 0 16px 0;">Aperçu global du résultat</p>
          <div style="display:flex; justify-content:space-around; text-align:center; color:#e2e8f0;">
            <div><p style="opacity:0.7; font-size:12px; margin:0;">Score (%)</p>
                <p style="font-size:26px; font-weight:700; margin:4px 0;">{percentage:.1f}%</p></div>
            <div><p style="opacity:0.7; font-size:12px; margin:0;">Note</p>
                <p style="font-size:26px; font-weight:700; margin:4px 0;">{note_sur10:.2f}</p>
                <span style="background:rgba(34,197,94,0.25); color:#d1fae5; font-size:11px; padding:2px 8px; border-radius:10px;">sur 10.00</span></div>
            <div><p style="opacity:0.7; font-size:12px; margin:0;">Questions</p>
                <p style="font-size:26px; font-weight:700; margin:4px 0;">{num_questions}</p></div>
          </div>
          <p style="color:#e2e8f0; font-size:14px; margin-top:20px;">{encouragement}</p>
        </div>
        """, unsafe_allow_html=True)


    # -------- Rendu d’une carte question
    def question_card(self, i: int, q: Question, disabled_state: bool): # type: ignore
        mode_label = "Choix unique" if getattr(q, "mode", "single") == "single" else "Choix multiples"

        st.markdown(
            f"""
            <div class="q-card">
                <div class="q-card__head">
                    <div class="q-card__head-title">
                        Question n°{i+1} : <span>{q.question}</span>
                    </div>
                    <div class="q-chip">{mode_label}</div>
                </div>
                <div class="q-card__body">
            """,
            unsafe_allow_html=True
        )

        # 🌟 CLÉ BASÉE SUR L'ID DE COURSE
        key_prefix = f"q_{i}_answer_{st.session_state.quiz_run_id}" 
        current_answer = st.session_state.user_answers.get(i, [])

        # Si c'est une question à choix unique (radio boutons)
        if getattr(q, "mode", "single") == 'single':
            placeholder = "--- Sélectionne une réponse ---"
            options_with_placeholder = [placeholder] + (q.choices or [])
            default_index = 0
            if current_answer and current_answer[0] in options_with_placeholder:
                default_index = options_with_placeholder.index(current_answer[0])

            selection = st.radio(
                " ", options_with_placeholder, key=key_prefix, index=default_index,
                disabled=disabled_state, label_visibility="collapsed"
            )
            st.session_state.user_answers[i] = [] if selection == placeholder else [selection]
        else:
            # Pour une question à choix multiples, on utilise des cases à cocher
            selected_answers = []
            for choice in q.choices or []:
                # 🌟 CLÉ RENFORCÉE (ajoute le choix au préfixe)
                checkbox_key = f"{key_prefix}_choice_{choice}" 
                
                selected_answers.append(st.checkbox(
                    choice, 
                    key=checkbox_key, 
                    value=choice in current_answer, 
                    disabled=disabled_state
                ))

            st.session_state.user_answers[i] = [q.choices[j] for j in range(len(selected_answers)) if selected_answers[j]]

        # Si le quiz a été soumis, on affiche la correction
        if st.session_state.quiz_submitted:
            self._display_correction(i, q)

        st.markdown("</div></div>", unsafe_allow_html=True)

    def show_quiz(self):
        if not st.session_state.quiz_generated:
            return

        if st.session_state.quiz_submitted:
            st.header("CORRECTIONS DU QUIZ")
            self._display_summary_and_score()
        else:
            st.header(f"QUESTIONS ({len(st.session_state.quiz_questions)})")

        answered = sum(1 for a in st.session_state.user_answers.values() if len(a) > 0)
        total = len(st.session_state.quiz_questions)
        st.caption(f"Progression : {answered}/{total} répondues")
        st.progress(0 if total == 0 else answered/total)

        for i, q in enumerate(st.session_state.quiz_questions):
            self.question_card(i, q, disabled_state=st.session_state.quiz_submitted)  # Appel à la méthode `question_card`

    def _display_correction(self, index: int, question: Question): # type: ignore
        score = float(st.session_state.scores.get(index, 0.0))
        if score >= 0.99:
            st.success(f"✔️ Correct ({score:.2f}/1.00)")
        elif score > 0.0:
            st.warning(f"⚠️ Partiel ({score:.2f}/1.00)")
        else:
            st.error(f"❌ Incorrect ({score:.2f}/1.00)")

        with st.expander("Voir la réponse attendue", expanded=False):
            correct_data = getattr(question, "correct", None)
            if isinstance(correct_data, list):
                correct_text = ", ".join(str(c) for c in correct_data if c)
            elif isinstance(correct_data, str):
                correct_text = correct_data.strip()
            else:
                correct_text = ""
            if not correct_text:
                correct_text = "— Aucune donnée disponible —"
            st.markdown(f"<div class='q-answer'><strong>Réponses attendues :</strong><br>{correct_text}</div>", unsafe_allow_html=True)

    def submit_and_correct(self):
        if not st.session_state.quiz_generated or st.session_state.quiz_submitted:
            return
        total_score = 0.0
        scores = {}
        for i, q in enumerate(st.session_state.quiz_questions):
            user_selection = st.session_state.user_answers.get(i, [])
            score = QuizCorrector.calculate_score(q, user_selection)
            scores[i] = float(score)
            total_score += float(score)
        st.session_state.scores = scores
        st.session_state.total_score = float(total_score)
        st.session_state.quiz_submitted = True

        # Historique
        try:
            st.session_state.quiz_history.append({
                "date": datetime.now(),
                "score": float(total_score),
                "total": len(st.session_state.quiz_questions),
                "tags": st.session_state.get("last_selected_fields", [])
            })
        except Exception:
            pass

        st.session_state.just_submitted = True
        st.rerun()

    def _display_performance_by_tag(self):
        questions = st.session_state.quiz_questions
        scores = st.session_state.scores
        
        selected_tags_for_quiz = st.session_state.get("last_selected_fields", [])
        
        tag_scores = {tag: 0.0 for tag in selected_tags_for_quiz}
        tag_counts = {tag: 0 for tag in selected_tags_for_quiz}
        
        if not selected_tags_for_quiz:
            st.info("Aucun domaine sélectionné pour générer le quiz. La performance par tag ne peut être affichée.")
            return

        for i, q in enumerate(questions):
            score = scores.get(i, 0.0)
            tags_of_question = getattr(q, 'tags', [])
            
            for tag in tags_of_question:
                if tag in selected_tags_for_quiz: 
                    tag_scores[tag] = tag_scores.get(tag, 0.0) + score
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        final_tags = [tag for tag in selected_tags_for_quiz if tag_counts.get(tag, 0) > 0]
        
        # 1. Vérifiez s'il reste des tags
        if not final_tags:
            st.info("Aucune question valide n'a pu être associée aux domaines sélectionnés pour l'analyse de performance.")
            return
            
        # 2. Construisez le DataFrame
        scores_by_tag_df = pd.DataFrame({
            'Tag': final_tags,
            'Score Total': [tag_scores[tag] for tag in final_tags],
            'Nombre Questions': [tag_counts[tag] for tag in final_tags]
        })
        scores_by_tag_df['Score Moyen'] = scores_by_tag_df['Score Total'] / scores_by_tag_df['Nombre Questions']

        # 3. VÉRIFICATION CRITIQUE : VÉRIFIEZ SI LE DATAFRAME EST VIDE AVANT DE VISUALISER
        if scores_by_tag_df.empty:
            st.info("Le DataFrame de performance par domaine est vide. Aucune visualisation possible.")
            return
            
        # 4. Affichage du diagramme (le reste de votre code de visualisation...)
        st.markdown("---")
        st.header("Performance par domaine")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # --- Diagramme en Donut (Plotly Express) ---
            donut_fig = px.pie(
                scores_by_tag_df, 
                values='Score Total', 
                names='Tag', 
                title='Contribution au score total',
                hole=.4, 
                color_discrete_sequence=px.colors.sequential.Viridis 
            )
            
            # Ici, l'accès est sécurisé car scores_by_tag_df n'est pas vide
            donut_fig.update_traces(
                # La colonne 'Score Moyen' doit exister, ce qui est le cas
                customdata=scores_by_tag_df[['Score Moyen']].values,
                hovertemplate="<b>%{label}</b><br>Score Total: %{value:.2f}<br>Score moyen: %{customdata[0]:.2f}/1.0<extra></extra>",
                textposition='inside'
            )
            
            donut_fig.update_layout(
                title_x=0.5,
                showlegend=True,
                template="plotly_dark",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(donut_fig, use_container_width=True)

        # ... (le code pour le diagramme radar suit)
        with col2:
            if len(final_tags) < 3:
                 st.warning(f"3 domaines ou plus ({len(final_tags)} disponibles) sont nécessaires pour un diagramme radar significatif.")
                 st.caption(f"Le diagramme radar est une simple ligne ou un point avec seulement {len(final_tags)} domaine(s).")
            else:
                categories = scores_by_tag_df['Tag'].tolist()
                performance = scores_by_tag_df['Score Moyen'].tolist()
                
                categories.append(categories[0])
                performance.append(performance[0])

                radar_fig = go.Figure(
                    data=[
                        go.Scatterpolar(
                            r=performance,
                            theta=categories,
                            fill='toself',
                            name='Score Moyen (max 1.0)',
                            line_color='#2980b9' 
                        )
                    ],
                    layout=go.Layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1.0], 
                                gridcolor="#64748b",
                                linecolor="#64748b"
                            ),
                            angularaxis=dict(
                                linecolor="#64748b",
                                tickfont=dict(size=10)
                            )
                        ),
                        showlegend=False,
                        title='Score moyen par domaine',
                        margin=dict(l=20, r=20, t=50, b=20),
                        template="plotly_dark"
                    )
                )

                radar_fig.update_layout(title_x=0.5) 
                st.plotly_chart(radar_fig, use_container_width=True)

        st.caption("Le Diagramme en donut montre la distribution du **score total**. Le Diagramme Radar affiche le **score moyen normalisé** (max 1.0) pour chaque domaine.")
            
    def show_visualization(self, num_questions: int):
        if not st.session_state.quiz_submitted:
            return
        
        # 1. VISUALISATION BARRES DE SCORES PAR QUESTION 
        scores_df = pd.DataFrame({
            'Question': [f'Q{i+1}' for i in range(num_questions)],
            'Score': [st.session_state.scores.get(i, 0.0) for i in range(num_questions)]
        })
        scores_df['Statut'] = scores_df['Score'].apply(
            lambda s: 'Correct' if s >= 0.99 else ('Partiel' if s > 0 else 'Incorrect')
        )
        st.header("Résultats détaillés")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(
            x='Question', y='Score', hue='Statut', data=scores_df, dodge=False,
            palette={'Correct': '#2e7d32', 'Partiel': '#ef6c00', 'Incorrect': '#c62828'}, ax=ax
        )
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("Score (max 1.0)")
        ax.set_xlabel("")
        ax.set_title("Score par question")
        st.pyplot(fig)
        csv = scores_df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Télécharger les scores (CSV)", data=csv, file_name="scores_quiz.csv", mime="text/csv")
        
        # 2. NOUVEL APPEL POUR LA PERFORMANCE PAR DOMAINE
        self._display_performance_by_tag()


# ==============================
# EN-TÊTE – STYLE BLEU (remplacé par #0f172a)
# ==============================
st.markdown("""
<div class="hero">
    <div style="font-size:34px; font-weight:700; margin-bottom:6px; display:flex; align-items:center; justify-content:center; gap:10px;">
        📚 GENERATEUR DE QUIZ INTERACTIF
    </div>
    <div style="font-size:16px; opacity:0.9;">
        Testez vos connaissances, question après question.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================
# DATASET & INIT
# ==============================

# Initialisation des classes pour l'application
try:
    dataset = QuestionDataset("quiz_dataset.json") 
    quiz_view = QuizView(dataset)
except Exception as e:
    st.error(f"Erreur d'initialisation du dataset: {e}. Vérifiez 'quiz_dataset.json' et 'models.py'. Mode démo actif.")
    
    class AppSpecificDummyView(QuizView):
        def __init__(self, dataset):
            super().__init__(dataset)
        
        def generate_quiz(self, fields, num):
            st.warning("Mode démo: la génération de quiz utilise des questions factices.")
            st.session_state.quiz_questions = QuizGenerator(self.dataset).generate_quiz(fields, num)
            st.session_state.quiz_generated = True
            st.session_state.quiz_submitted = False
            st.session_state.user_answers = {i: [] for i in range(len(st.session_state.quiz_questions))}
            st.session_state.last_selected_fields = fields
            st.session_state.quiz_run_id = str(datetime.now().timestamp()) 
            st.success(f"✅ Quiz de {len(st.session_state.quiz_questions)} questions généré (mode démo)!")
            st.rerun()

        def show_visualization(self, num_questions: int):
            st.warning("Mode démo: les visualisations par question sont désactivées. Affichage de la performance par tag démo.")
            self._display_performance_by_tag()
        
        def _display_performance_by_tag(self):
            demo_tags = st.session_state.get("last_selected_fields", ["Démo1", "Démo2"])
            if len(demo_tags) < 2:
                 demo_tags = ["Démo1", "Démo2"]

            scores_by_tag_df = pd.DataFrame({
                'Tag': demo_tags,
                'Score Total': [0.6 * 5, 0.8 * 5] if len(demo_tags) >= 2 else [0.7 * 10], 
                'Nombre Questions': [5, 5] if len(demo_tags) >= 2 else [10]
            })
            scores_by_tag_df['Score Moyen'] = scores_by_tag_df['Score Total'] / scores_by_tag_df['Nombre Questions']
            
            st.markdown("---")
            st.header("🎯 Performance par Domaine (Tag) [DEMO]")
            col1, col2 = st.columns([1, 1])

            with col1:
                donut_fig = px.pie(scores_by_tag_df, values='Score Total', names='Tag', title='Contribution au Score Total', hole=.4, template="plotly_dark")
                st.plotly_chart(donut_fig, use_container_width=True)
            
            with col2:
                if len(demo_tags) < 3:
                     st.warning(f"3 domaines ou plus ({len(demo_tags)} disponibles) sont nécessaires pour un diagramme radar significatif.")
                else:
                    categories = scores_by_tag_df['Tag'].tolist()
                    performance = scores_by_tag_df['Score Moyen'].tolist()
                    categories.append(categories[0])
                    performance.append(performance[0])
                    radar_fig = go.Figure(data=[go.Scatterpolar(r=performance, theta=categories, fill='toself', name='Score Moyen (max 1.0)', line_color='#2980b9')], template="plotly_dark", layout=go.Layout(polar=dict(radialaxis=dict(range=[0, 1.0]))))
                    radar_fig.update_layout(title='Score Moyen Normalisé par Domaine')
                    st.plotly_chart(radar_fig, use_container_width=True)

    dataset = QuestionDataset(None) 
    quiz_view = AppSpecificDummyView(dataset)


# ==============================
# SIDEBAR — cartes stylées (expanders)
# ==============================
with st.sidebar:
    # ---- Carte 1 : Commandes
    with st.expander("⚙️ Commandes", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Réinitialiser", use_container_width=True):
                quiz_view.reset_quiz()
        with col2:
            disable_generate = st.session_state.get('quiz_generated', False) and not st.session_state.get('quiz_submitted', False)
            if st.button("✨ Générer", disabled=disable_generate, use_container_width=True):
                quiz_view.generate_quiz(
                    st.session_state.get('last_selected_fields', []),
                    num_questions=st.session_state.get('num_questions', 10)
                )

    # ---- Carte 2 : Configuration du quiz
    with st.expander("🧭 Configuration du quiz", expanded=True):
        if not quiz_view.all_tags:
            st.warning("Aucun tag disponible dans le dataset.")
            selected_fields = []
        else:
            default_tags = st.session_state.get(
                'last_selected_fields',
                quiz_view.all_tags[:2] if len(quiz_view.all_tags) >= 2 else quiz_view.all_tags
            )
            selected_fields = st.multiselect(
                "🎯 Domaines :",
                options=quiz_view.all_tags,
                default=default_tags,
                key="multiselect_tags"
            )
            if 'multiselect_tags' in st.session_state:
                st.session_state.last_selected_fields = st.session_state.multiselect_tags

            st.session_state.num_questions = st.slider(
                "📝 Nombre de questions",
                min_value=3, max_value=30,
                value=st.session_state.get('num_questions', 10),
                step=1,
                key="num_questions_slider"
            )
            st.checkbox("🔀 Mélanger l’ordre des choix", value=True, key="shuffle_choices")

            with st.expander("Aide rapide", expanded=False):
                st.markdown(
                    "- **Choix unique** : coche une réponse.\n"
                    "- **Choix multiple** : sélectionne toutes les bonnes.\n"
                    "- Tu peux **réinitialiser** à tout moment."
                )

    # ---- Carte 3 : Historique
    with st.expander("🕘 Historique des sessions", expanded=True):
        if st.session_state.get("quiz_history"):
            rows = [{
                "date": h["date"].strftime("%Y-%m-%d %H:%M") if hasattr(h["date"], "strftime") else str(h["date"]),
                "score": f'{h["score"]:.2f}/{h["total"]}',
                "tags": ", ".join(h.get("tags", []))
            } for h in reversed(st.session_state["quiz_history"][-10:])]
            st.table(rows)
        else:
            st.write("Aucun historique")

# ==============================
# CONTENU
# ==============================
quiz_view.show_quiz()

if st.session_state.get('quiz_generated', False) and not st.session_state.get('quiz_submitted', False):
    st.markdown("---")
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("✅ Soumettre et corriger", use_container_width=True):
            quiz_view.submit_and_correct()

if st.session_state.get('quiz_submitted', False):
    quiz_view.show_visualization(len(st.session_state.quiz_questions))
        
    st.markdown("---")
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("🔄 Recommencer un nouveau quiz", use_container_width=True):
            quiz_view.reset_quiz()