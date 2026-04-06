import streamlit as st
from typing import Dict, Any

# ==========================================
# UTILITÁRIOS DE FORMATAÇÃO
# ==========================================
def format_br(valor: float) -> str:
    """Formata para o padrão monetário brasileiro (R$ 1.234,56)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================
# MOTOR DE CÁLCULO (BUSINESS LOGIC EXAUSTIVA)
# ==========================================
class MotorTarifarioCDP:
    """
    Motor de faturamento estruturado linha a linha com as Deliberações:
    - DIREXE 06/2025 (Vila do Conde)
    - DIREXE 07/2025 (Belém)
    - DIREXE 08/2025 (Santarém)
    """
    def __init__(self):
        self.tarifas = {
            "Vila do Conde": {
                "Tabela_I": {
                    "Longo Curso": {"fixo": 2261.95, "GS": 2.56, "GL": 2.30, "CG": 1.15, "Cont": 0.48, "Nenhuma": 0.0},
                    "Cabotagem": {"fixo": 2261.95, "GS": 1.16, "GL": 2.30, "CG": 1.15, "Cont": 0.48, "Nenhuma": 0.0},
                    "Navegação Interior": {"fixo": 2261.95, "tpb_unico": 0.48},
                    "Apoio Portuário": {"fixo": 2261.95, "tpb_unico": 0.48},
                    "Apoio Marítimo": {"fixo": 2261.95, "tpb_unico": 0.48},
                    "Fundeio": {"Operando": 4417.09, "Parado": 3155.42}
                },
                "Tabela_II": {
                    "Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59,
                    "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33
                },
                "Tabela_III": {"GS": 6.02, "GL": 8.11, "CG": 4.91, "Contêiner Cheio": 73.50, "Contêiner Vazio": 36.74, "Nenhuma": 0.0},
                "Tabela_IV": {"GS": 6.02, "GL": 8.11, "CG": 4.91, "Contêiner Cheio": 73.50, "Contêiner Vazio": 36.74, "Nenhuma": 0.0},
                "Tabela_V": {"ad_valorem_15_dias": 0.005}, # 0,50%
                "Tabela_VII": {"Agua": 15.49},
                "Tabela_VIII": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
            },
            "Belém": {
                "Tabela_I": {
                    "Longo Curso": {"fixo": 628.32, "GS": 1.14, "GL": 0.60, "CG": 0.23, "Cont": 0.80, "Nenhuma": 0.0},
                    "Cabotagem": {"fixo": 628.32, "GS": 0.52, "GL": 0.60, "CG": 0.23, "Cont": 0.80, "Nenhuma": 0.0},
                    "Navegação Interior": {"fixo": 628.32, "tpb_unico": 0.16},
                    "Apoio Portuário": {"fixo": 628.32, "tpb_unico": 0.16},
                    "Apoio Marítimo": {"fixo": 628.32, "tpb_unico": 0.16},
                    "Fundeio": {"Operando": 4417.09, "Parado": 3155.42}
                },
                "Tabela_II": {
                    "Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59,
                    "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33
                },
                "Tabela_III": {"GS": 4.88, "GL": 5.10, "CG": 4.60, "Contêiner Cheio": 60.00, "Contêiner Vazio": 30.00, "Nenhuma": 0.0},
                "Tabela_IV": {"GS": 4.88, "GL": 5.10, "CG": 4.60, "Contêiner Cheio": 60.00, "Contêiner Vazio": 30.00, "Nenhuma": 0.0},
                "Tabela_V": {"ad_valorem_15_dias": 0.005},
                "Tabela_VII": {"Agua": 15.49},
                "Tabela_VIII": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
            },
            "Santarém": {
                "Tabela_I": {
                    "Longo Curso": {"fixo": 359.04, "GS": 3.41, "GL": 2.19, "CG": 0.17, "Cont": 0.16, "Nenhuma": 0.0},
                    "Cabotagem": {"fixo": 359.04, "GS": 3.58, "GL": 0.22, "CG": 1.15, "Cont": 0.22, "Nenhuma": 0.0},
                    "Navegação Interior": {"fixo": 359.04, "tpb_unico": 0.10},
                    "Apoio Portuário": {"fixo": 359.04, "tpb_unico": 0.10},
                    "Apoio Marítimo": {"fixo": 359.04, "tpb_unico": 0.10},
                    "Fundeio": {"Operando": 3690.75, "Parado": 2636.55} # Diferença normativa em Santarém
                },
                "Tabela_II": {
                    "Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59,
                    "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33
                },
                "Tabela_III": {"GS": 4.91, "GL": 4.91, "CG": 4.91, "Contêiner Cheio": 50.00, "Contêiner Vazio": 25.00, "Nenhuma": 0.0},
                "Tabela_IV": {"GS": 4.91, "GL": 4.91, "CG": 4.91, "Contêiner Cheio": 50.00, "Contêiner Vazio": 25.00, "Nenhuma": 0.0},
                "Tabela_V": {"ad_valorem_15_dias": 0.005},
                "Tabela_VII": {"Agua": 15.49},
                "Tabela_VIII": {"Pavimentada": 7.23, "Nao Pavimentada": 5.79}
            }
        }

    def processar(self, req: Dict[str, Any]) -> Dict[str, Any]:
        p = self.tarifas[req["porto"]]
        nav = req["navegacao"]
        carga = req["carga"]
        
        extrato = {}

        # ---------------------------------------------------------
        # TABELA I - Acesso Aquaviário e Fundeio
        # ---------------------------------------------------------
        t1_nav = p["Tabela_I"][nav]
        fixo_t1 = t1_nav["fixo"]
        
        # Define a taxa por TPB dependendo do tipo de navegação
        if nav in ["Navegação Interior", "Apoio Portuário", "Apoio Marítimo"]:
            taxa_tpb = t1_nav["tpb_unico"]
        else:
            # Identifica a chave de carga para LC e Cabotagem
            chave_tpb = "Cont" if "Contêiner" in carga else ("GS" if carga == "Granel Sólido" else ("GL" if carga == "Granel Líquido" else ("CG" if carga == "Carga Geral" else "Nenhuma")))
            taxa_tpb = t1_nav[chave_tpb]
            
        val_acesso = fixo_t1 + (req["tpb"] * taxa_tpb)
        extrato["Tabela I - Acesso Aquaviário"] = {
            "valor": val_acesso, 
            "mem": f"Fixo R$ {format_br(fixo_t1)} + ({req['tpb']} TPB x R$ {format_br(taxa_tpb)})"
        }

        if req["dias_fundeio"] > 0:
            status_fundeio = "Operando" if req["fundeio_operando"] else "Parado"
            taxa_fundeio = p["Tabela_I"]["Fundeio"][status_fundeio]
            val_fundeio = req["dias_fundeio"] * taxa_fundeio
            extrato["Tabela I - Fundeio"] = {
                "valor": val_fundeio, 
                "mem": f"{req['dias_fundeio']} dia(s) x R$ {format_br(taxa_fundeio)} ({status_fundeio})"
            }

        # ---------------------------------------------------------
        # TABELA II - Instalações de Acostagem
        # ---------------------------------------------------------
        if req["horas_atracacao"] > 0:
            taxa_t2 = p["Tabela_II"][nav]
            val_acostagem = req["comprimento"] * req["horas_atracacao"] * taxa_t2
            extrato["Tabela II - Acostagem"] = {
                "valor": val_acostagem, 
                "mem": f"{req['comprimento']}m x {req['horas_atracacao']}h x R$ {format_br(taxa_t2)}"
            }

        # ---------------------------------------------------------
        # TABELA III e IV - Infraestrutura Operacional e Movimentação
        # ---------------------------------------------------------
        if carga != "Nenhuma" and req["movimentacao"] > 0:
            chave_op = "GS" if carga == "Granel Sólido" else ("GL" if carga == "Granel Líquido" else ("CG" if carga == "Carga Geral" else carga))
            
            taxa_t3 = p["Tabela_III"][chave_op]
            extrato["Tabela III - Infra. Operacional"] = {
                "valor": req["movimentacao"] * taxa_t3, 
                "mem": f"{req['movimentacao']} x R$ {format_br(taxa_t3)}"
            }
            
            taxa_t4 = p["Tabela_IV"][chave_op]
            extrato["Tabela IV - Movimentação de Carga"] = {
                "valor": req["movimentacao"] * taxa_t4, 
                "mem": f"{req['movimentacao']} x R$ {format_br(taxa_t4)}"
            }

        # ---------------------------------------------------------
        # TABELA V - Armazenagem (Regra Ad Valorem 0,50%)
        # ---------------------------------------------------------
        if req["valor_mercadoria"] > 0:
            taxa_t5 = p["Tabela_V"]["ad_valorem_15_dias"]
            val_armaz = req["valor_mercadoria"] * taxa_t5
            extrato["Tabela V - Armazenagem"] = {
                "valor": val_armaz, 
                "mem": f"R$ {format_br(req['valor_mercadoria'])} x {taxa_t5*100}% (Ad Valorem)"
            }

        # ---------------------------------------------------------
        # TABELA VII - Diversos Padronizados (Água)
        # ---------------------------------------------------------
        if req["volume_agua"] > 0:
            taxa_t7 = p["Tabela_VII"]["Agua"]
            val_agua = req["volume_agua"] * taxa_t7
            extrato["Tabela VII - Fornecimento de Água"] = {
                "valor": val_agua, 
                "mem": f"{req['volume_agua']}m³ x R$ {format_br(taxa_t7)}"
            }

        # ---------------------------------------------------------
        # TABELA VIII - Uso Temporário (Arrendamento Simplificado)
        # ---------------------------------------------------------
        if req["area_t8"] > 0:
            tipo_piso = req["tipo_piso_t8"]
            taxa_t8 = p["Tabela_VIII"][tipo_piso]
            val_uso_temp = req["area_t8"] * taxa_t8
            extrato["Tabela VIII - Uso Temporário"] = {
                "valor": val_uso_temp, 
                "mem": f"{req['area_t8']}m² x R$ {format_br(taxa_t8)} ({tipo_piso})"
            }

        # CÁLCULO DO TOTAL GERAL
        extrato["TOTAL_GERAL"] = sum(item["valor"] for item in extrato.values())
        return extrato

# ==========================================
# INTERFACE DO USUÁRIO (STREAMLIT)
# ==========================================
st.set_page_config(page_title="ERP Tarifário CDP 2025", layout="wide", page_icon="⚓")
st.title("⚓ Sistema Tarifário Oficial CDP - DIREXE 2025")
st.markdown("Cálculo exato parametrizado com as tabelas I a VIII dos portos de Belém, Santarém e Vila do Conde.")

motor = MotorTarifarioCDP()

# --- BARRA LATERAL (CONFIGURAÇÃO BASE) ---
with st.sidebar:
    st.header("⚙️ Operação Principal")
    porto = st.selectbox("Complexo Portuário", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade de Navegação", [
        "Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Portuário", "Apoio Marítimo"
    ])
    carga = st.selectbox("Natureza da Carga", [
        "Granel Sólido", "Granel Líquido", "Carga Geral", "Contêiner Cheio", "Contêiner Vazio", "Nenhuma"
    ])
    
    st.divider()
    if st.button("🔄 Reiniciar Formulário", use_container_width=True):
        st.rerun()

# --- FORMULÁRIOS DIVIDIDOS EM ABAS ---
tab1, tab2, tab3 = st.tabs(["🚢 Embarcação (Tabelas I e II)", "📦 Movimentação (Tabelas III, IV e V)", "🏗️ Diversos e Áreas (Tabelas VII e VIII)"])

with tab1:
    st.subheader("Dados Físicos da Embarcação e Acostagem")
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("Porte Bruto (TPB/DWT)", min_value=0, value=15000)
    comprimento = c2.number_input("Comprimento Linear (m)", min_value=0.0, value=120.0)
    horas_atracacao = c3.number_input("Permanência no Berço (Horas)", min_value=0, value=48)
    
    st.subheader("Situação de Fundeio (Espera)")
    c4, c5 = st.columns(2)
    dias_fundeio = c4.number_input("Dias ao Largo (Fundeio)", min_value=0, value=0)
    fundeio_operando = c5.checkbox("A embarcação realizou operação comercial durante o fundeio?")

with tab2:
    st.subheader("Dados de Movimentação (Tabelas III e IV)")
    lbl_unidade = "Unidades" if "Contêiner" in carga else "Toneladas"
    movimentacao = st.number_input(f"Volume Movimentado ({lbl_unidade})", min_value=0, value=5000, disabled=(carga=="Nenhuma"))
    
    st.subheader("Armazenagem Ad Valorem (Tabela V)")
    st.info("A Tabela V da CDP é calculada sobre o valor comercial da mercadoria (0,50% para o 1º período).")
    valor_mercadoria = st.number_input("Valor Comercial da Carga (R$)", min_value=0.0, value=0.0, step=1000.0)

with tab3:
    st.subheader("Utilidades (Tabela VII)")
    volume_agua = st.number_input("Fornecimento de Água Potável (m³)", min_value=0, value=0)
    
    st.subheader("Uso Temporário de Áreas (Tabela VIII)")
    c6, c7 = st.columns(2)
    area_t8 = c6.number_input("Área Ocupada (m²)", min_value=0, value=0)
    tipo_piso_t8 = c7.radio("Condição do Pavimento", ["Pavimentada", "Nao Pavimentada"], disabled=(area_t8==0))

st.divider()

# --- PROCESSAMENTO ---
if st.button("GERAR EXTRATO OFICIAL (DIREXE 2025)", type="primary", use_container_width=True):
    
    payload = {
        "porto": porto, "navegacao": navegacao, "carga": carga,
        "tpb": tpb, "comprimento": comprimento, "horas_atracacao": horas_atracacao,
        "dias_fundeio": dias_fundeio, "fundeio_operando": fundeio_operando,
        "movimentacao": movimentacao, "valor_mercadoria": valor_mercadoria,
        "volume_agua": volume_agua, "area_t8": area_t8, "tipo_piso_t8": tipo_piso_t8
    }
    
    res = motor.processar(payload)
    
    st.success(f"## FATURAMENTO LÍQUIDO APURADO: R$ {format_br(res['TOTAL_GERAL'])}")
    
    st.markdown("### 📋 Memória de Cálculo Auditável por Tabela")
    
    # Montagem da tabela final dinâmica
    html_table = "| Referência Normativa | Valor Apurado (R$) | Trilha de Cálculo (Fatores x Taxas CDP) |\n| :--- | :--- | :--- |\n"
    for chave, dados in res.items():
        if chave != "TOTAL_GERAL" and dados["valor"] > 0:
            html_table += f"| **{chave}** | R$ {format_br(dados['valor'])} | `{dados['mem']}` |\n"
            
    if len(res) == 1: # Só tem a chave TOTAL_GERAL
        st.warning("Nenhum dado tributável foi inserido na simulação.")
    else:
        st.markdown(html_table)