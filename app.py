import streamlit as st
from typing import Dict, Any

# ==========================================
# CAMADA DE NEGÓCIOS (DOMÍNIO)
# ==========================================

class MotorTarifarioCDP:
    """
    Motor central de processamento das tarifas portuárias da Companhia Docas do Pará.
    Contempla todas as tabelas (I a VIII), portos, navegações e tipos de carga.
    """
    def __init__(self):
        # Matriz Tarifária Completa (Valores a serem calibrados conforme PDFs finais)
        self.tarifas = {
            "Vila do Conde": {
                "regras_gerais": {
                    "t2_atracacao_normal": 0.59, "t2_atracacao_multa": 0.85,
                    "t4_patio": 2.10, "t4_armazem": 4.50,
                    "t5_balanca": 55.00, "t5_guindaste": 250.00,
                    "t7_agua": 22.00,
                    "t8_limpeza": 300.00, "t8_isps": 0.35,
                    "fundeio_operando": 4417.09, "fundeio_parado": 3155.42
                },
                "Longo Curso": {
                    "t1_fixa": 628.32, "t1_tpb": 0.80, 
                    "Carga": {"Granel Sólido": 6.02, "Granel Líquido": 8.11, "Carga Geral": 4.91, "Contêiner Cheio": 73.50, "Contêiner Vazio": 15.00}
                },
                "Cabotagem": {
                    "t1_fixa": 300.00, "t1_tpb": 0.40, 
                    "Carga": {"Granel Sólido": 4.50, "Granel Líquido": 6.00, "Carga Geral": 3.00, "Contêiner Cheio": 50.00, "Contêiner Vazio": 10.00}
                },
                "Navegação Interior": {
                    "t1_fixa": 150.00, "t1_tpb": 0.15, 
                    "Carga": {"Granel Sólido": 2.00, "Granel Líquido": 2.50, "Carga Geral": 1.50, "Contêiner Cheio": 25.00, "Contêiner Vazio": 5.00}
                },
                "Apoio Marítimo": {
                    "t1_fixa": 100.00, "t1_tpb": 0.10, 
                    "Carga": {"Granel Sólido": 0.00, "Granel Líquido": 0.00, "Carga Geral": 1.00, "Contêiner Cheio": 0.00, "Contêiner Vazio": 0.00}
                }
            },
            "Belém": {
                "regras_gerais": {
                    "t2_atracacao_normal": 0.59, "t2_atracacao_multa": 0.85,
                    "t4_patio": 1.50, "t4_armazem": 3.80,
                    "t5_balanca": 55.00, "t5_guindaste": 200.00,
                    "t7_agua": 18.50,
                    "t8_limpeza": 250.00, "t8_isps": 0.35,
                    "fundeio_operando": 4417.09, "fundeio_parado": 3155.42
                },
                "Longo Curso": {
                    "t1_fixa": 628.32, "t1_tpb": 0.80, 
                    "Carga": {"Granel Sólido": 5.00, "Granel Líquido": 5.00, "Carga Geral": 4.88, "Contêiner Cheio": 60.00, "Contêiner Vazio": 12.00}
                },
                "Cabotagem": {
                    "t1_fixa": 300.00, "t1_tpb": 0.40, 
                    "Carga": {"Granel Sólido": 3.00, "Granel Líquido": 3.00, "Carga Geral": 3.00, "Contêiner Cheio": 40.00, "Contêiner Vazio": 8.00}
                },
                "Navegação Interior": {
                    "t1_fixa": 150.00, "t1_tpb": 0.15, 
                    "Carga": {"Granel Sólido": 1.80, "Granel Líquido": 1.80, "Carga Geral": 1.50, "Contêiner Cheio": 20.00, "Contêiner Vazio": 4.00}
                },
                "Apoio Marítimo": {
                    "t1_fixa": 100.00, "t1_tpb": 0.10, 
                    "Carga": {"Granel Sólido": 0.00, "Granel Líquido": 0.00, "Carga Geral": 1.00, "Contêiner Cheio": 0.00, "Contêiner Vazio": 0.00}
                }
            },
            "Santarém": {
                "regras_gerais": {
                    "t2_atracacao_normal": 0.50, "t2_atracacao_multa": 0.75,
                    "t4_patio": 1.20, "t4_armazem": 3.00,
                    "t5_balanca": 45.00, "t5_guindaste": 180.00,
                    "t7_agua": 15.00,
                    "t8_limpeza": 200.00, "t8_isps": 0.25,
                    "fundeio_operando": 3690.75, "fundeio_parado": 2636.55
                },
                "Longo Curso": {
                    "t1_fixa": 359.04, "t1_tpb": 0.16, 
                    "Carga": {"Granel Sólido": 4.00, "Granel Líquido": 4.00, "Carga Geral": 4.91, "Contêiner Cheio": 50.00, "Contêiner Vazio": 10.00}
                },
                "Cabotagem": {
                    "t1_fixa": 200.00, "t1_tpb": 0.08, 
                    "Carga": {"Granel Sólido": 2.50, "Granel Líquido": 2.50, "Carga Geral": 3.00, "Contêiner Cheio": 35.00, "Contêiner Vazio": 5.00}
                },
                "Navegação Interior": {
                    "t1_fixa": 100.00, "t1_tpb": 0.05, 
                    "Carga": {"Granel Sólido": 1.50, "Granel Líquido": 1.50, "Carga Geral": 1.50, "Contêiner Cheio": 15.00, "Contêiner Vazio": 3.00}
                },
                "Apoio Marítimo": {
                    "t1_fixa": 80.00, "t1_tpb": 0.05, 
                    "Carga": {"Granel Sólido": 0.00, "Granel Líquido": 0.00, "Carga Geral": 1.00, "Contêiner Cheio": 0.00, "Contêiner Vazio": 0.00}
                }
            }
        }

    def calcular_atracacao(self, porto: str, comprimento: float, horas: int) -> float:
        """Aplica a regra normativa de sobretaxa para uso de berço superior a 48 horas."""
        rg = self.tarifas[porto]["regras_gerais"]
        if horas <= 48:
            return comprimento * horas * rg["t2_atracacao_normal"]
        
        custo_base = comprimento * 48 * rg["t2_atracacao_normal"]
        horas_extras = horas - 48
        custo_extra = comprimento * horas_extras * rg["t2_atracacao_multa"]
        return custo_base + custo_extra

    def processar_orcamento(self, req: Dict[str, Any]) -> Dict[str, float]:
        """Processa o payload e retorna o extrato detalhado por Tabela Tarifária."""
        porto = req["porto"]
        nav = req["navegacao"]
        carga = req["carga"]
        
        rg = self.tarifas[porto]["regras_gerais"]
        rn = self.tarifas[porto][nav]
        
        # TABELA I - Acesso Aquaviário e Fundeio
        # Isenção/Redução de TPB baseada na navegação (exemplo regulatório para Apoio Marítimo < 5000 DWT)
        taxa_tpb = 0.0 if (nav == "Apoio Marítimo" and req["tpb"] < 5000) else rn["t1_tpb"]
        c_acesso = rn["t1_fixa"] + (req["tpb"] * taxa_tpb)
        
        c_fundeio = 0.0
        if req["dias_fundeio"] > 0:
            chave_fundeio = "fundeio_operando" if req["fundeio_operacao"] else "fundeio_parado"
            c_fundeio = req["dias_fundeio"] * rg[chave_fundeio]
            
        # TABELA II - Atracação
        c_atracacao = self.calcular_atracacao(porto, req["comprimento"], req["horas"])
        
        # TABELA III - Operacional (Respeitando a unidade da carga selecionada)
        taxa_carga = rn["Carga"].get(carga, 0.0)
        c_operacional = req["movimentacao"] * taxa_carga
        
        # TABELA IV - Armazenagem
        c_armazem = 0.0
        if req["tipo_area"] == "Pátio Descoberto":
            c_armazem = req["area_m2"] * req["dias_armaz"] * rg["t4_patio"]
        elif req["tipo_area"] == "Armazém Coberto":
            c_armazem = req["area_m2"] * req["dias_armaz"] * rg["t4_armazem"]
            
        # TABELA V - Equipamentos
        c_equip = (req["qtd_pesagens"] * rg["t5_balanca"]) + (req["horas_guindaste"] * rg["t5_guindaste"])
        
        # TABELAS VII e VIII - Utilidades e Diversos
        c_agua = req["volume_agua"] * rg["t7_agua"]
        c_limpeza = rg["t8_limpeza"] if req["usar_limpeza"] else 0.0
        c_isps = (req["movimentacao"] * rg["t8_isps"]) if req["usar_isps"] else 0.0

        return {
            "Tab_I_Acesso": c_acesso,
            "Tab_I_Fundeio": c_fundeio,
            "Tab_II_Atracacao": c_atracacao,
            "Tab_III_Operacional": c_operacional,
            "Tab_IV_Armazenagem": c_armazem,
            "Tab_V_Equipamentos": c_equip,
            "Tab_VII_Agua": c_agua,
            "Tab_VIII_Diversos": c_limpeza + c_isps,
            "TOTAL_GERAL": sum([c_acesso, c_fundeio, c_atracacao, c_operacional, c_armazem, c_equip, c_agua, c_limpeza, c_isps])
        }

# ==========================================
# CAMADA DE APRESENTAÇÃO (STREAMLIT UI)
# ==========================================

st.set_page_config(page_title="ERP Portuário CDP", layout="wide", page_icon="⚓")

st.title("⚓ Engine de Faturamento Portuário (CDP)")
st.markdown("Sistema parametrizado com as diretrizes da ANTAQ e DIREXE para as bacias portuárias do Pará.")

engine = MotorTarifarioCDP()

# --- BARRA LATERAL (PARÂMETROS FIXOS DA OPERAÇÃO) ---
with st.sidebar:
    st.header("⚙️ Escopo da Operação")
    porto = st.selectbox("Complexo Portuário", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade de Navegação", [
        "Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Marítimo"
    ])
    carga = st.selectbox("Perfil da Carga (Tabela III)", [
        "Granel Sólido", "Granel Líquido", "Carga Geral", "Contêiner Cheio", "Contêiner Vazio"
    ])
    
    st.divider()
    if st.button("Limpar Formulário", use_container_width=True):
        st.rerun()

# --- ÁREA PRINCIPAL (FORMULÁRIOS DIVIDIDOS EM ABAS) ---
tab1, tab2, tab3 = st.tabs(["🚢 Tabela I e II (Embarcação e Berço)", "⚖️ Tabela III (Movimentação)", "🏗️ Tabela IV a VIII (Infraestrutura e Serviços)"])

with tab1:
    st.subheader("Dados da Embarcação e Tempo de Berço")
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("TPB / DWT do Navio", min_value=0, value=15000, step=1000)
    comprimento = c2.number_input("Comprimento Linear (m)", min_value=0.0, value=120.0, step=5.0)
    horas = c3.number_input("Horas de Atracação", min_value=0, value=48, help="Penalidade automática aplicada após 48h.")
    
    st.subheader("Fundeio (Espera ao Largo)")
    c4, c5 = st.columns(2)
    dias_fundeio = c4.number_input("Dias em Fundeio", min_value=0, value=0, step=1)
    fundeio_operacao = c5.checkbox("Realizou operação comercial durante o fundeio?", value=False)

with tab2:
    st.subheader("Volume de Operação")
    # Lógica de UX: Muda o rótulo dependendo do tipo de carga escolhido na sidebar
    lbl_unidade = "Unidades (TEU/Caixas)" if "Contêiner" in carga else "Toneladas"
    movimentacao = st.number_input(f"Quantidade a Movimentar ({lbl_unidade})", min_value=0, value=5000, step=100)

with tab3:
    st.subheader("Utilização de Infraestrutura e Serviços Acessórios")
    c6, c7, c8 = st.columns(3)
    
    with c6:
        tipo_area = st.radio("Armazenagem (Tabela IV)", ["Nenhuma", "Pátio Descoberto", "Armazém Coberto"])
        area_m2 = st.number_input("Área (m²)", min_value=0, value=0, step=100, disabled=(tipo_area=="Nenhuma"))
        dias_armaz = st.number_input("Dias Armazenado", min_value=0, value=0, step=1, disabled=(tipo_area=="Nenhuma"))
        
    with c7:
        st.markdown("**Equipamentos (Tabela V)**")
        qtd_pesagens = st.number_input("Qtd. de Pesagens (Balança)", min_value=0, value=0, step=10)
        horas_guindaste = st.number_input("Horas de Guindaste/Empilhadeira", min_value=0, value=0, step=1)
        
    with c8:
        st.markdown("**Utilidades e Diversos (Tab VII e VIII)**")
        volume_agua = st.number_input("Fornecimento de Água (m³)", min_value=0, value=0, step=10)
        usar_limpeza = st.checkbox("Incluir Taxa de Limpeza de Berço", value=False)
        usar_isps = st.checkbox("Aplicar Taxa de Segurança (ISPS Code)", value=True)

st.divider()

# --- PROCESSAMENTO E EXIBIÇÃO ---
if st.button("PROCESSAR FATURAMENTO", type="primary", use_container_width=True):
    
    # Montagem do DTO (Data Transfer Object)
    payload = {
        "porto": porto, "navegacao": navegacao, "carga": carga,
        "tpb": tpb, "comprimento": comprimento, "horas": horas,
        "dias_fundeio": dias_fundeio, "fundeio_operacao": fundeio_operacao,
        "movimentacao": movimentacao, 
        "tipo_area": tipo_area, "area_m2": area_m2, "dias_armaz": dias_armaz, 
        "qtd_pesagens": qtd_pesagens, "horas_guindaste": horas_guindaste,
        "volume_agua": volume_agua, "usar_limpeza": usar_limpeza, "usar_isps": usar_isps
    }
    
    # Invocação do Motor Tarifário
    res = engine.processar_orcamento(payload)
    
    # Área de Resultados
    st.success(f"## Faturamento Total Estimado: R$ {res['TOTAL_GERAL']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Dashboards e Alertas de Compliance
    if horas > 48:
        st.warning(f"⚠️ **Regra de Compliance:** Aplicada sobretaxa na Tabela II devido à ocupação do berço por {horas} horas (limite normativo de 48h).")
    if navegacao == "Apoio Marítimo" and tpb < 5000:
        st.info("ℹ️ **Isenção/Redução Aplicada:** Embarcação de Apoio Marítimo teve ajuste na base de cálculo de Acesso Aquaviário.")
        
    st.markdown("---")
    st.markdown("### Espelho de Conferência (Auditoria)")
    
    # Renderização da Tabela de Resultados
    st.markdown(f"""
    | Referência Normativa | Descrição Comercial | Valor Apurado (R$) |
    | :--- | :--- | :--- |
    | **Tabela I** | Acesso Aquaviário | {res['Tab_I_Acesso']:,.2f} |
    | **Tabela I** | Taxa de Fundeio | {res['Tab_I_Fundeio']:,.2f} |
    | **Tabela II** | Atracação de Berço | {res['Tab_II_Atracacao']:,.2f} |
    | **Tabela III** | Infraestrutura Operacional ({carga}) | {res['Tab_III_Operacional']:,.2f} |
    | **Tabela IV** | Armazenagem ({tipo_area}) | {res['Tab_IV_Armazenagem']:,.2f} |
    | **Tabela V** | Uso de Equipamentos | {res['Tab_V_Equipamentos']:,.2f} |
    | **Tabela VII** | Fornecimento de Água | {res['Tab_VII_Agua']:,.2f} |
    | **Tabela VIII**| Serviços Diversos / Segurança ISPS | {res['Tab_VIII_Diversos']:,.2f} |
    """.replace(",", "X").replace(".", ",").replace("X", "."))