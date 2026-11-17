# Responsável: Mateus Zanatta
# Testes funcionais do LocalEats com Playwright.
import re
from pathlib import Path

from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.login_page import LoginPage

PASTA_EVIDENCIAS = Path(__file__).resolve().parent.parent / "evidencias"


# TF01 - Criar uma conta pela interface e chegar à página inicial
def test_criar_conta_redireciona_para_pagina_inicial(page: Page, novo_usuario):
    login = LoginPage(page)
    login.abrir()
    # Sem login, o sistema leva o visitante para a tela de entrada.
    expect(page).to_have_url(re.compile(r"login\.html$"))

    login.criar_conta(**novo_usuario)

    home = HomePage(page)
    expect(page).to_have_url(re.compile(r"index\.html$"))
    expect(home.saudacao_usuario).to_contain_text("Olá, Mateus")
    expect(home.titulo).to_be_visible()

    page.screenshot(path=PASTA_EVIDENCIAS / "tf01-conta-criada.png", full_page=True)


# TF02 - Selecionar a categoria "Mexicana" e ver apenas restaurantes mexicanos
def test_filtrar_categoria_mexicana_exibe_apenas_restaurantes_mexicanos(
    page: Page, usuario_logado: HomePage
):
    home = usuario_logado

    home.filtrar_por_categoria("Mexicana")

    expect(home.botao_categoria("Mexicana")).to_have_class(re.compile(r"\bactive\b"))
    expect(home.botao_categoria("Todos")).not_to_have_class(re.compile(r"\bactive\b"))
    # Ao clicar, a lista é trocada por "Buscando..."; esperar o primeiro card
    # garante que a lista filtrada já chegou antes de verificar o conteúdo.
    expect(home.cards_restaurantes.first).to_be_visible()
    expect(home.cards_restaurantes.filter(has_not_text="Mexicana")).to_have_count(0)

    page.screenshot(path=PASTA_EVIDENCIAS / "tf02-filtro-mexicana.png", full_page=True)
