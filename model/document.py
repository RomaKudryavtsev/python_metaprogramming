from pathlib import Path


class Document:
    def __init__(self, content: str = ""):
        self.content = content

    def load(self, file_path: Path):
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        try:
            with file_path.open("r", encoding="utf-8") as file:
                self.content = file.read()
            print(f"Document loaded from {file_path}")
            return self
        except Exception as e:
            print(f"Error loading document from {file_path}: {e}")
            raise

    def save(self, file_path: Path):
        try:
            with file_path.open("w", encoding="utf-8") as file:
                file.write(self.content)
            print(f"Document saved to {file_path}")
            return self
        except Exception as e:
            print(f"Error saving document to {file_path}: {e}")
            raise

    def get_content(self) -> str:
        return self.content

    def __repr__(self):
        display_content = (
            self.content[:50] + "..." if len(self.content) > 50 else self.content
        )
        return f'<Document: "{display_content}">'
