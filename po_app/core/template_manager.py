from typing import Dict, List


class Template:
    def __init__(self, id: str, type_: str, lang: str, name: str, content: str) -> None:
        self.id = id
        self.type = type_
        self.lang = lang
        self.name = name
        self.content = content

    def render(self, ctx: Dict) -> str:
        # TODO: replace with a proper template engine if needed
        out = self.content
        for k, v in ctx.items():
            out = out.replace(f"{{{{{k}}}}}", str(v))
        return out


class TemplateManager:
    def __init__(self, repo):
        self.repo = repo

    def list(self) -> List[Template]:
        return self.repo.fetch_all_templates()

    def get(self, id_: str) -> Template:
        return self.repo.get_template(id_)

    def upsert(self, tpl: Template) -> None:
        self.repo.save_template(tpl)

    def remove(self, id_: str) -> None:
        self.repo.delete_template(id_)

