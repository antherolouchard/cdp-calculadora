import streamlit as st

# Configuração da página
st.set_page_config(page_title="Simulador de Tarifas - CDP", layout="centered", page_icon="⚓")

st.title("⚓ Calculadora Completa de Tarifas Portuárias")
st.markdown("Simulador operacional para os portos da Companhia Docas do Pará (CDP).")

# Dicionário de tarifas (Valores das Tabelas IV, V, VII e VIII são referenciais para o MVP)
tarifas = {
    "Belém": {
        "t1_fixa": 628.32, "t1_tpb": 0.80, 
        "t2_atracacao": 0.59, 
        "t3_operacional": 4.88,
        "t4_armaz_m2_dia": 1.50,   # Tabela IV: R$ por m² ao dia
        "t5_balanca": 55.00,       # Tabela V: R$ por pesagem/veículo
        "t7_agua_m3": 18.50,       # Tabela VII: R$ por m³ de água fornecida
        "t8_taxa_limpeza": 250.00  # Tabela VIII: Taxa fixa de limpeza/serviços diversos
    },
    "Vila do Conde": {
        "t1_fixa": 628.32, "t1_tpb": 0.80, 
        "t2_atracacao": 0.59, 
        "t3_operacional": 6.02,
        "t4_armaz_m2_dia": 2.10,
        "t5_balanca": 55.00,
        "t7_agua_m3": 22.00,
        "t8_taxa_limpeza": 300.00
    },
    "Santarém": {
        "t1_fixa": 359.04, "t1_tpb": 0.16, 
        "t2_atracacao": 0.50, 
        "t3_operacional": 4.91,
        "t4_armaz_m2_dia": 1.20,
        "t5_balanca": 45.00,
        "t7_agua_m3": 15.00,
        "t8_taxa_limpeza": 200.00
    }
}

porto = st.selectbox("Selecione o Porto da Simulação", ["Belém", "Vila do Conde", "Santarém"])
p = tarifas[porto]

# Organizando a interface em Abas para melhor usabilidade
tab1, tab2 = st.tabs(["🚢 Tabela I, II e III (Navio e Operação)", "🏗️ Tabela IV, V, VII e VIII (Serviços e Infra)"])

with tab1:
    st.subheader("Dados da Embarcação e Carga")
    col1, col2 = st.columns(2)
    with col1:
        tpb_navio = st.number_input("TPB do Navio (Ton)", min_value=0, value=30000, step=1000)
        comprimento = st.number_input("Comprimento (Metros)", min_value=0.0, value=190.0, step=10.0)
    with col2:
        horas_atracado = st.number_input("Tempo de Atracação (Horas)", min_value=0, value=48, step=1)
        movimentacao = st.number_input("Volume Movimentado (Ton)", min_value=0, value=25000, step=500)

with tab2:
    st.subheader("Armazenagem, Equipamentos e Utilidades")
    col3, col4 = st.columns(2)
    with col3:
        area_armazenagem = st.number_input("Área de Armazenagem (m²)", min_value=0, value=0, step=100)
        dias_armazenagem = st.number_input("Dias no Pátio/Armazém", min_value=0, value=0, step=1)
        qtd_pesagens = st.number_input("Qtd. de Pesagens (Balança)", min_value=0, value=0, step=10)
    with col4:
        volume_agua = st.number_input("Fornecimento de Água (m³)", min_value=0, value=0, step=10)
        usar_servicos_div = st.checkbox("Incluir Taxa de Serviços Diversos/Limpeza (Tab. VIII)")

st.divider()

# Botão de cálculo em destaque
if st.button("Gerar Extrato de Estimativa", type="primary", use_container_width=True):
    
    # Cálculos Tabela I, II e III
    custo_acesso = p["t1_fixa"] + (tpb_navio * p["t1_tpb"])
    custo_atracacao = comprimento * horas_atracado * p["t2_atracacao"]
    custo_operacional = movimentacao * p["t3_operacional"]
    
    # Cálculos Tabela IV, V, VII e VIII
    custo_armazenagem = area_armazenagem * dias_armazenagem * p["t4_armaz_m2_dia"]
    custo_equipamentos = qtd_pesagens * p["t5_balanca"]
    custo_fornecimento = volume_agua * p["t7_agua_m3"]
    custo_diversos = p["t8_taxa_limpeza"] if usar_servicos_div else 0.0

    total_navio_carga = custo_acesso + custo_atracacao + custo_operacional
    total_servicos = custo_armazenagem + custo_equipamentos + custo_fornecimento + custo_diversos
    total_geral = total_navio_carga + total_servicos

    # Exibição Profissional dos Resultados
    st.subheader("Extrato de Custos Estimados")
    
    # Usando colunas para mostrar um resumo executivo
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric(label="Subtotal Operação", value=f"R$ {total_navio_carga:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    res_col2.metric(label="Subtotal Serviços", value=f"R$ {total_servicos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    res_col3.metric(label="TOTAL PREVISTO", value=f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.markdown("### Detalhamento por Tabela Tarifária")
    
    # Tabela detalhada
    detalhamento = f"""
    | Tabela | Descrição | Valor Estimado (R$) |
    | :--- | :--- | :--- |
    | **Tab I** | Acesso Aquaviário | {custo_acesso:,.2f} |
    | **Tab II** | Atracação e Uso de Berço | {custo_atracacao:,.2f} |
    | **Tab III** | Infraestrutura Operacional | {custo_operacional:,.2f} |
    | **Tab IV** | Armazenagem (Pátios/Armazéns) | {custo_armazenagem:,.2f} |
    | **Tab V** | Uso de Equipamentos (Balança) | {custo_equipamentos:,.2f} |
    | **Tab VII** | Fornecimento de Utilidades (Água) | {custo_fornecimento:,.2f} |
    | **Tab VIII**| Serviços Diversos | {custo_diversos:,.2f} |
    """
    # Ajustando o formato numérico brasileiro na string markdown
    detalhamento_br = detalhamento.replace(",", "X").replace(".", ",").replace("X", ".")
    st.markdown(detalhamento_br)
    
    st.info("💡 Dica de TI: Este extrato pode ser exportado para PDF em futuras atualizações para envio direto ao cliente ou agência marítima.")