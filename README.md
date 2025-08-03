# 📈 Modelo Preditivo de Preços para Airbnb no Rio de Janeiro

![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)

## 📝 Descrição do Projeto

Este projeto de Data Science foi desenvolvido como parte do meu portfólio pessoal e tem como objetivo a construção de um modelo de Machine Learning capaz de prever o preço de diárias de imóveis na cidade do Rio de Janeiro, com base em dados da plataforma Airbnb. O ciclo do projeto foi completo, desde a coleta e limpeza dos dados até o deploy de uma aplicação web interativa.

> ### 🚀 Acesse a aplicação interativa aqui: [App Previsão de Preços Airbnb](https://app-previsao-precos-airbnb.streamlit.app/)

---

## 🎯 Metodologia Aplicada

O projeto foi estruturado seguindo as principais etapas de um pipeline de Ciência de Dados:

#### 1. Limpeza e Pré-processamento de Dados
* Análise e tratamento de valores ausentes (`NaN`).
* Correção dos tipos de dados de cada coluna (int, float, object).
* Remoção de *outliers* de alto valor, interpretados como imóveis do segmento de luxo, para focar o modelo no mercado de aluguéis convencionais.

#### 2. Análise Exploratória de Dados (EDA)
* Criação de um mapa de dispersão com 5.000 observações para visualizar a relação entre geolocalização e preço.
* Geração de nuvens de palavras a partir dos títulos e resumos dos anúncios, confirmando que a **localização** é um fator crucial para a precificação (com forte presença de termos como "praia", "Copacabana", "Ipanema").
* Análise de correlação entre as variáveis numéricas.
* Visualização da distribuição das variáveis com histogramas, boxplots e gráficos de barras.

#### 3. Engenharia de Features
* Tratamento de variáveis categóricas com agrupamentos e codificação.
* Aplicação de **One-Hot Encoding** para variáveis nominais e **Codificação Ordinal** para variáveis com hierarquia.

#### 4. Modelagem e Avaliação
* Foram comparados 4 modelos de regressão: `Regressão Linear`, `Lasso`, `Random Forest` e `Extra Trees`.
* A performance foi avaliada com base nas métricas **R² (Coeficiente de Determinação)** e **RMSE (Raiz do Erro Quadrático Médio)**.
* Utilização de **Validação Cruzada** (`cross_val_score`) para obter uma média de performance mais robusta.
* Otimização de hiperparâmetros com **GridSearchCV** para os modelos de `Lasso`, `Random Forest` e `Extra Trees`.
* O modelo **Random Forest Regressor** apresentou o melhor desempenho geral, com um **R² de 97%** nos dados de teste.

#### 5. Deploy
* O modelo final foi salvo e implementado em uma aplicação web interativa utilizando a biblioteca **Streamlit**.
* O deploy da aplicação foi realizado na **Streamlit Cloud**, tornando-a acessível publicamente.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** `Python`
* **Análise e Computação Científica:** `Pandas`, `NumPy`, `SciPy`
* **Machine Learning:**
    * `Scikit-learn` (para modelagem, pré-processamento e avaliação)
    * `Joblib` (para serialização e salvamento do modelo)
* **Visualização de Dados:**
    * `Matplotlib` e `Seaborn` (para gráficos estáticos)
    * `Folium` (para mapas interativos)
* **Processamento de Linguagem Natural (NLP):**
    * `NLTK` (Natural Language Toolkit)
    * `WordCloud` (para visualização de frequência de palavras)
* **Aplicação Web:** `Streamlit`

---
## 👨‍💻 Autor

Desenvolvido por **[Ronaldo C. Silva]**.

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)]([linkedin.com/in/ronaldocsilva])
