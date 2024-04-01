# Arquivo usado para fazer update, add, delete de propriedades e dados do csv. Usar apenas se souber oque está fazendo.
import pandas as pd

df = pd.read_csv('dados.csv', header=0)

# Para apagar itens do arquivo, não executar
# df.drop(0, inplace=True)

df.rename(columns={'acidente':'acidentes'}, inplace=True)
df.rename(columns={'tipo_acidente':'acidentes_leves'}, inplace=True)
df.rename(columns={'dia_semana':'acidentes_graves'}, inplace=True)
df.rename(columns={'precip':'vias_interditadas'}, inplace=True)

df.rename(columns={'tipo_congest':'congest_moderado'}, inplace=True)
df['congest_intenso'] = None
df['congest_parado'] = None
df['precip'] = None
df['dia_semana'] = None
df['dia_coleta'] = None

print(df.head())

df.to_csv('dados.csv', index=False)
