from model import Document


# When we add functions to the Document class, we need to ensure that the function receives an instance of Document as its first argument.
def count_words(document: Document) -> int:
    print("Executing word_counter plugin: Counting words...")
    content = document.get_content()
    words = content.split()
    return len(words)


PLUGIN_ACTIONS = [
    {
        "type": "add_method",
        "name": "count_words",
        "function": count_words,
    },
]
