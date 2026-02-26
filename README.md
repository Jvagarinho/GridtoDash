# GridToDash - Excel to PDF Automated Reporter

<p align="center">
  <img src="logo.png" alt="GridToDash Logo" width="200"/>
</p>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/IterioTech-Powered-blue" alt="Powered by IterioTech">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Streamlit-1.28%2B-red" alt="Streamlit 1.28+">
  </a>
</p>

GridToDash é uma aplicação Streamlit profissional que permite transformar ficheiros Excel/CSV em relatórios PDF polidos e personalizados. Perfeito para pequenos empresário que precisam de relatórios rápidos sem experiência em design.

## Funcionalidades

- 📊 **Upload de Ficheiros** - Suporta ficheiros Excel (.xlsx) e CSV
- 🔢 **Seletor de Coluna para Métricas** - Escolha qual coluna numérica usar para calcular soma e média
- 📈 **Seletor de Eixo X** - Escolha qual coluna mostrar como labels no gráfico
- 📉 **Seletor de Eixo Y** - Escolha qual coluna usar para valores no gráfico
- 📊 **Gráficos Visuais** - Gráfico de barras dinâmico com suporte a múltiplas colunas
- 📄 **Seletor de Colunas para PDF** - Escolha quais colunas incluir no relatório
- 📄 **Relatório PDF** - Geração automática de PDF profissional
- 🌐 **Bilingue** - Suporte para Português e Inglês
- 🎨 **Design Moderno** - Interface bonita com animações e estilo boutique

## Screenshots

### Interface Principal
> A interface mostra o logo, seletor de idioma, upload de ficheiros, seletor de coluna para métricas, eixo X/Y, colunas para PDF, métricas, gráfico e tabela de dados.

### Relatório PDF Gerado
> O PDF inclui métricas, gráfico de barras, e tabela com os dados selecionados do ficheiro.

## Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/Jvagarinho/GridToDash.git
cd GridToDash
```

### 2. Criar Ambiente Virtual (Opcional mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## Deploy no Streamlit Cloud

1. Faça push do código para o GitHub
2. Aceda a [share.streamlit.io](https://share.streamlit.io)
3. Selecione o repositório e branch
4. Clique em "Deploy"

## Estrutura do Projeto

```
GridToDash/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências Python
├── logo.png           # Logo da aplicação
├── .gitignore         # Ficheiros a ignorar
└── README.md          # Documentação
```

## Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Processamento de Dados**: Pandas, OpenPyXL
- **Gráficos**: Matplotlib
- **PDF**: FPDF
- **Estilização**: CSS Customizado

## Como Usar

1. **Selecione o Idioma** - Use os botões PT/EN na sidebar
2. **Carregue um Ficheiro** - Arraste ou selecione um ficheiro Excel ou CSV
3. **Escolha a Coluna para Métricas** - Selecione qual coluna numérica usar para Total Sum e Average Value
4. **Escolha o Eixo X** - Selecione qual coluna aparecer como labels no gráfico
5. **Escolha o Eixo Y** - Selecione qual coluna usar para os valores no gráfico
6. **Selecione Colunas para PDF** - Escolha quais colunas incluir no relatório
7. **Visualize os Dados** - See métricas, gráfico e tabela de dados
8. **Gere o PDF** - Clique em "Gerar Relatório PDF"
9. **Download** - Faça download do relatório gerado

## Formato do Ficheiro de Entrada

O ficheiro Excel/CSV deve conter:
- Pelo menos uma coluna numérica para cálculo de métricas
- Colunas de texto são exibidas na tabela e gráfico

Exemplo:
| Produto | Vendas | Stock | Vendedor |
|---------|--------|-------|----------|
| Produto A | 1000 | 50 | João |
| Produto B | 2500 | 30 | Maria |

## Idiomas Suportados

- 🇵🇹 Português
- 🇬🇧 Inglês

## Licença

MIT License

## Autor

Desenvolvido por IterioTech

---

<p align="center">
  Feito com ❤️ por IterioTech
</p>
