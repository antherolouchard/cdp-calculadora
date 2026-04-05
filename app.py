import streamlit as st

# Configuração da página
st.set_page_config(page_title="Simulador de Tarifas - CDP", layout="centered", page_icon="⚓")

st.title("⚓ Calculadora Completa de Tarifas Portuárias")
st.markdown("Simulador operacional para os portos da Companhia Docas do Pará (CDP).")

# Dicionário de tarifas (Valores referenciais)
tarifas = {
    "Belém": {
        "t1_fixa": 628.32, "t1_tpb": 0.80, "t2_atracacao": 0.59, "t3_operacional": 4.88,
        "t4_armaz_m2_dia": 1.50, "t5_balanca": 55.00, "t7_agua_m3": 18.50, "t8_taxa_limpeza": 250.00
    },
    "Vila do Conde": {
        "t1_fixa": 628.32, "t1_tpb": 0.80, "t2_atracacao": 0.59, "t3_operacional": 6.02,
        "t4_armaz_m2_dia": 2.10, "t5_balanca": 55.00, "t7_agua_m3": 22.00, "t8_taxa_limpeza": 300.00
    },
    "Santarém": {
        "t1_fixa": 359.04, "t1_tpb": 0.16, "t2_atracacao": 0.50, "t3_operacional": 4.91,
        "t4_armaz_m2_dia": 1.20, "t5_balanca": 45.00, "t7_agua_m3": 15.00, "t8_taxa_limpeza": 200.00
    }
}

porto = st.selectbox("Selecione o Porto da Simulação", ["Belém", "Vila do Conde", "Santarém"])
p = tarifas[porto]

tab1, tab2 = st.tabs(["🚢 Navio e Operação", "🏗️ Serviços e Infra"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        tpb_navio = st.number_input("TPB do Navio (Ton)", min_value=0, value=30000, step=1000)
        comprimento = st.number_input("Comprimento (Metros)", min_value=0.0, value=190.0, step=10.0)
    with col2:
        horas_atracado = st.number_input("Tempo de Atracação (Horas)", min_value=0, value=48, step=1)
        movimentacao = st.number_input("Volume Movimentado (Ton)", min_value=0, value=25000, step=500)

with tab2:
    col3, col4 = st.columns(2)
    with col3:
        area_armazenagem = st.number_input("Área de Armazenagem (m²)", min_value=0, value=0, step=100)
        dias_armazenagem = st.number_input("Dias no Pátio/Armazém", min_value=0, value=0, step=1)
        qtd_pesagens = st.number_input("Qtd. de Pesagens (Balança)", min_value=0, value=0, step=10)
    with col4:
        volume_agua = st.number_input("Fornecimento de Água (m³)", min_value=0, value=0, step=10)
        usar_servicos_div = st.checkbox("Incluir Taxa de Serviços Diversos (Tab. VIII)")

st.divider()

# --- ÁREA DOS BOTÕES ---
col_btn1, col_btn2 = st.columns([3, 1]) # Coluna do calcular é maior que a do limpar

with col_btn1:
    btn_calcular = st.button("Gerar Extrato de Estimativa", type="primary", use_container_width=True)

with col_btn2:
    if st.button("Limpar Dados", use_container_width=True):
        st.rerun() # Reinicia o app e zera os campos

# --- LÓGICA DE CÁLCULO ---
if btn_calcular:
    custo_acesso = p["t1_fixa"] + (tpb_navio * p["t1_tpb"])
    custo_atracacao = comprimento * horas_atracado * p["t2_atracacao"]
    custo_operacional = movimentacao * p["t3_operacional"]
    custo_armazenagem = area_armazenagem * dias_armazenagem * p["t4_armaz_m2_dia"]
    custo_equipamentos = qtd_pesagens * p["t5_balanca"]
    custo_fornecimento = volume_agua * p["t7_agua_m3"]
    custo_diversos = p["t8_taxa_limpeza"] if usar_servicos_div else 0.0

    total_geral = custo_acesso + custo_atracacao + custo_operacional + custo_armazenagem + custo_equipamentos + custo_fornecimento + custo_diversos

    st.subheader("Extrato de Custos Estimados")
    st.metric(label="TOTAL PREVISTO", value=f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Tabela simplificada para o extrato
    st.markdown(f"""
    | Tabela | Detalhamento | Valor (R$) |
    | :--- | :--- | :--- |
    | I, II, III | Operação Portuária | {(custo_acesso+custo_atracacao+custo_operacional):,.2f} |
    | IV, V, VII, VIII | Serviços e Utilidades | {(custo_armazenagem+custo_equipamentos+custo_fornecimento+custo_diversos):,.2f} |
    """.replace(",", "X").replace(".", ",").replace("X", "."))