import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

data = {
    'temperatura': [25.8, 25.5, 21.8, 22.2, 20.7, 20.9, 22.3, 23.3, 22.7, 22.1, 21.4, 22.6, 22.1, 22.5, 22.7, 
                    25.4, 26.8, 25.9, 24.0, 24.3, 26.6, 26.8, 22.4, 23.7, 23.7, 23.3, 24.6, 24.3, 22.6, 22.5, 
                    23.4, 25.4, 27.2, 27.9, 28.4, 25.5, 24.3, 25.3, 27.3, 28.0, 28.4, 25.5, 23.1, 24.7, 24.3,
                    26.7, 20.9, 20.5, 21.7, 23.4, 25.2, 25.4, 25.3, 26.6, 27.8, 24.6, 23.8, 25.0, 26.5, 26.9, 
                    29.1, 28.2, 27.2, 27.1, 27.2, 27.3, 20.8, 18.7, 20.1, 20.5, 20.2, 17.4, 18.3, 19.5, 21.0, 
                    21.2, 20.7, 21.7, 22.7, 22.9, 24.0, 25.5, 22.3, 24.2, 21.5, 22.5, 23.5, 24.4, 23.7, 19.9],
    'umidade': [0.74, 0.58, 0.54, 0.57, 0.68, 0.68, 0.74, 0.73, 0.82, 0.83, 0.76, 0.71, 0.78, 0.83, 0.82, 
                0.76, 0.70, 0.72, 0.77, 0.67, 0.63, 0.64, 0.89, 0.85, 0.80, 0.84, 0.83, 0.80, 0.87, 0.83, 
                0.79, 0.72, 0.69, 0.70, 0.67, 0.78, 0.78, 0.75, 0.73, 0.68, 0.67, 0.77, 0.91, 0.81, 0.89, 
                0.82, 0.97, 0.88, 0.77, 0.73, 0.76, 0.73, 0.77, 0.73, 0.68, 0.83, 0.89, 0.85, 0.76, 0.81, 
                0.73, 0.72, 0.65, 0.67, 0.63, 0.62, 0.92, 0.86, 0.82, 0.85, 0.83, 0.73, 0.70, 0.72, 0.79, 
                0.81, 0.71, 0.61, 0.58, 0.64, 0.65, 0.68, 0.81, 0.74, 0.89, 0.83, 0.84, 0.76, 0.82, 0.92],
    'umidade_porcento': [74, 58, 54, 57, 68, 68, 74, 73, 82, 83, 76, 71, 78, 83, 82, 76, 70, 72, 
    77, 67, 63, 64, 89, 85, 80, 84, 83, 80, 87, 83, 79, 72, 69, 70, 67, 78, 
    78, 75, 73, 68, 67, 77, 91, 81, 89, 82, 97, 88, 77, 73, 76, 73, 77, 73, 
    68, 83, 89, 85, 76, 81, 73, 72, 65, 67, 63, 62, 92, 86, 82, 85, 83, 73, 
    70, 72, 79, 81, 71, 61, 58, 64, 65, 68, 81, 74, 89, 83, 84, 76, 82, 92],
    'sensacao_termica': [26.8, 25.4, 21.8, 22.1, 20.7, 20.8, 22.6, 23.6, 23.2, 22.4, 21.6, 22.7, 22.4, 22.7, 22.9, 
                         26.7, 27.6, 26.9, 24.2, 24.6, 26.8, 27.6, 22.4, 24.4, 24.0, 24.1, 25.7, 24.9, 23.0, 22.9, 
                         24.0, 26.0, 28.3, 29.6, 29.8, 26.9, 25.0, 26.6, 28.8, 30.1, 30.0, 26.4, 23.4, 25.8, 25.1, 
                         28.9, 20.9, 20.5, 21.7, 23.7, 26.6, 26.4, 26.7, 28.0, 29.4, 25.5, 24.6, 26.4, 28.6, 29.8, 
                         31.1, 29.9, 28.4, 28.2, 27.7, 28.2, 20.8, 18.7, 20.2, 20.6, 20.2, 17.4, 18.3, 19.4, 21.1, 
                         21.3, 20.6, 21.7, 22.7, 22.9, 24.0, 26.0, 22.5, 24.6, 21.5, 22.9, 24.2, 25.0, 24.4, 19.9]
}

df = pd.DataFrame(data)

umidadeEscolha = input("Qual tipo de umidade vai querer usar? (escolhas: 'umidade' e 'umidade_porcento')\nR: ").strip().lower()

if umidadeEscolha not in ['umidade', 'umidade_porcento']:
    print("Escolha inválida. Use 'umidade' ou 'umidade_porcento'.")
else:
    #Regressão Linear Múltipla
    X = df[['temperatura', umidadeEscolha]].values
    y = df['sensacao_termica'].values

    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    a0 = model.intercept_
    a1, a2 = model.coef_

    print(f"\nEquação encontrada:")
    print(f"sensacao_termica = {a0:.4f} + {a1:.4f} * temperatura + {a2:.4f} * {umidadeEscolha}")
    print(f"Coeficiente de determinação R²: {r2:.4f}")

    #Gerando o grid para superfície de regressão
    temp_range = np.linspace(df['temperatura'].min(), df['temperatura'].max(), 20)
    umid_range = np.linspace(df[umidadeEscolha].min(), df[umidadeEscolha].max(), 20)
    temp_grid, umid_grid = np.meshgrid(temp_range, umid_range)

    X_grid = np.column_stack((temp_grid.ravel(), umid_grid.ravel()))
    y_grid = model.predict(X_grid).reshape(temp_grid.shape)


    #Gráfico 3D com pontos e plano de regressão
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=df['temperatura'], 
        y=df[umidadeEscolha], 
        z=df['sensacao_termica'],
        mode='markers',
        marker=dict(size=5, color='black', opacity=0.8),
        name='Dados reais'
    ))

    fig.add_trace(go.Surface(
        x=temp_grid, 
        y=umid_grid, 
        z=y_grid,
        colorscale='Viridis',
        opacity=0.7,
        showscale=False,
        name='Plano de regressão'
    ))

    fig.update_layout(
        title=f'Relação entre Temperatura, Umidade e Sensação Térmica<br>R² = {r2:.3f}',
        scene=dict(
            xaxis_title='Temperatura (°C)',
            yaxis_title='Umidade (%)' if umidadeEscolha == 'umidade_porcento' else 'Umidade (0-1)',
            zaxis_title='Sensação Térmica (°C)',
            aspectratio=dict(x=1, y=1, z=0.7),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
    ))

    fig.show()