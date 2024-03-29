import discord
from discord.ext import commands
import manager as manager

client = commands.Bot(command_prefix = '')

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send("Comando não encontrado. Para obter os comandos digite 'c'")
    raise error

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['c'])
async def comandos(ctx):
    await ctx.send("""Comandos:
    'ajuda' ou '?' - Exemplo de input
    'itens' - Lista de Itens
    'pedido' ou 'p' (seguido do pedido) - Anotar pedido
    'remover' ou 'r' (seguido do número do pedido) - Remove pedido do banco de dados
    'tabela' ou 't' - Mostra tabela em string no chat (Não formatada!!!)
    'excel' ou 'xl' - Exporta o banco de dados para excel
    'csv' - Exporta o banco de dados para csv
    'comandos' ou 'c' - Lista de Comandos""")

@client.command(aliases=['?'])
async def ajuda(ctx):
    await ctx.send("Nome, Instagram, Grupo(J, A, I), Sexo(M, F), Valor, Data Pedido, Data Entrega, Pedido(Quantidade-Item1;Quantidade-Item2;...)")

@client.command()
async def itens(ctx):
    await ctx.send("""Itens:
    Brigadeiro 4
    Brigadeiro 6
    Brigadeiro NN 4
    Brigadeiro NN 6
    Brownie G
    Brownie B
    Cento Brigadeiro
    Cento Beijinho
    Panettone""")

@client.command(aliases=['p'])
async def pedido(ctx, *, nota):
    result = manager.mainfunction(nota)
    await ctx.send(result)

@client.command(aliases=['r'])
async def remover(ctx, num):
    result = manager.remove(num)
    await ctx.send(result)

@client.command(aliases=['t'])
async def tabela(ctx):
    result = manager.show()
    await ctx.send(result)

@client.command(aliases=['xl'])
async def excel(ctx):
    result = manager.excel()
    await ctx.send(result)

@client.command()
async def csv(ctx):
    result = manager.csv()
    await ctx.send(result)



client.run('discordkey')
