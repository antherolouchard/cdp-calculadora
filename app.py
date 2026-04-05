import streamlit as st

st.set_page_config(page_title="Simulador de Tarifas - CDP", layout="wide", page_icon="⚓")

st.title("⚓ Calculadora de Tarifas Portuárias (Avançada)")
st.markdown("Simulador operacional para Vila do Conde, Belém e Santarém (Baseado nas Deliberações DIREXE).")

# --- BASE DE DADOS COMPLETA (3 PORTOS) ---
# Substitua os valores abaixo pelos exatos dos PDFs das tabelas de 2026 da CDP.
tarifas = {
    "Vila do Conde": {
        "regras_gerais": {
            "t2_atracacao": 0.59, 
            "t4_patio_m2_dia": 2.10, "t4_armazem_m2_dia": 4.50, # Área descoberta vs coberta
            "t5_balanca": 55.00, "t5_guindaste_hora": 250.00,   # Equipamentos
            "t7_agua_m3": 22.00, 
            "t8_limpeza_fixa": 300.00, "t8_isps_ton": 0.35      # Segurança por Ton/Unidade
        },
        "Longo Curso": {
            "t1_fixa": 628.32, "t1_tpb": 0.80,
            "Granel Sólido": 6.02, "Granel Líquido": 8.11, "Carga Geral": 4.91, 
            "Contêiner Cheio": 73.50, "Contêiner Vazio": 15.00
        },
        "Cabotagem": {
            "t1_fixa": 300.00, "t1_tpb": 0.40,
            "Granel Sólido": 4.50, "Granel Líquido": 6.00, "Carga Geral": 3.00, 
            "Contêiner Cheio": 50.00, "Contêiner Vazio": 10.00
        }
    },
    "Belém": {
        "regras_gerais": {
            "t2_atracacao": 0.59, 
            "t4_patio_m2_dia": 1.50, "t4_armazem_m2_dia": 3.80,
            "t5_balanca": 55.00, "t5_guindaste_hora": 200.00,
            "t7_agua_m3": 18.50, 
            "t8_limpeza_fixa": 250.00, "t8_isps_ton": 0.35
        },
        "Longo Curso": {
            "t1_fixa": 628.32, "t1_tpb": 0.80,
            "Granel Sólido": 5.00, "Granel Líquido": 5.00, "Carga Geral": 4.88, 
            "Contêiner Cheio": 60.00, "Contêiner Vazio": 12.00
        },
        "Cabotagem": {
            "t1_fixa": 300.00, "t1_tpb": 0.40,
            "Granel Sólido": 3.00, "Granel Líquido": 3.00, "Carga Geral": 3.00, 
            "Contêiner Cheio": 40.00, "Contêiner Vazio": 8.00
        }
    },
    "Santarém": {
        "regras_gerais": {
            "t2_atracacao": 0.50, 
            "t4_patio_m2_dia": 1.20, "t4_armazem_m2_dia": 3.00,
            "t5_balanca": 45.00, "t5_guindaste_hora": 180.00,
            "t7_agua_m3": 15.00, 
            "t8_limpeza_fixa": 200.00, "t8_isps_ton": 0.25
        },
        "Longo Curso": {
            "t1_fixa": 359.04, "t1_tpb": 0.16,
            "Granel Sólido": 4.00, "Granel Líquido": 4.00, "Carga Geral": 4.91, 
            "Contêiner Cheio": 50.00, "Contêiner Vazio": 10.00
        },
        "Cabotagem": {
            "t1_fixa": 200.00, "t1_tpb": 0.08,
            "Granel Sólido": 2.50, "Granel Líquido": 2.50, "Carga Geral": 3.00, 
            "Contêiner Cheio": 35.00, "Contêiner Vazio": 5.00
        }
    }
}

# --- INTERFACE DE CONFIGURAÇÃO ---
st.subheader("1. Configuração da Operação")
col1, col2, col3 = st.columns(3)

with col1:
    porto = st.selectbox("Selecione o Porto", ["Vila do Conde", "Belém", "Santarém"])
with col2:
    navegacao = st.selectbox("Tipo de Navegação", ["Longo Curso", "Cabotagem"])
with col3:
    tipo_carga = st.selectbox("Tipo de Carga", ["Granel Sólido", "Granel Líquido", "Carga Geral", "Contêiner Cheio", "Contêiner Vazio"])

st.divider()

# Recuperando dados do porto selecionado
p_geral = tarifas[porto]["regras_gerais"]
p_nav = tarifas[porto][navegacao]
is_conteiner = "Contêiner" in tipo_carga

tab1, tab2 = st.tabs(["🚢 Navio e Movimentação (Tab I, II e III)", "🏗️ Infraestrutura e Serviços (Tab IV a VIII)"])

with tab1:
    st.markdown("**Dados de Atracação e Operação**")
    c1, c2, c3 = st.columns(3)
    with c1:
        tpb_navio = st.number_input("TPB do Navio (Ton)", min_value=0, value=30000, step=1000)
    with c2:
        comprimento = st.number_input("Comprimento (m)", min_value=0.0, value=190.0, step=10.0)
        horas_atracado = st.number_input("Horas no Berço", min_value=0, value=48, step=1)
    with c3:
        if is_conteiner:
            movimentacao = st.number_input("Quantidade (Unidades)", min_value=0, value=500, step=50)
            unidade_medida = "Unidades"
        else:
            movimentacao = st.number_input("Volume (Toneladas)", min_value=0, value=25000, step=500)
            unidade_medida = "Toneladas"

with tab2:
    st.markdown("**Uso de Instalações, Equipamentos e Facilidades**")
    c4, c5, c6 = st.columns(3)
    with c4:
        tipo_area = st.radio("Tipo de Armazenagem", ["Nenhuma", "Pátio Descoberto", "Armazém Coberto"])
        area_m2 = st.number_input("Área Utilizada (m²)", min_value=0, value=0, step=100, disabled=(tipo_area=="Nenhuma"))
        dias_armaz = st.number_input("Dias de Armazenagem", min_value=0, value=0, step=1, disabled=(tipo_area=="Nenhuma"))
    with c5:
        qtd_pesagens = st.number_input("Pesagens (Qtd Caminhões)", min_value=0, value=0, step=10)
        horas_guindaste = st.number_input("Uso de Guindaste (Horas)", min_value=0, value=0, step=1)
    with c6:
        volume_agua = st.number_input("Água Fornecida (m³)", min_value=0, value=0, step=10)
        usar_limpeza = st.checkbox("Incluir Taxa de Limpeza de Berço")
        usar_isps = st.checkbox("Incluir Taxa de Segurança (ISPS Code)", value=True, help="Calculado sobre o volume movimentado")

st.divider()

col_btn1, col_btn2 = st.columns([4, 1])
with col_btn1:
    btn_calcular = st.button("Gerar Orçamento Prévio", type="primary", use_container_width=True)
with col_btn2:
    if st.button("Zerar Campos", use_container_width=True):
        st.rerun()

# --- MOTOR DE CÁLCULO ---
if btn_calcular:
    # Tabelas I, II, III
    c_acesso = p_nav["t1_fixa"] + (tpb_navio * p_nav["t1_tpb"])
    c_atracacao = comprimento * horas_atracado * p_geral["t2_atracacao"]
    c_operacional = movimentacao * p_nav[tipo_carga]
    
    # Tabela IV (Armazenagem)
    c_armaz = 0.0
    if tipo_area == "Pátio Descoberto":
        c_armaz = area_m2 * dias_armaz * p_geral["t4_patio_m2_dia"]
    elif tipo_area == "Armazém Coberto":
        c_armaz = area_m2 * dias_armaz * p_geral["t4_armazem_m2_dia"]
        
    # Tabela V (Equipamentos)
    c_equip = (qtd_pesagens * p_geral["t5_balanca"]) + (horas_guindaste * p_geral["t5_guindaste_hora"])
    
    # Tabelas VII e VIII (Utilidades e Diversos)
    c_agua = volume_agua * p_geral["t7_agua_m3"]
    c_limpeza = p_geral["t8_limpeza_fixa"] if usar_limpeza else 0.0
    c_isps = (movimentacao * p_geral["t8_isps_ton"]) if usar_isps else 0.0
    c_diversos = c_limpeza + c_isps

    total = c_acesso + c_atracacao + c_operacional + c_armaz + c_equip + c_agua + c_diversos

    # Exibição do Dashboard
    st.success(f"## CUSTO TOTAL ESTIMADO: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Criando métricas visuais
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Acesso & Berço (I e II)", f"R$ {(c_acesso + c_atracacao):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    m2.metric("Operação (III)", f"R$ {c_operacional:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    m3.metric("Infra e Equip (IV e V)", f"R$ {(c_armaz + c_equip):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    m4.metric("Utilidades e Seg. (VII e VIII)", f"R$ {(c_agua + c_diversos):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.markdown("---")
    st.markdown("### Espelho de Faturamento Detalhado")
    st.markdown(f"""
    | Rubrica | Base de Cálculo | Valor Apurado (R$) |
    | :--- | :--- | :--- |
    | **Tab. I - Acesso Aquaviário** | {tpb_navio} TPB x R$ {p_nav['t1_tpb']:.2f} + Fixo | {c_acesso:,.2f} |
    | **Tab. II - Atracação** | {comprimento}m x {horas_atracado}h x R$ {p_geral['t2_atracacao']:.2f} | {c_atracacao:,.2f} |
    | **Tab. III - Operacional** | {movimentacao} {unidade_medida} x R$ {p_nav[tipo_carga]:.2f} | {c_operacional:,.2f} |
    | **Tab. IV - Armazenagem** | {area_m2}m² x {dias_armaz} dias ({tipo_area}) | {c_armaz:,.2f} |
    | **Tab. V - Equipamentos** | Balança + Guindaste | {c_equip:,.2f} |
    | **Tab. VII - Fornecimento** | {volume_agua}m³ de Água | {c_agua:,.2f} |
    | **Tab. VIII - Diversos** | Limpeza + Segurança (ISPS) | {c_diversos:,.2f} |
    """.replace(",", "X").replace(".", ",").replace("X", "."))