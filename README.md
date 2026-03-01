# GridToDash - Excel to PDF Automated Reporter

<p align="center">
  <img src="logo.png" alt="GridToDash Logo" width="200"/>
</p>

<p align="center">
  <a href="https://gridtodash.streamlit.app">
    <img src="https://img.shields.io/badge/Live Demo-6-green" alt="Live Demo">
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

- 🔐 **Autenticação** - Sistema de login e registo de utilizadores
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

## Autenticação

A aplicação usa MongoDB para guardar os utilizadores. Para configurar:

### Variáveis de Ambiente

Se estiveres a correr localmente, cria um ficheiro `.env`:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=AppName
MONGODB_DB=gridtodash
```

### No Streamlit Cloud

Adiciona os secrets:

```toml
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/?appName=AppName"
MONGODB_DB = "gridtodash"
```

## Deploy no Streamlit Cloud

1. Faça push do código para o GitHub
2. Aceda a [share.streamlit.io](https://share.streamlit.io)
3. Selecione o repositório e branch
4. Clique em "Deploy"
5. Adicione os secrets (MONGODB_URI e MONGODB_DB) nas configurações

## Estrutura do Projeto

```
GridToDash/
├── app.py              # Aplicação principal
├── login.py            # Módulo de autenticação
├── requirements.txt    # Dependências Python
├── logo.png           # Logo da aplicação
├── convex/            # Funções Convex (opcional)
├── .streamlit/        # Configurações Streamlit
├── .gitignore         # Ficheiros a ignorar
└── README.md         # Documentação
```

## Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Base de Dados**: MongoDB (autenticação)
- **Processamento de Dados**: Pandas, OpenPyXL
- **Gráficos**: Matplotlib
- **PDF**: FPDF
- **Estilização**: CSS Customizado

## Como Usar

1. **Crie uma conta** - Use o formulário de registo
2. **Inicie sessão** - Faça login com email e password
3. **Selecione o Idioma** - Use os botões PT/EN na sidebar
4. **Carregue um Ficheiro** - Arraste ou selecione um ficheiro Excel ou CSV
5. **Escolha a Coluna para Métricas** - Selecione qual coluna numérica usar para Total Sum e Average Value
6. **Escolha o Eixo X** - Selecione qual coluna aparecer como labels no gráfico
7. **Escolha o Eixo Y** - Selecione qual coluna usar para os valores no gráfico
8. **Selecione Colunas para PDF** - Escolha quais colunas incluir no relatório
9. **Visualize os Dados** - See métricas, gráfico e tabela de dados
10. **Gere o PDF** - Clique em "Gerar Relatório PDF"
11. **Download** - Faça download do relatório gerado

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
