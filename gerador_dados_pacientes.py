"""
gerador_dados_pacientes.py
==========================
Script de geração de dados sintéticos para acompanhamento de idosos em Home Care.
Projeto de extensão universitária - Diagnóstico de Saúde Geriátrica.

Conformidade: LGPD e ética em saúde — NENHUM dado real; apenas simulação por código.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
from typing import List
import os

# Semente para reprodutibilidade (essencial em pesquisa e auditoria)
np.random.seed(42)
Faker.seed(42)
fake = Faker("pt_BR")


def gerar_pacientes(n_pacientes: int = 30) -> pd.DataFrame:
    """
    Gera a tabela de pacientes com perfil geriátrico realista.
    
    Justificativa: Idade 65-95 reflete a faixa típica de idosos em acompanhamento
    domiciliar; comorbidades Diabetes/Hipertensão são as mais prevalentes e
    impactam diretamente pressão, glicemia e cicatrização.
    """
    ids = [f"PAC_{i:03d}" for i in range(1, n_pacientes + 1)]
    idades = np.random.randint(65, 96, size=n_pacientes)
    generos = np.random.choice(["M", "F"], size=n_pacientes, p=[0.45, 0.55])
    # Distribuição realista: mais hipertensão, depois diabetes, depois nenhuma
    comorbidades = np.random.choice(
        ["Diabetes", "Hipertensão", "Nenhuma"],
        size=n_pacientes,
        p=[0.35, 0.45, 0.20],
    )
    return pd.DataFrame({
        "id_paciente": ids,
        "idade": idades,
        "genero": generos,
        "comorbidade": comorbidades,
    })


def gerar_serie_semanal(
    id_paciente: str,
    idade: int,
    comorbidade: str,
    data_inicio: datetime,
    n_semanas: int = 26,
) -> List[dict]:
    """
    Gera série temporal semanal para um paciente, com correlações clínicas embutidas.
    
    Correlações programadas:
    - Diabetes → maior variabilidade na glicemia (picos e vales).
    - Hipertensão → tendência de PA mais alta e variável.
    - Glicemia alta → estagnação ou lentidão na redução do tamanho do curativo
      (evidência clínica: hiperglicemia prejudica cicatrização).
    """
    registros = []
    # Valores iniciais por comorbidade (baseline realista)
    pa_sist_base = 125 + (15 if comorbidade == "Hipertensão" else 0) + np.random.uniform(-10, 10)
    pa_diast_base = 78 + (8 if comorbidade == "Hipertensão" else 0) + np.random.uniform(-5, 5)
    glic_base = 100 + (30 if comorbidade == "Diabetes" else 0) + np.random.uniform(-15, 15)
    peso_base = 68 + np.random.uniform(-12, 15)
    # Área de curativo em cm²: começa entre 8 e 25 (casos típicos de escara/úlcera)
    area_curativo = np.random.uniform(8, 25)
    
    # Parâmetros de "velocidade de cicatrização" base (redução semanal em cm²)
    # Quanto maior a idade, tendência a cicatrizar mais devagar (literatura geriátrica)
    taxa_cicatrizacao_base = 0.15 - (idade - 70) * 0.002  # ajuste por idade
    taxa_cicatrizacao_base = max(0.03, min(0.25, taxa_cicatrizacao_base))
    
    for semana in range(n_semanas):
        data = data_inicio + timedelta(weeks=semana)
        
        # Pressão arterial: tendência suave + ruído; hipertensos com mais variância
        ruido_sist = np.random.normal(0, 12 if comorbidade == "Hipertensão" else 7)
        ruido_diast = np.random.normal(0, 8 if comorbidade == "Hipertensão" else 5)
        # Pequena deriva temporal (simula "pacientes que pioram" ou "silent rise")
        deriva = np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2]) * (semana / 20)
        pa_sist = max(90, min(180, pa_sist_base + ruido_sist + deriva * 2))
        pa_diast = max(60, min(110, pa_diast_base + ruido_diast + deriva))
        
        # Glicemia: diabéticos com picos e maior variância (simula descontrole)
        if comorbidade == "Diabetes":
            # Picos aleatórios em algumas semanas (descontrole glicêmico)
            pico = 60 * np.random.binomial(1, 0.25) if np.random.random() < 0.3 else 0
            ruido_glic = np.random.normal(0, 35)
        else:
            pico = 0
            ruido_glic = np.random.normal(0, 15)
        glicemia = max(70, min(350, glic_base + ruido_glic + pico))
        
        # Peso: leve flutuação semanal (realista em idosos)
        peso = max(45, min(120, peso_base + np.random.normal(0, 0.8)))
        
        # Curativo: redução semanal, MAS desacelerada quando glicemia alta
        # Justificativa: hiperglicemia retarda cicatrização (mecanismos inflamatórios e de reparo)
        fator_glicemia = 1.0
        if glicemia > 180:
            fator_glicemia = 0.3  # forte atraso
        elif glicemia > 140:
            fator_glicemia = 0.6  # atraso moderado
        elif glicemia > 120:
            fator_glicemia = 0.85
        reducao = taxa_cicatrizacao_base * area_curativo * fator_glicemia * (0.8 + 0.4 * np.random.random())
        area_curativo = max(0.5, area_curativo - reducao)
        
        registros.append({
            "id_paciente": id_paciente,
            "data": data.strftime("%Y-%m-%d"),
            "pressao_sistolica": round(pa_sist, 1),
            "pressao_diastolica": round(pa_diast, 1),
            "glicemia_mg_dL": round(glicemia, 1),
            "peso_kg": round(peso, 1),
            "area_curativo_cm2": round(area_curativo, 2),
        })
    
    return registros


def main():
    """Orquestra a geração e exportação do dataset sintético."""
    n_pacientes = 30
    data_inicio = datetime(2024, 1, 1)
    n_semanas = 26  # ~6 meses
    
    print("Gerando tabela de pacientes...")
    df_pacientes = gerar_pacientes(n_pacientes)
    
    print("Gerando séries temporais de acompanhamento semanal...")
    todas_visitas = []
    for _, row in df_pacientes.iterrows():
        visitas = gerar_serie_semanal(
            row["id_paciente"],
            row["idade"],
            row["comorbidade"],
            data_inicio,
            n_semanas,
        )
        todas_visitas.extend(visitas)
    
    df_visitas = pd.DataFrame(todas_visitas)
    
    # Merge para incluir idade, gênero e comorbidade em cada registro (facilita EDA)
    df_final = df_visitas.merge(
        df_pacientes,
        on="id_paciente",
        how="left",
    )
    
    # Ordenação para leitura e análises temporais
    df_final = df_final.sort_values(["id_paciente", "data"]).reset_index(drop=True)
    
    os.makedirs("dados", exist_ok=True)
    caminho = os.path.join("dados", "dados_sinteticos_idosos.csv")
    df_final.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"Dataset exportado: {caminho}")
    print(f"Shape: {df_final.shape[0]} registros, {df_final.shape[1]} colunas")
    return df_final


if __name__ == "__main__":
    main()
