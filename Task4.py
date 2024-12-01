class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    def find_closest_words(self, word, max_fine=3):
        results = []
        seen_words = set()
        self._dfs(self.root, word, 0, "", 0, max_fine, results, seen_words)
        results.sort(key=lambda x: x[1])
        return [res[0] for res in results]

    def _dfs(self, node, word, index, current_word, fine, max_fine, results, seen_words):
        if fine > max_fine:
            return

        if index == len(word):
            if node.is_end_of_word and current_word not in seen_words:
                results.append((current_word, fine))
                seen_words.add(current_word)
            return
        char = word[index]

        if char in node.children:
            self._dfs(node.children[char], word, index + 1, current_word + char, fine, max_fine, results, seen_words)

        for child_char, child_node in node.children.items():
            if child_char != char:  # Только если символы различны
                self._dfs(child_node, word, index + 1, current_word + child_char,fine + 1, max_fine, results, seen_words)

        for child_char, child_node in node.children.items():
            self._dfs(child_node, word, index + 1, current_word + child_char, fine + 1, max_fine, results, seen_words)

        self._dfs(node, word, index + 1, current_word, fine + 1, max_fine, results, seen_words)

if __name__ == "__main__":
    trie = Trie()
    words = ["apple", "apply", "ape", "apt", "bat", "bath", "cat", "cap"]
    for word in words:
        trie.insert(word)
    input_word = input("Введите слово: ")
    closest_words = trie.find_closest_words(input_word)
    if closest_words:
        print("Ближайшие слова:", closest_words)
    else:
        print("Ближайших слов не найдено.")