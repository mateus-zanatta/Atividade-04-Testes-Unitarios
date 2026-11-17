# Responsável: Mateus Zanatta
# Fixtures compartilhadas pelos testes funcionais.
# O pytest carrega este arquivo automaticamente; não é preciso importá-lo.
import uuid

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage

# O LocalEats roda na Vercel e a primeira resposta pode demorar.
# Aumenta o tempo máximo que cada expect() espera (padrão: 5 s).
# Isso NÃO é uma espera fixa: o expect termina assim que a condição é atendida.
expect.set_options(timeout=15_000)


@pytest.fixture
def novo_usuario():
    """Dados de um usuário novo, com e-mail único a cada execução."""
    return {
        "nome": "Mateus Teste",
        "email": f"mateus.teste.{uuid.uuid4().hex[:8]}@teste.com",
        "senha": "senha123",
    }


@pytest.fixture
def usuario_logado(page, novo_usuario):
    """Cria uma conta pela interface e devolve a página inicial já carregada."""
    login = LoginPage(page)
    login.abrir()
    login.criar_conta(**novo_usuario)

    home = HomePage(page)
    # Espera a primeira carga da lista terminar antes de o teste interagir.
    expect(home.cards_restaurantes.first).to_be_visible()
    return home
