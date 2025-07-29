import pandas as pd
import streamlit as st
import joblib
import folium


# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide")
st.title("Previsão de preço Airbnb - Rio de Janeiro")

# --- CRIAÇÃO DAS ABAS ---
tab_previsao, = st.tabs(["Ferramenta de Previsão"])

# --- ABA 1: FERRAMENTA DE PREVISÃO ---
with tab_previsao:

    st.header("Preveja o Valor de um Imóvel")

    mapa_nomes = {
        'latitude': 'Latitude', 'longitude': 'Longitude', 'accommodates': 'Quantos hóspedes o imóvel pode acomodar',
        'bathrooms': 'Nº de Banheiros (lavabo equivale a 0.5)', 'bedrooms': 'Nº de Quartos', 'beds': 'Nº de Camas',
        'minimum_nights': 'Noites mínimas de estadia', 'ano': 'Ano', 'mes': 'Mês',
        'numero_de_amenities': 'Nº de Comodidades (Exemplo: TV, Internet, Ar condicionado,...)', 'host_listings_count': 'Quantas casas/quartos o anfitrião hospeda no Airbnb',
        'host_is_superhost': 'Anfitrião é Superhost', 'instant_bookable': 'Reserva Instantânea',
        'property_type': 'Tipo de Propriedade', 'room_type': 'Tipo de Quarto', 'cancellation_policy': 'Política de Cancelamento'
    }


    mapa_restricoes = {
        'host_listings_count': (0, 6), 'accommodates': (1, 9), 'bathrooms': (1.0, 4.0),
        'bedrooms': (0, 3), 'beds': (0, 6), 'minimum_nights': (1, 8),
        'numero_de_amenities': (1, 30), 'mes': (1, 12)
    }


    # Adicione este dicionário no seu código
    mapa_traducoes = {'property_type': {
                  'Apartment': 'Apartamento',
                  'Bed and breakfast': 'Cama e Café (B&B)',
                  'Condominium': 'Condomínio',
                  'Guest suite': 'Suíte de Hóspedes',
                  'Guesthouse': 'Pousada',
                  'Hostel': 'Hostel',
                  'House': 'Casa',
                  'Serviced apartment': 'Apart-hotel',
                  'Loft': 'Loft',
                  'Outros': 'Outros'},
                  'room_type': {
                  'Entire home/apt': 'Espaço Inteiro',
                  'Private room': 'Quarto Privado',
                  'Outros': 'Outros'},
                  'cancellation_policy': {
                  'flexible': 'Flexível',
                  'moderate': 'Moderada',
                  'strict': 'Rigorosa',
                  'strict_14_with_grace_period': 'Rigorosa (14 dias com carência)'
                    }}


    x_numericos = {'latitude': 0.0, 'longitude': 0.0, 'accommodates': 1, 'bathrooms': 1.0, 'bedrooms': 1, 'beds': 1,
                   'minimum_nights': 1, 'mes': 1, 'numero_de_amenities': 1, 'host_listings_count': 1}
    

    x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}


    x_listas = {
        'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite',
                          'Guesthouse', 'Hostel', 'House', 'Serviced apartment', 'Loft', 'Outros'],
        'room_type': ['Entire home/apt', 'Private room', 'Outros'],
        'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
    }


    dicionario_features = {}
    for item in x_listas:
        for valor in x_listas[item]:
            dicionario_features[f'{item}_{valor}'] = 0


    ano_selecionado = st.selectbox(label=mapa_nomes['ano'], options=[2018, 2019, 2020])


    st.subheader('Valores Numéricos')
    col1, col2 = st.columns(2)
    campos_numericos = list(x_numericos.keys())


    with col1:
        for item in campos_numericos[:5]:
            label_amigavel = mapa_nomes[item]
            min_val, max_val = mapa_restricoes.get(item, (None, None))
            valor_inicial = min_val if min_val is not None else 0.0
            if item in ('latitude', 'longitude'):
                valor = st.number_input(label_amigavel, value=valor_inicial, step=0.00001, format="%.5f", key=f'pred_{item}')
            elif item == 'bathrooms':
                valor = st.number_input(label_amigavel, min_value=float(min_val), max_value=float(max_val), value=float(valor_inicial), step=0.5, key=f'pred_{item}')
            else:
                valor = st.number_input(label=label_amigavel, min_value=int(min_val), max_value=int(max_val), value=int(valor_inicial), step=1, key=f'pred_{item}')
            x_numericos[item] = valor


    with col2:
        for item in campos_numericos[5:]:
            label_amigavel = mapa_nomes[item]
            min_val, max_val = mapa_restricoes.get(item, (None, None))
            valor_inicial = min_val if min_val is not None else 0.0
            valor = st.number_input(label=label_amigavel, min_value=int(min_val), max_value=int(max_val), value=int(valor_inicial), step=1, key=f'pred_{item}')
            x_numericos[item] = valor

    st.subheader('Características (Sim/Não)')
    col1_tf, col2_tf = st.columns(2)


    with col1_tf:
        item = 'host_is_superhost'
        label_amigavel = mapa_nomes[item]
        valor = st.selectbox(label=label_amigavel, options=('Não', 'Sim'), key=f'pred_{item}')
        x_tf[item] = 1 if valor == 'Sim' else 0


    with col2_tf:
        item = 'instant_bookable'
        label_amigavel = mapa_nomes[item]
        valor = st.selectbox(label=label_amigavel, options=('Não', 'Sim'), key=f'pred_{item}')
        x_tf[item] = 1 if valor == 'Sim' else 0

    st.subheader('Outras Características')
    col1_listas, col2_listas = st.columns(2)
    campos_listas = list(x_listas.keys())


    with col1_listas:
        for item in campos_listas[:2]:  # Itera sobre 'property_type' e 'room_type'
            label_amigavel = mapa_nomes[item]
            
            # Pega as opções traduzidas para exibir ao usuário
            opcoes_traduzidas = list(mapa_traducoes[item].values())
            
            # Cria o selectbox com as opções em português
            selecao_pt = st.selectbox(label=label_amigavel, options=opcoes_traduzidas, key=f'pred_{item}')
            
            # Encontra o valor original (em inglês) correspondente à seleção em português
            valor_original_en = next(key for key, value in mapa_traducoes[item].items() if value == selecao_pt)
            
            # Atualiza o dicionário de features com o valor original que o modelo entende
            dicionario_features[f'{item}_{valor_original_en}'] = 1


    with col2_listas:
        for item in campos_listas[2:]: # Itera sobre 'cancellation_policy'
            label_amigavel = mapa_nomes[item]
            
            # Pega as opções traduzidas para exibir ao usuário
            opcoes_traduzidas = list(mapa_traducoes[item].values())
            
            # Cria o selectbox com as opções em português
            selecao_pt = st.selectbox(label=label_amigavel, options=opcoes_traduzidas, key=f'pred_{item}')
            
            # Encontra o valor original (em inglês) correspondente à seleção em português
            valor_original_en = next(key for key, value in mapa_traducoes[item].items() if value == selecao_pt)
            
            # Atualiza o dicionário de features com o valor original que o modelo entende
            dicionario_features[f'{item}_{valor_original_en}'] = 1

    if st.button('Prever Valor do Imóvel'):
        dicionario_features.update(x_numericos)
        dicionario_features.update(x_tf)
        dicionario_features['ano'] = ano_selecionado
        valores_x = pd.DataFrame(dicionario_features, index=[0])
        try:
            modelo = joblib.load('modelo.joblib')
            dados = pd.read_csv('dados.csv')
            colunas = list(dados.columns)[1:-1]
            valores_x = valores_x[colunas]
            preco = modelo.predict(valores_x)
            st.success(f"Valor Previsto do Imóvel: R$ {preco[0]:.2f}")
        except FileNotFoundError:
            st.error("Arquivo 'modelo.joblib' ou 'colunas.joblib' não encontrado.")
        except Exception as e:
            st.error(f"Ocorreu um erro na previsão: {e}")

# streamlit run deploy_projeto_airbnb_v4.py

