# Termo Solver

Um script em Python que revela as palavras diárias do jogo [Termo](https://term.ooo/) para qualquer data específica através de uma engenharia reversa do algoritmo original.

## 📖 Sobre o Projeto

Este projeto surgiu da curiosidade de entender como funciona o algoritmo por trás do popular jogo de palavras brasileiro Termo. Através da inspeção da página do jogo na aba "Sources" do Chrome, o código JavaScript ofuscado original foi extraído, reformatado utilizando ferramentas de beautifier e posteriormente analisado para a compreensão de seu funcionamento.

Ou seja, o processo envolveu a engenharia reversa do sistema que determina as palavras diárias para todos os modos de jogo:

- **Termo** (1 palavra)
- **Dueto** (2 palavras)
- **Quarteto** (4 palavras)

O algoritmo original foi então replicado em Python, mantendo a mesma lógica e permitindo consultar as respostas de qualquer data.

## 🔍 Como o Algoritmo Funciona

O jogo utiliza um algoritmo determinístico baseado em:
- Um índice calculado a partir da data (dias desde 02/01/2022)
- Arrays de índices pré-computados para Dueto e Quarteto
- Uma lista completa de palavras válidas para respostas
- Duas fórmulas específicas para determinar as respostas no Termo e nas variações Dueto e Quarteto

Todas essas estruturas foram convertidas do código JavaScript original.

## 🚀 Executando o Script

### Requisitos

- Python 3.6 ou superior
- Arquivos de dados na pasta `dados`:
  - `Dueto índices.txt`
  - `Quarteto índices.txt`
  - `Palavras.txt`

### Execução

```bash
python termo.py
```
Ou simplesmente abra o arquivo "termo.py".

O script solicitará uma data no formato `DD/MM/AAAA` e retornará as respostas correspondentes para todos os modos.

### Exemplo de Uso

```
Digite uma data (formato DD/MM/AAAA) ou 'sair' para encerrar: 27/07/2025

--- Respostas ---
Termo: ótima
Dueto: naves e ossos
Quarteto: tarja, falir, sadia e garfo
```

## 📦 Criando o Executável

Para ter um executável que não necessita que o Python esteja instalado, você pode criar um usando o PyInstaller.

### Instalação do PyInstaller

```bash
pip install pyinstaller
```

### Gerando o Executável

Abra o Windows Powershell (ou uma alternativa) e execute o seguinte comando no diretório do projeto:

```bash
pyinstaller --onefile --add-data "dados/Dueto índices.txt;dados" --add-data "dados/Quarteto índices.txt;dados" --add-data "dados/Palavras.txt;dados" --name "termo" --clean "termo.py"
```

#### Explicação dos Parâmetros:

- `--onefile`: Cria um único arquivo executável
- `--add-data`: Inclui os arquivos de dados necessários no executável (Dueto índices, Quarteto índices e Palavras)
  - Formato: `"origem;destino"` (Windows) ou `"origem:destino"` (Linux/Mac, é necessária a modificação do comando para esses sistemas operacionais)
- `--name "termo"`: Define o nome do executável como "termo"
- `--clean`: Limpa o cache antes de compilar
- `termo.py`: Arquivo Python principal

### Localização do Executável

Após a compilação, o executável estará disponível em:
- **Windows**: `dist/termo.exe`
- **Linux/Mac**: `dist/termo`

## ⚠️ Considerações

- O script funciona oficialmente para datas entre 02/01/2022 e 31/12/9999 (lançamento oficial do Termo e limite do suporte da biblioteca do Python)
- Datas anteriores ao lançamento ainda retornarão resultados baseados no algoritmo, mas com um aviso de que as palavras são resultados hipotéticos e estendidos
- Os arquivos de dados devem estar presentes para o funcionamento do script em Python (isso não é necessário para o executável)

## 🛠️ Detalhes Específicos

O código tenta manter uma correspondência com as funções originais do JavaScript:
- `decodificar_indices_do_array()` ↔ funções "JB" e "ZB"
- `solucoes_diarias()` ↔ funções "bc()" e "ey()"
- `indice_do_dia_a_partir_de_string()` ↔ função "Eh()"

Todas as correspondências estão presentes no topo do arquivo "termo.py".

## 📄 Licença

Este projeto é apenas para fins educacionais. Todos os direitos do jogo Termo pertencem ao [Fernando Serboncini](https://fserb.com/), seu criador original.

---
