#mainのプロットりーで一旦の完成系時間で年度ごとラベル
#藤原さんの速度を上げる実験法
#速度の最適化のために、TULCAの計算を外で行い、一度のTULCA呼び出しに変えるべき
#fit_with_new_weightでアップデータを行うようにする
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
from sklearn.decomposition import FactorAnalysis
import pandas as pd
from data_preprocessing_year import preprocess_data
from tulca.tulca import TULCA
from umap import UMAP
import tensorly as tl
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots

global_X = []
global_y = []
global_Z_tda = []
global_y_value=3
app = dash.Dash(__name__)
tulca = TULCA(n_components=np.array([10, 2]),optimization_method="evd")
#scatterと、pulldownBarchartを一緒にするべき
#プルダウンメニューでTDAの大きさを決めれるようにする
#tensor分解と散布図による分析にする。
#散布図をパタパタ帰れるようにする

app.layout = html.Div([
    dcc.Slider(
        id='bar1-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    dcc.Slider(
        id='bar2-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    dcc.Slider(
        id='bar3-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    dcc.Slider(
        id='bar4-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    dcc.Slider(
        id='bar5-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    dcc.Slider(
        id='bar6-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
        dcc.Slider(
        id='bar7-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    dcc.Slider(
        id='bar8-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    dcc.Slider(
        id='bar9-slider',
        min=0,
        max=1,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(0, 11, 1)},
        tooltip={'placement': 'bottom'}
    ),
    html.Button('決定', id='submit-button', n_clicks=0),
    dcc.Graph(
        id='scatter-plot',
        style={'width': '80%', 'height': '80vh'}  # 幅は80%、高さはビューポートの80%に設定
    ),
    dcc.Graph(id='selected-data-time-output'),
    dcc.Graph(id='rack-pc-loadings'),
    dcc.Graph(id='bar-chart')
    
])

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('bar1-slider', 'value'),
     State('bar2-slider', 'value'),
     State('bar3-slider', 'value'),
     State('bar4-slider', 'value'),
     State('bar5-slider', 'value'),
     State('bar6-slider', 'value'),
     State('bar7-slider', 'value'),
     State('bar8-slider', 'value'),
     State('bar9-slider', 'value')
     ]
)
def display_scatter_plot(n_clicks, bar1_value, bar2_value, bar3_value,bar4_value, bar5_value, bar6_value,bar7_value, bar8_value, bar9_value):
    tg = [bar1_value,bar2_value,bar3_value] 
    bg = [bar4_value,bar5_value,bar6_value]
    bw = [bar7_value,bar8_value,bar9_value] 
    
    print(tg)
    print(bg)
    print(bw)
    #tulca = TULCA(n_components=np.array([10, 2]), w_tg=tg, w_bg=bg, w_bw=bw, optimization_method="evd")
    #tulca = TULCA(n_components=np.array([10, 2]), optimization_method="evd")
     
    X_tda = tulca.fit_with_new_weights(w_tg=tg, w_bg=bg, w_bw=bw).transform(global_X, global_y)
    rank = 3  # 分解のランク
    factors = tl.decomposition.parafac(X_tda, rank=rank)
    data={
        'Column1':factors[1][0][:, 0],
        'Column2':factors[1][0][:, 1],
        'Column3':factors[1][0][:, 2],
        'ColorIndex':global_y
    }
    df=pd.DataFrame(data)
    alpha=tulca.get_current_alphas()
    print("alpha")
    print(alpha)
    # fig=px.scatter(df,x=df['Column1'],y=df['Column2'],color=df['y'])
    # # 棒グラフを追加
    # fig.add_trace(px.scatter(df,x=df['Column1'],y=df['Column3'],color=df['y']))
    # fig.add_trace(px.scatter(df,x=df['Column2'],y=df['Column3'],color=df['y']))
    # return fig
    # Scatterグラフを作成
    # Scatterグラフを作成
    fig = px.scatter(df, x='Column1', y='Column2', color='ColorIndex',
                    labels={'Column1': 'X-Axis', 'Column2': 'Y-Axis'},
                    title='Scatter Plots')

    # 別の Scatter グラフを追加
    scatter_trace = go.Scatter(
        x=df['Column1'],
        y=df['Column3'],
        mode='markers',
        marker=dict(color=df['ColorIndex'], colorscale='Viridis'),
        text=df['ColorIndex'],
        showlegend=False,  # 凡例を表示しないように設定
        visible=False  # 初期表示を有効に設定
    )
    fig.add_trace(scatter_trace)

    # 別の Scatter グラフを追加
    scatter_trace2 = go.Scatter(
        x=df['Column2'],
        y=df['Column3'],
        mode='markers',
        marker=dict(color=df['ColorIndex'], colorscale='Viridis'),
        text=df['ColorIndex'],
        showlegend=False,  # 凡例を表示しないように設定
        visible=False  # 初期表示を有効に設定
    )
    fig.add_trace(scatter_trace2)

    # レイアウトの設定
    fig.update_layout(
        xaxis=dict(title='Column1 or Column2'),
        yaxis=dict(title='Column3'),
        coloraxis=dict(colorbar=dict(title='Color Index')),
        updatemenus=[
            {
                'buttons': [
                    {'label': 'Scatter Plot Column1 vs. Column2',
                    'method': 'update',
                    'args': [{'visible': [True, False, False]}]},
                    {'label': 'Scatter Plot Column1 vs. Column3',
                    'method': 'update',
                    'args': [{'visible': [False, True, False]}]},
                    {'label': 'Scatter Plot Column2 vs. Column3',
                    'method': 'update',
                    'args': [{'visible': [False, False, True]}]}
                ],
                'direction': 'down',
                'showactive': True,
                'x': 0.01,
                'xanchor': 'left',
                'y': 1.05,
                'yanchor': 'top'
            }
        ]
    )

    # グラフを表示

    return fig

@app.callback(
    Output('rack-pc-loadings', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('bar1-slider', 'value'),
     State('bar2-slider', 'value'),
     State('bar3-slider', 'value'),
     State('bar4-slider', 'value'),
     State('bar5-slider', 'value'),
     State('bar6-slider', 'value'),
     State('bar7-slider', 'value'),
     State('bar8-slider', 'value'),
     State('bar9-slider', 'value')
     ]
)
def display_heat_map_plot(n_clicks, bar1_value, bar2_value, bar3_value,bar4_value, bar5_value, bar6_value,bar7_value, bar8_value, bar9_value):
    tg = [bar1_value,bar2_value,bar3_value] 
    bg = [bar4_value,bar5_value,bar6_value]
    bw = [bar7_value,bar8_value,bar9_value] 
    
    #ここ変更し忘れない
    #tulca = TULCA(n_components=np.array([10, 2]), w_tg=tg, w_bg=bg, w_bw=bw, optimization_method="evd")
    #tulca = TULCA(n_components=np.array([10, 2]), optimization_method="evd")
    
    X_tda = tulca.fit_with_new_weights(w_tg=tg, w_bg=bg, w_bw=bw).transform(global_X, global_y)
    Us = tulca.get_projection_matrices()
    print(len(Us[0][:,1]))
    print(len(Us[0][0,:]))
    
    Z_heatmap =[]
    for i in range(10):
        heat=Us[0][:,i].reshape(36,24)
        Z_heatmap.append(heat)
    
    fig_heatmap = make_subplots(rows=10, cols=1, subplot_titles=[f'Heatmap {i+1}' for i in range(10)], shared_xaxes=True)

    for i in range(10):
        fig_heatmap.add_trace(go.Heatmap(
            z=Z_heatmap[i],
            x=[i for i in range(Z_heatmap[i].shape[1])],
            y=[i for i in range(Z_heatmap[i].shape[0])],
            colorscale='Viridis'
        ), row=i+1, col=1)

    fig_heatmap.update_layout(
        title='Heatmap Subplots',
        xaxis_title='X軸',
        yaxis_title='Y軸',
        height=3600,  # 適切な高さに調整
        width=360    # 適切な幅に調整
    )


    return fig_heatmap

@app.callback(
    Output('selected-data-time-output', 'figure'),  # 'figure'プロパティを更新する
    [Input('scatter-plot', 'selectedData')]
)
def display_selected_data_time_output(selectedData):
    if selectedData is None:
        return {
            'data': [],  # データなしでグラフを初期化
            'layout': {
                'title': "選択されたデータはありません。",
            }
        }
    
    # 選択されたデータの座標を取得
    points = selectedData['points']
    # pointIndexでインデックスを取得可能
    selected_indices = [point['pointIndex'] for point in points]

    # 平均データの計算
    average_data = np.mean(global_X[:, :, 0], axis=1)

    # ハイライトする点の設定
    highlighted_points = np.full_like(average_data, np.nan)
    highlighted_points[selected_indices] = average_data[selected_indices]

    # プロットの設定
    average_trace = go.Scatter(
        x=np.arange(average_data.shape[0]),
        y=average_data,
        mode='lines',
        name='Average Data'
    )
    highlighted_trace = go.Scatter(
        x=np.arange(average_data.shape[0]),
        y=highlighted_points,
        mode='markers',
        marker=dict(
            size=8,
            color='red',  # ハイライトの色を設定
        ),
        name='Selected Points'
    )

    # グラフの図形データを返す
    return {
        'data': [average_trace, highlighted_trace],
        'layout': {
            'title': "選択されたデータ",
            # 他のレイアウト設定を追加できます
        }
    }
    

# @app.callback(
#     Output('selected-data-output', 'children'),
#     [Input('scatter-plot', 'selectedData')]
# )
# def display_selected_data(selectedData):
#     if selectedData is None:
#         return "選択されたデータはありません。"
#     # 選択されたデータの座標を取得
#     points = selectedData['points']
#     # pointIndexでインデックスを取得可能
#     selected_indices = [point['pointIndex'] for point in points]

#     # 時系列に沿って864個のプロットを重ねて表示
#     fig1 = go.Figure()

#     # 以下が変更された部分です
#     average_data = np.mean(global_X[:, :, 0], axis=1)
#     fig1.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=average_data,
#         mode='lines',
#         name='Average Data'
#     ))
#     # selected_indices に基づいてハイライトする点を表示
#     highlighted_points = np.full_like(average_data, np.nan)
#     highlighted_points[selected_indices] = average_data[selected_indices]

#     fig1.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=highlighted_points,
#         mode='markers',
#         marker=dict(
#             size=8,
#             color='red',  # ハイライトの色を設定
#         ),
#         name='Selected Points'
#     ))

#     # 新しいプロットを表示
#         # 時系列に沿って864個のプロットを重ねて表示
#     fig2 = go.Figure()

#     # 以下が変更された部分です
#     average_data = np.mean(global_X[:, :, 1], axis=1)
#     fig2.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=average_data,
#         mode='lines',
#         name='Average Data'
#     ))
#     highlighted_points = np.full_like(average_data, np.nan)
#     highlighted_points[selected_indices] = average_data[selected_indices]

#     fig2.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=highlighted_points,
#         mode='markers',
#         marker=dict(
#             size=8,
#             color='red',  # ハイライトの色を設定
#         ),
#         name='Selected Points'
#     ))

#     # 新しいプロットを表示
#         # 時系列に沿って864個のプロットを重ねて表示
#     fig3 = go.Figure()

#     # 以下が変更された部分です
#     average_data = np.mean(global_X[:, :, 2], axis=1)
#     fig3.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=average_data,
#         mode='lines',
#         name='Average Data'
#     ))
#     highlighted_points = np.full_like(average_data, np.nan)
#     highlighted_points[selected_indices] = average_data[selected_indices]

#     fig3.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=highlighted_points,
#         mode='markers',
#         marker=dict(
#             size=8,
#             color='red',  # ハイライトの色を設定
#         ),
#         name='Selected Points'
#     ))

#     # 新しいプロットを表示
#         # 時系列に沿って864個のプロットを重ねて表示
#         # 時系列に沿って864個のプロットを重ねて表示
#     fig4 = go.Figure()

#     # 以下が変更された部分です
#     average_data = np.mean(global_X[:, :, 3], axis=1)
#     fig4.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=average_data,
#         mode='lines',
#         name='Average Data'
#     ))
#     highlighted_points = np.full_like(average_data, np.nan)
#     highlighted_points[selected_indices] = average_data[selected_indices]

#     fig4.add_trace(go.Scatter(
#         x=np.arange(average_data.shape[0]),
#         y=highlighted_points,
#         mode='markers',
#         marker=dict(
#             size=8,
#             color='red',  # ハイライトの色を設定
#         ),
#         name='Selected Points'
#     ))

        
#     Z_heatmap =[]
#     for i in selected_indices:
#         heat=global_X[i,:,0].reshape(36,24)
#         Z_heatmap.append(heat)
    
#     fig_heatmap1 = make_subplots(rows=len(selected_indices), cols=1, subplot_titles=[f'Heatmap {i+1}' for i in range(10)], shared_xaxes=True)

#     for i in range(len(selected_indices)):
#         fig_heatmap1.add_trace(go.Heatmap(
#             z=Z_heatmap[i],
#             x=[i for i in range(Z_heatmap[i].shape[1])],
#             y=[i for i in range(Z_heatmap[i].shape[0])],
#             colorscale='Viridis'
#         ), row=i+1, col=1)

#     fig_heatmap1.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360*len(selected_indices),  # 適切な高さに調整
#         width=360    # 適切な幅に調整
#     )
#     Z_heatmap =[]
#     for i in selected_indices:
#         heat=global_X[i,:,1].reshape(36,24)
#         Z_heatmap.append(heat)
    
#     fig_heatmap2 = make_subplots(rows=len(selected_indices), cols=1, subplot_titles=[f'Heatmap {i+1}' for i in range(10)], shared_xaxes=True)

#     for i in range(len(selected_indices)):
#         fig_heatmap2.add_trace(go.Heatmap(
#             z=Z_heatmap[i],
#             x=[i for i in range(Z_heatmap[i].shape[1])],
#             y=[i for i in range(Z_heatmap[i].shape[0])],
#             colorscale='Viridis'
#         ), row=i+1, col=1)

#     fig_heatmap2.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360*len(selected_indices),  # 適切な高さに調整
#         width=360    # 適切な幅に調整
#     )
#     Z_heatmap =[]
#     for i in selected_indices:
#         heat=global_X[i,:,2].reshape(36,24)
#         Z_heatmap.append(heat)
    
#     fig_heatmap3 = make_subplots(rows=len(selected_indices), cols=1, subplot_titles=[f'Heatmap {i+1}' for i in range(10)], shared_xaxes=True)

#     for i in range(len(selected_indices)):
#         fig_heatmap3.add_trace(go.Heatmap(
#             z=Z_heatmap[i],
#             x=[i for i in range(Z_heatmap[i].shape[1])],
#             y=[i for i in range(Z_heatmap[i].shape[0])],
#             colorscale='Viridis'
#         ), row=i+1, col=1)

#     fig_heatmap3.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360*len(selected_indices),  # 適切な高さに調整
#         width=360    # 適切な幅に調整
#     )
#     Z_heatmap =[]
#     for i in selected_indices:
#         heat=global_X[i,:,3].reshape(36,24)
#         Z_heatmap.append(heat)
    
#     fig_heatmap4 = make_subplots(rows=len(selected_indices), cols=1, subplot_titles=[f'Heatmap {i+1}' for i in range(10)], shared_xaxes=True)

#     for i in range(len(selected_indices)):
#         fig_heatmap4.add_trace(go.Heatmap(
#             z=Z_heatmap[i],
#             x=[i for i in range(Z_heatmap[i].shape[1])],
#             y=[i for i in range(Z_heatmap[i].shape[0])],
#             colorscale='Viridis',
#         ), row=i+1, col=1)

#     fig_heatmap4.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360*len(selected_indices),  # 適切な高さに調整
#         width=360    # 適切な幅に調整
#     )
    
    
#     #平均化した物
#     Z_heatmap=np.zeros((864), dtype=float)
#     Z_heatmap=Z_heatmap.reshape(36, 24)
#     for i in selected_indices:
#         heatmap_slice = global_X[i, :, 0].reshape(36, 24)
#         Z_heatmap += heatmap_slice

#     # 平均化
#     num_slices = len(selected_indices)
#     Z_heatmap /= num_slices    
    
#     fig_heatmap1_ave =go.Figure()

#     fig_heatmap1_ave.add_trace(go.Heatmap(
#         z=Z_heatmap,
#         x=[i for i in range(Z_heatmap.shape[1])],
#         y=[i for i in range(Z_heatmap.shape[0])],
#         coloraxis="coloraxis",

#     ))

#     fig_heatmap1_ave.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360,  # 適切な高さに調整
#         width=360,    # 適切な幅に調整
#         coloraxis=dict(colorscale="turbo", cmin=-2, cmax=2)

#     )
    
#     #平均化した物
#     Z_heatmap=np.zeros((864), dtype=float)
#     Z_heatmap=Z_heatmap.reshape(36, 24)
#     for i in selected_indices:
#         heatmap_slice = global_X[i, :, 1].reshape(36, 24)
#         Z_heatmap += heatmap_slice

#     # 平均化
#     num_slices = len(selected_indices)
#     Z_heatmap /= num_slices    
    
#     fig_heatmap2_ave =go.Figure()

#     fig_heatmap2_ave.add_trace(go.Heatmap(
#         z=Z_heatmap,
#         x=[i for i in range(Z_heatmap.shape[1])],
#         y=[i for i in range(Z_heatmap.shape[0])],
#         coloraxis="coloraxis",

#     ))

#     fig_heatmap2_ave.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360,  # 適切な高さに調整
#         width=360,    # 適切な幅に調整
#         coloraxis=dict(colorscale="turbo", cmin=-2, cmax=2)
#     )
    
#     #平均化した物
#     Z_heatmap=np.zeros((864), dtype=float)
#     Z_heatmap=Z_heatmap.reshape(36, 24)
#     for i in selected_indices:
#         heatmap_slice = global_X[i, :, 2].reshape(36, 24)
#         Z_heatmap += heatmap_slice

#     # 平均化
#     num_slices = len(selected_indices)
#     Z_heatmap /= num_slices    
    
#     fig_heatmap3_ave =go.Figure()

#     fig_heatmap3_ave.add_trace(go.Heatmap(
#         z=Z_heatmap,
#         x=[i for i in range(Z_heatmap.shape[1])],
#         y=[i for i in range(Z_heatmap.shape[0])],
#         coloraxis="coloraxis"
#     ))

#     fig_heatmap3_ave.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360,  # 適切な高さに調整
#         width=360,    # 適切な幅に調整
#         coloraxis=dict(colorscale="turbo", cmin=-2, cmax=2)
#     )
    
#     #平均化した物
#     Z_heatmap=np.zeros((864), dtype=float)
#     Z_heatmap=Z_heatmap.reshape(36, 24)
#     for i in selected_indices:
#         heatmap_slice = global_X[i, :, 3].reshape(36, 24)
#         Z_heatmap += heatmap_slice

#     # 平均化
#     num_slices = len(selected_indices)
#     Z_heatmap /= num_slices    
    
#     fig_heatmap4_ave =go.Figure()

#     fig_heatmap4_ave.add_trace(go.Heatmap(
#         z=Z_heatmap,
#         x=[i for i in range(Z_heatmap.shape[1])],
#         y=[i for i in range(Z_heatmap.shape[0])],
#         coloraxis="coloraxis",
#     ))

#     fig_heatmap4_ave.update_layout(
#         title='Heatmap Subplots',
#         xaxis_title='X軸',
#         yaxis_title='Y軸',
#         height=360,  # 適切な高さに調整
#         width=360,    # 適切な幅に調整
#         coloraxis=dict(colorscale="turbo", cmin=-2, cmax=2)
#     )
    
#     # 新しいプロットを表示
#     fig1.show()
#     fig2.show()
#     fig3.show()
#     fig4.show()
#     fig_heatmap1.show()
#     fig_heatmap2.show()
#     fig_heatmap3.show()
#     fig_heatmap4.show()
#     fig_heatmap1_ave.show()
#     fig_heatmap2_ave.show()
#     fig_heatmap3_ave.show()
#     fig_heatmap4_ave.show()
#     print(selected_indices)
#     return f"heat"

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('bar1-slider', 'value'),
     State('bar2-slider', 'value'),
     State('bar3-slider', 'value'),
     State('bar4-slider', 'value'),
     State('bar5-slider', 'value'),
     State('bar6-slider', 'value'),
     State('bar7-slider', 'value'),
     State('bar8-slider', 'value'),
     State('bar9-slider', 'value')
     ]
    
)
def display_heat_map_plot(n_clicks, bar1_value, bar2_value, bar3_value,bar4_value, bar5_value, bar6_value,bar7_value, bar8_value, bar9_value):
    tg = [bar1_value,bar2_value,bar3_value] 
    bg = [bar4_value,bar5_value,bar6_value]
    bw = [bar7_value,bar8_value,bar9_value] 

    #tulca = TULCA(n_components=np.array([10, 2]), w_tg=tg, w_bg=bg, w_bw=bw, optimization_method="evd")
    #tulca = TULCA(n_components=np.array([10, 2]), optimization_method="evd")
        
    X_tda = tulca.fit_with_new_weights(w_tg=tg, w_bg=bg, w_bw=bw).transform(global_X, global_y)
    rank = 3  # 分解のランク
    factors = tl.decomposition.parafac(X_tda, rank=rank)
    Us = tulca.get_projection_matrices()
    data1={
        'Column1':factors[1][1][:, 0],
        'Column2':factors[1][1][:, 1],
        'Column3':factors[1][1][:, 2],
    }
    data2={
        'Column4':factors[1][2][:, 0],
        'Column5':factors[1][2][:, 1],
        'Column6':factors[1][2][:, 2],
    }
    data3={

        'Column7':Us[1][:,0],
        'Column8':Us[1][:,1],
    }
    
    df = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)

    # 棒グラフの作成
    bar_fig = px.bar(
        df,
        x=np.arange(len(df['Column1'])),
        y=df['Column1'],
        title=f'Bar Chart',
    )
    # 別の Bar グラフを追加
    bar_trace2 = go.Bar(
        x=np.arange(len(df['Column2'])),
        y=df['Column2'],
        visible=False  # 初期表示を有効に設定
    )
    bar_fig.add_trace(bar_trace2)
    
    # 別の Bar グラフを追加
    bar_trace3 = go.Bar(
        x=np.arange(len(df['Column3'])),
        y=df['Column3'],
        visible=False  # 初期表示を有効に設定
    )
    bar_fig.add_trace(bar_trace3)
        # 別の Bar グラフを追加
    bar_trace4 = go.Bar(
        x=np.arange(len(df2['Column4'])),
        y=df2['Column4'],
        visible=False  # 初期表示を有効に設定
    )
    bar_fig.add_trace(bar_trace4)
        # 別の Bar グラフを追加
    bar_trace5 = go.Bar(
        x=np.arange(len(df2['Column5'])),
        y=df2['Column5'],
        visible=False  # 初期表示を有効に設定
    )
    bar_fig.add_trace(bar_trace5)
        # 別の Bar グラフを追加
    bar_trace6 = go.Bar(
        x=np.arange(len(df2['Column6'])),
        y=df2['Column6'],
        visible=False  # 初期表示を有効に設定
    )
    bar_fig.add_trace(bar_trace6)
        # 別の Bar グラフを追加
    bar_trace7 = go.Bar(
        x=np.arange(len(df3['Column7'])),
        y=df3['Column7'],
        visible=False  # 初期表示を有効に設定
    )
    bar_fig.add_trace(bar_trace7)
        # 別の Bar グラフを追加
    bar_trace8 = go.Bar(
        x=np.arange(len(df3['Column8'])),
        y=df3['Column8'],
        visible=False  # 初期表示を有効に設定
    )
    bar_fig.add_trace(bar_trace8)

     # レイアウトの設定
    bar_fig.update_layout(
        xaxis=dict(title='x'),
        yaxis=dict(title='feature'),
        updatemenus=[
            {
                'buttons': [
                    {'label': 'Column1',
                    'method': 'update',
                    'args': [{'visible': [True, False, False, False, False, False, False, False]}]},
                    {'label': 'Column2',
                    'method': 'update',
                    'args': [{'visible': [False, True, False, False, False, False, False, False]}]},
                    {'label': 'Column3',
                    'method': 'update',
                    'args': [{'visible': [False, False, True, False, False, False, False, False]}]},
                    {'label': 'Column4',
                    'method': 'update',
                    'args': [{'visible': [False, False, False, True, False, False, False, False]}]},
                    {'label': 'Column5',
                    'method': 'update',
                    'args': [{'visible': [False, False, False, False, True, False, False, False]}]},
                    {'label': 'Column6',
                    'method': 'update',
                    'args': [{'visible': [False, False, False, False, False, True, False, False]}]},
                    {'label': 'Column7',
                    'method': 'update',
                    'args': [{'visible': [False, False, False, False, False, False, True, False]}]},
                    {'label': 'Column8',
                    'method': 'update',
                    'args': [{'visible': [False, False, False, False, False, False, False, True]}]}
                ],
                'direction': 'down',
                'showactive': True,
                'x': 0.01,
                'xanchor': 'left',
                'y': 1.05,
                'yanchor': 'top'
            }
        ]
    )
    return bar_fig
    
    # x_range = np.arange(len(data[selected_column]))
    # return {
    #     'data': [
    #         {'x': x_range, 'y': data[selected_column], 'type': 'bar', 'name': selected_column},
    #     ],
    #     'layout': {
    #         'title': f'Bar Chart - {selected_column}',
    #         'xaxis': {'title': 'ColorIndex'},
    #         'yaxis': {'title': 'Values'}
    #     }
    # }

if __name__ == '__main__':
    global_X, global_y = preprocess_data()
    #global_y -= 1
    xtulca=tulca.fit_transform(global_X, global_y)
    app.run_server(debug=True)
