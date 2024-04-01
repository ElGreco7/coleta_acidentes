import requests
import urllib3
import datetime
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URLs e Headers
headers_waze = {'Referer': 'https://www.waze.com/pt-BR/live-map'}
waze_url = 'https://www.waze.com/row-rtserver/web/TGeoRSS?bottom=-3.179700819552629&left=-60.37982940673829&ma=200&mj=100&mu=20&right=-59.58881378173829&top=-2.9110532097493453&types=alerts'

headers_windy = {'Referer': 'https://www.windy.com/-3.132/-59.983?rain,-3.760,-59.985,8'}
windy_url  = 'https://node.windy.com/pois/v2/stations/-3.132/-59.983?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDkzMTY3MjIsImlhdCI6MTcwOTE0MzkyMiwiaW5mIjp7InVhIjoiTW96aWxsYVwvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvMTIwLjAuMC4wIFNhZmFyaVwvNTM3LjM2IE9QUlwvMTA2LjAuMC4wIiwiaXAiOiIyMDAuMjQyLjQzLjIwMiJ9fQ.uktVdTZD3w4KRUQdcSev-bbJuoNurXHvhTHoP9buXAY&token2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtYWdpYyI6MzE3LCJpYXQiOjE3MDkxNDM5MjQsImV4cCI6MTcwOTMxNjcyNH0.-qqIsxxCOZPLI5lD2svhYZYFdupOmVXLc1TvCOBWKXI&uid=2d389b75-e7fd-e46c-4fb5-76a2e029c45e&sc=19&pr=0&v=41.2.3&poc=24'

# variavel para armazenar data e horário atual
tempus = datetime.datetime.now()

# variavel para armazenar data da coleta
dia_coleta = tempus.strftime("%d-%m-%Y")

# Funçao de descricao dos dias da semana
def descricao_semana():
    semana = tempus.strftime('%A')
    ds = ''
    if semana == 'Monday':
        ds = 'Segunda-Feira'
    elif semana == 'Tuesday':
        ds = 'Terça-Feira'
    elif semana == 'Wednesday':
        ds = 'Quarta-Feira'
    elif semana == 'Thursday':
        ds = 'Quinta-Feira'
    elif semana == 'Friday':
        ds = 'Sexta-Feira'
    elif semana == 'Saturday':
        ds = 'Sabado'
    elif semana == 'Sunday':
        ds = 'Domingo'
    
    return ds

# Requisição
a = requests.get(waze_url, headers=headers_waze)
b = requests.get(windy_url, headers=headers_windy)

# Transformando em Json
waze = a.json()
windy = b.json()

# variaveis que serão exportadas
acidentes = 0
congest = 0
dia_semana = descricao_semana()

# variaveis de especificacao para acidentes
grave  = 0
leve = 0
interd = 0
# variaveis de especificacao para congestionamento
moderado = 0
intenso = 0
parado = 0

# amazenar valores às variaveis de exportação
for row in waze['alerts']:
        
    if row['type'] == 'ACCIDENT':
        acidentes = acidentes + 1
        if row['subtype'] == 'ACCIDENT_MINOR':
            leve = leve + 1
        elif row['subtype'] == 'ACCIDENT_MAJOR':
            grave  = grave + 1
        elif row['subtype'] == 'ROAD_CLOSED_EVENT':
            interd = interd + 1     
                
    if row['type'] == 'JAM':
        congest = congest + 1
        if row['subtype'] == 'JAM_MODERATE_TRAFFIC':
            moderado = moderado + 1
        elif row['subtype'] == 'JAM_HEAVY_TRAFFIC':
            intenso = intenso + 1
        elif row['subtype'] == 'JAM_STAND_STILL_TRAFFIC':
            parado = parado + 1

for row in windy:
    
    if row['name']== 'Manaus' and row['precip']!= 'None':
        precipitacao = row['precip']
    else:
        precipitacao = 0

# mostra na tela variaveis de importação
print(str(acidentes) + ', ' + str(leve) + ', ' + str(grave) + ', ' + str(interd) + ', ' + str(congest) + ', ' + str(moderado) + ', ' + str(intenso) + ', ' + str(parado) + ', ' + str(precipitacao) + ', ' + dia_semana + ', ' + dia_coleta)

# variavel para armazenar os dados de exportação
dados = [
    [acidentes, leve, grave, interd, congest, moderado, intenso, parado, precipitacao, dia_semana, dia_coleta]
]

# operação para escrever os dados no arquivo csv e confirmar dados salvos no final
with open('dados.csv', 'a', newline='') as objeto:
    writer = csv.writer(objeto)

    for row in dados:
        writer.writerow(row)

print('dados salvos')
