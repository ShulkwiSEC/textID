import os
import re
import collections
import math

class StylometryEngine:
    """
    Forensic engine using Rank-Sync Correlation (v6.0).
    Uses high-dimensional pattern correlation for definitive identity.
    """
    
    # Top 100+ most stable stylometric markers (English + Arabic)
    MARKERS = [
        # --- English (Expanded) ---
        "the", "and", "to", "of", "a", "in", "that", "is", "it", "was", "as", "for", "with", "be", "by", "at", 
        "on", "he", "she", "but", "his", "her", "not", "which", "you", "all", "this", "from", "they", "had", 
        "are", "we", "my", "me", "if", "an", "who", "when", "there", "so", "up", "out", "no", "what", "more", 
        "into", "their", "has", "very", "one", "him", "could", "been", "would", "shall", "should", "will", 
        "only", "do", "can", "than", "then", "its", "our", "were", "them", "some", "these", "your", "his",
        "about", "how", "over", "after", "most", "may", "often", "always", "never", "sometimes", "because",

        # --- Arabic (Function Words & Pronouns) ---
        "من", "في", "على", "إلى", "عن", "مع", "هذا", "هذه", "الذي", "التي", 
        "أن", "إن", "لا", "ما", "لم", "لن", "قد", "كان", "كانت", "كل",      
        "هو", "هي", "هم", "نحن", "أنا", "بعد", "قبل", "عند", "حتى", "إذا",   
        
        # --- Punctuation ---
        ".", ",", ";", ":", "!", "?", "-", "(", ")", "\"", 
        "،", "؛", "؟", "«", "»",

        # --- AI Style Markers ---
        "however", "therefore", "additionally", "moreover", "furthermore", "consequently",
        "overall", "summary", "conclusion", "instance", "example", "notably", "significant",
        "provides", "ensures", "crucial", "essential", "actually", "basically", "literally",
        "delve", "tapestry", "embark", "comprehensive", "versatile", "transform", "pivotal"
    ]

    def __init__(self, data_dir="data"):
        self.registry = {}
        if os.path.exists(data_dir):
            for author in sorted(os.listdir(data_dir)):
                path = os.path.join(data_dir, author)
                if os.path.isdir(path):
                    sig = self._signature(self._load(path))
                    if sig:
                        self.registry[author] = sig

    def _load(self, path):
        content = []
        for file in sorted(os.listdir(path)):
            with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
                content.append(f.read())
        return "\n".join(content).lower()

    def _signature(self, text):
        if not text.strip(): return None
        
        # 1. Forensic Word Vector
        tokens = re.findall(r'\b\w+\b|[.,;:\-!?()\"،؛؟«»]', text)
        counts = collections.Counter(tokens)
        total = len(tokens) or 1
        return [counts.get(m, 0) / total for m in self.MARKERS]

    def _correlate(self, v1, v2):
        # Cosine Similarity: Measure the 'angle' of the habit patterns
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(b * b for b in v2))
        return dot / (mag1 * mag2) if mag1 * mag2 > 0 else 0

    def predict(self, text):
        target_sig = self._signature(text.lower())
        if not target_sig: return []
        
        scores = []
        for author, sig in self.registry.items():
            # Correlate the baseline pattern with the signal
            score = self._correlate(target_sig, sig)
            scores.append((author, score))
            
        # Amplified exponential filter to highlight the dominant pattern
        # Increased to 30 for high-confidence separation
        total = sum(math.exp(s * 30) for _, s in scores) or 1
        return sorted([(a, math.exp(s * 30) / total) for a, s in scores], key=lambda x: x[1], reverse=True)