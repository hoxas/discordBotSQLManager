import sqlite3, datetime, numpy, openpyxl, pandas as pd

def getYear():
    try:
        year = datetime.datetime.now().year
    except Exception:
        return 'Error Retrieving Year'
    else:         
        return year

def con():
    connection = sqlite3.connect('cacao.db')
    cursor = connection.cursor()
    def commit():
        try:
            connection.commit()
            connection.close()
        except Exception as e:
            print(e)
            return(e)
    return connection, cursor, commit

def mainfunction (inp):
    year = getYear()
    connection, cursor, commit = con()

    # separando input pelas virgulas
    inplist = inp.split(',')
    i = 0
    while i < len(inplist) - 1:
        inplist[i] = inplist[i].strip()
        i += 1

    # erro se lista < 7 itens
    if len(inplist) < 7:
        return 'Faltam argumentos!'

    # com instagram ou 8 parametros
    if len(inplist) == 8:
        # add @ se não estiver presente
        if inplist[1][0] != '@':
            inplist[1] = f"@{inplist[1]}"

        # grupo e sexo para maiúsculo
        inplist[2] = inplist[2].upper()
        inplist[3] = inplist[3].upper()
        
        # adicionando o ano à data se não estiver presente
        i = 5
        while i < 7:
            if len(inplist[i]) < 8:
                inplist[i] = f'{inplist[i]}/{str(year)}'
            i += 1
        
        # inserindo na tabela pedidos
        try:
            insert = f"INSERT INTO pedidos ('Nome','Instagram','Grupo','Sexo','Valor','Data Pedido','Data Entrega') VALUES ('{inplist[0]}', '{inplist[1]}', '{inplist[2]}', '{inplist[3]}', '{inplist[4]}', '{inplist[5]}', '{inplist[6]}')"
            cursor.execute(insert)
        except Exception as e:
            print(e)
            return e

        # tirando ; do ultimo item se presente
        inplist[7] = inplist[7].rstrip(';')

        # separando itens distintos e quantidades
        itenspedidos = inplist[7].split(';')
        i = 0
        while i < len(itenspedidos):
            itenspedidos[i] = itenspedidos[i].split('-')
            itenspedidos[i][0] = itenspedidos[i][0].strip()
            itenspedidos[i][1] = itenspedidos[i][1].strip()
            i += 1
        
        # selecionando colunas de acordo com itens
        i = 0
        colunas = ''
        while i < len(itenspedidos):
            if i < len(itenspedidos) - 1:
                colunas += f"'{itenspedidos[i][1]}',"
            else:
                colunas += f"'{itenspedidos[i][1]}'"
            i += 1

        # selecionando quantidade de itens
        i = 0
        quantidades = ''
        while i < len(itenspedidos):
            if i < len(itenspedidos) - 1:
                quantidades += itenspedidos[i][0] + ','
            else:
                quantidades += itenspedidos[i][0]
            i += 1
        
        # inserindo itens distintos e suas quantidades na tabela itenspedidos
        try:
            insert = f"INSERT INTO itensPedidos ({colunas}) VALUES ({quantidades})"
            cursor.execute(insert)
        except Exception as e:
            print(e)
            return e
    
    #sem instagram ou 7 parametros
    if len(inplist) == 7:
        # grupo e sexo para maiúsculo
        inplist[1] = inplist[1].upper()
        inplist[2] = inplist[2].upper()
        
        # adicionando o ano à data se não estiver presente
        i = 4
        while i < 6:
            if len(inplist[i]) < 8:
                inplist[i] = f'{inplist[i]}/{str(year)}'
            i += 1

        # inserindo na tabela pedidos
        try:
            insert = f"INSERT INTO pedidos ('Nome','Grupo','Sexo','Valor','Data Pedido','Data Entrega') VALUES ('{inplist[0]}', '{inplist[1]}', '{inplist[2]}', '{inplist[3]}', '{inplist[4]}', '{inplist[5]}')"
            cursor.execute(insert)
        except Exception as e:
            print(e)
            return e

        # tirando ; do ultimo item se presente
        inplist[6] = inplist[6].rstrip(';')

        # separando itens distintos e quantidades
        itenspedidos = inplist[6].split(';')
        i = 0
        while i < len(itenspedidos):
            itenspedidos[i] = itenspedidos[i].split('-')
            itenspedidos[i][0] = itenspedidos[i][0].strip()
            itenspedidos[i][1] = itenspedidos[i][1].strip()
            i += 1
        
        # selecionando colunas de acordo com itens
        i = 0
        colunas = ''
        while i < len(itenspedidos):
            if i < len(itenspedidos) - 1:
                colunas += f"'{itenspedidos[i][1]}',"
            else:
                colunas += f"'{itenspedidos[i][1]}'"
            i += 1

        # selecionando quantidade de itens
        i = 0
        quantidades = ''
        while i < len(itenspedidos):
            if i < len(itenspedidos) - 1:
                quantidades += itenspedidos[i][0] + ','
            else:
                quantidades += itenspedidos[i][0]
            i += 1

        # inserindo itens distintos e suas quantidades na tabela itenspedidos
        try:
            insert = f"INSERT INTO itensPedidos ({colunas}) VALUES ({quantidades})"
            cursor.execute(insert)
        except Exception as e:
            print(e)
            return e
    
    commit()
    return 'Pedido Anotado!'

def remove(rowId):
    connection, cursor, commit = con()
    delete = f'DELETE FROM pedidos WHERE id = {rowId};'
    cursor.execute(delete)
    delete2 = f'DELETE FROM itensPedidos WHERE id = {rowId}'
    cursor.execute(delete2)
    commit()
    return f'Pedido Número {rowId} removido.'

def show():
    connection = con()[0]
    df = pd.read_sql("""SELECT pedidos.*, itensPedidos.'Brigadeiro 4', itenspedidos.'Brigadeiro 6', itensPedidos.'Brigadeiro NN 4', itensPedidos.'Brigadeiro NN 6', itensPedidos.'Brownie G', itensPedidos.'Brownie B', itensPedidos.'Cento Brigadeiro', itensPedidos.'Cento Beijinho', itensPedidos.'Panettone' 
            FROM pedidos
            INNER JOIN itensPedidos ON pedidos.id = itensPedidos.id;
            """, connection)
    connection.close()
    return df.to_string(index=False, show_dimensions=True)

def excel():
    connection = con()[0]
    df = pd.read_sql("""SELECT pedidos.*, itensPedidos.'Brigadeiro 4', itenspedidos.'Brigadeiro 6', itensPedidos.'Brigadeiro NN 4', itensPedidos.'Brigadeiro NN 6', itensPedidos.'Brownie G', itensPedidos.'Brownie B', itensPedidos.'Cento Brigadeiro', itensPedidos.'Cento Beijinho', itensPedidos.'Panettone' 
        FROM pedidos
        INNER JOIN itensPedidos ON pedidos.id = itensPedidos.id;
        """, connection)
    connection.close()
    df.to_excel('pedidos.xlsx', sheet_name='Pedidos', index=False)
    return 'Exportado para Excel'

def csv():
    connection = con()[0]
    df = pd.read_sql("""SELECT pedidos.*, itensPedidos.'Brigadeiro 4', itenspedidos.'Brigadeiro 6', itensPedidos.'Brigadeiro NN 4', itensPedidos.'Brigadeiro NN 6', itensPedidos.'Brownie G', itensPedidos.'Brownie B', itensPedidos.'Cento Brigadeiro', itensPedidos.'Cento Beijinho', itensPedidos.'Panettone' 
        FROM pedidos
        INNER JOIN itensPedidos ON pedidos.id = itensPedidos.id;
        """, connection)
    connection.close()
    df.to_csv('pedidos.csv', index=False)
    return 'Exportado para CSV'

#mainfunction('a,a,m,25,20/05,12/05,1-Brigadeiro 6;2-Brigadeiro 4;')
#mainfunction('a,a,a,m,25,20/05,12/05,1-Cento Brigadeiro;')
#mainfunction('a,a,a')