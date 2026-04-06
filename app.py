import streamlit as st
from typing import Dict, Any

# ==========================================
# UTILITÁRIOS E FORMATAÇÃO
# ==========================================
def format_br(valor: float) -> str:
    """Formata para o padrão monetário brasileiro (R$ 1.234,56)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================
# BASE DE DADOS TARIFÁRIA INTEGRAL (DIREXE 2025)
# DADOS EXTRAÍDOS DIRETAMENTE DOS ANEXOS
# ==========================================
TARIFAS_CDP = {
    "Vila do Conde": {
        "Tabela_I_Fixo": 2261.95,
        "Tabela_I_Var": {"Granel Sólido": 2.56, "Granel Líquido": 2.30, "Carga Geral": 1.15, "Contêineres": 0.48, "Veículos/Carga Viva": 1.15},
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Apoio": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": 6.02, "Granel Líquido": 8.11, "Carga Geral": 4.91,
            "Contêiner Cheio": 73.50, "Contêiner Vazio": 36.74,
            "Ro-Ro: Caminhão": 38.27, "Ro-Ro: Cavalo": 9.57, "Ro-Ro: Leve": 3.82,
            "Animais: Até 1t": 6.34, "Animais: Acima 1t": 12.61
        },
        "Tabela_V_Armazenagem": {"Pátio": 2.10, "Armazém": 4.50, "AdValorem": 0.005},
        "Tabela_VII_Diversos": {
            "Agua": 15.49, "Energia_kWh": 1.62, "Energia_Reefer_Dia": 120.50, "Pesagem": 1.15,
            "Certidao": 1850.00, "Armazem_Diversos": 2.10, "Patio_Diversos": 1.10,
            "Apoio_Coberta": 2.10, "Apoio_Descoberta_Terra": 1.10, "Apoio_Descoberta_Agua": 0.55
        },
        "Tabela_VIII": {
            "Regime": "Arrendamento_Mes",
            "NC_Primaria": 12.50, "NC_Remota": 7.50, "NC_Agua": 3.75,
            "C_Primaria": 10.00, "C_Sitio": 5.00, "C_Granel": 8.00, "Giro12": 2.50
        }
    },
    "Santarém": {
        "Tabela_I_Fixo": 359.04,
        "Tabela_I_Var": {"Granel Sólido": 3.41, "Granel Líquido": 2.19, "Carga Geral": 0.17, "Contêineres": 0.16, "Veículos/Carga Viva": 0.17},
        "Tabela_I_Fundeio": {"Operando": 3690.75, "Parado": 2636.55},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Apoio": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": 4.91, "Granel Líquido": 4.91, "Carga Geral": 4.91,
            "Contêiner Cheio": 50.00, "Contêiner Vazio": 25.00,
            "Ro-Ro: Caminhão": 38.30, "Ro-Ro: Cavalo": 9.59, "Ro-Ro: Leve": 3.82,
            "Animais: Até 1t": 0.00, "Animais: Acima 1t": 0.00 # Isento na imagem
        },
        "Tabela_V_Armazenagem": {"Pátio": 1.20, "Armazém": 3.00, "AdValorem": 0.005},
        "Tabela_VII_Diversos": {
            "Agua": 15.49, "Energia_kWh": 1.62, "Energia_Reefer_Dia": 120.50, "Pesagem": 1.15,
            "Certidao": 1850.00, "Armazem_Diversos": 1.50, "Patio_Diversos": 0.80,
            "Apoio_Coberta": 1.50, "Apoio_Descoberta_Terra": 0.80, "Apoio_Descoberta_Agua": 0.40
        },
        "Tabela_VIII": {
            "Regime": "Arrendamento_Mes",
            "NC_Primaria": 6.25, "NC_Remota": 3.75, "NC_Agua": 1.88,
            "C_Primaria": 5.00, "C_Sitio": 2.50, "C_Granel": 4.00, "Giro12": 1.25
        }
    },
    "Belém": {
        "Tabela_I_Fixo": 628.32,
        "Tabela_I_Var": {"Granel Sólido": 1.14, "Granel Líquido": 0.60, "Carga Geral": 0.23, "Contêineres": 0.80, "Veículos/Carga Viva": 0.23},
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Apoio": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": 4.88, "Granel Líquido": 5.10, "Carga Geral": 4.60,
            "Contêiner Cheio": 60.00, "Contêiner Vazio": 30.00,
            "Ro-Ro: Caminhão": 38.14, "Ro-Ro: Cavalo": 9.55, "Ro-Ro: Leve": 3.81,
            "Animais: Até 1t": 6.34, "Animais: Acima 1t": 12.61
        },
        "Tabela_V_Armazenagem": {"Pátio": 1.50, "Armazém": 3.80, "AdValorem": 0.005},
        "Tabela_VII_Diversos": {
            "Agua": 15.49, "Energia_kWh": 1.62, "Energia_Reefer_Dia": 120.50, "Pesagem": 1.15,
            "Certidao": 1850.00, "Armazem_Diversos": 1.80, "Patio_Diversos": 0.90,
            "Apoio_Coberta": 1.80, "Apoio_Descoberta_Terra": 0.90, "Apoio_Descoberta_Agua": 0.45
        },
        "Tabela_VIII": {
            "Regime": "Uso_Temporario_Dia",
            "Pavimentada": 0.48, "NaoPavimentada": 0.38, "Agua": 0.18
        }
    }
}

# ==========================================
# MOTOR DE CÁLCULO
# ==========================================
class EngineFaturamentoCDP:
    def calcular(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        porto = dados["porto"]
        t = TARIFAS_CDP[porto]
        extrato = {}

        # Tabela I - Acesso
        taxa_var = t["Tabela_I_Var"].get(dados["carga"], 0.0)
        extrato["Tabela I - Acesso"] = {"v": t["Tabela_I_Fixo"] + (dados["tpb"] * taxa_var), "m": f"Fixo R$ {format_br(t['Tabela_I_Fixo'])} + ({dados['tpb']} TPB x R$ {format_br(taxa_var)})"}

        # Tabela II - Acostagem
        taxa_t2 = t["Tabela_II_Acostagem"]["Apoio"] if "Apoio" in dados["nav"] else t["Tabela_II_Acostagem"]["Longo Curso"]
        extrato["Tabela II - Acostagem"] = {"v": dados["comp"] * dados["horas"] * taxa_t2, "m": f"{dados['comp']}m x {dados['horas']}h x R$ {format_br(taxa_t2)}"}

        # Tabela III e IV
        chave_op = dados["carga_detalhe"] if dados["carga_detalhe"] else dados["carga"]
        taxa_op = t["Tabela_III_IV"].get(chave_op, 0.0)
        extrato["Tabela III - Infra Operacional"] = {"v": dados["mov"] * taxa_op, "m": f"{dados['mov']} x R$ {format_br(taxa_op)}"}

        # Tabela V - Armazenagem
        if dados["t5_mod"] == "Ad Valorem":
            extrato["Tabela V - Armazenagem"] = {"v": dados["t5_valor"] * t["Tabela_V_Armazenagem"]["AdValorem"], "m": f"R$ {format_br(dados['t5_valor'])} x 0,50%"}
        elif dados["t5_area"] > 0:
            taxa_t5 = t["Tabela_V_Armazenagem"].get(dados["t5_tipo"], 0.0)
            extrato["Tabela V - Armazenagem"] = {"v": dados["t5_area"] * dados["t5_dias"] * taxa_t5, "m": f"{dados['t5_area']}m² x {dados['t5_dias']}d x R$ {format_br(taxa_t5)}"}

        # Tabela VII - Diversos
        s7 = t["Tabela_VII_Diversos"]
        if dados["t7_agua"] > 0: extrato["Tabela VII - Água"] = {"v": dados["t7_agua"] * s7["Agua"], "m": f"{dados['t7_agua']}m³ x R$ {format_br(s7['Agua'])}"}
        if dados["t7_kwh"] > 0: extrato["Tabela VII - Energia"] = {"v": dados["t7_kwh"] * s7["Energia_kWh"], "m": f"{dados['t7_kwh']}kWh x R$ {format_br(s7['Energia_kWh'])}"}
        if dados["t7_reefer"] > 0: extrato["Tabela VII - Reefer"] = {"v": dados["t7_reefer"] * s7["Energia_Reefer_Dia"], "m": f"{dados['t7_reefer']} container/dia x R$ {format_br(s7['Energia_Reefer_Dia'])}"}
        if dados["t7_pesagem"] > 0: extrato["Tabela VII - Pesagem"] = {"v": dados["t7_pesagem"] * s7["Pesagem"], "m": f"{dados['t7_pesagem']} ton x R$ {format_br(s7['Pesagem'])}"}
        if dados["t7_cert"] > 0: extrato["Tabela VII - Certidões"] = {"v": dados["t7_cert"] * s7["Certidao"], "m": f"{dados['t7_cert']} unid x R$ {format_br(s7['Certidao'])}"}
        if dados["t7_apoio_m2"] > 0:
            taxa_apoio = s7.get(dados["t7_apoio_tipo"], 0.0)
            extrato["Tabela VII - Áreas de Apoio"] = {"v": dados["t7_apoio_m2"] * dados["t7_apoio_dias"] * taxa_apoio, "m": f"{dados['t7_apoio_m2']}m² x {dados['t7_apoio_dias']}d x R$ {format_br(taxa_apoio)}"}

        # Tabela VIII - A REVISADA
        s8 = t["Tabela_VIII"]
        if s8["Regime"] == "Uso_Temporario_Dia":
            area_t8 = dados["t8_m2_belem"]
            taxa_t8 = s8.get(dados["t8_tipo_belem"], 0.0)
            if area_t8 > 0:
                extrato["Tabela VIII - Uso Temporário"] = {"v": area_t8 * dados["t8_dias_belem"] * taxa_t8, "m": f"{area_t8}m² x {dados['t8_dias_belem']}d x R$ {format_br(taxa_t8)} (Belém)"}
        else:
            # VDC ou STM (Arrendamento Simplificado)
            v8 = 0.0
            memo8 = []
            if dados["t8_nc_m2"] > 0:
                tx = s8.get(dados["t8_nc_local"], 0.0)
                v8 += dados["t8_nc_m2"] * dados["t8_meses"] * tx
                memo8.append(f"NC: {dados['t8_nc_m2']}m² x {dados['t8_meses']}mês x R$ {format_br(tx)}")
            if dados["t8_c_m2"] > 0:
                tx = s8.get(dados["t8_c_local"], 0.0)
                v8 += dados["t8_c_m2"] * dados["t8_meses"] * tx
                memo8.append(f"C: {dados['t8_c_m2']}m² x {dados['t8_meses']}mês x R$ {format_br(tx)}")
            if dados["t8_giro"] > 0:
                v8 += dados["t8_giro"] * s8["Giro12"]
                memo8.append(f"Giro12: {dados['t8_giro']} x R$ {format_br(s8['Giro12'])}")
            if v8 > 0:
                extrato["Tabela VIII - Arrendamento Simplificado"] = {"v": v8, "m": " | ".join(memo8)}

        extrato["TOTAL"] = sum(item["v"] for item in extrato.values())
        return extrato

# ==========================================
# INTERFACE
# ==========================================
st.set_page_config(page_title="Simulador CDP Sênior", layout="wide")
st.title("⚓ Sistema Tarifário Oficial CDP - DIREXE 2025")

with st.sidebar:
    st.header("Parâmetros Base")
    porto = st.selectbox("Porto Organizado", ["Vila do Conde", "Belém", "Santarém"])
    nav = st.selectbox("Navegação", ["Longo Curso", "Cabotagem", "Apoio Portuário", "Interior"])
    carga = st.selectbox("Grupo de Carga", ["Granel Sólido", "Granel Líquido", "Carga Geral", "Contêineres", "Veículos/Carga Viva"])
    
    carga_detalhe = None
    if carga == "Contêineres": carga_detalhe = st.radio("Tipo:", ["Contêiner Cheio", "Contêiner Vazio"])
    elif carga == "Veículos/Carga Viva":
        carga_detalhe = st.radio("Detalhe:", ["Ro-Ro: Caminhão", "Ro-Ro: Cavalo", "Ro-Ro: Leve", "Animais: Até 1t", "Animais: Acima 1t"])

tab1, tab2, tab3, tab4 = st.tabs(["🚢 Embarcação", "📦 Operação e Armazenagem", "🛠️ Serviços Diversos (VII)", "🏗️ Tabela VIII"])

with tab1:
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("Porte Bruto (TPB)", value=15000)
    comp = c2.number_input("Comprimento (m)", value=120.0)
    horas = c3.number_input("Permanência (h)", value=48)

with tab2:
    mov = st.number_input("Volume Movimentado (Ton/Unid)", value=5000.0)
    st.divider()
    st.subheader("Armazenagem (Tab V)")
    t5_mod = st.radio("Modalidade Tab V", ["Por Área (m²)", "Ad Valorem"])
    t5_area = t5_dias = t5_valor = 0.0
    t5_tipo = "Pátio"
    if t5_mod == "Por Área (m²)":
        t5_tipo = st.selectbox("Local", ["Pátio", "Armazém"])
        t5_area = st.number_input("Área (m²)", value=0.0)
        t5_dias = st.number_input("Dias", value=0)
    else:
        t5_valor = st.number_input("Valor Comercial da Carga (R$)", value=0.0)

with tab3:
    c1, c2 = st.columns(2)
    t7_agua = c1.number_input("Água (m³)", 0.0)
    t7_kwh = c2.number_input("Energia (kWh)", 0.0)
    t7_reefer = c1.number_input("Container Reefer (Unid x Dias)", 0)
    t7_pesagem = c2.number_input("Pesagem (Ton)", 0.0)
    t7_cert = st.number_input("Certidões (Qtd)", 0)
    st.divider()
    st.subheader("Uso de Área para Fins Diversos e Apoio")
    t7_apoio_tipo = st.selectbox("Finalidade/Tipo", ["Armazem_Diversos", "Patio_Diversos", "Apoio_Coberta", "Apoio_Descoberta_Terra", "Apoio_Descoberta_Agua"])
    t7_apoio_m2 = st.number_input("Área Apoio (m²)", 0.0)
    t7_apoio_dias = st.number_input("Dias Apoio", 0)

with tab4:
    st.subheader(f"Regra Específica: {porto}")
    t8_m2_belem = t8_dias_belem = t8_nc_m2 = t8_c_m2 = t8_giro = t8_meses = 0.0
    t8_tipo_belem = t8_nc_local = t8_c_local = ""

    if porto == "Belém":
        st.info("Regime de Uso Temporário (Diário)")
        t8_tipo_belem = st.selectbox("Pavimentação", ["Pavimentada", "NaoPavimentada", "Agua"])
        t8_m2_belem = st.number_input("Área (m²)", 0.0, key="b1")
        t8_dias_belem = st.number_input("Dias", 0, key="b2")
    else:
        st.info("Regime de Arrendamento Simplificado (Mensal)")
        t8_meses = st.number_input("Meses (ou fração)", 1, key="m1")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Cargas Não Consolidadas**")
            t8_nc_local = st.selectbox("Tipo de Área (NC)", ["NC_Primaria", "NC_Remota", "NC_Agua"])
            t8_nc_m2 = st.number_input("Área NC (m²)", 0.0)
        with c2:
            st.markdown("**Cargas Consolidadas/Granel**")
            t8_c_local = st.selectbox("Tipo de Área (C)", ["C_Primaria", "C_Sitio", "C_Granel"])
            t8_c_m2 = st.number_input("Área C (m²)", 0.0)
        t8_giro = st.number_input("Base Giro 12 (Indicador)", 0.0)

if st.button("CALCULAR FATURAMENTO ESTIMADO", type="primary", use_container_width=True):
    engine = EngineFaturamentoCDP()
    res = engine.calcular(locals())
    st.success(f"### TOTAL: R$ {format_br(res['TOTAL'])}")
    for k, v in res.items():
        if k != "TOTAL" and v["v"] > 0:
            with st.expander(f"{k}"):
                st.write(f"**Valor:** R$ {format_br(v['v'])}")
                st.caption(f"Fórmula: {v['m']}")