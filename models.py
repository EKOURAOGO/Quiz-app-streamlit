import json
import random

# --- 1. La Classe Question ---
class Question:
    """Represents a single quiz question, encapsulant ses données."""
    def __init__(self, data: dict):
        self.question = data.get('question')
        self.choices = data.get('choices')
        self.correct = data.get('correct')
        self.mode = data.get('mode') 
        self.tags = data.get('tags')
        
    def __repr__(self):
        return f"Question(Q='{self.question[:30]}...', Mode='{self.mode}')"

# --- 2. La Classe QuestionDataset (Singleton) ---
class QuestionDataset:
    """
    Singleton class to load quiz questions from a JSON file once.
    """
    _instance = None
    _data = []

    def __new__(cls, file_path="quiz_dataset.json"):
        # La logique de Singleton n'est exécutée qu'une seule fois
        if cls._instance is None or file_path != getattr(cls._instance, '_file_path', None):
            cls._instance = super(QuestionDataset, cls).__new__(cls)
            cls._instance._file_path = file_path
            cls._instance._load_data(file_path)
            cls._instance._unique_tags = cls._instance._extract_unique_tags()
        return cls._instance

    def _load_data(self, file_path):
        """
        Loads data from JSON and converts entries to Question objects.
        """
        if file_path is None:
             self._data = []
             return
             
        try:
            with open(file_path, 'r', encoding='utf-8') as f: 
                raw_data = json.load(f)
            self._data = [Question(q_data) for q_data in raw_data]
        except FileNotFoundError:
            self._data = []
        except Exception:
            self._data = []

    def _extract_unique_tags(self):
        tags = set()
        for q in self._data:
            # Assure que 'tags' est une liste avant d'itérer
            if isinstance(q.tags, list):
                 tags.update(q.tags)
        return sorted(list(tags))
    
    def get_all_questions(self):
        return self._data

    def get_unique_tags(self):
        return self._unique_tags

# --- 3. La Classe QuizGenerator ---
class QuizGenerator:
    """
    Generates a quiz from a dataset filtered by fields/tags.
    """
    def __init__(self, dataset: QuestionDataset):
        self.dataset = dataset

    def generate_quiz(self, selected_tags: list, num_questions=10):
        """Filters questions by tags and selects a random subset."""
        all_questions = self.dataset.get_all_questions()
        
        filtered_questions = [
            q for q in all_questions 
            if any(tag in selected_tags for tag in q.tags)
        ]

        if len(filtered_questions) > num_questions:
            # Assure que le quiz est aléatoire
            return random.sample(filtered_questions, num_questions)
        
        return filtered_questions

# --- 4. La Classe QuizCorrector ---
class QuizCorrector:
    """
    Corrects a quiz and calculates scores based on mode-specific logic.
    """
    @staticmethod
    def calculate_score(question: Question, selected_answers: list) -> float:
        """Calculates score based on the mode ('single' or 'multiple')."""
        
        if question.mode == 'single':
            if selected_answers and question.correct and selected_answers[0] == question.correct[0]:
                return 1.0
            return 0.0

        elif question.mode == 'multiple':
            # Score proportionnel: max(0, (C/TotalC) - (I/TotalC))
            correct_set = set(question.correct)
            selected_set = set(selected_answers)
            
            num_correct_answers = len(correct_set)
            
            if num_correct_answers == 0:
                return 0.0
            
            # C: Réponses correctes sélectionnées
            correct_selected = len(correct_set.intersection(selected_set))
            
            # I: Réponses incorrectes sélectionnées (pénalité)
            incorrect_selected = len(selected_set.difference(correct_set))
            
            score_correct_portion = correct_selected / num_correct_answers
            penalty_portion = incorrect_selected / num_correct_answers
            
            final_score = score_correct_portion - penalty_portion
            
            return max(0.0, final_score)
        
        return 0.0