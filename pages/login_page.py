# Responsável: Mateus Zanatta
# Page Object da tela "Entrar | Local Eats" (login.html).
from playwright.sync_api import Page

URL_LOCALEATS = "https://local-eats-unisenac.vercel.app/"


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.aba_criar_conta = page.get_by_role("button", name="Criar Conta")
        # Os <label> da página não estão ligados aos campos (não têm "for"),
        # por isso os campos são localizados pelo placeholder.
        self.campo_nome = page.get_by_placeholder("Seu nome")
        self.campo_email = page.get_by_placeholder("novo@teste.com")
        self.campo_senha = page.get_by_placeholder("Min. 3 caracteres")
        self.botao_registrar = page.get_by_role("button", name="Registrar")

    def abrir(self):
        # Sem usuário logado, o LocalEats redireciona para login.html.
        self.page.goto(URL_LOCALEATS)

    def criar_conta(self, nome, email, senha):
        self.aba_criar_conta.click()
        self.campo_nome.fill(nome)
        self.campo_email.fill(email)
        self.campo_senha.fill(senha)
        self.botao_registrar.click()
