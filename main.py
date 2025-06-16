from pathlib import Path
from model import Document
from plugin_manager import PluginManager


def main():
    plugin_manager = PluginManager(Path("plugins"))
    plugin_manager.load_plugins_from_dir()
    plugin_manager.apply_plugin_actions(Document)
    doc = Document("Hello, world!")
    doc_path = Path("doc_a.txt")
    doc.save(doc_path)
    words_count = doc.count_words()
    print(f"Word count: {words_count}")
    doc_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
