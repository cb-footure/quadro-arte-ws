import streamlit as st
import pandas as pd 
import requests as requests
import json
from pandas.io.json import json_normalize
import glob as glob
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, ConnectionPatch,Ellipse
import PIL
from PIL import Image
from PIL import Image, ImageDraw, ImageFilter
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageOps
from random import randint
from time import sleep
import matplotlib.font_manager as font_manager
import matplotlib as mpl 
import pylab as pl
import json
from pandas.io.json import json_normalize
import math
from math import hypot
import requests
from mplsoccer.pitch import Pitch
from matplotlib.patches import Arc
from scipy.spatial import ConvexHull
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import sklearn
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import paired_euclidean_distances
import numpy as np
from sklearn.preprocessing import StandardScaler 
import base64
import os
#------------------------------------------------------------------------------------------------------- 
st.title('Footure Plot')
menu=['Plotagem campinho','Quadro de stats jogador por time']
choice=st.sidebar.selectbox('Menu',menu)
if choice == 'Plotagem campinho':
   token=st.text_input('Token')
   fr=st.text_input('From (2021-01-01)')
   to=st.text_input('To (2021-12-31)')
   player=st.text_input('ID jogador')
   
   def get_binary_file_downloader_html(bin_file, file_label='File'):
       with open(bin_file, 'rb') as f:
           data = f.read()
       bin_str = base64.b64encode(data).decode()
       href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
       return href
   
   headers = {'Accept': '*/*','Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Host': 'searchapi.wyscout.com',
  'Origin': 'https://platform.wyscout.com',
  'Referer': 'https://platform.wyscout.com/app/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

   payload ={
      'lang': 'en','from': fr,'to': to,'score': 'winning,draw,losing','columns': 'name,positions,minutes_on_field,total_actions,total_actions_success,goal,assist,shot,shot_success,xg_shot,pass,pass_success,long_pass,long_pass_success,cross,cross_success,dribble,dribble_success,duel,duel_success,aerial_duel,aerial_duel_success,interception,loss,own_half_loss,recovery,opponent_half_recovery,yellow_card_minute,red_card_minute',
      'venue':'home,away','token': token,'groupId': '1231619','subgroupId': '286367'
      }


   site = ('https://searchapi.wyscout.com/api/v1/match_stats/players/{}?'.format(player))
   r = requests.get(site,headers=headers,data=payload)
   r.status_code
   parsed = json.loads(r.text)
   data = json.loads(r.text)
   df= json_normalize(data,sep='_')
   df['id']= player

   opcao_temporada=st.checkbox('Selecionar por temporada',value=False)
   if opcao_temporada == True:
      lista_temporada=list(df['match_seasonName'].unique())
      botao_temporada=st.multiselect('Selecione a temporada desejada',lista_temporada)
      df=df[df['match_seasonName'].isin(botao_temporada)].reset_index(drop=True)
      
   opcao_campeonato=st.checkbox('Selecionar por campeonato',value=False)
   if opcao_campeonato == True:
      lista_campeonato=list(df['match_competition'].unique())
      botao_campeonato=st.multiselect('Selecione a temporada desejada',lista_campeonato)
      df=df[df['match_competition'].isin(botao_campeonato)].reset_index(drop=True)
   df_jogador=df
   df_jogador
   match_list = [ ]
   for i in range(len(df)): 
      match_id = df['match_id'][i]
      match = df['match_name'][i]
      competition = df['match_competition'][i]

      match_dic = {'match_id': match_id, 'match':match, 'competition': competition}
      match_list.append(pd.DataFrame(match_dic, index=[0]))
   match_df = pd.concat(match_list, axis=0, ignore_index=True)
   match_list.clear()
   lista_id = [ ]
   for x in range(len(match_df)):
      lista_id.append(match_df['match_id'][x])
   headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'searchapi.wyscout.com',
    'If-None-Match': """W/"f32bd1ebe4815670ade3d5582448495a""",
    'Origin': 'https://platform.wyscout.com',
    'Referer': 'https://platform.wyscout.com/app/?',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

   payload = {
      'ids[]': player,
      'lang': 'en',
      'token': token,
      'groupId': '1231619',
      'subgroupId': '289819'
   }

   site = 'https://searchapi.wyscout.com/api/v1/shadow_teams/players.json?'

   r = requests.get(site,headers=headers,params=payload)
   r.status_code
   parsed = json.loads(r.text)
   data = json.loads(r.text)
   df= pd.json_normalize(data,sep='_')
   info_jogador=pd.DataFrame(df['players'][0])
   #----------------------------------------------------------------------------
   def heatmap():
     jogos = (','.join(str(x) for x in lista_id))
     headers = {'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Host': 'searchapi.wyscout.com',
      'If-None-Match': """W/"cd3d5af7ad718eb1d50c2a73598ea45f""",
      'Origin': 'https://platform.wyscout.com',
      'Referer': 'https://platform.wyscout.com/app/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-site',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

     params ={ 
        'match_ids': jogos,
        'score': 'winning,draw,losing',
        'token': token,
        'groupId': '1231619',
        'subgroupId': '289819'
      }


     site = f'https://searchapi.wyscout.com/api/v1/match_stats/players/{player}/heatmap?/'
     r = requests.get(site, headers=headers,params=params)
     r.status_code
     parsed = json.loads(r.text)
     data = json.loads(r.text)
     df= json_normalize(data,sep='_') 
     r.status_code
    #  r.url

     heatmap_series = (df['heatmap']).to_dict()
     heatmap = pd.DataFrame.from_dict(heatmap_series)

     lista_df = []

     for i in range(len(heatmap)):
       dicionario = (heatmap.iloc[i])
       for k,v in dicionario.items():
         novo_dic = v
         for z in novo_dic:
           lista_df.append(pd.DataFrame(z,index=[0]))

     heatmap = pd.concat(lista_df, axis=0, ignore_index=True)
     cor_fundo = '#000000'
     fig, ax = plt.subplots(figsize=(15,10))
     pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,
                    stripe=False, line_zorder=2)
     pitch.draw(ax=ax)
     cor_ponto = 'black' 
     sns.kdeplot(heatmap["x"],heatmap["y"], shade=True, n_levels=250,cmap='CMRmap')
      #Spectral_r
     ax.set_ylim(101,-0.5)
     ax.set_xlim(-0.5,101)
     font = {'family': 'sans',
              'color':  'darkred',
              'weight': 'bold',
              'size': 20,
              }
      #plt.title(f'{titulo}',color='White',fontdict=font)
      # ax.annotate('@LeituradoJogo',xy=(92,102),fontsize=15,color='white')
      #ax.annotate('Dados via WyScout',xy=(0,102),fontsize=15,color='white')
     plt.savefig(f'calor_{nome_jogador}.jpg',quality=95,bbox_inches='tight',facecolor=cor_fundo)
#      plt.savefig(f'calor_{nome_jogador}.jpg',quality=95,bbox_inches='tight',facecolor=cor_fundo)
        
     plt.show()
     st.pyplot(fig)
     st.markdown(get_binary_file_downloader_html(f'calor_{nome_jogador}.jpg', 'Heatmap'), unsafe_allow_html=True)
   
   #-----------------------------------------------------------------------------
   def assist(cor_fundo='#2c2b2b'):
     match_id = lista_id
     lista_sonar = []
     for i in match_id:
       headers=  {'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'searchapi.wyscout.com',
        'If-None-Match': 'W/"c5907d0dda9817e991caaf4ed3536068"',
        'Origin': 'https://platform.wyscout.com',
        'Referer': 'https://platform.wyscout.com/app/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; CrOS armv7l 12607.81.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.119 Safari/537.36' } 


       payload = {'match_id': i,
        'lang':'', 
        'debug':'', 
        'event_type': 'passes',
        'score': 'winning,draw,losing',
        'minutes':'', 
        'position':'', 
        'under_card':'', 
        'token': token,
        'groupId': '1231619',
        'subgroupId': '286367'} 

       sleep(randint(2, 7))
       site = ('https://searchapi.wyscout.com/api/v1/match_report/players/{}/passes?'.format(player))
       r = requests.get(site,headers=headers,data=payload)
       r.status_code

       parsed = json.loads(r.text)
       data = json.loads(r.text)
       df= pd.json_normalize(data,sep='_') 

        
       df_final =pd.DataFrame(df['data_passes'][0])
       lista_sonar.append(df_final)
     global sonar_final
     sonar_final = pd.concat(lista_sonar,axis=0,ignore_index=True)
     assist = sonar_final[sonar_final['is_assist']==True].reset_index()
     key_pass = sonar_final[sonar_final['is_key_pass']==True].reset_index()
     key_pass

    #  cor_fundo = '#2C2B2B'
     pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,orientation='horizontal',half=True,
                stripe=False, line_zorder=2)
     fig, ax = pitch.draw()
     cor_ponto = 'black' 

     def plot_scatter_df(df,cor,zo):
       pitch.scatter(df.to_x, df.to_y, s=200, edgecolors=cor,lw=2, c=cor_fundo, zorder=zo+1, ax=ax)
      # plt.scatter(data=df, x='to_x',y='to_y',color=cor,zorder=zo+1,label='df',edgecolors='white',s=200)
       for linha in range(len(df)):
         x_inicial = df['from_x'][linha]
         y_inicial = df['from_y'][linha]
         x_final = df['to_x'][linha]
         y_final = df['to_y'][linha]
        # plt.plot([x_inicial,x_final],[y_inicial,y_final],color=cor,lw=5)
         lc1 = pitch.lines(x_inicial, y_inicial,
                      x_final, y_final,
                      lw=5, transparent=True, comet=True, label='completed passes',
                      color=cor, ax=ax,zorder=zo)
        
    
     plot_scatter_df(key_pass,'#FEA300',9)
     plot_scatter_df(assist,'#00FF79',12)
     plt.savefig(f'assist_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)
     plt.show()
     st.pyplot(fig)
      
     st.markdown(get_binary_file_downloader_html(f'assist_{nome_jogador}.png', 'Assist'), unsafe_allow_html=True)
    #  return fig
    #----------------------------------------------------------------------------
   def progressivo(cor_fundo='#2c2b2b'):
     passe_detalhado = sonar_final
     passe_detalhado
     lista_distancia = []
     for w in range(len(passe_detalhado)): 
       x1 = (passe_detalhado['from_x'][w])
       x2 = (passe_detalhado['to_x'][w])
       y1 = (passe_detalhado['from_y'][w])
       y2 = (passe_detalhado['to_y'][w])
       distancia = math.hypot(x2-x1, y2-y1)
       lista_distancia.append(distancia)

     passe_detalhado['distancia'] = lista_distancia
     passe_detalhado['distancia'] = passe_detalhado['distancia']/1.2
     passe_detalhado['progressão'] = (passe_detalhado['to_x'] - passe_detalhado['from_x'])/1.2 
     passe_detalhado

     lista_progressão = []
     for i in range(len(passe_detalhado)):
       x_inicial = passe_detalhado['from_x'][i]
       x_final = passe_detalhado['to_x'][i]
       progressão = passe_detalhado['progressão'][i]

       if True:
         if (x_inicial < 50 and x_final < 50) and progressão >= 30:
           lista_progressão.append(True)
         elif (x_inicial < 50 and x_final < 50) and progressão < 30:
           lista_progressão.append(False)
          
         elif (x_inicial < 50 and x_final > 50) and progressão >= 15:
           lista_progressão.append(True)
         elif (x_inicial < 50 and x_final > 50) and progressão < 15:
           lista_progressão.append(False)
          
         elif (x_inicial > 50 and x_final > 50) and progressão >= 10:
           lista_progressão.append(True)
         elif (x_inicial > 50 and x_final > 50) and progressão < 10:
           lista_progressão.append(False)
         else:
           lista_progressão.append(False)
     passe_detalhado['progressivo'] = lista_progressão

     progressivo = passe_detalhado[passe_detalhado['progressivo']== True].reset_index(drop=True)
     progressivo_certo = progressivo[progressivo['successful']==True].reset_index(drop=True)
     progressivo_errado = progressivo[progressivo['successful']==False].reset_index(drop=True)



    #  cor_fundo = '#2C2B2B'
     progressivo
     pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,orientation='horizontal',
                  stripe=False, line_zorder=2)
     fig, ax = pitch.draw()
      # zo =12
     cor_ponto = 'black' 

     def plot_scatter_df(df,cor,zo):
       pitch.scatter(df.to_x, df.to_y, s=200, edgecolors=cor,lw=2, c=cor_fundo, zorder=zo+1, ax=ax)
        # plt.scatter(data=df, x='to_x',y='to_y',color=cor,zorder=zo+1,label='df',edgecolors='white',s=200)
       for linha in range(len(df)):
         x_inicial = df['from_x'][linha]
         y_inicial = df['from_y'][linha]
         x_final = df['to_x'][linha]
         y_final = df['to_y'][linha]
          # plt.plot([x_inicial,x_final],[y_inicial,y_final],color=cor,lw=5)
         lc1 = pitch.lines(x_inicial, y_inicial,
                        x_final, y_final,
                        lw=5, transparent=True, comet=True, label='completed passes',
                        color=cor, ax=ax,zorder=zo)
          
      
     plot_scatter_df(progressivo_certo,'#00FF79',12)
     plot_scatter_df(progressivo_errado,'#FD2B2C',9)
     plt.savefig(f'progressivo_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)

     plt.show()
     st.pyplot(fig)
     st.markdown(get_binary_file_downloader_html(f'progressivo_{nome_jogador}.png', 'Progressivo'), unsafe_allow_html=True)

    #---------------------------------------------------------------------------
   def defensivo(cor_fundo='#2c2b2b'):

    lista_frames_dados_de_um_jogo = []
    for i in lista_id:
      tipos = ['interceptions','defensive_duels']
      for tipo in tipos:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'searchapi.wyscout.com',
            'Origin': 'https://platform.wyscout.com',
            'Referer': 'https://platform.wyscout.com/app/?',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
            }

        params = {
            'match_id': i,
            'lang':'', 
            'debug':'', 
            'score': 'winning,draw,losing',
            'minutes': '',
            'position':'', 
            'under_card':'' ,
            'token': token,
            'event_type': tipo,
            'groupId': '1231619',
            'subgroupId': '289819'
        }

        sleep(randint(2, 7))
        site = f'https://searchapi.wyscout.com/api/v1/match_report/players/{player}/actions?'
        r= requests.get(site,headers=headers,params=params)


        parsed = json.loads(r.text)
        data = json.loads(r.text)
        df= pd.json_normalize(data,sep='_') 

        dados = pd.DataFrame(df['data_actions'][0])
        dados['tipo'] = tipo 
        lista_frames_dados_de_um_jogo.append(dados) 

    jogo_geral = pd.concat(lista_frames_dados_de_um_jogo,ignore_index=True,axis=0)


    dic_nome = {'interceptions':'interceptação','defensive_duels' : 'desarmes'}
    jogo_geral = jogo_geral.replace(dic_nome)
    tipos_ações= list(jogo_geral['tipo'].unique())

    # cor_fundo = '#2C2B2B'

    pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,orientation='horizontal',
            stripe=False, line_zorder=2)
    fig, ax = pitch.draw()
      
    cor_ponto = 'black' 

    df_tipo = jogo_geral
    ação_certa = df_tipo[df_tipo['successful'] == True].reset_index(drop=True)
    ação_errada = df_tipo[df_tipo['successful'] == False].reset_index(drop=True)

    zo =12
    cor_ponto = 'black'
#     defense = df_tipo[(np.abs(stats.zscore(df_tipo[['x','y']])) < .5)]
#     defpoints = defense[['x','y']].values
#     hull = ConvexHull(defense[['x','y']])


    def plot_scatter_df(df,cor,adjust=False):
        plt.scatter(data=df, x='x',y='y',color=cor,zorder=zo+1,label='df')
        if adjust:
            for simplex in hull.simplices:
            #Draw a black line between each
                plt.plot(defpoints[simplex, 0], defpoints[simplex, 1], 'r-',color=cor)
            plt.fill(defpoints[hull.vertices,0], defpoints[hull.vertices,1],c=cor, alpha=0.1,hatch='/')
    plot_scatter_df(ação_certa,'#00FF79',adjust=False)
    plot_scatter_df(ação_errada,'#FD2B2C')

      
    
    plt.savefig(f'defensivo_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)

    plt.show()
    st.pyplot(fig)
    st.markdown(get_binary_file_downloader_html(f'defensivo_{nome_jogador}.png', 'Defensivo'), unsafe_allow_html=True)
    # return fig
    #-------------------------------------------------------------------------
   def cruzamento(cor_fundo='#2c2b2b'):
     match_list = lista_id

     lista_todos_jogos = []
     for match_id in match_list:
       headers = {'Accept': '*/*',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
       'Connection': 'keep-alive',
       'Host': 'searchapi.wyscout.com',
       'Origin': 'https://platform.wyscout.com',
       'Referer': 'https://platform.wyscout.com/app/',
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}


       payload ={'match_id': match_id,
                'lang':'', 
                'debug':'', 
                'event_type': 'crosses',
                'score': 'winning,draw,losing',
                'minutes':'', 
                'position': '',
                'under_card': '',
                'token': token,
                'groupId': '1231619',
                'subgroupId': '289819'
        }

       site = f'https://searchapi.wyscout.com/api/v1/match_report/players/{player}/passes?'
       r = requests.get(site, headers=headers,data=payload)
       r.status_code
       parsed = json.loads(r.text)
       data = json.loads(r.text)
       df= json_normalize(data,sep='_') 

       passes_series = (df['data_passes']).to_dict()
       passe = pd.DataFrame.from_dict(passes_series)

       cruzamento_jogo = []

       for i in range(len(passe)):
         dicionario = (passe.iloc[i])
         lista_frame_cruzamento_jogo = []
         for k,v in dicionario.items():
           novo_dic = v
           tabela_cruzamento = (pd.DataFrame(v,index=[0]))
           lista_todos_jogos.append(tabela_cruzamento)

     cruzamento = pd.concat(lista_todos_jogos,ignore_index=True,axis=0)
     cruzamento_certo = cruzamento[cruzamento['successful']==True].reset_index()
     cruzamento_errado = cruzamento[cruzamento['successful']==False].reset_index()

     df=cruzamento
      # cor_fundo = '#EEEBEA'
    #  cor_fundo = '#2C2B2B' 
     pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,orientation='horizontal',half=True,
                  stripe=False, line_zorder=2)
     fig, ax = pitch.draw()

      # zo =12
     cor_ponto = 'black' 
     def plot_scatter_df(df,cor,zo):
        pitch.scatter(df.to_x, df.to_y, s=200, edgecolors=cor,lw=2, c=cor_fundo, zorder=zo+1, ax=ax)
        # plt.scatter(data=df, x='to_x',y='to_y',color=cor,zorder=zo+1,label='df',edgecolors='white',s=200)
        for linha in range(len(df)):
          x_inicial = df['from_x'][linha]
          y_inicial = df['from_y'][linha]
          x_final = df['to_x'][linha]
          y_final = df['to_y'][linha]
          # plt.plot([x_inicial,x_final],[y_inicial,y_final],color=cor,lw=5)
          lc1 = pitch.lines(x_inicial, y_inicial,
                        x_final, y_final,
                        lw=5, transparent=True, comet=True, label='completed passes',
                        color=cor, ax=ax,zorder=zo)

     plot_scatter_df(cruzamento_certo,'#00FF79',zo=12)
     plot_scatter_df(cruzamento_errado,'#FD2B2C',zo=9)

      #legenda 
      # plt.scatter(x=49,y=80,color='#00FF79',zorder=40,s=300)
      # plt.scatter(x=49,y=60,color='#FD2B2C',zorder=40,s=300)
     plt.rc('font', family='Helvetica')

     plt.savefig(f'cruzamento_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)
     plt.show()
     st.pyplot(fig)
     st.markdown(get_binary_file_downloader_html(f'cruzamento_{nome_jogador}.png', 'Cruzamento'), unsafe_allow_html=True)
    #  return fig
    #-------------------------------------------------------------------------
   def recepção(cor_fundo='#2C2B2B'):
    def passe_recebido(cor_fundo='#2C2B2B'):
      lista_passe_recebido = []
      for match_id in lista_id:
        params = {
            'match_id': match_id,
            'lang': 'en',
            'event_type': 'passes',
            'score': 'winning,draw,losing',
            'minutes': '',
            'position': '',
            'under_card':'', 
            'token': token,
            'groupId': '1231619',
            'subgroupId': '289819',
            'event_type': 'received_pass'
        }
        site = f'https://searchapi.wyscout.com/api/v1/match_report/players/{player}/actions?'
        r = requests.get(site,headers=headers,data=params)
        if r.status_code != 200:
          print('erro request')
          break
        parsed = json.loads(r.text)
        data = json.loads(r.text)
        df= pd.json_normalize(data,sep='_') 

        df_passe_recebido = pd.DataFrame(df['data_actions'][0])
        lista_passe_recebido.append(df_passe_recebido)

      df_recebido = pd.concat(lista_passe_recebido,axis=0,ignore_index=True)
      return(df_recebido)


    # cor_fundo='#EEEBEA'
    # cor_fundo='#2C2B2B'
    passe_recebido = passe_recebido()
    recep = passe_recebido[['x','y']]
    pitch = Pitch(pitch_type='wyscout', figsize=(30,20),pitch_color=cor_fundo,orientation='horizontal',
                stripe=False, line_zorder=2)
    fig, ax = pitch.draw() 
    cor_divisao = 'red'

    recep['y_invertido'] = 100 - recep['y']
    y = list(recep['y_invertido'])
    x = list(recep['x'])


    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list('name', [cor_fundo, '#F43B87'])

    plt.hist2d(x,y, bins=[np.arange(0, 110, 10), np.arange(0, 110, 10)], cmap=cmap)
    plt.savefig(f'recepção_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)
    plt.show()
    st.pyplot(fig)
    st.markdown(get_binary_file_downloader_html(f'recepção_{nome_jogador}.png', 'Recepções'), unsafe_allow_html=True)
    # return fig
        #----------------------------------------------------------------------------------------
   def passe_plot(cor_fundo='#2C2B2B'):
    def passes():
      lista_passe = []
      for match_id in lista_id:
        params = {
            'match_id': match_id,
            'lang': 'en',
            'event_type': 'passes',
            'score': 'winning,draw,losing',
            'minutes': '',
            'position': '',
            'under_card':'', 
            'token': token,
            'groupId': '1231619',
            'subgroupId': '289819',
        }
        site = f'https://searchapi.wyscout.com/api/v1/match_report/players/{player}/passes?'
        r = requests.get(site,headers=headers,data=params)
        if r.status_code != 200:
          print('erro request')
          break
        parsed = json.loads(r.text)
        data = json.loads(r.text)
        df= pd.json_normalize(data,sep='_') 
        

        df_passe = pd.DataFrame(df['data_passes'][0])
        lista_passe.append(df_passe)

      df_passe= pd.concat(lista_passe,axis=0,ignore_index=True)
      return(df_passe)

    global df_passe 
    df_passe = passes()
    
    passe_certo = df_passe[df_passe['successful']==True].reset_index(drop=True)
    passe_errado = df_passe[df_passe['successful']==False].reset_index(drop=True)



    # cor_fundo = '#2C2B2B'
    # progressivo
    pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,orientation='horizontal',
                stripe=False, line_zorder=2)
    fig, ax = pitch.draw()


    # zo =12
    cor_ponto = 'black' 

    def plot_scatter_df(df,cor,zo):
      pitch.scatter(df.to_x, df.to_y, s=200, edgecolors=cor,lw=2, c=cor_fundo, zorder=zo+1, ax=ax)
      # plt.scatter(data=df, x='to_x',y='to_y',color=cor,zorder=zo+1,label='df',edgecolors='white',s=200)
      for linha in range(len(df)):
        x_inicial = df['from_x'][linha]
        y_inicial = df['from_y'][linha]
        x_final = df['to_x'][linha]
        y_final = df['to_y'][linha]
        # plt.plot([x_inicial,x_final],[y_inicial,y_final],color=cor,lw=5)
        lc1 = pitch.lines(x_inicial, y_inicial,
                      x_final, y_final,
                      lw=5, transparent=True, comet=True, label='completed passes',
                      color=cor, ax=ax,zorder=zo)
        
    
    plot_scatter_df(passe_certo,'#00FF79',12)
    plot_scatter_df(passe_errado,'#FD2B2C',9)
    plt.savefig(f'passe_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)

    plt.show()
    st.pyplot(fig)
    st.markdown(get_binary_file_downloader_html(f'passe_{nome_jogador}.png', 'Passe'), unsafe_allow_html=True)
    # return fig
            #-------------------------------------------------------------------------------------------------------
   def cluster(cor_fundo='#2C2B2B'):
    global df_passe
    passe_plot()
    passe_filtrado =  df_passe
    passe_filtrado = passe_filtrado[['from_x','from_y','to_x','to_y']]
    passe_filtrado = passe_filtrado.rename(columns={'from_x':'x','from_y':'y'})


    passe_filtrado = passe_filtrado[['x','y','to_x','to_y']]
    passe_filtrado['y_invertido'] = 100 - passe_filtrado['y']
    y = list(passe_filtrado['y_invertido'])
    x = list(passe_filtrado['x'])
    counts, x_bin, y_bin = np.histogram2d(x,y, bins=[np.arange(0, 110, 10), np.arange(0, 110, 10)])

    # bin the data into equally spaced groups
    x_cut = pd.cut(passe_filtrado.x, np.linspace(0, 110, 10), right=False)
    y_cut = pd.cut(passe_filtrado.y_invertido,np.linspace(0, 110, 10), right=False)


    df_bins = pd.DataFrame({'x_interval':x_cut,'y_interval':y_cut})
    df_bins['quantidade'] = 1
    bin_top = df_bins.groupby(['x_interval','y_interval'])['quantidade'].count().reset_index()
    bin_top = bin_top.sort_values('quantidade',ascending=False).reset_index().head(10)


    lista_x_bin = []
    lista_y_bin = []
    for linha in range(len(bin_top)):
      lista_x_bin.append(bin_top['x_interval'][linha])
      lista_y_bin.append(bin_top['y_interval'][linha])

    passe_filtrado = passe_filtrado[['x','y','to_x','to_y']]
    bins_geral = df_bins.join(passe_filtrado)
    df_passe_plot = bins_geral[(bins_geral['x_interval'].isin(lista_x_bin)) & (bins_geral['y_interval'].isin(lista_y_bin))].reset_index(drop=True)
    # df_passe_plot


    #-------------------------------------------------------------------------------------------------------------
    # df_passe_plot = df_passe[['from_x','from_y','to_x','to_y']]
    df_passe_plot = df_passe_plot[['x','y','to_x','to_y']]
  
    valores = df_passe_plot.values

    passes_total = len(df_passe_plot)
    max_cluster = int(len(df_passe_plot)/8)
    min_cluster = int(len(df_passe_plot)/15)
    dic_geral_clusters = []
    df_passe = df_passe_plot

    #### KMEANS
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    from sklearn.metrics import silhouette_score

    dic_sill = {}
    for i in range(min_cluster, max_cluster):
      km = KMeans(n_clusters=i)
      km.fit(valores)
      label = km.predict(valores)
      sill = silhouette_score(valores,label)
      dic_sill.update({i:sill})

    df_sill = pd.DataFrame(dic_sill,index=[0]).transpose().reset_index()
    n_cluster = df_sill.sort_values(0,ascending=False).reset_index()['index'][0]
    valor =  df_sill.sort_values(0,ascending=False).reset_index()[0][0]
    print(f'{n_cluster}:{valor}')
    dic_geral_clusters.append({'metodo':'kmeans','n_cluster':'n_cluster','acerto':valor})

    km = KMeans(
        n_clusters=n_cluster, init='random',
        n_init=1, max_iter=300, 
        tol=1e-04, random_state=0
    )
    y_km = km.fit_predict(valores)

    # cor_fundo='#2C2B2B'
    df_passe['cluster'] = y_km
    df_passe['quantidade'] = 0
    cluster = df_passe.groupby('cluster')['quantidade'].count().reset_index().sort_values('quantidade',ascending=False).reset_index(drop=True)
    lista_cluster = list(cluster['cluster'])[0:3]
    df_plot = df_passe[df_passe['cluster'].isin(lista_cluster)].reset_index(drop=True)

    # df_plot
    pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,orientation='horizontal',
                stripe=False, line_zorder=2)
    fig, ax = pitch.draw()
    # zo=2   
    def plot_scatter_df(df,cor,zo):
      pitch.scatter(df.to_x, df.to_y, s=200, edgecolors=cor,lw=2, c=cor_fundo, zorder=zo+1, ax=ax)
      # plt.scatter(data=df, x='to_x',y='to_y',color=cor,zorder=zo+1,label='df',edgecolors='white',s=200)
      for linha in range(len(df)):
        x_inicial = df['x'][linha]
        y_inicial = df['y'][linha]
        x_final = df['to_x'][linha]
        y_final = df['to_y'][linha]
        # plt.plot([x_inicial,x_final],[y_inicial,y_final],color=cor,lw=5)
        lc1 = pitch.lines(x_inicial, y_inicial,
                      x_final, y_final,
                      lw=5, transparent=True, comet=True, label='completed passes',
                      color=cor, ax=ax,zorder=zo)
    
    lista_cor = ['#FF4E63','#8D9713','#00A6FF']
    for clus,cor in zip(lista_cluster,lista_cor):
      df = (df_plot[df_plot['cluster'] == clus].reset_index())
      df['cor'] = cor 
      plot_scatter_df(df,cor,2)
    plt.savefig(f'cluster_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)
    plt.show()
    st.pyplot(fig)
    st.markdown(get_binary_file_downloader_html(f'cluster_{nome_jogador}.png', 'Cluster'), unsafe_allow_html=True)
    # return fig
              #-----------------------------------------------------------------------------------------------
   def xg(cor_fundo='#2c2b2b'):
    lista_xg = []
    
    for x in lista_id:
      jogo = x
      headers = {'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Host': 'searchapi.wyscout.com',
      'If-None-Match':"""W/"d0354abd55fce562c787982a78c55780""",
      'Origin': 'https://platform.wyscout.com',
      'Referer': 'https://platform.wyscout.com/app/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-site',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

      payload = {'match_id': x,
      'lang':'',
      'debug': '',
      'event_type': 'shots',
      'score': 'winning,draw,losing',
      'minutes':'', 
      'position':'', 
      'under_card':'', 
      'token': token,
      'groupId': '1231619',
      'subgroupId': '286367'}

      sleep(randint(2, 7))
      site = 'https://searchapi.wyscout.com/api/v1/match_report/players/{}/shots?'.format(player)
      r = requests.get(site,data=payload,headers=headers)
      
      parsed = json.loads(r.text)
      data = json.loads(r.text)
      df= pd.json_normalize(data,sep='_') 
      
      shot_series = (df['data_shots']).to_dict()
      shot = pd.DataFrame.from_dict(shot_series)

      lista_df = []


      for i in range(len(shot)):
        dicionario = (shot.iloc[i])
        for k,v in dicionario.items():
          novo_dic = v 
          minuto = novo_dic['minute']
          tempo = novo_dic['period']
          # jogador = novo_dic['player']
          xg = novo_dic['xg']
          x = novo_dic['x']
          y= novo_dic['y']
          outcome = novo_dic['shotOutcome']
          tipo = novo_dic['footName']

          data_xg = {'jogo':jogo,'minuto':minuto,'tempo':tempo,'xg':xg,'x':x,'y':y,'outcome':outcome,'tipo':tipo}
          df_final = pd.DataFrame(data=data_xg, index=[0])
          lista_df.append(df_final)
    
      try:
        
        xg_jogador = pd.concat(lista_df, axis=0, ignore_index=True)
        lista_df.clear()
        lista_xg.append(xg_jogador)
      except: 
        pass
      
    try:
      xg_final = pd.concat(lista_xg, axis=0, ignore_index=True)
      lista_xg.clear()
    except:
      pass

    # cor_fundo='#2C2B2B'
    pitch = Pitch(pitch_type='wyscout', figsize=(15,10),pitch_color=cor_fundo,orientation='horizontal',half=True,
                stripe=False, line_zorder=2)
    fig, ax = pitch.draw()

    zo= 12
    

    for i in range(len(xg_final)):
        x = (xg_final['x'][i])
        y = (xg_final['y'][i])
        xg_valor = xg_final['xg']
        tamanho_dot = [1400 * x for x in xg_valor][i]

        # if xg_final['outcome'][i] == 'blocked':
      #     plt.scatter(x, y, marker='o', s=tamanho_dot, color='#FFC000',label='bloqueado',zorder=zo+1)
        if xg_final['outcome'][i] == 'goal':
            plt.scatter(x, y, marker='o', s=tamanho_dot, color='#00F979', alpha=0.8,label='gol',zorder=zo+1,ec='white',lw=2)
        else:
            plt.scatter(x, y, marker='o', s=tamanho_dot, color=cor_fundo, alpha=0.8,zorder=zo,ec='white',lw=2)
        # elif xg_final['outcome'][i] == 'gk_save':
        #     plt.scatter(x, y, marker='o', s=tamanho_dot, color='#00B4FF',label='salvo',zorder=zo+1,ec='white',lw=2)
        # elif xg_final['outcome'][i] == 'wide':
        #     plt.scatter(x, y, marker='o', s=tamanho_dot, color='#FF0000',label='fora',zorder=zo+1,ec='white',lw=2)
        # elif xg_final['outcome'][i] == 'post':
        #     plt.scatter(x, y, marker='o', s=tamanho_dot, color='#8B0FFF',label='trave',zorder=zo+1,ec='white',lw=2))
        
    # plt.title('{} (Xg = {}) \n\n ({})'.format(time,xg_soma,jogo),color='white')
    

    #LEGENDA
    # plt.scatter(48, 15, marker='*', s=300, color='#84FF00',label='gol',zorder=zo+1)
    # plt.scatter(48, 25, marker='o', s=300, color='#00B4FF',label='salvo',zorder=zo+1)
    # plt.scatter(48, 35, marker='x', s=300, color='#FF0000',label='fora',zorder=zo+1)
    # plt.scatter(48, 45, marker='s', s=300, color='#FFC000',label='bloqueado',zorder=zo+1)
    # plt.scatter(48, 60, marker='p', s=300, color='#8B0FFF',label='trave',zorder=zo+1)

    plt.savefig(f'xg_{nome_jogador}.png',dpi=300,bbox_inches = "tight",facecolor=cor_fundo)

    plt.show()
    st.pyplot(fig)
    st.markdown(get_binary_file_downloader_html(f'xg_{nome_jogador}.png', 'xg'), unsafe_allow_html=True)
    # return fig

   info_jogador  = info_jogador.replace(to_replace=['RW','LW','RWF','LWF','LAMF','RAMF'],value='Extremo')
   info_jogador  = info_jogador.replace(to_replace=['CF'],value='Atacante')
   info_jogador  = info_jogador.replace(to_replace=['RCB','LCB','CB','RCB3','LCB3'],value='Zagueiro')
   info_jogador  = info_jogador.replace(to_replace=['RB','RWB','RB5','RBW'],value='Lateral direito')
   info_jogador  = info_jogador.replace(to_replace=['LB','LWB','LB5','LBW'],value='Lateral Esquerdo')
   info_jogador  = info_jogador.replace(to_replace=['AMF',],value='Meio Campista')
   info_jogador  = info_jogador.replace(to_replace=['DM','RCMF3','LCMF3','LDMF','RDMF','DMF','RCMF','LCMF'],value='Volante')
   info_jogador  = info_jogador.replace(to_replace=['GK'],value='Goleiro')
   nome_jogador=info_jogador['name'][0]
   
   st.write('## Gráficos')
   st.write('Obs: Caso escolha **progressivo**, selecione **assist** antes')
   opcao_campo=st.checkbox('Selecionar gráfico',value=False)
   color = st.color_picker('Escolha uma cor', '#2c2b2b')
   st.write('A cor é', color)
   if opcao_campo == True:
      lista_campo=['Assist','Progressivo','Recepção','Defensivo','Cruzamento','Cluster','xG','Heatmap']
      botao_campo=st.multiselect('Selecione o gráfico',lista_campo)
      if 'Assist' in botao_campo:
         assist(color)
      if 'Progressivo' in botao_campo:
         progressivo(color)
      if 'Recepção' in botao_campo:
         recepção(color)
      if 'Defensivo' in botao_campo:
         defensivo(color)
      if 'Cruzamento' in botao_campo:
         cruzamento(color)
        #  cruzamento
      if 'Cluster' in botao_campo:
         cluster(color)
      if 'xG' in botao_campo:
         xg(color)
      if 'Heatmap' in botao_campo:
         heatmap()

   st.write('## Arte Quadro')

   opcao_quadro=st.checkbox('Deseja Quadro do atleta?',value=False)
   if opcao_quadro == True:
      # df_jogador = df
      # df_jogador
      minutos_df = df_jogador.groupby('id')['playerStats_minutes_on_field'].sum().reset_index().rename(columns={'playerStats_minutes_on_field':'Minutos em campo'})
      jogos = df_jogador.groupby('id')['playerStats_minutes_on_field'].count().reset_index().rename(columns={'playerStats_minutes_on_field':'Jogos'})
      df_jogador_sum = df_jogador.groupby('id').sum().reset_index()
      lista_colunas = []
      for coluna in df_jogador_sum: 
        if (coluna.startswith('playerStats')) == True:
          lista_colunas.append(coluna)

      lista_colunas = lista_colunas[1:]
      lista_df_per_90 = []
      for linha in range(len(df_jogador_sum)):
          minutos = df_jogador_sum['playerStats_minutes_on_field'][linha]
          id_jogador  = df_jogador_sum['id'][linha]
          dic_df_90 = {'id': id_jogador,'playerStats_minutes_on_field':minutos}

          for coluna in lista_colunas:
            valor_coluna =(df_jogador_sum[coluna][linha])
            def p90_Calculator(variable_value, minutes_played):
              ninety_minute_periods = minutes_played/90
              p90_value = variable_value/ninety_minute_periods
              return p90_value
            per_90 = p90_Calculator(valor_coluna, minutos)
            dic_df_90.update({coluna:per_90})
          df_90_jogador = pd.DataFrame(dic_df_90,index=[0])
          lista_df_per_90.append(df_90_jogador)
      df_90 = pd.concat(lista_df_per_90,ignore_index=True)
      df_90 = df_90.fillna(0)
      df_90 = df_90.round(2)

      jogador = nome_jogador
      clube = info_jogador['current_team_name'][0]    
      campeonato = st.text_input('Digite o nome do campeonato, caso tenha mais de um coloque todas')
      temporada= st.text_input('Digite a temporada')
      minutos_em_campo = minutos_df['Minutos em campo'][0].astype('int')
      space=st.number_input('Digite um número de espaçamento entre 800 e 1400')

      def arte_posicoes(df):
        posição=df['primary_position'][0]
        # # df['primary_position'][0]='Zagueiro'
        # # posição=df['primary_position'][0]
        # posição='Meio Campista'
        if posição=='Zagueiro':
          defensivo(color)
          recepção(color)
          assist(color)
          progressivo(color)
        elif posição=='Lateral Esquerdo':
          defensivo(color)
          recepção(color)
          cruzamento(color)
        elif posição=='Lateral direito':
          defensivo(color)
          recepção(color)
          cruzamento(color)
        elif posição=='Volante':
          defensivo(color)
          recepção(color)
          cluster(color)
          assist(color)
          progressivo(color)
        elif posição=='Meio Campista':
          xg(color)
          recepção(color)
          cluster(color)
          assist(color)
        elif posição=='Extremo':
          xg(color)
          recepção(color)
          cruzamento(color)
          assist(color)
        elif posição=='Atacante':
          xg(color)
          recepção(color)
          assist(color)
      arte_posicoes(info_jogador)

      try:
        chute_no_alvo = df_jogador_sum['playerStats_shot_on_goal'][0].astype('int')
      except:
        chute_no_alvo = 0
      try:
        gols = df_jogador_sum['playerStats_non_penalty_goal'][0].astype('int')
      except:
        gols = 0
      try:
        xg_total = round(df_jogador_sum['playerStats_xg_shot'][0]  - ((df_jogador_sum['playerStats_goal'][0] - df_jogador_sum['playerStats_non_penalty_goal'][0]) * 0.75),2)
      except:
        xg_total = 0
      try:
        xg_por_chute = round(df_jogador_sum['playerStats_xg_shot'][0]/df_jogador_sum['playerStats_shot'][0],2)
      except:
        xg_por_chute = 0
      try:
        passe_chave = df_jogador_sum['playerStats_key_pass_success'][0].astype('int')
      except:
        passe_chave = 0
      try:
        assistencia = df_jogador_sum['playerStats_assist_success'][0].astype('int')
      except:
        assistencia = 0
      try:
        xA = round(df_jogador_sum['playerStats_xg_assist'][0],2)
      except:
        xA = 0
      try:
        duelos_1_x_1= df_jogador_sum['playerStats_defensive_one_on_one_success'][0].astype('int')
      except:
        duelos_1_x_1 = 0
      try:
        interceptacoes = df_jogador_sum['playerStats_interception_success'][0].astype('int')
      except:
        interceptacoes = 0
      try:
        desarmes = df_jogador_sum['playerStats_defensive_duel_success'][0].astype('int')
      except:
        desarmes = 0
      try:
        progressivo_por_passe = round((df_jogador_sum['playerStats_progressive_pass_success'][0]/df_jogador_sum['playerStats_pass_success'][0])*100,2)
      except:
        progressivo_por_passe = 0
      try:
        cruzamentos_certos_porcentagem = round((df_jogador_sum['playerStats_cross_success'][0]/df_jogador_sum['playerStats_cross'][0])*100,2)
      except:
        cruzamentos_certos_porcentagem = 0

      
      recepção = f'recepção_{jogador}.png'
      assist =  f'assist_{jogador}.png'
      xg =  f'xg_{jogador}.png'
      defensivo = f'defensivo_{jogador}.png'
      passes_progressivos = f'progressivo_{jogador}.png'
      passes_cluster = f'cluster_{jogador}.png'
      cruzamento = f"cruzamento_{jogador}.png"

      arte = Image.new('RGB', (6419,4542), '#2C2B2B')
      W,H  = arte.size
      #TITULO
      font = ImageFont.truetype('Camber/Camber-Bd.ttf',400)
      msg = f'{jogador}'

      draw = ImageDraw.Draw(arte)
      w, h = draw.textsize(msg,spacing=20,font=font)
      w_titulo, h_titulo = draw.textsize(msg,spacing=20,font=font)
      draw.text((269,121),msg, fill='white',spacing= 20,font=font)
      #Linhas título
      draw = ImageDraw.Draw(arte)
      draw.line((150,100,W-150, 100,), fill='white', width=5)         #(x_final,y_final,x_inicial,y_inicial)
      draw.line((150,510,W-150, 510,), fill='white', width=5)         #(x_final,y_final,x_inicial,y_inicial)
      #TIME
      font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',160)
      msg = f'{clube}'
      draw = ImageDraw.Draw(arte)
      w_time, h_time = draw.textsize(msg,spacing=20,font=font)
      draw.text((269+w_titulo+300,270),msg, fill='white',spacing= 20,font=font)
      posição_traço = 269+w_titulo+300+w_time+60
      #linha campeonato
      draw = ImageDraw.Draw(arte)
      draw.line((posição_traço+30,220,posição_traço+30, 460), fill='white', width=5)         #(x_final,y_final,x_inicial,y_inicial)
      posição_campeonato = posição_traço+120
      font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',160)
      msg = f'{campeonato}'
      draw = ImageDraw.Draw(arte)
      draw.text((posição_campeonato,270),msg, fill='white',spacing= 20,font=font)
      

      
      posição_temporada=posição_campeonato+space
      font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',160)
      msg = f'{temporada}'
      draw = ImageDraw.Draw(arte)
      draw.text((posição_temporada,270),msg, fill='white',spacing= 20,font=font)
      #Logo
      fot =Image.open('Logos/Copy of pro_branco.png')
      w,h = fot.size
      fot = fot.resize((int(w/1.5),int(h/1.5)))
      fot = fot.copy()
      arte.paste(fot,(5203,3908),fot)
      # info_jogador



      def quadro_posicoes(df):
        posição=df['primary_position'][0]
        # posição='Meio Campista'
        if posição=='Zagueiro':

          im = Image.open(recepção)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1331,2047))
          arte.paste(im,(305,1100))
          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Onde recebe a bola'
          draw = ImageDraw.Draw(arte)
          draw.text((305,930),msg, fill='white',spacing= 30,font=font)
          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{minutos_em_campo} Minutos em campo'
          draw = ImageDraw.Draw(arte)
          draw.text((305,3200),msg, fill='white',spacing= 20,font=font)
          #----------------------------------------------------------------------------------------------------------------------------------------------------------
          #Defensivo
          im = Image.open(defensivo)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(2300,1030))

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Cobertura Defensiva'
          draw = ImageDraw.Draw(arte)
          draw.text((2370,930),msg, fill='white',spacing= 30,font=font)



          draw = ImageDraw.Draw(arte)
          draw.line((2350,3400,3700, 3400), fill='white', width=3) #(x_final,y_final,x_inicial,y_inicial)


          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(2250,3200))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{duelos_1_x_1} Duelos 1x1 ganhos'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3480),msg, fill='white',spacing= 30,font=font)

          msg = f'{interceptacoes} Interceptações'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3580),msg, fill='white',spacing= 30,font=font)

          msg = f'{desarmes} Desarmes'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3680),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((2500,3250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Errado'
          draw = ImageDraw.Draw(arte)
          draw.text((3050,3250),msg, fill='white',spacing= 30,font=font)

          #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

          #Passes progressivos
          im = Image.open(passes_progressivos)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(4550,1030))


          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Passes Progressivos'
          draw = ImageDraw.Draw(arte)
          draw.text((4620,930),msg, fill='white',spacing= 30,font=font)

          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(4550,3200))



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((4800,3250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Errado'
          draw = ImageDraw.Draw(arte)
          draw.text((5330,3250),msg, fill='white',spacing= 30,font=font)


          draw = ImageDraw.Draw(arte)
          draw.line((4600,3400,6000, 3400), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{progressivo_por_passe}% Passes progressivos/passe'
          draw = ImageDraw.Draw(arte)
          draw.text((4600,3480),msg, fill='white',spacing= 30,font=font)
          arte.save(f'quadro_{jogador}.png',quality=95,bbox_inches = "tight",facecolor='#2C2B2B')
          st.image(f'quadro_{jogador}.png')

        elif posição=='Lateral Esquerdo':

          #RECEPÇÃO
          im = Image.open(recepção)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1331,2047))
          arte.paste(im,(305,1100))
          

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Onde recebe a bola'
          draw = ImageDraw.Draw(arte)
          draw.text((305,930),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{minutos_em_campo} Minutos em campo'
          draw = ImageDraw.Draw(arte)
          draw.text((305,3200),msg, fill='white',spacing= 20,font=font)
          #----------------------------------------------------------------------------------------------------------------------------------------------------------
          #xg
          im = Image.open(defensivo)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(2300,1030))

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Cobertura Defensiva'
          draw = ImageDraw.Draw(arte)
          draw.text((2370,930),msg, fill='white',spacing= 30,font=font)



          draw = ImageDraw.Draw(arte)
          draw.line((2350,3400,3700, 3400), fill='white', width=3) #(x_final,y_final,x_inicial,y_inicial)


          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(2250,3200))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{duelos_1_x_1} Duelos 1x1 ganhos'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3480),msg, fill='white',spacing= 30,font=font)

          msg = f'{interceptacoes} Interceptações'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3580),msg, fill='white',spacing= 30,font=font)

          msg = f'{desarmes} Desarmes'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3680),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((2500,3250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Errado'
          draw = ImageDraw.Draw(arte)
          draw.text((3050,3250),msg, fill='white',spacing= 30,font=font)

          #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

          #Cruzamento
          im = Image.open(cruzamento)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(4550,1030))


          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Cruzamentos'
          draw = ImageDraw.Draw(arte)
          draw.text((4620,930),msg, fill='white',spacing= 30,font=font)

          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(4550,2200))



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((4800,2250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Errado'
          draw = ImageDraw.Draw(arte)
          draw.text((5330,2250),msg, fill='white',spacing= 30,font=font)


          draw = ImageDraw.Draw(arte)
          draw.line((4600,2460,6000, 2460), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{cruzamentos_certos_porcentagem}% de cruzamento certos'
          draw = ImageDraw.Draw(arte)
          draw.text((4600,2520),msg, fill='white',spacing= 30,font=font)

          arte.save(f'quadro_{jogador}.png',quality=95,bbox_inches = "tight",facecolor='#2C2B2B')
          st.image(f'quadro_{jogador}.png')

        elif posição=='Lateral direito':

          #RECEPÇÃO
          im = Image.open(recepção)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1331,2047))
          arte.paste(im,(305,1100))
          

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Onde recebe a bola'
          draw = ImageDraw.Draw(arte)
          draw.text((305,930),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{minutos_em_campo} Minutos em campo'
          draw = ImageDraw.Draw(arte)
          draw.text((305,3200),msg, fill='white',spacing= 20,font=font)
          #----------------------------------------------------------------------------------------------------------------------------------------------------------
          #xg
          im = Image.open(defensivo)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(2300,1030))

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Cobertura Defensiva'
          draw = ImageDraw.Draw(arte)
          draw.text((2370,930),msg, fill='white',spacing= 30,font=font)



          draw = ImageDraw.Draw(arte)
          draw.line((2350,3400,3700, 3400), fill='white', width=3) #(x_final,y_final,x_inicial,y_inicial)


          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(2250,3200))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{duelos_1_x_1} Duelos 1x1 ganhos'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3480),msg, fill='white',spacing= 30,font=font)

          msg = f'{interceptacoes} Interceptações'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3580),msg, fill='white',spacing= 30,font=font)

          msg = f'{desarmes} Desarmes'
          draw = ImageDraw.Draw(arte)
          draw.text((2350,3680),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((2500,3250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Errado'
          draw = ImageDraw.Draw(arte)
          draw.text((3050,3250),msg, fill='white',spacing= 30,font=font)

          #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

          #Cruzamento
          im = Image.open(cruzamento)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(4550,1030))


          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Cruzamentos'
          draw = ImageDraw.Draw(arte)
          draw.text((4620,930),msg, fill='white',spacing= 30,font=font)

          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(4550,2200))



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((4800,2250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Errado'
          draw = ImageDraw.Draw(arte)
          draw.text((5330,2250),msg, fill='white',spacing= 30,font=font)


          draw = ImageDraw.Draw(arte)
          draw.line((4600,2460,6000, 2460), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{cruzamentos_certos_porcentagem}% de cruzamento certos'
          draw = ImageDraw.Draw(arte)
          draw.text((4600,2520),msg, fill='white',spacing= 30,font=font)

          arte.save(f'quadro_{jogador}.png',quality=95,bbox_inches = "tight",facecolor='#2C2B2B')
          st.image(f'quadro_{jogador}.png')


        elif posição=='Volante':

          #RECEPÇÃO
          im = Image.open(recepção)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1331,2047))
          arte.paste(im,(305,1100))
          

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Onde recebe a bola'
          draw = ImageDraw.Draw(arte)
          draw.text((305,930),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{minutos_em_campo} Minutos em campo'
          draw = ImageDraw.Draw(arte)
          draw.text((305,3200),msg, fill='white',spacing= 20,font=font)
          #------------------------------------------------------------------------------
          # DEFENSIVO

          im = Image.open(defensivo)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(1700,1040))


          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Cobertura Defensiva'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,930),msg, fill='white',spacing= 30,font=font)

          draw = ImageDraw.Draw(arte)
          draw.line((1780,3400,3100, 3400), fill='white', width=3) 

          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(1700,3200))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{duelos_1_x_1} Duelos 1x1 ganhos'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,3480),msg, fill='white',spacing= 30,font=font)

          msg = f'{interceptacoes} Interceptações'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,3580),msg, fill='white',spacing= 30,font=font)

          msg = f'{desarmes} Desarmes'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,3680),msg, fill='white',spacing= 30,font=font)



          #---------------------------------------------------------------------------

          im = Image.open(passes_cluster)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(3150,1040))


          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Passes mais Comuns'
          draw = ImageDraw.Draw(arte)
          draw.text((3230,930),msg, fill='white',spacing= 30,font=font)



          #------------------------------------------------------------------------------------
          im = Image.open(passes_progressivos)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(4600,1040))

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Passes Progressivos'
          draw = ImageDraw.Draw(arte)
          draw.text((4680,930),msg, fill='white',spacing= 30,font=font)

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{progressivo_por_passe}% Passes progressivos/passes'
          draw = ImageDraw.Draw(arte)
          draw.text((4670,3480),msg, fill='white',spacing= 30,font=font)

          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(4600,3200))

          draw = ImageDraw.Draw(arte)
          draw.line((4660,3400,6100, 3400), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((4860,3250),msg, fill='white',spacing= 20,font=font)
          draw.text((1950,3250),msg, fill='white',spacing= 20,font=font)
          msg = f'Errado'
          draw.text((5380,3250),msg, fill='white',spacing= 20,font=font)
          draw.text((2470,3250),msg, fill='white',spacing= 20,font=font)

          arte.save(f'quadro_{jogador}.png',quality=95,bbox_inches = "tight",facecolor='#2C2B2B')
          st.image(f'quadro_{jogador}.png')


        elif posição=='Meio Campista':

          #RECEPÇÃO
          im = Image.open(recepção)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1331,2047))
          arte.paste(im,(305,1100))
          

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Onde recebe a bola'
          draw = ImageDraw.Draw(arte)
          draw.text((305,930),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{minutos_em_campo} Minutos em campo'
          draw = ImageDraw.Draw(arte)
          draw.text((305,3200),msg, fill='white',spacing= 20,font=font)

          #Passe finalização
          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Passes para finalização'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,930),msg, fill='white',spacing= 30,font=font)

          im = Image.open(assist)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(1700,1040))

          im = Image.open('Arquivos/legenda-assist.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(1700,2200))



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Chave'
          draw = ImageDraw.Draw(arte)
          draw.text((1970,2250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Assistência'
          draw = ImageDraw.Draw(arte)
          draw.text((2470,2250),msg, fill='white',spacing= 30,font=font)


          draw = ImageDraw.Draw(arte)
          draw.line((1780,2450,3100, 2450), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{passe_chave} Passes chave'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,2520),msg, fill='white',spacing= 30,font=font)

          msg = f'{assistencia} Assistências'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,2620),msg, fill='white',spacing= 30,font=font)

          msg = f'{xA} xA'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,2720),msg, fill='white',spacing= 30,font=font)

          #Cluster

          im = Image.open(passes_cluster)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,2166))
          arte.paste(im,(3150,1040))


          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Passes mais Comuns'
          draw = ImageDraw.Draw(arte)
          draw.text((3230,930),msg, fill='white',spacing= 30,font=font)

          #XG
          im = Image.open(xg)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(4600,1040))



          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Qualidade das chances'
          draw = ImageDraw.Draw(arte)
          draw.text((4680,930),msg, fill='white',spacing= 30,font=font)

          draw = ImageDraw.Draw(arte)
          draw.line((4660,2550,6000, 2550), fill='white', width=3) 

          im = Image.open('Arquivos/legenda-xg-tamanho (1).png')
          border = (800, 900, 500, 200) # left, up, right, bottom
          im = ImageOps.crop(im, border)
          im = im.rotate(270,expand=4)
          w,h = im.size
          im = im.resize((int(w/1.5),int(h/1.5)))
          im = im.copy()
          arte.paste(im,(4650,2200))

          im = Image.open('Arquivos/legenda-xg-gol.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(5500,2200))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{chute_no_alvo} Chutes no alvo'
          draw = ImageDraw.Draw(arte)
          draw.text((4660,2630),msg, fill='white',spacing= 30,font=font)


          msg = f'{gols} Gols'
          draw = ImageDraw.Draw(arte)
          draw.text((4660,2730),msg, fill='white',spacing= 30,font=font)


          msg = f'{xg_total} xG total'
          draw = ImageDraw.Draw(arte)
          draw.text((5500,2630),msg, fill='white',spacing= 30,font=font)

          msg = f'{xg_por_chute} xG por chute'
          draw = ImageDraw.Draw(arte)
          draw.text((5500,2730),msg, fill='white',spacing= 30,font=font)

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Maior qualidade das chances'
          draw = ImageDraw.Draw(arte)
          draw.text((4660,2400),msg, fill='white',spacing= 30,font=font)
          msg = f'Gol'
          draw.text((5750,2250),msg, fill='white',spacing= 30,font=font)

          arte.save(f'quadro_{jogador}.png',quality=95,bbox_inches = "tight",facecolor='#2C2B2B')
          st.image(f'quadro_{jogador}.png')

        elif posição=='Extremo':

          #RECEPÇÃO
          im = Image.open(recepção)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1331,2047))
          arte.paste(im,(305,1100))
          

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Onde recebe a bola'
          draw = ImageDraw.Draw(arte)
          draw.text((305,930),msg, fill='white',spacing= 30,font=font)



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{minutos_em_campo} Minutos em campo'
          draw = ImageDraw.Draw(arte)
          draw.text((305,3200),msg, fill='white',spacing= 20,font=font)

          #Passe finalização
          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Passes para finalização'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,930),msg, fill='white',spacing= 30,font=font)

          im = Image.open(assist)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(1700,1040))

          im = Image.open('Arquivos/legenda-assist.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(1700,2200))



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Chave'
          draw = ImageDraw.Draw(arte)
          draw.text((1970,2250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Assistência'
          draw = ImageDraw.Draw(arte)
          draw.text((2470,2250),msg, fill='white',spacing= 30,font=font)


          draw = ImageDraw.Draw(arte)
          draw.line((1780,2450,3100, 2450), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{passe_chave} Passes chave'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,2520),msg, fill='white',spacing= 30,font=font)

          msg = f'{assistencia} Assistências'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,2620),msg, fill='white',spacing= 30,font=font)

          msg = f'{xA} xA'
          draw = ImageDraw.Draw(arte)
          draw.text((1780,2720),msg, fill='white',spacing= 30,font=font)

          #Cruzamento

          im = Image.open(cruzamento)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(3150,1040))


          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Cruzamentos'
          draw = ImageDraw.Draw(arte)
          draw.text((3230,930),msg, fill='white',spacing= 30,font=font)

          im = Image.open('Arquivos/legenda-acerto-erro.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(3200,2200))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Certo'
          draw = ImageDraw.Draw(arte)
          draw.text((3470,2250),msg, fill='white',spacing= 20,font=font)
          msg = f'Errado'
          draw.text((3980,2250),msg, fill='white',spacing= 20,font=font)

          draw = ImageDraw.Draw(arte)
          draw.line((3230,2450,4540, 2450), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{cruzamentos_certos_porcentagem}% de cruzamentos certos'
          draw = ImageDraw.Draw(arte)
          draw.text((3230,2530),msg, fill='white',spacing= 30,font=font)

          #XG
          im = Image.open(xg)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(4600,1040))



          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Qualidade das chances'
          draw = ImageDraw.Draw(arte)
          draw.text((4680,930),msg, fill='white',spacing= 30,font=font)

          draw = ImageDraw.Draw(arte)
          draw.line((4660,2550,6000, 2550), fill='white', width=3) 

          im = Image.open('Arquivos/legenda-xg-tamanho (1).png')
          border = (800, 900, 500, 200) # left, up, right, bottom
          im = ImageOps.crop(im, border)
          im = im.rotate(270,expand=4)
          w,h = im.size
          im = im.resize((int(w/1.5),int(h/1.5)))
          im = im.copy()
          arte.paste(im,(4650,2200))

          im = Image.open('Arquivos/legenda-xg-gol.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(5500,2200))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{chute_no_alvo} Chutes no alvo'
          draw = ImageDraw.Draw(arte)
          draw.text((4660,2630),msg, fill='white',spacing= 30,font=font)


          msg = f'{gols} Gols'
          draw = ImageDraw.Draw(arte)
          draw.text((4660,2730),msg, fill='white',spacing= 30,font=font)


          msg = f'{xg_total} xG total'
          draw = ImageDraw.Draw(arte)
          draw.text((5500,2630),msg, fill='white',spacing= 30,font=font)

          msg = f'{xg_por_chute} xG por chute'
          draw = ImageDraw.Draw(arte)
          draw.text((5500,2730),msg, fill='white',spacing= 30,font=font)

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Maior qualidade das chances'
          draw = ImageDraw.Draw(arte)
          draw.text((4660,2400),msg, fill='white',spacing= 30,font=font)
          msg = f'Gol'
          draw.text((5750,2250),msg, fill='white',spacing= 30,font=font)

          arte.save(f'quadro_{jogador}.png',quality=95,bbox_inches = "tight",facecolor='#2C2B2B')
          st.image(f'quadro_{jogador}.png')

        if posição=='Atacante':

          #RECEPÇÃO
          im = Image.open(recepção)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1331,2047))
          arte.paste(im,(305,1100))
          

          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Onde recebe a bola'
          draw = ImageDraw.Draw(arte)
          draw.text((305,930),msg, fill='white',spacing= 30,font=font)
          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{minutos_em_campo} Minutos em campo'
          draw = ImageDraw.Draw(arte)
          draw.text((305,3200),msg, fill='white',spacing= 20,font=font)
          #xg
          im = Image.open(xg)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(2300,1030))
          font = ImageFont.truetype('Camber/Camber-Rg.ttf',120)
          msg = f'Qualidade das chances'
          draw = ImageDraw.Draw(arte)
          draw.text((2370,930),msg, fill='white',spacing= 30,font=font)
          ##legenda gol
          im = Image.open('Arquivos/legenda-xg-gol.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(3200,2200))

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Gol'
          draw = ImageDraw.Draw(arte)
          draw.text((3450,2250),msg, fill='white',spacing= 20,font=font)
          ##legenda tamanho
          im = Image.open('Arquivos/legenda-xg-tamanho (1).png')
          border = (800, 900, 500, 200) # left, up, right, bottom
          im = ImageOps.crop(im, border)
          im = im.rotate(270,expand=4)
          w,h = im.size
          im = im.resize((int(w/1.5),int(h/1.5)))
          im = im.copy()
          arte.paste(im,(2350,2200))

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Maior qualidade das chances'
          draw = ImageDraw.Draw(arte)
          draw.text((2380,2400),msg, fill='white',spacing= 30,font=font)


          draw = ImageDraw.Draw(arte)
          draw.line((2350,2580,3700, 2580), fill='white', width=3) #(x_final,y_final,x_inicial,y_inicial)

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{chute_no_alvo} Chutes no alvo'
          draw = ImageDraw.Draw(arte)
          draw.text((2380,2630),msg, fill='white',spacing= 30,font=font)


          msg = f'{gols} Gols'
          draw = ImageDraw.Draw(arte)
          draw.text((2380,2730),msg, fill='white',spacing= 30,font=font)


          msg = f'{xg_total} xG total'
          draw = ImageDraw.Draw(arte)
          draw.text((3240,2630),msg, fill='white',spacing= 30,font=font)

          msg = f'{xg_por_chute} xG por chute'
          draw = ImageDraw.Draw(arte)
          draw.text((3240,2730),msg, fill='white',spacing= 30,font=font)

          #assist
          im = Image.open(assist)
          im = im.rotate(90,expand=5)
          im = im.copy()
          im = im.resize((1450,1150))
          arte.paste(im,(4550,1030))


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',120)
          msg = f'Passes para finalização'
          draw = ImageDraw.Draw(arte)
          draw.text((4620,930),msg, fill='white',spacing= 30,font=font)

          im = Image.open('Arquivos/legenda-assist.png')
          im = im.resize((852,174))
          im = im.copy()
          arte.paste(im,(4550,2200))



          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Chave'
          draw = ImageDraw.Draw(arte)
          draw.text((4800,2250),msg, fill='white',spacing= 30,font=font)


          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',90)
          msg = f'Assistência'
          draw = ImageDraw.Draw(arte)
          draw.text((5330,2250),msg, fill='white',spacing= 30,font=font)


          draw = ImageDraw.Draw(arte)
          draw.line((4600,2460,6000, 2460), fill='white', width=3) 

          font = ImageFont.truetype('Camber/Camber-RgItalic.ttf',70)
          msg = f'{passe_chave} Passes chave'
          draw = ImageDraw.Draw(arte)
          draw.text((4600,2520),msg, fill='white',spacing= 30,font=font)

          msg = f'{assistencia} Assistências'
          draw = ImageDraw.Draw(arte)
          draw.text((4600,2620),msg, fill='white',spacing= 30,font=font)


          msg = f'{xA} xA'
          draw = ImageDraw.Draw(arte)
          draw.text((4600,2720),msg, fill='white',spacing= 30,font=font)

          arte.save(f'quadro_{jogador}.png',quality=95,bbox_inches = "tight",facecolor='#2C2B2B')
          st.image(f'quadro_{jogador}.png')


      quadro_posicoes(info_jogador)
      st.markdown(get_binary_file_downloader_html(f'quadro_{jogador}.png', 'Quadro'), unsafe_allow_html=True)
      opcao_invertido=st.checkbox('Deseja Inverter',value=False)
      if opcao_invertido == True:
        arte = PIL.ImageOps.invert(arte)
        arte.save(f'quadro-invertido_{jogador}.png',quality=95,bbox_inches = "tight",facecolor=color)
        st.image(f'quadro-invertido_{jogador}.png')
        st.markdown(get_binary_file_downloader_html(f'quadro-invertido_{jogador}.png', 'Quadro'), unsafe_allow_html=True)


if choice == 'Quadro de stats jogador por time':

  time_nome = st.text_input('Nome do time')
  id_time = st.text_input('ID do time')
  times_dic = {time_nome: id_time} 
    
  id_times = list(times_dic.values())
  nome_times = list(times_dic.keys())


  temporada = st.text_input('Temporada')

  token = st.text_input('Token')
  From = st.text_input('2021-01-05')
  To =  st.text_input('2021-12-12')

  lista_frames = []
  for time_id, club in zip(id_times,nome_times):
    team_id = time_id
    


    headers = {'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'searchapi.wyscout.com',
    'If-None-Match': """W/"f32bd1ebe4815670ade3d5582448495a""",
    'Origin': 'https://platform.wyscout.com',
    'Referer': 'https://platform.wyscout.com/app/?',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    payload = {'lang': 'en',
    'from': From,
    'to': To,
    'score': 'winning,draw,losing',
    'columns': 'name,team',
    'token': token,
    'groupId': '1231619',
    'subgroupId': '289819'}

    site = 'https://searchapi.wyscout.com/api/v1/team_stats/teams/{}/stats?'.format(team_id)
    r = requests.get(site,headers=headers,data=payload)
    if r.status_code != 200:
      print('deu erro')
    parsed = json.loads(r.text)
    data = json.loads(r.text)
    df= json_normalize(data,sep='_') 
    df
    lista_jogos = []
    lista_campeonato = []


    jogos_id = df['matches'].to_dict()
    jogos_id =  pd.DataFrame.from_dict(jogos_id)
    for i in range(len(jogos_id)):
      dicionario = (jogos_id.iloc[i])
      for k,v in dicionario.items():
        novo_dic = v
        info = pd.DataFrame(data=v)
        id_jogo = (info.iloc[6][0])
        lista_jogos.append(id_jogo)
        id_campeonato = (info.iloc[2][0])
        lista_campeonato.append(id_campeonato)



    for match_id in lista_jogos:

      headers = {
          'Accept': '*/*',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
          'Connection': 'keep-alive',
          'Host': 'searchapi.wyscout.com',
          'Origin': 'https://platform.wyscout.com',
          'Referer': 'https://platform.wyscout.com/',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-site',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
      }

      params = {
          'match_id': match_id,
          'lang': 'en',
          'score': 'winning,draw,losing',
          'minutes': '',
          'formation': '',
          'opp_formation':'', 
          'token': token,
          'groupId': '1231619',
          'subgroupId': '289819',
      }

      sleep(randint(0,5))
      site = f'https://searchapi.wyscout.com/api/v1/team_stats/teams/{team_id}/filtered_formations?'
      r = requests.get(site,headers=headers,params=params)
      r.status_code
      parsed = json.loads(r.text)
      data = json.loads(r.text)
      df= pd.json_normalize(data,sep='_') 

      numero_mudanças_time = len(df['data_formations'][0])
    
      for x in range(0,numero_mudanças_time):
        lineup = df['data_formations'][0][x]['lineups']
        frame_lineup = pd.DataFrame(lineup)
        frame_lineup['time'] = club
        lista_frames.append(frame_lineup)


  frame_jogadores = pd.concat(lista_frames,axis=0,ignore_index=True).drop_duplicates('playerId')
  lista_posição_wyscout = list(frame_jogadores['code'])

  frame_jogadores  = frame_jogadores.replace(to_replace=['rw','lw','rwf','lwf','lamf','ramf'],value='Extremo')
  frame_jogadores  = frame_jogadores.replace(to_replace=['cf','ss'],value='Atacante')
  frame_jogadores  = frame_jogadores.replace(to_replace=['rcb','lcb','cb','rcb3','lcb3'],value='Zagueiro')
  frame_jogadores  = frame_jogadores.replace(to_replace=['rb','rwb','rb5'],value='Lateral direito')
  frame_jogadores  = frame_jogadores.replace(to_replace=['lb','lwb','lb5'],value='Lateral Esquerdo')
  frame_jogadores  = frame_jogadores.replace(to_replace=['amf',],value='Meio Campista')
  frame_jogadores  = frame_jogadores.replace(to_replace=['dm','rcmf3','lcmf3','ldmf','rdmf','dmf','rcmf','lcmf'],value='Volante')
  frame_jogadores  = frame_jogadores.replace(to_replace=['gk'],value='Goleiro')

  frame_jogadores['posição_wyscout'] = lista_posição_wyscout

  listas_ids_time = list(frame_jogadores['playerId'])

  lista_df = []
  for id_player in listas_ids_time:
      id_player = int(id_player)
      try:
        headers = {'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'searchapi.wyscout.com',
        'Origin': 'https://platform.wyscout.com',
        'Referer': 'https://platform.wyscout.com/app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

        payload ={
            'lang': 'en','from': From,'to': To,'score': 'winning,draw,losing','columns': 'name,positions,minutes_on_field,total_actions,total_actions_success,goal,assist,shot,shot_success,xg_shot,pass,pass_success,long_pass,long_pass_success,cross,cross_success,dribble,dribble_success,duel,duel_success,aerial_duel,aerial_duel_success,interception,loss,own_half_loss,recovery,opponent_half_recovery,yellow_card_minute,red_card_minute',
            'venue':'home,away','token': token,'groupId': '1231619','subgroupId': '286367'
            }
        site = ('https://searchapi.wyscout.com/api/v1/match_stats/players/{}?'.format(id_player))

        sleep(randint(0,3))
        r = requests.get(site,headers=headers,params=payload)

        while  (r.status_code) == 401:
                        
          token = str(input('token'))
          time.sleep(8)
          payload ={
            'lang': 'en','from': From,'to': To,'score': 'winning,draw,losing','columns': 'name,positions,minutes_on_field,total_actions,total_actions_success,goal,assist,shot,shot_success,xg_shot,pass,pass_success,long_pass,long_pass_success,cross,cross_success,dribble,dribble_success,duel,duel_success,aerial_duel,aerial_duel_success,interception,loss,own_half_loss,recovery,opponent_half_recovery,yellow_card_minute,red_card_minute',
            'venue':'home,away','token': token,'groupId': '1231619','subgroupId': '286367'
            }
          r = requests.get(site,headers=headers,params=payload)
          time.sleep(5)
        else:
          parsed = json.loads(r.text)
          data = json.loads(r.text)
          df= pd.json_normalize(data,sep='_')
          df = df.fillna(0)
          df['id'] = id_player
          if len(df) > 0 :
            lista_df.append(df)
      
      except:
        pass

    
  df_jogador = pd.concat(lista_df,axis=0,ignore_index=True)
  df_jogador = df_jogador.fillna(0)
  df_jogador = df_jogador.reset_index(drop=True)



  minutos_df = df_jogador.groupby('id')['playerStats_minutes_on_field'].sum().reset_index().rename(columns={'playerStats_minutes_on_field':'Minutos em campo'})
  jogos = df_jogador.groupby('id')['playerStats_minutes_on_field'].count().reset_index().rename(columns={'playerStats_minutes_on_field':'Jogos'})
  df_jogador_sum = df_jogador.groupby('id').sum().reset_index()


  lista_colunas = []
  for coluna in df_jogador_sum: 
    if (coluna.startswith('playerStats')) == True:
      lista_colunas.append(coluna)

  lista_colunas = lista_colunas[1:]

  lista_df_per_90 = []
  for linha in range(len(df_jogador_sum)):
    minutos = df_jogador_sum['playerStats_minutes_on_field'][linha]
    id_jogador  = df_jogador_sum['id'][linha]
    dic_df_90 = {'id': id_jogador,'playerStats_minutes_on_field':minutos}

    for coluna in lista_colunas:
      valor_coluna =(df_jogador_sum[coluna][linha])
      def p90_Calculator(variable_value, minutes_played):
          
          ninety_minute_periods = minutes_played/90
          p90_value = variable_value/ninety_minute_periods
          return p90_value

      per_90 = p90_Calculator(valor_coluna, minutos)
      dic_df_90.update({coluna:per_90})
    
    df_90_jogador = pd.DataFrame(dic_df_90,index=[0])
    lista_df_per_90.append(df_90_jogador)


  df_90 = pd.concat(lista_df_per_90,ignore_index=True)
  df_90 = df_90.fillna(0)



  df_90 = df_90.round(2)


  try:
    df_90['xG/chute'] = round(df_90['playerStats_xg_shot']/df_90['playerStats_shot'],2)
  except:
    pass

  try:  
    df_90['xG diferença'] = round(df_90['playerStats_goal'] - df_90['playerStats_xg_shot'],2)
  except:
    pass

  try:  
    df_90['Passes Certos %'] = round(df_90['playerStats_pass_success']/df_90['playerStats_pass']*100,2)
  except:
    pass

  try:  
    df_90['Passes Progressivos/Passes %'] = round(df_90['playerStats_progressive_pass_success']/df_90['playerStats_pass_success'],2)*100
  except:
    pass

  try:
    df_90['xA/assistência'] = round(df_90['playerStats_xg_assist'] /df_90['playerStats_shot_assist'],2)
  except:
    pass

  try:
    df_90['xA diferença'] =round(df_90['playerStats_shot_assist'] - df_90['playerStats_xg_assist'],2)
  except:
    pass

  try:
    df_90['Passes Verticais/Passes %'] = round(df_90['playerStats_vertical_pass']/df_90['playerStats_pass_success']*100,2)
  except:
    pass

  try:
    df_90['Gol decisivo/gol %'] = round(df_90['playerStats_decisive_goal_success'] / df_90['playerStats_goal']*100,2)
  except:
    pass

  try:
    df_90['Toque na área %'] = round(df_90['playerStats_touch_in_box'] / df_90['playerStats_action']*100,2)
  except:
    pass

  try:
    df_90['Finalização/Toque na área'] = round( df_90['playerStats_shot_from_box']/ df_90['playerStats_touch_in_box']*100,2)
  except:
    pass

  df_90 = df_90.round(2)

  df_90 = df_90.fillna(0)

  df = df_90[list(df_90.columns[16:])].fillna(0)
  data = df
  colunas_machine = list(df.columns)

  scaler = MinMaxScaler(feature_range=(0, 1))
  scaler.fit(data)
  scaled_data = scaler.transform(data)
  min_max_df = pd.DataFrame(scaled_data)



  numeros = list(range(0,len(min_max_df.columns)))
  dic = {}
  for nome,numero in zip(colunas_machine,numeros):
    dic.update({numero:nome})
  min_max_df  = min_max_df.rename(columns=dic)


  pct_df = min_max_df.rank(pct=True)

  jogador = st.checkbox('Selecionar jogador', value = False)

  if jogador == True:

    id_jogador_escolhido = st.text_input('ID jogador')
    nome_jogador = st.text_input('Nome jogador ')

    pct_df['id'] = df_90['id']
    df_player_quartille = pct_df[pct_df['id'] == int(id_jogador_escolhido)].reset_index(drop=True)
    df_player_filtrado =  df_player_quartille[df_player_quartille > 0.75].dropna(axis=1).reset_index(drop=True)
    lista_colunas_acima = list(df_player_filtrado.columns)
    stats_escolhidas = st.multiselect('Selecione as colunas',lista_colunas_acima)
    # stats_escolhidas = ['playerStats_interception','playerStats_progressive_pass_success', 'playerStats_pass_to_penalty_area_success','playerStats_pre_shot_assist_success','playerStats_touch_in_box_success','playerStats_controlled_penalty_area_entry', 'Toque na área %','playerStats_opponent_half_recovery_success']
    
    # sleep(5)
    nomes = pd.read_csv('content/drive/MyDrive/Footure/Relatorios/colunas_jogador_por_jogador_colunas_colunas_jogador_por_jogador.csv') 

    nomes_antigos = list(nomes['Coluna'])
    nomes_traduzidos = list(nomes['Tradução'])
    dic_nomes = {}
    for antigo,novo in zip(nomes_antigos,nomes_traduzidos):
      dic_nomes.update({antigo:novo})



    df_90_filtrado = df_90[['id'] + stats_escolhidas].reset_index(drop=True)
    df_90_filtrado_jogador = df_90_filtrado[df_90_filtrado['id'] == int(id_jogador_escolhido)].reset_index(drop=True)
    df_final = df_90_filtrado_jogador.T.reset_index()[1:].rename(columns={'index':'Métrica',0:'Números'}).reset_index(drop=True)
    df_final = df_final.replace(dic_nomes)


    arte = Image.new('RGB',(1600,1000),color='black')
    W,H = arte.size
    font = ImageFont.truetype('Camber/Camber-Bd.ttf',70)
    msg = f'Stats - {nome_jogador} {temporada}'
    draw = ImageDraw.Draw(arte)
    w, h = draw.textsize(msg,spacing=20,font=font)
    draw.text(((W-w)/9,50),msg, fill='white',spacing= 20,font=font)

    draw = ImageDraw.Draw(arte)
    draw.line((1800,130, 0,130), fill='white', width=3)

    altura = 150
    for metrica in list(df_final['Métrica']):
      altura += 90
      font = ImageFont.truetype('Camber/Camber-Rg.ttf',30)
      msg = f'{metrica}'
      draw = ImageDraw.Draw(arte)
      draw.text(((W-w)/9,altura),msg, fill='white',spacing= 20,font=font)

      draw = ImageDraw.Draw(arte)
      draw.line(((((W-w)/9)-5),altura+50, 1110,altura+50), fill='white', width=1)

    altura = 150
    for metrica in list(df_final['Números']):
      altura += 90
      font = ImageFont.truetype('Camber/Camber-Bd.ttf',40)
      msg = f'{metrica}'
      draw = ImageDraw.Draw(arte)
      draw.text((1000,altura),msg, fill='white',spacing= 20,font=font)
    arte.save(f'content/drive/MyDrive/Footure/Streamlit plot/Stats/{nome_jogador}.png')

  st.image(f'content/drive/MyDrive/Footure/Streamlit plot/Stats/{nome_jogador}.png')

  
