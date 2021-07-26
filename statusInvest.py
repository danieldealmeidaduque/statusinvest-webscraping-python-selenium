import time
import datetime
from selenium import webdriver

# Toggle para executar so uma vez o cabecalho do arquivo de saida
cabecalho = True
umaVez = True

def pega_dados_acao(cod_acao, driver):
    dict_acao = {}
    dict_aux = {}
    dict_atuacao = {}
    dict_balanco = {}

    print(" --   " + cod_acao + "   -- ")
    try:
        driver.get("https://statusinvest.com.br/acoes/" + cod_acao)
    except:
        print("Erro ao acessar o site")
        return None

    try:
        dict_aux["VALOR ATUAL"] = "R$ " + driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[1]/div/div[1]/div/div[1]/strong").text
        dict_aux["MIN. 52 SEMANAS"] = "R$ " + driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[1]/div/div[2]/div/div[1]/strong").text
        dict_aux["MAX. 52 SEMANAS"] = "R$ " + driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[1]/div/div[3]/div/div[1]/strong").text
        dict_aux["VALORIZACAO(12M)"] = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[1]/div/div[5]/div/div[1]/strong").text
    except:
        print("Erro ao pegar a cotacao, valorizacao.. ")
        return None

    try:
        tituloTipo = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[4]/div/div/div[1]/div/div/h3").text

        if tituloTipo == "TIPO":
            dict_aux["TIPO"] = driver.find_element_by_xpath(
                "/html/body/main/div[2]/div/div[4]/div/div/div[1]/div/div/strong").text
        else:
            dict_aux["TIPO"] = "UNIT"

        dict_aux["TAG ALONG"] = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[4]/div/div/div[2]/div/div/div/strong").text.replace(" ", "")
        dict_aux["LIQ. MED. DIARIA"] = "R$ " + driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[4]/div/div/div[3]/div/div/div/strong").text
        dict_aux["PARTICIPACAO NO IBOV"] = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[4]/div/div/div[4]/div/a/div/div/strong").text + "%"
    except:
        print("Erro ao pegar tipo, tag along.. ")
        return None

    try:
        ind_valuation = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[6]/div[2]/div/div[1]").text
        ind_valuation = limpa_dados(ind_valuation)
    except:
        print("Erro ao pegar os indices de valuation")
        return None

    try:
        ind_endividamento = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[6]/div[2]/div/div[2]").text
        ind_endividamento = limpa_dados(ind_endividamento)
    except:
        print("Erro ao pegar os indices de endividamento")
        return None

    try:
        ind_eficiencia = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[6]/div[2]/div/div[3]").text
        ind_eficiencia = limpa_dados(ind_eficiencia)
    except:
        print("Erro ao pegar os indices de eficiencia")
        return None

    try:
        ind_rentabilidade = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[6]/div[2]/div/div[4]").text
        ind_rentabilidade = limpa_dados(ind_rentabilidade)
    except:
        print("Erro ao pegar os indices de rentabilidade")
        return None

    try:
        ind_crescimento = driver.find_element_by_xpath(
            "/html/body/main/div[2]/div/div[6]/div[2]/div/div[5]").text
        ind_crescimento = limpa_dados(ind_crescimento)
    except:
        print("Erro ao pegar os indices de crescimento")
        return None
    
    try:
        atuacao = driver.find_element_by_xpath("/html/body/main/div[5]/div/div[3]/div").text
        atuacao = atuacao.replace("arrow_forward", "").replace("\n\n","\n")
        atuacao = atuacao.split("\n")
        atuacao.pop()
        for i in range(len(atuacao)):
            if i % 2 == 0:
                dict_atuacao[atuacao[i]] = atuacao[i + 1]
    except:
        print("Erro ao pegar setor, subsetor e segmento")
        return None

    try:
        balanco = driver.find_element_by_xpath("/html/body/main/div[5]/div/div[2]").text
        balanco = balanco.replace("format_quote\n", "").replace("help_outline\n","")
        balanco = balanco.split("\n")
        balanco.pop()
        if len(balanco) == 21:
            balanco.insert(19,'-') 
        for i in range(len(balanco)):
            if i % 2 == 0:
                dict_balanco[balanco[i]] = balanco[i + 1]
    except:
        print("Erro ao pegar o balanco patrimonial")
        return None
    
    dict_acao.update({"INDICADORES AUXILIARES" : dict_aux})
    dict_acao.update({"ATUACAO" : dict_atuacao})
    dict_acao.update({"BALANCO" : dict_balanco})
    dict_acao.update(ind_valuation)
    dict_acao.update(ind_endividamento)
    dict_acao.update(ind_eficiencia)
    dict_acao.update(ind_rentabilidade)
    dict_acao.update(ind_crescimento)

    return dict_acao

def iniciaDriver():
    driver = webdriver.Chrome(
        executable_path='ChromeDriver/chromedriver.exe')
    return driver


def limpa_dados(dados):
    # tira lixo
    dados = dados.replace("format_quote\n", "").replace(
        "show_chart\nhelp_outline\n", "").replace("show_chart\nhelp_outline", "")

    # transforma o texto em lista
    lista_dados = dados.split("\n")
    lista_dados.pop()

    # transforma a lista em dicionario
    chavePrincipal = lista_dados.pop(0)
    listaChaves = []
    listaValores = []
    for i in range(len(lista_dados)):
        if i % 2 == 0:
            listaChaves.append(lista_dados[i])
        else:
            listaValores.append(lista_dados[i])

    dict_dados = {}
    dict_dados[chavePrincipal] = dict(
        zip(iter(listaChaves), iter(listaValores)))

    return dict_dados


def escreve_dict_no_arq(dadosAcoes, arq):
    global cabecalho
    global umaVez
    # Escreve o cabecalho com base na primeira acao
    if cabecalho:
        cabecalho = False
        arq.write("COD ACAO;")
        for chaveAcao in dadosAcoes:
            if umaVez:
                umaVez = False
                for chaveIndicador in dadosAcoes[chaveAcao]:                
                    for chaveValores in (dadosAcoes[chaveAcao])[chaveIndicador]:
                        arq.write(chaveValores + ";")
        arq.write("\n")
          
    # Escreve todos dados da acao no arquivo, inclusive seu codigo
    for chaveAcao in dadosAcoes:
        arq.write(chaveAcao + ";")
        for chaveIndicador in dadosAcoes[chaveAcao]:
            for chaveValores in (dadosAcoes[chaveAcao])[chaveIndicador]:
                valor = ((dadosAcoes[chaveAcao])[chaveIndicador])[chaveValores]
                arq.write(valor + ";")
        arq.write("\n")

if __name__ == "__main__":
    # Dicionário principal
    dict_acoes = {}

    # Inicia timer pra saber tempo de execucao do programa
    start = time.time()

    # Executa funcao para iniciar o driver do chrome
    driver = iniciaDriver()

    # Data do dia
    data_dia = datetime.datetime.today()
    dateFormated = data_dia.strftime('%d_%m_%Y')

    # Abre os arquivos
    arqEntrada = open("my_codes.txt", "r")
    arqSaida = open("indicadores_StatusInvest_" + dateFormated + ".csv", "w")

    # Le o arquivo dos codigos das ações e coloca em uma lista
    acoes = arqEntrada.read()
    listaAcoes = list(acoes.split("\n"))

    # Pega os dados para cada acao da lista de acoes
    for acao in listaAcoes:
        auxiliar = pega_dados_acao(acao, driver)
        if auxiliar != None:
            dict_acoes[acao] = auxiliar

    # Escreve os dados de todas acoes no arquivo de saida .csv    
    escreve_dict_no_arq(dict_acoes, arqSaida)

    # Fecha os arquivos e o driver
    arqEntrada.close()
    arqSaida.close()
    driver.quit()

    end = time.time()
    elapsed = end - start
    print("\n\nStatus Invest executou em " + time.strftime("%H:%M:%S",
                                                           time.gmtime(elapsed)) + ". Dia: " + dateFormated + "\n\n")
