import json
import pandas as pd
import numpy as np
# import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.under_sampling import RandomUnderSampler

# =======================
# 1. Carregar os dados
# =======================


def load_json_to_df(path, orient='index'):
    with open(path, 'r', encoding='utf-8') as f:
        return pd.DataFrame.from_dict(json.load(f), orient=orient)


# Carregamento dos arquivos
jobs_df = load_json_to_df('bases/vagas.json')
prospects_df = load_json_to_df('bases/prospects.json')
applicants_df = load_json_to_df('bases/applicants.json')

# =======================
# 2. Pré-processamento inicial
# =======================

# Expandir as prospecções
expanded_rows = []
for job_id, job_data in prospects_df.iterrows():
    for prospect in job_data['prospects']:
        expanded_rows.append({
            'codigo_vaga': job_id,
            'codigo_candidato': prospect['codigo'],
            'situacao': prospect['situacao_candidado']
        })

prospects_flat = pd.DataFrame(expanded_rows)

# Filtrar contratados vs não
prospects_flat['contratado'] = prospects_flat['situacao'].apply(
    lambda x: 1 if 'contratado' in x.lower() else 0)

# Juntar com dados do candidato
applicants_df['codigo_profissional'] = applicants_df.index
applicants_flat = applicants_df.apply(lambda row: {
    'codigo_candidato': row['infos_basicas']['codigo_profissional'],
    'nivel_profissional': row['informacoes_profissionais']['nivel_profissional'],
    'area_atuacao': row['informacoes_profissionais']['area_atuacao'],
    'nivel_academico': row['formacao_e_idiomas']['nivel_academico'],
    'nivel_ingles': row['formacao_e_idiomas']['nivel_ingles'],
    'nivel_espanhol': row['formacao_e_idiomas']['nivel_espanhol']
}, axis=1).tolist()
applicants_flat = pd.DataFrame(applicants_flat)

# Merge final
df = prospects_flat.merge(applicants_flat, on='codigo_candidato', how='left')

# =======================
# 3. Tratamento dos Dados
# =======================

# 1. Remover linhas onde 'contratado' não for 0 ou 1
df = df[df['contratado'].isin([0, 1])]

# 2. Preencher valores vazios em 'nivel_profissional' com "Desconhecido"
df['nivel_profissional'] = df['nivel_profissional'].replace(
    r'^\s*$', np.nan, regex=True)
df['nivel_profissional'] = df['nivel_profissional'].fillna("Desconhecido")

# 3. Remover linhas onde 'nivel_academico' está vazio
df['nivel_academico'] = df['nivel_academico'].replace(
    r'^\s*$', np.nan, regex=True)
df = df.dropna(subset=['nivel_academico'])

# 4. Preencher valores vazios em 'nivel_ingles' e 'nivel_espanhol' com "Nenhum"
df['nivel_ingles'] = df['nivel_ingles'].replace(r'^\s*$', np.nan, regex=True)
df['nivel_ingles'] = df['nivel_ingles'].fillna("Nenhum")
df['nivel_espanhol'] = df['nivel_espanhol'].replace(
    r'^\s*$', np.nan, regex=True)
df['nivel_espanhol'] = df['nivel_espanhol'].fillna("Nenhum")


def tratar_area(area):
    if pd.isna(area):
        return "Outros"
    area = area.strip()
    if area.startswith("TI") or area.startswith("Relacionamento Técnico"):
        return "TI"
    elif area.startswith("Comercial") or area.startswith("Novos"):
        return "Comercial"
    elif area.startswith("Administrativa"):
        return "Administrativa"
    elif area.startswith("Recursos Humanos"):
        return "Recursos Humanos"
    elif area.startswith("Financeira"):
        return "Financeira"
    elif area.startswith("Gestão"):
        return "Gestão"
    elif area.startswith("Jurídica"):
        return "Jurídica"
    elif area.startswith("Qualidade"):
        return "Qualidade"
    elif area.startswith("Marketing"):
        return "Marketing"
    else:
        return "Outros"


df['area_atuacao_tratada'] = df['area_atuacao'].apply(tratar_area)
df = df.drop('area_atuacao', axis=1)
df = df.rename(columns={'area_atuacao_tratada': 'area_atuacao'})

df_concatenado = df
rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(df_concatenado.drop(
    'contratado', axis=1), df_concatenado['contratado'])
df_balanced = pd.concat([pd.DataFrame(X_resampled), pd.DataFrame(
    y_resampled, columns=['contratado'])], axis=1)
df = df_balanced

# =======================
# 3. Pipeline de Treinamento
# =======================

# Features e target
X = df[['nivel_profissional', 'nivel_academico', 'nivel_ingles', 'nivel_espanhol']]
y = df['contratado']

# Pré-processador: one-hot encoding
categorical_cols = X.columns.tolist()
preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
])

# Modelo
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Treinamento
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Avaliação
y_pred = model.predict(X_test)
# print(classification_report(y_test, y_pred))

# =======================
# 4. Salvando o modelo
# =======================
# joblib.dump(model, 'modelo_contratacao.pkl')
filename = 'modelo_contratacao.pkl'
# pickle.dump(model, open(filename, 'wb'))
joblib.dump(model, 'modelo_contratacao.pkl')
