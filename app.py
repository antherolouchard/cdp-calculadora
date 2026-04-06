import streamlit as st
from typing import Dict, Any

# ==========================================
# UTILITÁRIOS E FORMATAÇÃO
# ==========================================
def format_br(valor: float) -> str:
    """Formata para o padrão monetário brasileiro (R$ 1.234,56)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================
# BASE DE DADOS TARIFÁRIA (MATRIZ EXAUSTIVA DIREXE 2025)
# ==========================================
# Estrutura fiel linha-a-linha das Deliberações 06, 07 e 08/2025 da CDP.
# As subcategorias (Ro-Ro, Animais, Contêineres) estão isoladas para 
# garantir o mapeamento exato da tarifa.

TARIFAS_CDP = {
    "Vila do Conde": {
        "Tabela_I_Fixo": {"Longo Curso": 2261.95, "Cabotagem": 2261.95, "Navegação Interior": 2261.95, "Apoio Portuário": 2261.95, "Apoio Marítimo": 2261.95},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 2.56, "Granel Líquido": 2.30, "Carga Geral": 1.15, "Contêineres": 0.48, "Veículos Roll-on/Roll-off": 1.15, "Carga Viva": 1.15, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 1.16, "Granel Líquido": 2.30, "Carga Geral": 1.15, "Contêineres": 0.48, "Veículos Roll-on/Roll-off": 1.15, "Carga Viva": 1.15, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.48},
            "Apoio Portuário": {"Toda Carga": 0.48},
            "Apoio Marítimo": {"Toda Carga": 0.48}
        },
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": {"t3": 6.02, "t4": 0.00}, # t4 é Convencional
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
        "Tabela_VII_Diversos": {"Agua": 15.49},
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
    },
    "Belém": {
        "Tabela_I_Fixo": {"Longo Curso": 628.32, "Cabotagem": 628.32, "Navegação Interior": 628.32, "Apoio Portuário": 628.32, "Apoio Marítimo": 628.32},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 1.14, "Granel Líquido": 0.60, "Carga Geral": 0.23, "Contêineres": 0.80, "Veículos Roll-on/Roll-off": 0.23, "Carga Viva": 0.23, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 0.52, "Granel Líquido": 0.60, "Carga Geral": 0.23, "Contêineres": 0.80, "Veículos Roll-on/Roll-off": 0.23, "Carga Viva": 0.23, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.16},
            "Apoio Portuário": {"Toda Carga": 0.16},
            "Apoio Marítimo": {"Toda Carga": 0.16}
        },
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": {"t3": 4.88, "t4": 0.00}, # t4 é Convencional
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
        "Tabela_VII_Diversos": {"Agua": 15.49},
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
    },
    "Santarém": {
        "Tabela_I_Fixo": {"Longo Curso": 359.04, "Cabotagem": 359.04, "Navegação Interior": 359.04, "Apoio Portuário": 359.04, "Apoio Marítimo": 359.04},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 3.41, "Granel Líquido": 2.19, "Carga Geral": 0.17, "Contêineres": 0.16, "Veículos Roll-on/Roll-off": 0.17, "Carga Viva": 0.17, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 3.58, "Granel Líquido": 0.22, "Carga Geral": 1.15, "Contêineres": 0.22, "Veículos Roll-on/Roll-off": 1.15, "Carga Viva": 1.15, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.10},
            "Apoio Portuário": {"Toda Carga": 0.10},
            "Apoio Marítimo": {"Toda Carga": 0.10}
        },
        "Tabela_I_Fundeio": {"Operando": 3690.75, "Parado": 2636.55},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_IV": {
            "Granel Sólido": {"t3": 4.91, "t4": 0.00}, # t4 é Convencional
            "Granel Líquido": {"t3": 4.91, "t4": 0.00},
            "Carga Geral": {"t3": 4.91, "t4": 0.00},
            "Contêiner Cheio": {"t3": 50.00, "t4": 0.00},
            "Contêiner Vazio": {"t3": 25.00, "t4": 0.00},
            "Ro-Ro: Carretas, reboques ou caminhões": {"t3": 38.30, "t4": 0.00}, 
            "Ro-Ro: Cavalo mecânico": {"t3": 9.59, "t4": 0.00},               
            "Ro-Ro: Automóveis e outros até 2t": {"t3": 3.82, "t4": 0.00},    
            "Animais: Até 1.000 kg": {"t3": 0.00, "t4": 0.00}, # Isento / Sem tarifa na imagem               
            "Animais: Acima de 1.000 kg": {"t3": 0.00, "t4": 0.00} # Isento / Sem tarifa na imagem            
        },
        "Tabela_V_Armazenagem": {"Ad_Valorem_1_Periodo": 0.005, "Pátio Descoberto": 1.20, "Armazém Coberto": 3.00},
        "Tabela_VII_Diversos": {"Agua": 15.49},
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

        # ---------------------------------------------------------
        # TABELA I - Acesso Aquaviário e Fundeio
        # ---------------------------------------------------------
        taxa_fixa_t1 = db["Tabela_I_Fixo"][nav]
        
        # Identifica a chave macro para a cobrança de TPB (Tabela I)
        if nav in ["Navegação Interior", "Apoio Portuário", "Apoio Marítimo"]:
            taxa_var_t1 = db["Tabela_I_Var"][nav]["Toda Carga"]
        else:
            taxa_var_t1 = db["Tabela_I_Var"][nav].get(req["carga_grupo"], 0.00)
            
        valor_t1_acesso = taxa_fixa_t1 + (req["tpb"] * taxa_var_t1)
        extrato["Tabela I - Acesso Aquaviário"] = {
            "valor": valor_t1_acesso,
            "mem": f"R$ {format_br(taxa_fixa_t1)} (Fixo) + [{format_br(req['tpb'])} TPB x R$ {format_br(taxa_var_t1)}]"
        }

        if req["dias_fundeio"] > 0:
            condicao_fundeio = "Operando" if req["fundeio_operando"] else "Parado"
            taxa_fundeio = db["Tabela_I_Fundeio"][condicao_fundeio]
            extrato["Tabela I - Fundeio"] = {
                "valor": req["dias_fundeio"] * taxa_fundeio,
                "mem": f"{req['dias_fundeio']} dia(s) x R$ {format_br(taxa_fundeio)} ({condicao_fundeio})"
            }

        # ---------------------------------------------------------
        # TABELA II - Instalações de Acostagem
        # ---------------------------------------------------------
        if req["horas_atracacao"] > 0:
            taxa_t2 = db["Tabela_II_Acostagem"][nav]
            valor_t2 = req["comprimento"] * req["horas_atracacao"] * taxa_t2
            extrato["Tabela II - Acostagem"] = {
                "valor": valor_t2,
                "mem": f"{format_br(req['comprimento'])}m x {req['horas_atracacao']}h x R$ {format_br(taxa_t2)}"
            }

        # ---------------------------------------------------------
        # TABELAS III e IV - Infraestrutura Operacional e Movimentação
        # ---------------------------------------------------------
        if req["carga_grupo"] != "Nenhuma":
            chave_t3_t4 = req["carga_especifica"] # Ex: "Ro-Ro: Cavalo mecânico" ou "Granel Sólido"
            
            taxas_op = db["Tabela_III_IV"].get(chave_t3_t4, {"t3": 0.0, "t4": 0.0})
            
            if req["qtd_t3"] > 0:
                extrato["Tabela III - Infra. Operacional"] = {
                    "valor": req["qtd_t3"] * taxas_op["t3"],
                    "mem": f"{format_br(req['qtd_t3'])} ({req['unid_medida']}) x R$ {format_br(taxas_op['t3'])} [{chave_t3_t4}]"
                }
            
            if req["qtd_t4"] > 0:
                extrato["Tabela IV - Movimentação"] = {
                    "valor": req["qtd_t4"] * taxas_op["t4"],
                    "mem": f"{format_br(req['qtd_t4'])} ({req['unid_medida']}) x R$ {format_br(taxas_op['t4'])} [{chave_t3_t4}]"
                }

        # ---------------------------------------------------------
        # TABELA V - Armazenagem
        # ---------------------------------------------------------
        if req["modalidade_t5"] == "Ad Valorem (%)" and req["valor_carga_t5"] > 0:
            taxa_t5 = db["Tabela_V_Armazenagem"]["Ad_Valorem_1_Periodo"]
            extrato["Tabela V - Armazenagem (Valor)"] = {
                "valor": req["valor_carga_t5"] * taxa_t5,
                "mem": f"R$ {format_br(req['valor_carga_t5'])} x {taxa_t5*100}% (Ad Valorem)"
            }
        elif req["modalidade_t5"] == "Por Área (m²)" and req["area_t5"] > 0:
            taxa_t5 = db["Tabela_V_Armazenagem"][req["tipo_area_t5"]]
            extrato["Tabela V - Armazenagem (Física)"] = {
                "valor": req["area_t5"] * req["dias_t5"] * taxa_t5,
                "mem": f"{format_br(req['area_t5'])}m² x {req['dias_t5']} dias x R$ {format_br(taxa_t5)} ({req['tipo_area_t5']})"
            }

        # ---------------------------------------------------------
        # TABELA VII e VIII - Diversos e Uso Temporário
        # ---------------------------------------------------------
        if req["volume_agua"] > 0:
            taxa_t7 = db["Tabela_VII_Diversos"]["Agua"]
            extrato["Tabela VII - Fornecimento de Água"] = {
                "valor": req["volume_agua"] * taxa_t7,
                "mem": f"{format_br(req['volume_agua'])}m³ x R$ {format_br(taxa_t7)}"
            }

        if req["area_t8"] > 0:
            taxa_t8 = db["Tabela_VIII_Uso_Temp"][req["tipo_piso_t8"]]
            extrato["Tabela VIII - Uso Temporário"] = {
                "valor": req["area_t8"] * taxa_t8,
                "mem": f"{format_br(req['area_t8'])}m² x R$ {format_br(taxa_t8)} ({req['tipo_piso_t8']})"
            }

        extrato["TOTAL_GERAL"] = sum(item["valor"] for item in extrato.values())
        return extrato

# ==========================================
# INTERFACE STREAMLIT FRONT-END (LEIAUTE REFATORADO)
# ==========================================
st.set_page_config(page_title="Simulador CDP Avançado", layout="wide", page_icon="⚓")
st.title("⚓ Motor de Faturamento CDP - DIREXE 2025")

motor = MotorTarifarioCDP()

# --- BARRA LATERAL (CONFIGURAÇÃO GERAL DO NAVIO) ---
with st.sidebar:
    st.header("⚙️ Escopo da Operação")
    porto = st.selectbox("Complexo Portuário", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade de Navegação", [
        "Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Portuário", "Apoio Marítimo"
    ])
    st.divider()
    if st.button("Limpar Formulário", use_container_width=True):
        st.rerun()

# --- ABAS DESTRINCHADAS E CLARAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🚢 1. Embarcação (Tab. I e II)", 
    "📦 2. Carga e Movimentação (Tab. III e IV)", 
    "🏢 3. Armazenagem (Tab. V)", 
    "🔌 4. Diversos e Áreas (Tab. VII e VIII)"
])

# ================= ABA 1: EMBARCAÇÃO =================
with tab1:
    st.subheader("Tabela I - Infraestrutura de Acesso Aquaviário")
    tpb = st.number_input("TPB / DWT (Porte Bruto)", min_value=0.0, value=15000.0)
    
    st.subheader("Tabela I - Fila e Fundeio")
    c1, c2 = st.columns(2)
    dias_fundeio = c1.number_input("Total de Dias em Fundeio", min_value=0, value=0)
    fundeio_operando = c2.checkbox("Realizou operação comercial no fundeio?")

    st.subheader("Tabela II - Instalações de Acostagem")
    c3, c4 = st.columns(2)
    comprimento = c3.number_input("Comprimento Linear da Embarcação (m)", min_value=0.0, value=120.0)
    horas_atracacao = c4.number_input("Permanência no Berço (Horas)", min_value=0, value=48)

# ================= ABA 2: CARGA / MOVIMENTAÇÃO =================
with tab2:
    st.subheader("Natureza da Operação")
    
    # O usuário seleciona primeiro o GRUPO MACRO
    carga_grupo = st.selectbox("Grupo Principal de Carga", [
        "Granel Sólido", "Granel Líquido", "Carga Geral", 
        "Contêineres", "Veículos Roll-on/Roll-off", "Carga Viva", "Nenhuma"
    ])

    carga_especifica = carga_grupo # Valor padrão caso não tenha subcategoria
    unid_medida = "Toneladas"

    # LÓGICA DE CASCATA: Abre as subcategorias específicas e ajusta a unidade
    if carga_grupo == "Contêineres":
        carga_especifica = st.radio("Condição do Contêiner:", ["Contêiner Cheio", "Contêiner Vazio"])
        unid_medida = "Unidades (TEU/Caixas)"
        
    elif carga_grupo == "Veículos Roll-on/Roll-off":
        carga_especifica = st.radio("Categoria do Veículo (Ro-Ro):", [
            "Ro-Ro: Carretas, reboques ou caminhões",
            "Ro-Ro: Cavalo mecânico",
            "Ro-Ro: Automóveis e outros até 2t"
        ])
        unid_medida = "Unidades (Veículos)"
        
    elif carga_grupo == "Carga Viva":
        carga_especifica = st.radio("Porte do Animal:", [
            "Animais: Até 1.000 kg",
            "Animais: Acima de 1.000 kg"
        ])
        unid_medida = "Cabeças"
        
    elif carga_grupo == "Nenhuma":
        unid_medida = "N/A"

    st.markdown("---")
    st.subheader(f"Incidência (Tabelas III e IV)")
    c5, c6 = st.columns(2)
    qtd_t3 = c5.number_input(f"Vol. Tabela III - Operacional ({unid_medida})", min_value=0.0, value=0.0, disabled=(carga_grupo=="Nenhuma"))
    qtd_t4 = c6.number_input(f"Vol. Tabela IV - Movimentação ({unid_medida})", min_value=0.0, value=0.0, disabled=(carga_grupo=="Nenhuma"))

# ================= ABA 3: ARMAZENAGEM =================
with tab3:
    st.subheader("Tabela V - Utilização da Infraestrutura de Armazenagem")
    modalidade_t5 = st.radio("Selecione a Modalidade Normativa de Cobrança", ["Por Área (m²)", "Ad Valorem (%)"])
    
    if modalidade_t5 == "Por Área (m²)":
        c7, c8, c9 = st.columns(3)
        tipo_area_t5 = c7.selectbox("Tipo de Instalação", ["Pátio Descoberto", "Armazém Coberto"])
        area_t5 = c8.number_input("Área Ocupada (m²)", min_value=0.0, value=0.0)
        dias_t5 = c9.number_input("Dias de Permanência", min_value=0, value=0)
        valor_carga_t5 = 0.0
    else:
        valor_carga_t5 = st.number_input("Valor Comercial Declarado da Carga (R$)", min_value=0.0, value=0.0)
        area_t5 = 0.0
        dias_t5 = 0
        tipo_area_t5 = "Pátio Descoberto"

# ================= ABA 4: DIVERSOS =================
with tab4:
    st.subheader("Tabela VII - Serviços Diversos Padronizados")
    volume_agua = st.number_input("Fornecimento de Água (m³)", min_value=0.0, value=0.0)
    
    st.subheader("Tabela VIII - Uso Temporário / Arrendamento Simplificado")
    c10, c11 = st.columns(2)
    area_t8 = c10.number_input("Metragem de Área Cedida (m²)", min_value=0.0, value=0.0)
    tipo_piso_t8 = c11.radio("Classificação do Solo", ["Pavimentada", "Nao Pavimentada"], disabled=(area_t8==0.0))

st.divider()

# --- PROCESSAMENTO PRINCIPAL ---
if st.button("GERAR ESPELHO DE FATURAMENTO", type="primary", use_container_width=True):
    payload = {
        "porto": porto, "navegacao": navegacao, 
        "carga_grupo": carga_grupo, "carga_especifica": carga_especifica,
        "tpb": tpb, "comprimento": comprimento, "horas_atracacao": horas_atracacao,
        "dias_fundeio": dias_fundeio, "fundeio_operando": fundeio_operando,
        "qtd_t3": qtd_t3, "qtd_t4": qtd_t4, "unid_medida": unid_medida,
        "modalidade_t5": modalidade_t5, "valor_carga_t5": valor_carga_t5, 
        "area_t5": area_t5, "dias_t5": dias_t5, "tipo_area_t5": tipo_area_t5,
        "volume_agua": volume_agua, "area_t8": area_t8, "tipo_piso_t8": tipo_piso_t8
    }
    
    res = motor.processar(payload)
    
    st.success(f"## TOTAL FATURADO: R$ {format_br(res['TOTAL_GERAL'])}")
    st.markdown("### 📋 Memória de Cálculo por Tabela (DIREXE 2025)")
    
    html = "| Rubrica (ANTAQ/CDP) | Valor Apurado (R$) | Trilha de Auditoria |\n| :--- | :--- | :--- |\n"
    for k, v in res.items():
        if k != "TOTAL_GERAL" and v["valor"] > 0:
            html += f"| **{k}** | R$ {format_br(v['valor'])} | `{v['mem']}` |\n"
            
    if len(res) == 1:
        st.warning("Nenhum parâmetro gerou tarifação. Preencha os campos nas abas para calcular o faturamento.")
    else:
        st.markdown(html)