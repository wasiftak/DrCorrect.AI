import csv
from spellchecker import SpellChecker

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class MedicalTextProcessor:
    def __init__(self):
        self.spell = SpellChecker(language=None, distance=2) 
        self.known_words = set()

    def _insert_word_into_trie(self, word):
        node = self.trie_root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def load_corpus_from_txt(self, filepath):
        print(f"Loading medical vocabulary from {filepath}...")
        try:
            with open(filepath, mode='r', encoding='utf-8') as infile:
                all_terms = {line.strip() for line in infile if line.strip()}
            
            self.known_words = all_terms
            self.spell.word_frequency.load_words(self.known_words)
            self.trie_root = TrieNode()
            for term in self.known_words:
                self._insert_word_into_trie(term)
            
            print(f"Vocabulary loaded with {len(self.known_words)} medical terms.")
            return True, len(self.known_words)
        except Exception as e:
            print(f"Error loading vocabulary: {e}")
            return False, 0

    def is_known(self, word):
        return word.lower() in self.known_words

    def get_correction_candidates(self, word):
        return self.spell.candidates(word)

    def get_unambiguous_correction(self, word):
        """
        Returns a correction only if there is exactly one candidate.
        """
        candidates = self.spell.candidates(word)
        if candidates and len(candidates) == 1:
            return candidates.pop()
        return None # Return None if there are 0 or more than 1 candidates

    def get_suggestions(self, prefix):
        if not prefix: return []
        node = self.trie_root
        for char in prefix:
            if char not in node.children: return []
            node = node.children[char]
        suggestions = []
        self._dfs_suggest(node, prefix, suggestions)
        return suggestions

    def _dfs_suggest(self, node, current_word, suggestions):
        if len(suggestions) >= 5: return
        if node.is_end_of_word: suggestions.append(current_word)
        for char, child_node in sorted(node.children.items()):
            self._dfs_suggest(child_node, current_word + char, suggestions)