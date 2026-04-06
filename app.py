import streamlit as st
from typing import Dict, Any

# ==========================================
# UTILITÁRIOS E FORMATAÇÃO
# ==========================================
def format_br(valor: float) -> str:
    """Formata para o padrão monetário brasileiro (R$ 1.234,56)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================
# BASE DE DADOS TARIFÁRIA INTEGRAL (DIREXE 06, 07 e 08/2025)
# ==========================================
TARIFAS_CDP = {
    "Vila do Conde": {
        "Tabela_I_Fixo": {"Longo Curso": 2261.95, "Cabotagem": 2261.95, "Navegação Interior": 2261.95, "Apoio Portuário": 2261.95, "Apoio Marítimo": 2261.95},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 2.56, "Granel Líquido": 2.30, "Carga Geral": 1.15, "Contêineres": 0.48, "Veículos Roll-on/Roll-off": 1.15, "Carga Viva": 1.15, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 1.16, "Granel Líquido": 2.30, "Carga Geral": 1.15, "Contêineres": 0.48, "Veículos Roll-on/Roll-off": 1.15, "Carga Viva": 1.15, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.48}, "Apoio Portuário": {"Toda Carga": 0.48}, "Apoio Marítimo": {"Toda Carga": 0.48}
        },
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": {"t3": 6.02, "t4": 0.00}, 
            "Granel Líquido": {"t3": 8.11, "t4": 0.00},
            "Carga Geral": {"t3": 4.91, "t4": 0.00},
            "Contêiner Cheio": {"t3": 73.50, "t4": 0.00},
            "Contêiner Vazio": {"t3": 36.74, "t4": 0.00},
            "Ro-Ro: Carretas, reboques ou caminhões": {"t3": 38.27, "t4": 0.00}, 
            "Ro-Ro: Cavalo mecânico": {"t3": 9.57, "t4": 0.00},               
            "Ro-Ro: Automóveis e outros até 2t": {"t3": 3.82, "t4": 0.00},    
            "Animais: Até 1.000 kg": {"t3": 6.34, "t4": 0.00},                
            "Animais: Acima de 1.000 kg": {"t3": 12.61, "t4": 0.00}            
        },
        "Tabela_V_Armazenagem": {"Ad_Valorem_1_Periodo": 0.005, "Pátio Descoberto": 2.10, "Armazém Coberto": 4.50},
        "Tabela_VII_Diversos": {
            "Agua": 15.49,
            "Energia_kWh": 1.62,
            "Energia_Conteiner_Dia": 120.50,
            "Pesagem_Ton": 1.15,
            "Area_Armazem_Fins_Diversos": 2.10,
            "Area_Patio_Fins_Diversos": 1.10,
            "Certidao_Operador_Portuario": 1850.00,
            "Area_Coberta_Apoio": 2.10,
            "Area_Descoberta_Apoio_Terra": 1.10,
            "Area_Descoberta_Apoio_Agua": 0.55
        },
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
    },
    "Belém": {
        "Tabela_I_Fixo": {"Longo Curso": 628.32, "Cabotagem": 628.32, "Navegação Interior": 628.32, "Apoio Portuário": 628.32, "Apoio Marítimo": 628.32},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 1.14, "Granel Líquido": 0.60, "Carga Geral": 0.23, "Contêineres": 0.80, "Veículos Roll-on/Roll-off": 0.23, "Carga Viva": 0.23, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 0.52, "Granel Líquido": 0.60, "Carga Geral": 0.23, "Contêineres": 0.80, "Veículos Roll-on/Roll-off": 0.23, "Carga Viva": 0.23, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.16}, "Apoio Portuário": {"Toda Carga": 0.16}, "Apoio Marítimo": {"Toda Carga": 0.16}
        },
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": {"t3": 4.88, "t4": 0.00}, 
            "Granel Líquido": {"t3": 5.10, "t4": 0.00},
            "Carga Geral": {"t3": 4.60, "t4": 0.00},
            "Contêiner Cheio": {"t3": 60.00, "t4": 0.00},
            "Contêiner Vazio": {"t3": 30.00, "t4": 0.00},
            "Ro-Ro: Carretas, reboques ou caminhões": {"t3": 38.14, "t4": 0.00}, 
            "Ro-Ro: Cavalo mecânico": {"t3": 9.55, "t4": 0.00},               
            "Ro-Ro: Automóveis e outros até 2t": {"t3": 3.81, "t4": 0.00},    
            "Animais: Até 1.000 kg": {"t3": 6.34, "t4": 0.00},                
            "Animais: Acima de 1.000 kg": {"t3": 12.61, "t4": 0.00}            
        },
        "Tabela_V_Armazenagem": {"Ad_Valorem_1_Periodo": 0.005, "Pátio Descoberto": 1.50, "Armazém Coberto": 3.80},
        "Tabela_VII_Diversos": {
            "Agua": 15.49,
            "Energia_kWh": 1.62,
            "Energia_Conteiner_Dia": 120.50,
            "Pesagem_Ton": 1.15,
            "Area_Armazem_Fins_Diversos": 1.80,
            "Area_Patio_Fins_Diversos": 0.90,
            "Certidao_Operador_Portuario": 1850.00,
            "Area_Coberta_Apoio": 1.80,
            "Area_Descoberta_Apoio_Terra": 0.90,
            "Area_Descoberta_Apoio_Agua": 0.45
        },
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
    },
    "Santarém": {
        "Tabela_I_Fixo": {"Longo Curso": 359.04, "Cabotagem": 359.04, "Navegação Interior": 359.04, "Apoio Portuário": 359.04, "Apoio Marítimo": 359.04},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 3.41, "Granel Líquido": 2.19, "Carga Geral": 0.17, "Contêineres": 0.16, "Veículos Roll-on/Roll-off": 0.17, "Carga Viva": 0.17, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 3.58, "Granel Líquido": 0.22, "Carga Geral": 1.15, "Contêineres": 0.22, "Veículos Roll-on/Roll-off": 1.15, "Carga Viva": 1.15, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.10}, "Apoio Portuário": {"Toda Carga": 0.10}, "Apoio Marítimo": {"Toda Carga": 0.10}
        },
        "Tabela_I_Fundeio": {"Operando": 3690.75, "Parado": 2636.55},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": {"t3": 4.91, "t4": 0.00}, 
            "Granel Líquido": {"t3": 4.91, "t4": 0.00},
            "Carga Geral": {"t3": 4.91, "t4": 0.00},
            "Contêiner Cheio": {"t3": 50.00, "t4": 0.00},
            "Contêiner Vazio": {"t3": 25.00, "t4": 0.00},
            "Ro-Ro: Carretas, reboques ou caminhões": {"t3": 38.30, "t4": 0.00}, 
            "Ro-Ro: Cavalo mecânico": {"t3": 9.59, "t4": 0.00},               
            "Ro-Ro: Automóveis e outros até 2t": {"t3": 3.82, "t4": 0.00},    
            "Animais: Até 1.000 kg": {"t3": 0.00, "t4": 0.00},                
            "Animais: Acima de 1.000 kg": {"t3": 0.00, "t4": 0.00}            
        },
        "Tabela_V_Armazenagem": {"Ad_Valorem_1_Periodo": 0.005, "Pátio Descoberto": 1.20, "Armazém Coberto": 3.00},
        "Tabela_VII_Diversos": {
            "Agua": 15.49,
            "Energia_kWh": 1.62,
            "Energia_Conteiner_Dia": 120.50,
            "Pesagem_Ton": 1.15,
            "Area_Armazem_Fins_Diversos": 1.50,
            "Area_Patio_Fins_Diversos": 0.80,
            "Certidao_Operador_Portuario": 1850.00,
            "Area_Coberta_Apoio": 1.50,
            "Area_Descoberta_Apoio_Terra": 0.80,
            "Area_Descoberta_Apoio_Agua": 0.40
        },
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 7.23, "Nao Pavimentada": 5.79}
    }
}

# ==========================================
# ENGINE DE NEGÓCIOS
# ==========================================
class MotorTarifarioCDP:
    def processar(self, req: Dict[str, Any]) -> Dict[str, Any]:
        db = TARIFAS_CDP[req["porto"]]
        nav = req["navegacao"]
        
        extrato = {}

        # --- TABELA I ---
        taxa_fixa_t1 = db["Tabela_I_Fixo"][nav]
        if nav in ["Navegação Interior", "Apoio Portuário", "Apoio Marítimo"]:
            taxa_var_t1 = db["Tabela_I_Var"][nav]["Toda Carga"]
        else:
            taxa_var_t1 = db["Tabela_I_Var"][nav].get(req["carga_grupo"], 0.00)
            
        extrato["Tabela I - Acesso Aquaviário"] = {
            "valor": taxa_fixa_t1 + (req["tpb"] * taxa_var_t1),
            "mem": f"R$ {format_br(taxa_fixa_t1)} (Fixo) + [{format_br(req['tpb'])} TPB x R$ {format_br(taxa_var_t1)}]"
        }

        if req["dias_fundeio"] > 0:
            condicao_fundeio = "Operando" if req["fundeio_operando"] else "Parado"
            taxa_fundeio = db["Tabela_I_Fundeio"][condicao_fundeio]
            extrato["Tabela I - Fundeio"] = {"valor": req["dias_fundeio"] * taxa_fundeio, "mem": f"{req['dias_fundeio']} dia(s) x R$ {format_br(taxa_fundeio)} ({condicao_fundeio})"}

        # --- TABELA II ---
        if req["horas_atracacao"] > 0:
            taxa_t2 = db["Tabela_II_Acostagem"][nav]
            extrato["Tabela II - Acostagem"] = {"valor": req["comprimento"] * req["horas_atracacao"] * taxa_t2, "mem": f"{format_br(req['comprimento'])}m x {req['horas_atracacao']}h x R$ {format_br(taxa_t2)}"}

        # --- TABELAS III e IV ---
        if req["carga_grupo"] != "Nenhuma":
            chave_t3_t4 = req["carga_especifica"]
            taxas_op = db["Tabela_III_IV"].get(chave_t3_t4, {"t3": 0.0, "t4": 0.0})
            
            if req["qtd_t3"] > 0:
                extrato["Tabela III - Infra. Operacional"] = {"valor": req["qtd_t3"] * taxas_op["t3"], "mem": f"{format_br(req['qtd_t3'])} ({req['unid_medida']}) x R$ {format_br(taxas_op['t3'])} [{chave_t3_t4}]"}
            
            if req["qtd_t4"] > 0 and taxas_op["t4"] > 0:
                extrato["Tabela IV - Movimentação"] = {"valor": req["qtd_t4"] * taxas_op["t4"], "mem": f"{format_br(req['qtd_t4'])} ({req['unid_medida']}) x R$ {format_br(taxas_op['t4'])} [{chave_t3_t4}]"}

        # --- TABELA V ---
        if req["modalidade_t5"] == "Ad Valorem (%)" and req["valor_carga_t5"] > 0:
            taxa_t5 = db["Tabela_V_Armazenagem"]["Ad_Valorem_1_Periodo"]
            extrato["Tabela V - Armazenagem (Valor)"] = {"valor": req["valor_carga_t5"] * taxa_t5, "mem": f"R$ {format_br(req['valor_carga_t5'])} x {taxa_t5*100}% (Ad Valorem)"}
        elif req["modalidade_t5"] == "Por Área (m²)" and req["area_t5"] > 0:
            taxa_t5 = db["Tabela_V_Armazenagem"][req["tipo_area_t5"]]
            extrato["Tabela V - Armazenagem (Física)"] = {"valor": req["area_t5"] * req["dias_t5"] * taxa_t5, "mem": f"{format_br(req['area_t5'])}m² x {req['dias_t5']} dias x R$ {format_br(taxa_t5)} ({req['tipo_area_t5']})"}

        # --- TABELA VII (Mapeamento Completo e Exaustivo) ---
        t7_db = db["Tabela_VII_Diversos"]
        
        if req["t7_agua"] > 0:
            extrato["Tabela VII - Água Potável"] = {"valor": req["t7_agua"] * t7_db["Agua"], "mem": f"{format_br(req['t7_agua'])} m³ x R$ {format_br(t7_db['Agua'])}"}
            
        if req["t7_energia_kwh"] > 0:
            extrato["Tabela VII - Energia (Instalações)"] = {"valor": req["t7_energia_kwh"] * t7_db["Energia_kWh"], "mem": f"{format_br(req['t7_energia_kwh'])} kWh x R$ {format_br(t7_db['Energia_kWh'])}"}
            
        if req["t7_energia_conteiner"] > 0:
            extrato["Tabela VII - Energia (Contêineres)"] = {"valor": req["t7_energia_conteiner"] * t7_db["Energia_Conteiner_Dia"], "mem": f"{req['t7_energia_conteiner']} (unid x dias) x R$ {format_br(t7_db['Energia_Conteiner_Dia'])}"}
            
        if req["t7_pesagem"] > 0:
            extrato["Tabela VII - Pesagem de Veículos/Vagões"] = {"valor": req["t7_pesagem"] * t7_db["Pesagem_Ton"], "mem": f"{format_br(req['t7_pesagem'])} ton x R$ {format_br(t7_db['Pesagem_Ton'])}"}
            
        if req["t7_certidao_op"] > 0:
            extrato["Tabela VII - Certificado Operador Portuário"] = {"valor": req["t7_certidao_op"] * t7_db["Certidao_Operador_Portuario"], "mem": f"{req['t7_certidao_op']} unid x R$ {format_br(t7_db['Certidao_Operador_Portuario'])}"}

        if req["t7_area_armazem"] > 0 and req["t7_dias_armazem"] > 0:
            extrato["Tabela VII - Área Armazém (Fins Diversos)"] = {"valor": req["t7_area_armazem"] * req["t7_dias_armazem"] * t7_db["Area_Armazem_Fins_Diversos"], "mem": f"{format_br(req['t7_area_armazem'])} m² x {req['t7_dias_armazem']} dias x R$ {format_br(t7_db['Area_Armazem_Fins_Diversos'])}"}

        if req["t7_area_patio"] > 0 and req["t7_dias_patio"] > 0:
            extrato["Tabela VII - Área Pátio (Fins Diversos)"] = {"valor": req["t7_area_patio"] * req["t7_dias_patio"] * t7_db["Area_Patio_Fins_Diversos"], "mem": f"{format_br(req['t7_area_patio'])} m² x {req['t7_dias_patio']} dias x R$ {format_br(t7_db['Area_Patio_Fins_Diversos'])}"}

        if req["t7_area_cob_apoio"] > 0 and req["t7_dias_cob_apoio"] > 0:
            extrato["Tabela VII - Área Coberta (Apoio Operacional)"] = {"valor": req["t7_area_cob_apoio"] * req["t7_dias_cob_apoio"] * t7_db["Area_Coberta_Apoio"], "mem": f"{format_br(req['t7_area_cob_apoio'])} m² x {req['t7_dias_cob_apoio']} dias x R$ {format_br(t7_db['Area_Coberta_Apoio'])}"}

        if req["t7_area_desc_terra"] > 0 and req["t7_dias_desc_terra"] > 0:
            extrato["Tabela VII - Área Descoberta Terra (Apoio)"] = {"valor": req["t7_area_desc_terra"] * req["t7_dias_desc_terra"] * t7_db["Area_Descoberta_Apoio_Terra"], "mem": f"{format_br(req['t7_area_desc_terra'])} m² x {req['t7_dias_desc_terra']} dias x R$ {format_br(t7_db['Area_Descoberta_Apoio_Terra'])}"}

        if req["t7_area_desc_agua"] > 0 and req["t7_dias_desc_agua"] > 0:
            extrato["Tabela VII - Área Descoberta Espelho d'Água"] = {"valor": req["t7_area_desc_agua"] * req["t7_dias_desc_agua"] * t7_db["Area_Descoberta_Apoio_Agua"], "mem": f"{format_br(req['t7_area_desc_agua'])} m² x {req['t7_dias_desc_agua']} dias x R$ {format_br(t7_db['Area_Descoberta_Apoio_Agua'])}"}

        # --- TABELA VIII ---
        if req["area_t8"] > 0:
            taxa_t8 = db["Tabela_VIII_Uso_Temp"][req["tipo_piso_t8"]]
            extrato["Tabela VIII - Uso Temp. / Arrendamento"] = {"valor": req["area_t8"] * taxa_t8, "mem": f"{format_br(req['area_t8'])}m² x R$ {format_br(taxa_t8)} ({req['tipo_piso_t8']})"}

        extrato["TOTAL_GERAL"] = sum(item["valor"] for item in extrato.values())
        return extrato

# ==========================================
# INTERFACE STREAMLIT FRONT-END (Tabela VII Expandida)
# ==========================================
st.set_page_config(page_title="Simulador CDP Avançado", layout="wide")
st.title("⚓ Motor de Faturamento CDP - DIREXE 2025")

motor = MotorTarifarioCDP()

with st.sidebar:
    st.header("⚙️ Configuração Macro")
    porto = st.selectbox("Complexo Portuário", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade", ["Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Portuário", "Apoio Marítimo"])
    
    carga_grupo = st.selectbox("Grupo de Carga", [
        "Granel Sólido", "Granel Líquido", "Carga Geral", 
        "Contêineres", "Veículos Roll-on/Roll-off", "Carga Viva", "Nenhuma"
    ])
    
    carga_especifica = carga_grupo
    unid_medida = "Toneladas"

    if carga_grupo == "Contêineres":
        carga_especifica = st.radio("Condição:", ["Contêiner Cheio", "Contêiner Vazio"])
        unid_medida = "Unidades (TEU/Caixas)"
    elif carga_grupo == "Veículos Roll-on/Roll-off":
        carga_especifica = st.radio("Categoria (Ro-Ro):", ["Ro-Ro: Carretas, reboques ou caminhões", "Ro-Ro: Cavalo mecânico", "Ro-Ro: Automóveis e outros até 2t"])
        unid_medida = "Unidades (Veículos)"
    elif carga_grupo == "Carga Viva":
        carga_especifica = st.radio("Porte:", ["Animais: Até 1.000 kg", "Animais: Acima de 1.000 kg"])
        unid_medida = "Cabeças"
    elif carga_grupo == "Nenhuma":
        unid_medida = "N/A"

    st.divider()
    if st.button("Limpar Formulário", use_container_width=True):
        st.rerun()

t1, t2, t3, t4 = st.tabs([
    "🚢 1. Embarcação (I e II)", 
    "📦 2. Mov. e Armazenagem (III, IV, V)", 
    "🛠️ 3. Serviços e Apoio (VII)", 
    "🏗️ 4. Uso de Áreas (VIII)"
])

with t1:
    st.subheader("Tabela I e II - Acesso, Fundeio e Acostagem")
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("TPB / DWT", min_value=0.0, value=15000.0)
    comprimento = c2.number_input("Comprimento (m)", min_value=0.0, value=120.0)
    horas_atracacao = c3.number_input("Permanência Berço (h)", min_value=0, value=48)
    
    c4, c5 = st.columns(2)
    dias_fundeio = c4.number_input("Dias de Fundeio", min_value=0, value=0)
    fundeio_operando = c5.checkbox("Operação no fundeio?")

with t2:
    st.subheader(f"Movimentação (Tabelas III e IV)")
    c6, c7 = st.columns(2)
    qtd_t3 = c6.number_input(f"Vol. Tab III ({unid_medida})", min_value=0.0, value=0.0, disabled=(carga_grupo=="Nenhuma"))
    qtd_t4 = c7.number_input(f"Vol. Tab IV ({unid_medida})", min_value=0.0, value=0.0, disabled=(carga_grupo=="Nenhuma"), help="Tabela IV possui tarifas Convencionais na CDP. Consulte o Operador.")
    
    st.markdown("---")
    st.subheader("Armazenagem (Tabela V)")
    modalidade_t5 = st.radio("Modalidade", ["Por Área (m²)", "Ad Valorem (%)"])
    
    if modalidade_t5 == "Por Área (m²)":
        c8, c9, c10 = st.columns(3)
        tipo_area_t5 = c8.selectbox("Instalação Tab V", ["Pátio Descoberto", "Armazém Coberto"])
        area_t5 = c9.number_input("Área Tab V (m²)", min_value=0.0, value=0.0)
        dias_t5 = c10.number_input("Dias Tab V", min_value=0, value=0)
        valor_carga_t5 = 0.0
    else:
        valor_carga_t5 = st.number_input("Valor da Carga (R$)", min_value=0.0, value=0.0)
        area_t5, dias_t5 = 0.0, 0
        tipo_area_t5 = "Pátio Descoberto"

with t3:
    st.subheader("Fornecimentos (Tabela VII)")
    c11, c12, c13 = st.columns(3)
    t7_agua = c11.number_input("Água Potável (m³)", min_value=0.0, value=0.0)
    t7_energia_kwh = c12.number_input("Energia Área do Porto (kWh)", min_value=0.0, value=0.0)
    t7_energia_conteiner = c13.number_input("Energia Contêiner Refrigerado (unid x dias)", min_value=0, value=0)
    
    st.markdown("---")
    st.subheader("Serviços Específicos (Tabela VII)")
    c14, c15 = st.columns(2)
    t7_pesagem = c14.number_input("Pesagem de Vagões/Veículos (Ton/Fração)", min_value=0.0, value=0.0)
    t7_certidao_op = c15.number_input("Certificado Operador Portuário (Qtd)", min_value=0, value=0)
    
    st.markdown("---")
    st.subheader("Utilização de Áreas - Fins Diversos (Tabela VII)")
    st.info("Cobrança por m² x dia")
    c16, c17, c18, c19 = st.columns(4)
    t7_area_armazem = c16.number_input("Área Armazém (m²)", min_value=0.0, value=0.0)
    t7_dias_armazem = c17.number_input("Dias (Armazém)", min_value=0, value=0)
    t7_area_patio = c18.number_input("Área Pátio (m²)", min_value=0.0, value=0.0)
    t7_dias_patio = c19.number_input("Dias (Pátio)", min_value=0, value=0)
    
    st.subheader("Utilização de Áreas - Apoio Operacional (Tabela VII)")
    c20, c21, c22, c23 = st.columns(4)
    t7_area_cob_apoio = c20.number_input("Área Coberta Apoio (m²)", min_value=0.0, value=0.0)
    t7_dias_cob_apoio = c21.number_input("Dias (Cob. Apoio)", min_value=0, value=0)
    t7_area_desc_terra = c22.number_input("Área Desc. Terra (m²)", min_value=0.0, value=0.0)
    t7_dias_desc_terra = c23.number_input("Dias (Desc. Terra)", min_value=0, value=0)
    
    c24, c25 = st.columns(2)
    t7_area_desc_agua = c24.number_input("Área Desc. Espelho d'Água (m²)", min_value=0.0, value=0.0)
    t7_dias_desc_agua = c25.number_input("Dias (Espelho d'Água)", min_value=0, value=0)

with t4:
    st.subheader("Tabela VIII - Arrendamento Simplificado")
    st.info("Diferente da Tabela VII (Apoio e Fins Diversos), a Tabela VIII é para Uso Temporário e Arrendamento Simplificado.")
    c26, c27 = st.columns(2)
    area_t8 = c26.number_input("Metragem Cedida (m²)", min_value=0.0, value=0.0)
    tipo_piso_t8 = c27.radio("Piso Tab VIII", ["Pavimentada", "Nao Pavimentada"], disabled=(area_t8==0.0))

st.divider()

if st.button("GERAR ESPELHO DE FATURAMENTO", type="primary", use_container_width=True):
    payload = {
        "porto": porto, "navegacao": navegacao, 
        "carga_grupo": carga_grupo, "carga_especifica": carga_especifica,
        "tpb": tpb, "comprimento": comprimento, "horas_atracacao": horas_atracacao,
        "dias_fundeio": dias_fundeio, "fundeio_operando": fundeio_operando,
        "qtd_t3": qtd_t3, "qtd_t4": qtd_t4, "unid_medida": unid_medida,
        "modalidade_t5": modalidade_t5, "valor_carga_t5": valor_carga_t5, 
        "area_t5": area_t5, "dias_t5": dias_t5, "tipo_area_t5": tipo_area_t5,
        "t7_agua": t7_agua, "t7_energia_kwh": t7_energia_kwh, "t7_energia_conteiner": t7_energia_conteiner,
        "t7_pesagem": t7_pesagem, "t7_certidao_op": t7_certidao_op,
        "t7_area_armazem": t7_area_armazem, "t7_dias_armazem": t7_dias_armazem,
        "t7_area_patio": t7_area_patio, "t7_dias_patio": t7_dias_patio,
        "t7_area_cob_apoio": t7_area_cob_apoio, "t7_dias_cob_apoio": t7_dias_cob_apoio,
        "t7_area_desc_terra": t7_area_desc_terra, "t7_dias_desc_terra": t7_dias_desc_terra,
        "t7_area_desc_agua": t7_area_desc_agua, "t7_dias_desc_agua": t7_dias_desc_agua,
        "area_t8": area_t8, "tipo_piso_t8": tipo_piso_t8
    }
    
    res = motor.processar(payload)
    
    st.success(f"## TOTAL FATURADO: R$ {format_br(res['TOTAL_GERAL'])}")
    st.markdown("### 📋 Memória de Cálculo Oficial (CDP - DIREXE 2025)")
    
    html = "| Tabela/Rubrica (ANTAQ/CDP) | Valor Apurado (R$) | Trilha de Cálculo e Memória |\n| :--- | :--- | :--- |\n"
    for k, v in res.items():
        if k != "TOTAL_GERAL" and v["valor"] > 0:
            html += f"| **{k}** | R$ {format_br(v['valor'])} | `{v['mem']}` |\n"
            
    if len(res) == 1:
        st.warning("Preencha os campos operacionais nas abas acima para simular a tarifa.")
    else:
        st.markdown(html)