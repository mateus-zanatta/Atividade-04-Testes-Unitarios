# Responsável: Mateus Zanatta
# Page Object da página inicial "Explorar" (index.html).
from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.titulo = page.get_by_role(
            "heading", name="Descubra sabores incríveis na sua cidade"
        )
        self.saudacao_usuario = page.locator("#userBadge")
        self.cards_restaurantes = page.locator(".rest-card")

    def botao_categoria(self, nome):
        # exact=True evita confundir "Todos" com outro botão que contenha o texto.
        return self.page.get_by_role("button", name=nome, exact=True)

    def filtrar_por_categoria(self, nome):
        self.botao_categoria(nome).click()
