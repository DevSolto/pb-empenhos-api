# sagres-crawler

Script em Python para extrair **dados detalhados de empenhos** do sistema SAGRES Cidadão (TCE-PB), consumindo os dados da API pública por período de tempo e salvando localmente.

## 🎯 Objetivo

Coletar todos os empenhos emitidos por uma unidade gestora em um período (ex: janeiro a março de 2025), e para cada empenho encontrado, buscar os dados completos por meio de chamadas específicas da API.

---

## 📦 O que o script faz

1. Para cada mês no período desejado:
   - Faz requisições paginadas para listar os empenhos (`/funcoes/empenhos`).
   - Para cada empenho:
     - Extrai `numero_empenho` e `codigo_unidade_orcamentaria`.
     - Dispara nova requisição para obter os dados detalhados do empenho (`/funcoes/empenhos/{numero_empenho}`).
2. Salva os dados detalhados:
   - Em arquivos `.json` por mês ou por unidade gestora.
   - Ou (opcional) exporta para `.csv`.

---

## ✅ Pré-requisitos

- Python 3.9+
- Bibliotecas:

```bash
pip install requests pandas tqdm
```

---

## ⚙️ Como usar

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/sagres-crawler
cd sagres-crawler
```

2. Configure os parâmetros no arquivo `config.py`:
```python
UNIDADE_GESTORA = "201157"
DATA_INICIAL = "202501"  # AAAAMM
DATA_FINAL = "202503"
```

3. Execute:
```bash
python main.py
```

---

## 🧾 Estrutura da API utilizada

- **Listagem de empenhos (resumo):**
  ```
  GET /api/municipal/despesas/funcoes/empenhos
      ?unidades_gestoras=UG
      &page=N
      &size=50
      &ano_mes=AAAAMM
  ```

- **Detalhamento de empenho:**
  ```
  GET /api/municipal/despesas/funcoes/empenhos/{numero_empenho}
      ?unidades_gestoras=UG
      &codigo_unidade_orcamentaria=XXX
      &ano_mes=AAAAMM
  ```

---

## 🗃️ Saída esperada

- Arquivos `.json` contendo os empenhos detalhados por mês.
- (Opcional) Arquivo `.csv` com os dados agregados.

---

## 🛠️ Possibilidades futuras

- Exportação para banco de dados (SQLite/PostgreSQL).
- Análise e dashboards via Jupyter.
- Suporte a múltiplas unidades gestoras.