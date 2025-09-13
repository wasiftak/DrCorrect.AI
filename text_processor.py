from spellchecker import SpellChecker

class TrieNode:
    """A node in the Trie data structure."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class MedicalTextProcessor:
    """Handles all local text processing: suggestions and corrections."""
    def __init__(self):
        self.spell = SpellChecker(language=None, distance=2) 
        self.trie_root = TrieNode()
        # self.term_to_code is no longer used with this dataset

    def _insert_word_into_trie(self, word):
        """Inserts a single word into our Trie data structure."""
        node = self.trie_root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def load_corpus_from_txt(self, filepath):
        """Loads a large vocabulary from a simple text file."""
        print(f"Loading medical vocabulary from {filepath}...")
        try:
            with open(filepath, mode='r', encoding='utf-8') as infile:
                # Read all lines and strip whitespace/newlines
                all_terms = [line.strip() for line in infile]
            
            self.spell.word_frequency.load_words(all_terms)
            self.trie_root = TrieNode()
            for term in all_terms:
                self._insert_word_into_trie(term)
            
            print(f"Vocabulary loaded with {len(all_terms)} medical terms.")
            return True, len(all_terms)
        except Exception as e:
            print(f"Error loading vocabulary: {e}")
            return False, 0
            
    def correct_word(self, word):
        """Corrects a single word using a more reliable 'candidates' approach."""
        candidates = self.spell.candidates(word)
        if candidates:
            return candidates.pop()
        else:
            return word

    def get_suggestions(self, prefix):
        """Gets auto-suggestions for a given prefix using the Trie."""
        if not prefix: return []
        node = self.trie_root
        for char in prefix:
            if char not in node.children: return []
            node = node.children[char]
        suggestions = []
        self._dfs_suggest(node, prefix, suggestions)
        return suggestions

    def _dfs_suggest(self, node, current_word, suggestions):
        """Helper function for DFS traversal to find suggestions."""
        if len(suggestions) >= 5: return
        if node.is_end_of_word: suggestions.append(current_word)
        for char, child_node in sorted(node.children.items()):
            self._dfs_suggest(child_node, current_word + char, suggestions)