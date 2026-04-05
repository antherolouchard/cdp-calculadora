import streamlit as st

# Configuração da página
st.set_page_config(page_title="Simulador de Tarifas - CDP", layout="centered")

st.title("⚓ Calculadora de Tarifas Portuárias (CDP)")
st.markdown("Simulador rápido para os portos de Belém, Vila do Conde e Santarém.")

# Dicionário de tarifas (simplificado com base nas deliberações)
tarifas = {
    "Belém": {"fixa_acesso": 628.32, "tpb": 0.80, "atracacao": 0.59, "operacional": 4.88},
    "Vila do Conde": {"fixa_acesso": 628.32, "tpb": 0.80, "atracacao": 0.59, "operacional": 6.02},
    "Santarém": {"fixa_acesso": 359.04, "tpb": 0.16, "atracacao": 0.50, "operacional": 4.91}
}

# Criando as colunas de formulário na interface
col1, col2 = st.columns(2)

with col1:
    porto = st.selectbox("Selecione o Porto", ["Belém", "Vila do Conde", "Santarém"])
    tpb_navio = st.number_input("TPB do Navio (Toneladas)", min_value=0, value=30000, step=1000)
    comprimento = st.number_input("Comprimento do Navio (Metros)", min_value=0.0, value=190.0, step=10.0)

with col2:
    horas_atracado = st.number_input("Horas de Atracação", min_value=0, value=48, step=1)
    movimentacao = st.number_input("Volume Movimentado (Ton)", min_value=0, value=25000, step=500)

st.divider()

# Botão de cálculo
if st.button("Calcular Estimativa", type="primary"):
    p = tarifas[porto]
    
    custo_acesso = p["fixa_acesso"] + (tpb_navio * p["tpb"])
    custo_atracacao = comprimento * horas_atracado * p["atracacao"]
    custo_operacional = movimentacao * p["operacional"]
    total = custo_acesso + custo_atracacao + custo_operacional

    # Exibindo os resultados de forma visual
    st.subheader("Resumo dos Custos Estimados")
    st.write(f"**Acesso Aquaviário (Tabela I):** R$ {custo_acesso:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.write(f"**Uso do Berço (Tabela II):** R$ {custo_atracacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.write(f"**Infraestrutura Operacional (Tabela III):** R$ {custo_operacional:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.success(f"**CUSTO TOTAL ESTIMADO: R$ {total:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
    st.caption("Nota: Estes valores são estimativas baseadas nas Deliberações DIREXE vigentes e não substituem o faturamento oficial da Companhia Docas do Pará.")