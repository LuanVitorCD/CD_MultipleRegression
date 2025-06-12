# 📊 Sensação Térmica: Modelo de Regressão Linear Múltipla

🔗 **Demo Online:** https://regressaolinearmultipla-modelo.onrender.com/

---

## 🎯 Sobre

Este projeto aplica **Regressão Linear Múltipla** para predizer a sensação térmica a partir de variáveis meteorológicas (temperatura do ar e umidade relativa). A interface interativa em **Dash** exibe em tempo real:
- 📈 Gráfico 3D com pontos reais e superfície de regressão  
- 🧮 Equação final, coeficientes, intercepto e R²  
- 📅 Tabela filtrável por mês  

---

## 🧩 Tecnologias

- 🐍 **Python 3.8+**  
- 📊 **Pandas**  
- 🔢 **NumPy**  
- 🤖 **Scikit-learn**  
- 🌐 **Dash** (com HTML/CSS dinamizado)  
- 📈 **Plotly** (gráficos 3D)  
- ☁️ **OnRender** (hospedagem gratuita e CI via GitHub)  

---

## 🛠️ Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/LuanVitorCD/CD_MultipleRegression.git
cd CD_MultipleRegression

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicie a aplicação
python MultipleRegression_Main.py

# 5. Acesse no navegador
http://localhost:8050
```

---

## 📂 Estrutura do Projeto
sensacao-termica/
  
  ├─ MultipleRegression_Main.py    # Script principal (Dash + Plotly + ML)
  
  ├─ requirements.txt              # Bibliotecas necessárias
  
  └─ README.md                     # Este arquivo

---

## 🚀 Deploy
O app está configurado para deploy automático no OnRender via GitHub:

    1- Push no branch principal

    2- OnRender detecta mudanças e rebuilda

    3- URL sempre atualizada e disponível

