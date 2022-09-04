from dataclasses import dataclass

@dataclass
class Chapter:
    title: str
    slug: str
    order: int
    chapterno: int
    url: str
    content: str

    def updateContent(self, content):
        self.content = content