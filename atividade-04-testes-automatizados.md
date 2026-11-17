# Atividade 4: Testes Automatizados do LocalEats

## 1. Identificação

| Campo | Informação |
|---|---|
| Unidade Curricular | Qualidade de Software |
| Projeto | LocalEats |
| Sistema testado | https://local-eats-unisenac.vercel.app/ |
| Modalidade | Individual |
| Integrante | Mateus Zanatta |
| Regra unitária escolhida | Regra 2: calcular o desconto do pedido |
| Fluxos funcionais automatizados | Criar conta (TF01) e filtrar por categoria (TF02) |

## 2. Estrutura do diretório

```
atividade-04/
├── atividade-04-testes-automatizados.md   ← este arquivo
├── relatorio-pytest.txt                    ← saída do pytest -v
├── requirements.txt
├── pytest.ini                              ← configuração do pytest
├── src/
│   ├── __init__.py
│   └── regras_localeats.py                 ← função calcular_desconto
├── tests/
│   ├── __init__.py
│   ├── conftest.py                         ← fixtures dos testes funcionais
│   ├── test_regras_localeats.py            ← testes unitários (TU)
│   └── test_localeats.py                   ← testes funcionais (TF)
├── pages/                                  ← Page Object Model (diferencial)
│   ├── __init__.py
│   ├── login_page.py
│   └── home_page.py
└── evidencias/                             ← screenshots e traces (diferencial)
    ├── tf01-conta-criada.png
    ├── tf02-filtro-mexicana.png
    ├── trace-tf01-criar-conta.zip
    └── trace-tf02-filtro-mexicana.zip
```

## 3. Como executar

No PowerShell, dentro da pasta `atividades/atividade-04`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

- Os testes funcionais rodam em modo *headless* (sem abrir a janela). Para ver o navegador: `python -m pytest -v --headed`.
- Para gerar um trace novo: `python -m pytest --tracing on` (os arquivos vão para `test-results/`).
- Para abrir um trace: `python -m playwright show-trace evidencias/trace-tf02-filtro-mexicana.zip`.

## 4. Identificação das responsabilidades

| ID | Integrante | Tipo | Comportamento verificado | Arquivo e função |
|---|---|---|---|---|
| TU01 | Mateus Zanatta | Unitário | Pedido de R$ 150,00 recebe R$ 15,00 de desconto | `tests/test_regras_localeats.py::test_pedido_de_150_reais_recebe_desconto_de_15` |
| TU02 | Mateus Zanatta | Unitário | Pedido abaixo de R$ 100,00 não recebe desconto | `tests/test_regras_localeats.py::test_pedido_abaixo_de_100_reais_nao_recebe_desconto` |
| TU03 | Mateus Zanatta | Unitário (parametrizado) | Casos de borda: R$ 0,00, R$ 99,99, R$ 100,00 e R$ 100,01 | `tests/test_regras_localeats.py::test_desconto_nos_limites_da_regra` |
| TU04 | Mateus Zanatta | Unitário | Valor negativo gera `ValueError` | `tests/test_regras_localeats.py::test_valor_negativo_gera_value_error` |
| TF01 | Mateus Zanatta | Funcional | Criar conta pela interface e chegar à página inicial | `tests/test_localeats.py::test_criar_conta_redireciona_para_pagina_inicial` |
| TF02 | Mateus Zanatta | Funcional | Selecionar a categoria "Mexicana" e ver apenas restaurantes mexicanos | `tests/test_localeats.py::test_filtrar_categoria_mexicana_exibe_apenas_restaurantes_mexicanos` |

> O TU03 aparece 4 vezes no relatório (uma para cada valor do `parametrize`), mas é **um único teste**.
> Os testes funcionais aparecem com o sufixo `[chromium]`, que é o navegador usado pelo pytest-playwright.

## 5. Parte 1: Testes unitários e TDD

### Função implementada

Arquivo `src/regras_localeats.py`:

```python
VALOR_MINIMO_PARA_DESCONTO = 100
PERCENTUAL_DESCONTO = 0.10


def calcular_desconto(valor_pedido):
    if valor_pedido < 0:
        raise ValueError("O valor do pedido não pode ser negativo.")

    if valor_pedido < VALOR_MINIMO_PARA_DESCONTO:
        return 0

    return valor_pedido * PERCENTUAL_DESCONTO
```

### TDD de Mateus Zanatta

**Regra escolhida:** Regra 2: calcular o desconto do pedido (abaixo de R$ 100,00 não há desconto; a partir de R$ 100,00 o desconto é de 10%; a função retorna o valor do desconto; valores negativos geram `ValueError`).

**Primeiro teste escrito:**

```python
def test_pedido_de_150_reais_recebe_desconto_de_15():
    resultado = calcular_desconto(150)
    assert resultado == 15
```

**Por que o teste falhou inicialmente:** o arquivo `src/regras_localeats.py` existia, mas a função `calcular_desconto` ainda não. O pytest nem conseguiu carregar o arquivo de teste:

```
E   ImportError: cannot import name 'calcular_desconto' from 'src.regras_localeats'
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

**Implementação mínima realizada:** apenas o cálculo de 10%, sem nenhuma condição:

```python
def calcular_desconto(valor_pedido):
    return valor_pedido * 0.10
```

Resultado: `1 passed`. Eu esperava que `150 * 0.10` desse um número "quebrado" por causa de ponto flutuante, mas o resultado foi exatamente `15.0` e o teste passou.

**Segundo teste escrito:**

```python
def test_pedido_abaixo_de_100_reais_nao_recebe_desconto():
    resultado = calcular_desconto(80)
    assert resultado == 0
```

Ele falhou porque a implementação mínima dava desconto para qualquer valor:

```
>       assert resultado == 0
E       assert 8.0 == 0
========================= 1 failed, 1 passed in 0.02s ==========================
```

Ajuste: incluir `if valor_pedido < 100: return 0`. Resultado: `2 passed`.

**Testes seguintes (diferenciais):**

- **TU03 (borda, com `parametrize`):** testa R$ 0,00, R$ 99,99, R$ 100,00 e R$ 100,01. A primeira versão comparava com `==` e **falhou** no valor R$ 100,01:

  ```
  E       assert 10.001000000000001 == 10.001
  FAILED tests/test_regras_localeats.py::test_desconto_nos_limites_da_regra[100.01-10.001]
  ```

  A regra estava certa (10% de 100,01 é 10,001). O problema era comparar números decimais com `==`, porque o computador guarda `0.10` de forma aproximada. Correção no teste: `assert resultado == pytest.approx(desconto_esperado)`. Resultado: `6 passed`.
- **TU04 (exceção, com `pytest.raises`):** falhou com `Failed: DID NOT RAISE ValueError`, porque `-10` caía no `if < 100` e retornava `0`. Ajuste: validar `if valor_pedido < 0: raise ValueError(...)` antes das outras regras.

**Melhoria ou refatoração realizada:**

- Os números "mágicos" `100` e `0.10` viraram as constantes `VALOR_MINIMO_PARA_DESCONTO` e `PERCENTUAL_DESCONTO`. Assim, se a regra mudar, o valor é alterado em um lugar só e o código fica autoexplicativo.
- A função ganhou uma docstring com as regras.
- A verificação de valor negativo ficou como primeira linha (*guard clause*): o valor inválido é barrado antes de qualquer cálculo.
- Depois da refatoração os testes foram executados de novo: `7 passed` (TU03 conta como 4 execuções).

## 6. Parte 2: Testes funcionais com Playwright

### Exploração do sistema

Antes de escrever os testes, o LocalEats foi explorado. Comportamentos observados e usados nos testes:

- Sem usuário logado, qualquer página redireciona para `login.html` (título "Entrar | Local Eats").
- Na tela de login há as abas **Entrar** e **Criar Conta**. O cadastro pede nome (placeholder "Seu nome"), e-mail ("novo@teste.com") e senha ("Min. 3 caracteres"), com o botão **Registrar**.
- Após o cadastro, o usuário vai para `index.html`, o cabeçalho mostra **"Olá, <primeiro nome>"** e aparece o título **"Descubra sabores incríveis na sua cidade"**.
- A página inicial tem os botões de categoria **Todos, Italiana, Japonesa, Brasileira e Mexicana**. O botão selecionado recebe a classe CSS `active`.
- Cada restaurante é um card (`.rest-card`) com nome, faixa de preço, culinária, bairro e descrição.

### TF01: Criar conta e chegar à página inicial

Arquivo: `tests/test_localeats.py::test_criar_conta_redireciona_para_pagina_inicial`

1. Acessa o LocalEats e verifica (assertion 1) que foi redirecionado para `login.html`.
2. Clica em **Criar Conta**, preenche nome, e-mail único e senha, e clica em **Registrar**.
3. Verifica (assertions 2 a 4):
   - a URL termina em `index.html`;
   - o cabeçalho mostra "Olá, Mateus";
   - o título "Descubra sabores incríveis na sua cidade" está visível.

O e-mail é gerado com `uuid` a cada execução (`mateus.teste.<8 caracteres>@teste.com`), para o cadastro nunca falhar por e-mail repetido.

### TF02: Filtrar restaurantes pela categoria "Mexicana"

Arquivo: `tests/test_localeats.py::test_filtrar_categoria_mexicana_exibe_apenas_restaurantes_mexicanos`

1. A fixture `usuario_logado` (em `tests/conftest.py`) cria uma conta nova e espera a lista de restaurantes carregar.
2. O teste clica no botão **Mexicana**.
3. Verifica (4 assertions):
   - o botão "Mexicana" tem a classe `active`;
   - o botão "Todos" deixou de ter a classe `active`;
   - existe pelo menos um card de restaurante visível;
   - **nenhum** card deixa de conter o texto "Mexicana".

### Locators utilizados

| Locator | Onde | Por quê |
|---|---|---|
| `get_by_role("button", name="Criar Conta")` | LoginPage | Localiza pelo papel e texto visível, como o usuário enxerga |
| `get_by_placeholder("Seu nome")` (e os outros campos) | LoginPage | Os `<label>` da página não estão ligados aos campos (não têm `for`), então `get_by_label` não funciona |
| `get_by_role("heading", name="Descubra sabores...")` | HomePage | Título principal da página |
| `get_by_role("button", name=..., exact=True)` | HomePage | Botões de categoria, com texto exato |
| `locator("#userBadge")` | HomePage | Área do cabeçalho com a saudação; não tem papel/texto fixo |
| `locator(".rest-card")` | HomePage | Cards de restaurante; não há outro atributo mais estável |

### Sem esperas fixas

Nenhum teste usa `time.sleep` nem `page.wait_for_timeout`. Todas as verificações usam `expect(...)`, que **espera automaticamente** até a condição ser verdadeira (ou até o tempo limite). Como o site está na Vercel e às vezes demora para responder, o tempo limite do `expect` foi aumentado para 15 s em `tests/conftest.py` com `expect.set_options(timeout=15_000)`. Isso não deixa o teste mais lento: o `expect` termina assim que a condição é atendida.

## 7. Explicação individual (Mateus Zanatta): TF02

O TF02 verifica se o filtro de categoria realmente mostra só os restaurantes da categoria escolhida. Escolhi explicá-lo porque ele tem um cuidado de **sincronização** que não é óbvio.

Quando o botão "Mexicana" é clicado, o JavaScript do LocalEats faz duas coisas: troca imediatamente a lista por "Buscando..." e depois pede os restaurantes filtrados para a API. Se eu verificasse logo após o clique que "não existe card sem o texto Mexicana", o teste poderia passar **no momento errado**: enquanto aparece "Buscando...", não existe card nenhum, então "zero cards não mexicanos" seria verdade mesmo se o filtro estivesse quebrado (um falso positivo).

Por isso a ordem das assertions importa:

1. `expect(home.cards_restaurantes.first).to_be_visible()` espera a lista filtrada chegar e garante que há pelo menos um resultado;
2. só depois, `expect(home.cards_restaurantes.filter(has_not_text="Mexicana")).to_have_count(0)` confere que todos os cards exibidos são mexicanos.

O `filter(has_not_text="Mexicana")` pega os cards que **não** contêm a palavra "Mexicana". Se algum restaurante italiano ou japonês aparecesse, esse grupo teria pelo menos 1 elemento e o teste falharia. O teste também não depende da quantidade exata de restaurantes (hoje são 2), então continua válido se o professor cadastrar novos restaurantes mexicanos.

Pelo mesmo motivo, a fixture `usuario_logado` espera a **primeira** carga da lista antes de devolver a página: se o clique em "Mexicana" acontecesse com a carga inicial ainda em andamento, a resposta antiga ("Todos") poderia chegar depois e sobrescrever o filtro.

## 8. Diferenciais implementados

| Diferencial | Onde |
|---|---|
| Terceiro teste unitário para caso de borda | TU03 (R$ 0,00, R$ 99,99, R$ 100,00 e R$ 100,01) |
| Uso de `pytest.raises` | TU04, inclusive conferindo a mensagem com `match=` |
| Parametrização com `pytest.mark.parametrize` | TU03 |
| Organização com Page Object Model | `pages/login_page.py` e `pages/home_page.py` |
| Segundo teste funcional pelo mesmo integrante | TF02 |
| Screenshot da execução | `evidencias/tf01-conta-criada.png` e `evidencias/tf02-filtro-mexicana.png` (gerados pelos próprios testes a cada execução) |
| Trace do Playwright | `evidencias/trace-tf01-criar-conta.zip` e `evidencias/trace-tf02-filtro-mexicana.zip` |
| Registro de uma falha encontrada e corrigida | Seção 9 |

## 9. Falhas encontradas

### Falha encontrada e corrigida (nos testes)

- **Onde:** TU03, valor R$ 100,01.
- **Erro:** `assert 10.001000000000001 == 10.001`.
- **Causa:** números decimais (`float`) são guardados de forma aproximada no computador; `100.01 * 0.10` não dá exatamente `10.001`.
- **Correção:** comparar com `pytest.approx`, que aceita uma diferença minúscula. Não arredondei o valor dentro da função, porque a regra da atividade não pede arredondamento e isso mudaria o comportamento da regra só para "agradar" o teste.

### Defeito observado no sistema (não corrigido, apenas registrado)

- O campo de busca diz **"Buscar por culinária ou localização..."**, mas buscar por uma culinária (ex.: "Japonesa") mostra **"Nenhum restaurante encontrado."**, mesmo existindo restaurantes japoneses. Buscar por um bairro (ex.: "Centro") funciona.
- Pelo código do site (`js/app.js`), o texto digitado é enviado apenas como filtro de `location`. Ou seja, a busca por culinária anunciada no placeholder não está implementada.
- Esse fluxo não foi automatizado como teste funcional porque ele falharia sempre por causa do defeito do sistema, e não de um erro do teste.

## 10. Relatório da execução

O arquivo `relatorio-pytest.txt` contém a saída completa de `python -m pytest -v`. No PowerShell, o comando para gerá-lo novamente é:

```powershell
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

Resultado: **9 testes executados, 9 aprovados, 0 reprovados** (TU01, TU02, TU03 ×4, TU04, TF01 e TF02). Todos os testes da tabela da seção 4 aparecem no relatório.

## 11. Uso de inteligência artificial

**Ferramenta utilizada:** Claude (Anthropic), pelo Claude Code.

**Como a ferramenta foi utilizada:** para ler o enunciado, explorar o LocalEats (HTML, JavaScript e respostas da API), conduzir os passos do TDD executando os testes a cada etapa, escrever os testes funcionais com Page Object Model e montar este Markdown.

**Uma sugestão que precisou ser alterada ou rejeitada:**

- O script usado para **explorar** o site usava `page.wait_for_timeout(3000)` (uma espera fixa de 3 s) depois de cada clique. Essa abordagem foi rejeitada nos testes entregues: além de deixar o teste lento, ela não garante que a lista já carregou. Foi substituída por `expect(...)`, que espera a condição real (ver seção 7).
- A expectativa inicial era de que `150 * 0.10` geraria erro de ponto flutuante. Ao executar, o teste passou; o problema real apareceu em outro valor (R$ 100,01). A sugestão de arredondar o resultado dentro da função foi descartada: a correção foi feita no teste com `pytest.approx` (ver seção 9).
- Com o pytest 9.2 o relatório mostrava um aviso de depreciação vindo do plugin pytest-playwright (não do nosso código). Em vez de esconder o aviso, a versão do pytest foi fixada em 8.4.2 no `requirements.txt`.

**Como o código sugerido foi verificado:**

- Cada passo do TDD foi executado e a falha/sucesso foi conferida antes de seguir (as mensagens de erro reais estão na seção 5).
- Os testes funcionais foram executados 3 vezes seguidas, todas aprovadas, para verificar se eram estáveis.
- As screenshots foram abertas para confirmar visualmente o resultado (ex.: só os restaurantes "Sabor 9" e "Sabor 10", ambos mexicanos, com o botão "Mexicana" destacado).
- Os textos usados nos testes ("Criar Conta", "Registrar", "Olá, ...", "Descubra sabores incríveis na sua cidade", nomes das categorias) foram conferidos no HTML real do LocalEats.
