#!/usr/bin/env python3
# EXERCÍCIO_5

# Importar módulo de expressões regulares
import re

multifasta = input('Digite o nome do arquivo multifasta> ')

# Criação de listas
values = []
headers = []
seqs = []
buffer_seqs = []

p1 = r"^[ACGTacgt]+$"      # linha só de bases do DNA

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
        headers.append(line[1:]) #remoção do caracter >

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

print('seqNome','    ', 'A', 'T', 'G', 'C', sep='\t') #Cabeçalho com espaço entre as colunas

for header, info in dict_dados['seqs'].items():
    # header = nome da sequência (a chave)
    # info   = o dicionário interno com 'teor_bases' dentro

    teores = info['teor_bases']
    nome = header.split()[0]

    # print com espaço entre cada item
    print(nome, teores['A'], teores['T'], teores['G'], teores['C'], sep='\t')


# Extração de códons por header, nos 3 frames da fita líder

lista_frames = []   # lista externa: cada item é [frame1, frame2, frame3] de UMA sequência

for i in range(len(headers)):
    seq = seqs[i]
    f1 = re.findall(r".{3}", seq[0:])
    f2 = re.findall(r".{3}", seq[1:])
    f3 = re.findall(r".{3}", seq[2:])
    # Extração de códons por header, nos 3 frames da fita irmã (reversa complementar)
    seq = seqs[i]
    seq = seq[::-1]
    seq = seq.replace ("A","t")
    seq = seq.replace ("T", "a")
    seq = seq.replace ("C","g")
    seq = seq.replace ("G", "c")
    seq = seq.upper()
    f4 = re.findall(r".{3}", seq[0:])
    f5 = re.findall(r".{3}", seq[1:])
    f6 = re.findall(r".{3}", seq[2:])
    lista_frames.append([f1, f2, f3, f4, f5, f6])    # lista com 6 frames

# Iterar associando por índice
with open("Python_08.codons-6frames.nt", "w") as frames:
    for i in range(len(headers)):
        nome = headers[i].split()[0]
        for j in range(6):  # 0, 1, 2, 3, 4, 5
            print(f'{nome}-frame-{j+1}-codons', file=frames)
            print(' '.join(lista_frames[i][j]), file=frames)

#

tabela_de_traducao = {
    'GCT':'A', 'GCC':'A', 'GCA':'A', 'GCG':'A',
    'CGT':'R', 'CGC':'R', 'CGA':'R', 'CGG':'R', 'AGA':'R', 'AGG':'R',
    'AAT':'N', 'AAC':'N',
    'GAT':'D', 'GAC':'D',
    'TGT':'C', 'TGC':'C',
    'CAA':'Q', 'CAG':'Q',
    'GAA':'E', 'GAG':'E',
    'GGT':'G', 'GGC':'G', 'GGA':'G', 'GGG':'G',
    'CAT':'H', 'CAC':'H',
    'ATT':'I', 'ATC':'I', 'ATA':'I',
    'TTA':'L', 'TTG':'L', 'CTT':'L', 'CTC':'L', 'CTA':'L', 'CTG':'L',
    'AAA':'K', 'AAG':'K',
    'ATG':'M',
    'TTT':'F', 'TTC':'F',
    'CCT':'P', 'CCC':'P', 'CCA':'P', 'CCG':'P',
    'TCT':'S', 'TCC':'S', 'TCA':'S', 'TCG':'S', 'AGT':'S', 'AGC':'S',
    'ACT':'T', 'ACC':'T', 'ACA':'T', 'ACG':'T',
    'TGG':'W',
    'TAT':'Y', 'TAC':'Y',
    'GTT':'V', 'GTC':'V', 'GTA':'V', 'GTG':'V',
    'TAA':'*', 'TGA':'*', 'TAG':'*'
}

# Tradução: mesma estrutura de lista_frames, mas com strings de aminoácidos
lista_traduzida = []    # lista_traduzida[i][j] = proteína do frame j+1 da sequência i

for sub in lista_frames:                 #sub = 6 frames de cada sequência
    frames_aa = []                       #guarda os 6 frames traduzidos dessa sequência
    for codons in sub:                   #codons = lista de códons de um frame
        proteina = ''
        for codon in codons:
            if codon in tabela_de_traducao:
                aa = tabela_de_traducao[codon]
            else:
                aa = 'X'
            proteina = proteina + aa
        frames_aa.append(proteina)       #guarda a proteína desse frame
    lista_traduzida.append(frames_aa)    #guarda os 6 frames dessa sequência

# Escrita do arquivo .aa
with open("Python_08.translated.aa", "w") as aa_out:
    for i in range(len(headers)):
        nome = headers[i].split()[0]
        for j in range(6):                          #6 frames
            print(f'{nome}-frame-{j+1}-translated', file=aa_out)
            print(lista_traduzida[i][j], file=aa_out)
