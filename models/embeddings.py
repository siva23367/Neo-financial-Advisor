'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os
import re
from config.config import load_config

class EmbeddingModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.embeddings_path = "data/embeddings.json"
        self.documents = []
        self.tfidf_matrix = None
        self.is_fitted = False
        self.load_embeddings()
    
    def load_embeddings(self):
        if os.path.exists(self.embeddings_path):
            with open(self.embeddings_path, 'r') as f:
                data = json.load(f)
                self.documents = data.get("texts", [])
                
                if self.documents:
                    self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
                    self.is_fitted = True
        else:
            self.documents = []
            self.tfidf_matrix = None
            self.is_fitted = False
    
    def save_embeddings(self):
        os.makedirs(os.path.dirname(self.embeddings_path), exist_ok=True)
        
        data = {
            "texts": self.documents
        }
        
        with open(self.embeddings_path, 'w') as f:
            json.dump(data, f)
    
    def add_document(self, text, chunks):
        for chunk in chunks:
            # Clean and preprocess text
            cleaned_chunk = self.clean_text(chunk)
            if cleaned_chunk and len(cleaned_chunk.split()) > 3:  # Minimum 3 words
                self.documents.append(cleaned_chunk)
        
        # Retrain TF-IDF with new documents
        if self.documents:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
            self.is_fitted = True
            self.save_embeddings()
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text
    
    def find_similar(self, query, top_k=5, similarity_threshold=0.3):
        if not self.is_fitted or not self.documents:
            return []
        
        # Clean query
        cleaned_query = self.clean_text(query)
        
        # Transform query to TF-IDF
        query_vector = self.vectorizer.transform([cleaned_query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > similarity_threshold:
                results.append(self.documents[idx])
        
        return results

        '''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os
import re
from config.config import load_config

class EmbeddingModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.embeddings_path = "data/embeddings.json"
        self.documents = []
        self.tfidf_matrix = None
        self.is_fitted = False
        self.load_embeddings()
    
    def load_embeddings(self):
        try:
            if os.path.exists(self.embeddings_path):
                with open(self.embeddings_path, 'r') as f:
                    data = json.load(f)
                    self.documents = data.get("texts", [])
                    
                    if self.documents:
                        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
                        self.is_fitted = True
            else:
                self.documents, self.tfidf_matrix, self.is_fitted = [], None, False
        except Exception as e:
            print(f"❌ Error loading embeddings: {e}")
            self.documents, self.tfidf_matrix, self.is_fitted = [], None, False
    
    def save_embeddings(self):
        try:
            os.makedirs(os.path.dirname(self.embeddings_path), exist_ok=True)
            data = {"texts": self.documents}
            with open(self.embeddings_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"❌ Error saving embeddings: {e}")
    
    def add_document(self, text, chunks):
        try:
            for chunk in chunks:
                cleaned_chunk = self.clean_text(chunk)
                if cleaned_chunk and len(cleaned_chunk.split()) > 3:
                    self.documents.append(cleaned_chunk)
            
            if self.documents:
                self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
                self.is_fitted = True
                self.save_embeddings()
        except Exception as e:
            print(f"❌ Error adding document: {e}")
    
    def clean_text(self, text):
        if not text:
            return ""
        try:
            text = re.sub(r'\s+', ' ', text).strip()
            text = re.sub(r'[^\w\s.,!?-]', '', text)
            return text
        except Exception as e:
            print(f"❌ Error cleaning text: {e}")
            return ""
    
    def find_similar(self, query, top_k=5, similarity_threshold=0.3):
        if not self.is_fitted or not self.documents:
            return []
        try:
            cleaned_query = self.clean_text(query)
            query_vector = self.vectorizer.transform([cleaned_query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            top_indices = np.argsort(similarities)[::-1][:top_k]
            results = []
            for idx in top_indices:
                if similarities[idx] > similarity_threshold:
                    results.append(self.documents[idx])
            return results
        except Exception as e:
            print(f"❌ Error finding similar text: {e}")
            return []
