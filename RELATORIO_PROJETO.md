# Relatório do Projeto de Extensão Universitária  
## Diagnóstico de Saúde Geriátrica e Análise Exploratória

---

## 1. Identificação do Projeto

| Item | Descrição |
|------|------------|
| **Título** | Diagnóstico de Saúde Geriátrica e Análise Exploratória |
| **Modalidade** | Projeto de extensão universitária |
| **Contexto** | Apoio à enfermeira em Home Care / Acompanhamento de pacientes idosos crônicos |
| **Fase** | Diagnóstico de Saúde Geriátrica e Análise Exploratória (EDA) |
| **Dados** | Exclusivamente sintéticos (mock data), em conformidade com LGPD e ética em saúde |

---

## 2. Resumo

Este projeto desenvolveu uma pipeline de **Data Science e Health Analytics** para simular e analisar dados de acompanhamento de idosos em cenário domiciliar. Foram realizadas três etapas principais: (1) **geração de dados sintéticos** com correlações clínicas realistas (comorbidades, glicemia e cicatrização); (2) **análise exploratória (EDA)** com estatística descritiva, matriz de correlação e identificação de padrões de risco (ex.: tendência de alta na pressão arterial); (3) **visualização** para apoio à decisão da enfermeira (séries temporais e gráficos de dispersão). Todo o código foi comentado com justificativas técnicas e estatísticas para articulação entre teoria e prática no relatório acadêmico.

---

## 3. Contexto e Objetivos

### 3.1 Contexto

A enfermeira atende idosos em regime de **Home Care** e acompanhamento crônico, registrando variáveis como pressão arterial, glicemia, peso e evolução de curativos (ex.: escaras/úlceras). Anotações em papel e planilhas isoladas dificultam a visualização de **tendências ao longo do tempo** (ex.: subida silenciosa da pressão) e a relação entre **controle glicêmico e cicatrização**. O projeto visa demonstrar como dados organizados e análises exploratórias podem apoiar a prática clínica.

### 3.2 Objetivos

- Gerar um **dataset sintético** realista de acompanhamento semanal por 6 meses, com correlações clínicas embutidas (Diabetes, Hipertensão, glicemia × cicatrização).
- Realizar **análise exploratória** (EDA): descritiva, correlações e identificação de pacientes com tendência de risco (pressão em alta).
- Produzir **visualizações** úteis para a enfermeira: evolução temporal de pressão e glicemia por perfil, e relação entre idade/glicemia e cicatrização.
- Garantir **conformidade ética e LGPD**: uso exclusivo de dados sintéticos, sem dados reais de pacientes.

---

## 4. Conformidade Ética e LGPD

- **Nenhum dado real** de pacientes foi utilizado. Todos os registros são gerados por código (bibliotecas `numpy`, `faker` e lógica própria).
- O uso de **dados sintéticos** evita exposição de informações pessoais e atende às boas práticas de privacidade (LGPD) e de ética em pesquisa em saúde.
- Em uma futura etapa com dados reais, seria necessário aprovação de comitê de ética e tratamento dos dados conforme política de segurança da instituição.

---

## 5. Metodologia

A metodologia seguiu três passos alinhados às tarefas solicitadas:

1. **Passo 1 – Data Engineering & Augmentation:** desenvolvimento do script `gerador_dados_pacientes.py` para criação do dataset sintético e exportação em CSV.
2. **Passo 2 – Análise Exploratória (EDA):** desenvolvimento do notebook Jupyter `diagnostico_saude_eda.ipynb` para carregamento, análise descritiva, correlações e análise de risco.
3. **Passo 3 – Visualização e Comunicação:** inclusão no mesmo notebook de gráficos de linha (séries temporais) e de dispersão (scatter) para apoio à decisão.

As justificativas das técnicas (Pearson, regressão linear para tendência, séries temporais, etc.) estão comentadas no código e resumidas ao final do notebook e neste relatório.

---

## 6. Estrutura do Projeto

```
pex3/
├── requirements.txt                    # Dependências Python (pandas, numpy, faker, matplotlib, seaborn, jupyter)
├── gerador_dados_pacientes.py          # Script de geração de dados sintéticos
├── dados/
│   └── dados_sinteticos_idosos.csv     # Dataset gerado (780 registros, 10 colunas)
├── diagnostico_saude_eda.ipynb         # Notebook de EDA e visualizações
├── diagnostico_saude_eda_executado.ipynb  # Versão do notebook com saídas já executadas
└── RELATORIO_PROJETO.md                # Este relatório
```

---

## 7. Passo 1 – Geração de Dados Sintéticos

### 7.1 Objetivo

Produzir um dataset que simule **6 meses** de acompanhamento **semanal** de idosos, com variáveis clínicas realistas e **correlações lógicas** entre comorbidades e desfechos (pressão, glicemia, cicatrização).

### 7.2 Implementação

O script **`gerador_dados_pacientes.py`**:

- **Pacientes:** Gera 30 pacientes com:
  - **ID:** `PAC_001` a `PAC_030`
  - **Idade:** entre 65 e 95 anos (faixa geriátrica típica)
  - **Gênero:** M/F com proporção aproximada 45%/55%
  - **Comorbidade:** Diabetes (35%), Hipertensão (45%), Nenhuma (20%), refletindo prevalência comum em idosos

- **Acompanhamento semanal (26 semanas):** Para cada paciente, gera um registro por semana com:
  - **Data** (série semanal a partir de uma data inicial)
  - **Pressão sistólica e diastólica** (mmHg)
  - **Glicemia** (mg/dL)
  - **Peso** (kg)
  - **Área do curativo** (cm²), simulando ferida/úlcera que reduz ao longo do tempo

### 7.3 Correlações Clínicas Embutidas (Justificativa Técnica)

O gerador foi programado para refletir evidências da literatura e da prática clínica:

| Correlação | Implementação no código | Justificativa |
|------------|-------------------------|---------------|
| **Diabetes → maior variação na glicemia** | Diabéticos recebem ruído maior e picos aleatórios de glicemia em algumas semanas | Descontrole glicêmico é comum em idosos diabéticos; a variabilidade é maior que em não diabéticos. |
| **Hipertensão → PA mais alta e variável** | Baseline de PA aumentado e desvio-padrão maior no ruído semanal | Hipertensos têm níveis basais mais altos e maior variabilidade visitas a visitas. |
| **Glicemia alta → lentidão na cicatrização** | Redução semanal da área do curativo é multiplicada por um fator &lt; 1 quando glicemia &gt; 140 ou &gt; 180 mg/dL | Hiperglicemia prejudica mecanismos de reparo tecidual; feridas cicatrizam mais devagar com glicemia descontrolada. |
| **Idade → cicatrização mais lenta** | Taxa base de redução da área ajustada negativamente pela idade | Em geriatria, idade avançada está associada a menor capacidade de cicatrização. |

Assim, o dataset não é apenas aleatório: ele contém **padrões que a análise exploratória deve ser capaz de identificar** (por exemplo, correlação negativa entre glicemia média e redução da área do curativo).

### 7.4 Saída

- Arquivo gerado: **`dados/dados_sinteticos_idosos.csv`**
- Conteúdo: 780 linhas (30 pacientes × 26 semanas) e 10 colunas (id_paciente, data, pressao_sistolica, pressao_diastolica, glicemia_mg_dL, peso_kg, area_curativo_cm2, idade, genero, comorbidade).
- **Reprodutibilidade:** uso de `np.random.seed(42)` e `Faker.seed(42)` para que a mesma execução gere sempre o mesmo dataset.

---

## 8. Passo 2 – Análise Exploratória (EDA)

### 8.1 Carregamento e Preparação

No notebook **`diagnostico_saude_eda.ipynb`**:

- O CSV é carregado com **pandas** (`pd.read_csv`) com encoding `utf-8-sig`.
- A coluna **data** é convertida para **datetime** para permitir ordenação e análises temporais.
- Os dados são ordenados por **id_paciente** e **data** para garantir consistência em cálculos de tendência.

### 8.2 Análise Descritiva

- **Tamanho da amostra:** número de pacientes e total de registros (visitas).
- **Distribuição por comorbidade e por gênero:** contagem de pacientes em cada categoria (perfil da população sintética).
- **Estatísticas descritivas** (média, desvio-padrão, mín, máx, quartis) das variáveis numéricas: pressão sistólica e diastólica, glicemia, peso, área do curativo, idade.
- **Verificação de valores ausentes:** em dados sintéticos espera-se zero missings; em cenário real essa etapa orienta imputação ou exclusão.

**Justificativa:** A estatística descritiva é a base da EDA; caracteriza a população antes de qualquer inferência e é padrão em relatórios de saúde (perfil da população atendida).

### 8.3 Identificação de Padrões e Correlações

- **Matriz de correlação de Pearson:** calculada entre as variáveis numéricas (pressão sistólica, diastólica, glicemia, peso, área do curativo, idade). Exibida em **heatmap** (triângulo inferior) para facilitar leitura.
- **Correlação glicemia × velocidade de cicatrização:**  
  - Por paciente, são calculados: **glicemia média** no período e **redução total da área do curativo** (área inicial − área final).  
  - A correlação de Pearson entre essas duas variáveis é calculada. Espera-se **r &lt; 0**: maior glicemia média associada a menor redução da área (cicatrização mais lenta), refletindo a regra embutida no gerador.

**Justificativa:** O coeficiente de Pearson mede associação linear; em saúde é amplamente usado para explorar relações entre variáveis contínuas (ex.: controle glicêmico e desfecho de ferida).

### 8.4 Análise de Risco – Pressão Arterial “Silenciosa”

- Para cada paciente, é ajustada uma **regressão linear** da pressão sistólica em função do número da semana (0, 1, 2, …).
- O **coeficiente angular (slope)** representa a tendência média de variação da PA por semana (positivo = PA subindo ao longo do tempo).
- Pacientes com slope **≥ 0,3 mmHg/semana** são sinalizados como tendo **tendência de alta** na pressão arterial.
- Esses casos podem passar despercebidos em anotações de papel, pois a subida é gradual.

**Justificativa:** Regressão linear sobre a série temporal é uma forma simples e interpretável de quantificar tendência; útil para triagem de pacientes que merecem revisão clínica ou monitoramento mais próximo.

---

## 9. Passo 3 – Visualização e Comunicação de Dados

### 9.1 Gráficos de Linha (Séries Temporais)

- São escolhidos **dois pacientes** de perfis diferentes: um com **Diabetes** e outro com **Hipertensão**.
- Para cada um, são plotados em **subplots**:
  - Evolução da **pressão sistólica e diastólica** ao longo das semanas.
  - Evolução da **glicemia** ao longo das semanas (com linha de referência para glicemia de jejum, quando aplicável).
- Objetivo: permitir à enfermeira **comparar visualmente** a evolução de pressão e glicemia entre perfis e ao longo do tempo.

**Justificativa:** Gráficos de linha são a forma clássica de visualizar séries temporais em saúde; facilitam a identificação de tendências e picos.

### 9.2 Gráficos de Dispersão (Scatter)

- **Idade × redução da área do curativo:** cada ponto é um paciente; eixo Y = redução total da área (cm²) no período.
- **Glicemia média × redução da área do curativo:** mesmo eixo Y; eixo X = glicemia média do paciente no período.
- Objetivo: comunicar de forma intuitiva que **maior idade** ou **pior controle glicêmico** podem estar associados a **menor redução da ferida** (cicatrização mais lenta ou menor ganho no período).

**Justificativa:** Scatter plots permitem visualizar a relação entre duas variáveis contínuas e são adequados para comunicação com equipe não técnica.

### 9.3 Considerações para o Relatório Acadêmico

O notebook inclui uma seção em markdown resumindo as **justificativas** das técnicas utilizadas (estatística descritiva, correlação de Pearson, regressão linear para tendência, séries temporais, scatter plot), para apoio à redação do relatório descritivo do projeto de extensão e à articulação entre teoria e prática.

---

## 10. Tecnologias Utilizadas

| Tecnologia | Uso no projeto |
|------------|----------------|
| **Python** | Linguagem principal dos scripts e do notebook |
| **pandas** | Leitura do CSV, manipulação de tabelas, agregações e séries temporais |
| **numpy** | Geração de números aleatórios, regressão (polyfit), máscaras para heatmap |
| **faker** | Geração de dados fictícios (locale pt_BR; usado na estrutura do gerador) |
| **matplotlib** | Construção dos gráficos (linha e dispersão) |
| **seaborn** | Heatmap de correlação e tema visual dos gráficos |
| **Jupyter** | Notebook interativo para EDA e documentação do fluxo de análise |

Todas as dependências estão listadas em **`requirements.txt`** com versões mínimas recomendadas.

---

## 11. Como Executar o Projeto

1. **Instalar dependências**
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Gerar os dados sintéticos**
   ```bash
   python gerador_dados_pacientes.py
   ```
   Isso cria/sobrescreve `dados/dados_sinteticos_idosos.csv`.

3. **Executar a análise exploratória**
   - Abrir **`diagnostico_saude_eda.ipynb`** no Jupyter (ou no VS Code / Cursor com suporte a notebooks) e executar as células em ordem, **ou**
   - Executar o notebook em linha de comando (gera versão com saídas):
     ```bash
     jupyter nbconvert --to notebook --execute diagnostico_saude_eda.ipynb --output diagnostico_saude_eda_executado.ipynb
     ```
   O arquivo **`diagnostico_saude_eda_executado.ipynb`** contém todas as saídas (tabelas e gráficos) já preenchidas.

---

## 12. Resultados e Conclusões

- **Dataset sintético:** 30 pacientes, 26 semanas cada, com variáveis clínicas realistas e correlações embutidas (Diabetes, Hipertensão, glicemia × cicatrização, idade × cicatrização).
- **EDA:** Análise descritiva da população, matriz de correlação e correlação específica glicemia × redução da área do curativo evidenciam os padrões simulados.
- **Risco:** A identificação de pacientes com tendência de alta na pressão sistólica (slope ≥ 0,3 mmHg/semana) ilustra como a análise de séries temporais pode apoiar a detecção de padrões que anotações em papel não revelam facilmente.
- **Visualização:** Gráficos de linha e de dispersão oferecem suporte à comunicação com a enfermeira e à tomada de decisão baseada em evidências visuais.

O projeto atende aos requisitos da fase de **Diagnóstico de Saúde Geriátrica e Análise Exploratória**, utilizando apenas dados sintéticos em conformidade com LGPD e ética em saúde, e fornece base documentada e reproduzível para relatório acadêmico e possível extensão futura com dados reais (mediante aprovação ética e adequação à LGPD).

---

## 13. Referências e Notas

- **LGPD:** Lei nº 13.709/2018 – tratamento de dados pessoais.
- **Ética em pesquisa em saúde:** Resolução CNS 466/2012 e normas do Comitê de Ética em Pesquisa (CEP).
- **Dados sintéticos:** Utilizados para demonstração e ensino; não substituem estudos com dados reais quando o objetivo for inferência sobre populações reais.

---

*Documento gerado no âmbito do projeto de extensão universitária – Diagnóstico de Saúde Geriátrica e Análise Exploratória.*
