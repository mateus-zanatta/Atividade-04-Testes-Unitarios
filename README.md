# Atividade 4 — Testes Automatizados do LocalEats

Testes unitários (com TDD) e testes funcionais com Playwright para o sistema
[LocalEats](https://local-eats-unisenac.vercel.app/), da Unidade Curricular Qualidade de Software.

O registro completo da atividade está em
[`atividade-04-testes-automatizados.md`](atividade-04-testes-automatizados.md).

## Conteúdo

- `src/regras_localeats.py`: função `calcular_desconto` (Regra 2).
- `tests/test_regras_localeats.py`: testes unitários (TU01 a TU04).
- `tests/test_localeats.py`: testes funcionais com Playwright (TF01 e TF02).
- `pages/`: Page Object Model das telas de login e inicial.
- `evidencias/`: screenshots e traces do Playwright.
- `relatorio-pytest.txt`: resultado da execução dos testes.

## Como executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v
```
