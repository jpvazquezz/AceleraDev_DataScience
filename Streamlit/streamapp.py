import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt

# Pré-processamento dos dados
ibge = pd.read_excel('Cities_Brazil_IBGE.xlsx')
coord = pd.read_csv('BrazilianCities.csv')
coord.rename(columns={'Latitude':'Lat','Longitude':'Long', 'IBGE':'IBGECode'}, inplace=True)
lat_long = coord.sort_values(by='IBGECode')[['IBGECode', 'Lat','Long']]
ibge = ibge.merge(lat_long, on='IBGECode')
ibge.drop(labels=['Latitude','Longitude'], axis=1, inplace=True)
ibge.rename(columns={'PopCenso 2010': 'PopCenso_2010'}, inplace=True)


def latitude(cidade):
    df = ibge.query("LocalCidade=='{0}'".format(cidade))
    return df['Lat'].item()
def longitude(cidade):
    df = ibge.query("LocalCidade=='{0}'".format(cidade))
    return df['Long'].item()
def mapa(cidade):
    m = st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=latitude(cidade),
            longitude=longitude(cidade),
            zoom=8,
            pitch=50
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=[latitude(cidade), longitude(cidade)],
                get_position='[Long, Lat]',
                auto_highlight=True,
                elevation_scale=50,
                pickable=True,
                elevation_range=[0, 3000],
                extruded=True,
                coverage=1
            )
        ],
    ))
    return m


def main():
    barra = st.sidebar.selectbox(label='Menu', options=['Mapa', 'Sobre o app'])
    if barra is 'Mapa':
        st.title("Cidades brasileiras")
        st.subheader('Conhecendo melhor o país')
        st.markdown(
            '''Esse aplicativo tem o objetivo de estimular os brasileiros a obterem informações básicas sobre as cidades brasileiras, conforme
            a base de dados do IBGE. Assim sendo, escolha a cidade de sua preferência e explore alguns dos dados disponíveis.
            '''
        )
        st.subheader('Mapa do Brasil')

        cidade = st.text_input('Digite o nome da cidade (em letras maísculas e sem acento):')
        infos = ibge.query("LocalCidade=='{0}'".format(cidade))
        if cidade:
            mapa(cidade)
            st.subheader('Informações básicas')
            st.subheader('Estado:')
            st.write(infos['LocalEstado'].item())
            st.subheader('Quem nasce em {} é o que?'.format(cidade))
            st.write(infos['Gentilico'].item().capitalize())
            st.subheader('Censo Populacional - 2010')
            st.write(infos['PopCenso_2010'].item())
            st.subheader('IDHM')
            st.write(infos['IDHM'].item())
            st.subheader('Receitas realizadas em 2014')
            st.write(infos['ReceitasRealizadas_2014'].item())
            st.subheader('Despesas Empenhadas em 2014')
            st.write(infos['DespesasEmpenhadas_2014'].item())
            st.subheader('Produto Interno Bruto (PIB) em 2014')
            st.write(infos['Pib_2014'].item())
    if barra is 'Sobre o app':
        st.subheader('Sobre o app')
        st.write('''
            Esse app foi desenvolvido como protótipo ao longo da aceleração AceleraDeV DataScience, promovido pela 
            Codenation, hub de inovação voltado para capacitações na área de tecnologia.''')
        st.image('aceleradev.png')
        st.write(
            '''Seu autor é João Pedro Vazquez, formado em Ciência Política, mestre em Sociologia Política e, atualmente, cientista de dados em formação. 
            O aplicativo é voltado para fins didáticos, portanto, sugestões e críticas são mais do que bem-vinda.''')
        st.markdown(
            '''Contato:
            * [LinkedIn](www.linkedin.com/in/joão-pedro-vazquez)
            * [Github](https://github.com/jpvazquezz)''')


    #'LocalEstado', 'RegiaoBrasil',
    #'Gentilico', 'PopEstimada_2018', 'PopCenso 2010', 'IDHM',
    #'ReceitasRealizadas_2014', 'DespesasEmpenhadas_2014', 'Pib_2014'
    #if not cidade:
        #st.markdown('Cidade não encontrada. Por favor escreva novamente.')

if __name__ == '__main__':
	main()