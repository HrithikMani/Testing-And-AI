import os
import re

class PodLoader:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.elements = {}
        self.verbs = {}
        # Pre-load everything on init
        self._load_all_pods()

    def _parse_pod(self, src):
        """Parses a single .pod file content."""
        # Normalize newlines
        src = src.replace('\r\n', '\n')
        if not src.startswith('\n'):
            src = '\n' + src

        # Verb regex: ^$\n^@(\w+)$(.*?)\n^$
        # Matches @Verb blocks
        for m in re.findall(r'^$\n^@(\w+)$(.*?)\n^$', src, re.DOTALL | re.MULTILINE):
            self.verbs[m[0]] = m[1].strip()

        # Element regex: ^$\n^([-+*\d]+:)?(\w+):(.*?)^$
        # Matches timeout:name:definition blocks
        for m in re.findall(r'^$\n^([-+*\d]+:)?(\w+):(.*?)^$', src, re.DOTALL | re.MULTILINE):
            name = m[1]
            definition = m[2].strip()
            self.elements[name] = definition

    def _load_all_pods(self):
        """Walks the directory and loads all .pod files."""
        if not os.path.exists(self.root_dir):
            print(f"Warning: Pod directory {self.root_dir} does not exist.")
            return

        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.pod'):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            self._parse_pod(f.read())
                    except Exception as e:
                        print(f"Failed to load {full_path}: {e}")

    def get_element(self, name):
        """Returns the definition for an element name."""
        return self.elements.get(name)

    def get_verb(self, name):
        """Returns the definition for a verb."""
        return self.verbs.get(name)

    def search_elements(self, query):
        """Fuzzy search for element names."""
        query = query.lower()
        return [k for k in self.elements.keys() if query in k.lower()]
