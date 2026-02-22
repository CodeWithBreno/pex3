# Diagnóstico de Saúde Geriátrica — Análise Exploratória

Projeto de **extensão universitária** para apoio à enfermeira em Home Care / acompanhamento de idosos. Esta fase contempla **geração de dados sintéticos**, **análise exploratória (EDA)** e **visualizações** para apoio à decisão clínica.

**Dados:** exclusivamente sintéticos (mock data), em conformidade com LGPD e ética em saúde.

---

## Pré-requisitos

- **Python 3.8** ou superior  
- **pip** (gerenciador de pacotes do Python)

Para verificar no seu computador:

```bash
python --version
python -m pip --version
```

---

## Como executar o projeto no seu ambiente

### 1. Clonar ou baixar o repositório

```bash
git clone https://github.com/CodeWithBreno/pex3.git
cd pex3
```

Ou baixe o ZIP do repositório no GitHub, extraia e abra um terminal na pasta `pex3`.

---

### 2. (Opcional) Criar um ambiente virtual

Recomendado para isolar as dependências do projeto:

**Windows (PowerShell ou CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux ou macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Com o ambiente ativado, o prompt deve mostrar `(venv)` no início da linha.

---

### 3. Instalar as dependências

Na pasta do projeto (`pex3`), execute:

```bash
python -m pip install -r requirements.txt
```

Isso instala: `pandas`, `numpy`, `faker`, `matplotlib`, `seaborn` e `jupyter`.

---

### 4. Gerar os dados sintéticos

Execute o script que gera o dataset de acompanhamento (30 pacientes, 6 meses de registros semanais):

```bash
python gerador_dados_pacientes.py
```

Saída esperada:
- Mensagem indicando que o dataset foi exportado.
- Arquivo gerado: **`dados/dados_sinteticos_idosos.csv`** (780 registros).

---

### 5. Executar a análise exploratória (notebook)

**Opção A – Abrir no Jupyter (recomendado para o professor)**

1. Inicie o Jupyter:
   ```bash
   jupyter notebook
   ```
2. No navegador, abra o arquivo **`diagnostico_saude_eda.ipynb`**.
3. No menu: **Cell → Run All** (ou execute as células uma a uma com Shift+Enter).

**Opção B – Executar pela linha de comando (gera notebook com saídas)**

```bash
jupyter nbconvert --to notebook --execute diagnostico_saude_eda.ipynb --output diagnostico_saude_eda_executado.ipynb
```

Depois, abra **`diagnostico_saude_eda_executado.ipynb`** para ver todas as tabelas e gráficos já preenchidos.

---

## Estrutura do projeto

| Arquivo / Pasta | Descrição |
|-----------------|-----------|
| `requirements.txt` | Dependências Python do projeto |
| `gerador_dados_pacientes.py` | Script que gera os dados sintéticos |
| `dados/dados_sinteticos_idosos.csv` | Dataset gerado (criado ao rodar o script) |
| `diagnostico_saude_eda.ipynb` | Notebook de análise exploratória e visualizações |
| `RELATORIO_PROJETO.md` | Relatório completo do projeto (metodologia, justificativas, resultados) |

---

## Resumo do que o projeto faz

1. **Gerador de dados:** Simula 30 idosos com comorbidades (Diabetes, Hipertensão, Nenhuma), com registros semanais de pressão, glicemia, peso e área de curativo, incluindo correlações clínicas (ex.: glicemia alta atrasa cicatrização).
2. **Notebook EDA:** Carrega o CSV, faz análise descritiva, matriz de correlação, correlação glicemia × cicatrização, identifica pacientes com tendência de alta na pressão arterial e gera gráficos de série temporal e dispersão.

Para detalhes metodológicos e justificativas técnicas, consulte o ** [RELATORIO_PROJETO.md](RELATORIO_PROJETO.md)**.

---

## Problemas comuns

- **`pip` não encontrado:** Use `python -m pip` em vez de `pip` (ex.: `python -m pip install -r requirements.txt`).
- **Notebook não abre:** Confirme que o Jupyter foi instalado (`pip install jupyter` ou `pip install -r requirements.txt`) e que está na pasta do projeto ao rodar `jupyter notebook`.
- **Arquivo CSV não encontrado:** Execute primeiro o passo 4 (`python gerador_dados_pacientes.py`) para criar a pasta `dados` e o arquivo `dados_sinteticos_idosos.csv`.

---

**Repositório:** [github.com/CodeWithBreno/pex3](https://github.com/CodeWithBreno/pex3)
