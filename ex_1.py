#!/usr/bin/env python3
# EXERCÍCIO 1
# Importar módulo de expressões regulares
import re

multifasta = input('Digite o nome do arquivo multifasta: ')

# Criação de listas
values = []
headers = []
seqs = []
buffer_seqs = []

p1 = r"^[ACGTacgt]+$"      # linha só de bases do dna

# Abrir, iterar e recuperar headers e sequências
with open(multifasta) as file:
    for line in file:
        line = line.rstrip('\n')
        if not line:
            continue
        values.append(line)

index = 0
while index < len(values):
    line = values[index]

    if line.startswith(">"):
        # fecha o registro anterior, se houver
        if buffer_seqs:
            seqs.append("".join(buffer_seqs))
            buffer_seqs = []
        headers.append(line[1:])

    elif re.match(p1, line):
        buffer_seqs.append(line)

    index += 1

# fecha o último registro
if buffer_seqs:
    seqs.append("".join(buffer_seqs))

# Criação de dicionários aninhados (headers, sequências, teores de bases)

dict_dados = {'seqs': {}}

for i in range(len(headers)):
    header = headers[i]
    seq = seqs[i]
    seq_up = seq.upper()

    dict_dados['seqs'][header] = {
        'teor_bases': {
            'A': seq_up.count('A'),
            'T': seq_up.count('T'),
            'C': seq_up.count('C'),
            'G': seq_up.count('G'),
        }
    }

# Impressão das informações armazenadas no dicionário aninhado:

print('seqNome','    ', 'A', 'T', 'G', 'C', sep='\t') # Cabeçalho com espaço entre as colunas

for header, info in dict_dados['seqs'].items():
    # header = nome da sequência (a chave)
    # info   = o dicionário interno com 'teor_bases' dentro

    teores = info['teor_bases']
    nome = header.split()[0]

    # print com espaço entre cada item
    print(nome, teores['A'], teores['T'], teores['G'], teores['C'], sep='\t')

