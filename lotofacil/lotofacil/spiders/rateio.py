import scrapy
import pandas as pd

class RateioSpider(scrapy.Spider):
    name = 'rateio'
    start_urls = [f'https://www.mazusoft.com.br/lotofacil/resultado.php?concurso={i}' for i in range(2890, 0, -1)]
    all_data = []  # Lista para armazenar todos os dados

    def parse(self, response):
        concurso = response.url.split('=')[-1]
        rows = response.css('table.res-tb tr')[1:6]  # Selecionando apenas as primeiras 5 linhas
        for row in rows:
            cols = row.css('td::text').getall()
            cols = [ele.strip() for ele in cols]
            self.all_data.append([concurso] + cols)

        # Verificando se esta é a última requisição
        if int(concurso) == 1:
            self.save_to_csv()

    def save_to_csv(self):
        # Salvando todos os dados em um único arquivo CSV
        df = pd.DataFrame(self.all_data, columns=['Concurso', 'Faixa', 'Ganhadores', 'Prêmio'])
        df.to_csv('rateio_lotofacil.csv', index=False)
        print("Dados extraídos e salvos com sucesso!")
