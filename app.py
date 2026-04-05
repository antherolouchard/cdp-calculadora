import streamlit as st
from typing import Dict, Any

# ==========================================
# CAMADA DE UTILIDADES
# ==========================================
def format_br(valor: float) -> str:
    """Formata float para o padrão monetário brasileiro (ex: 1.234,56)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================
# CAMADA DE NEGÓCIOS (DOMÍNIO)
# ==========================================
class MotorTarifarioCDP:
    """
    Motor central de processamento das tarifas portuárias da CDP.
    Retorna o valor apurado e a respectiva memória de cálculo.
    """
    def __init__(self):
        # Matriz Tarifária Completa (Valores referenciais das deliberações)
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

    def calcular_atracacao(self, rg: Dict, comprimento: float, horas: int) -> Dict:
        """Aplica a regra normativa de sobretaxa para uso de berço e gera a memória."""
        if horas == 0:
            return {"valor": 0.0, "memoria": "Sem atracação"}
            
        if horas <= 48:
            valor = comprimento * horas * rg["t2_atracacao_normal"]
            memoria = f"[{format_br(comprimento)}m x {horas}h x R$ {format_br(rg['t2_atracacao_normal'])}]"
            return {"valor": valor, "memoria": memoria}
        
        # Multa por ultrapassar 48h
        custo_base = comprimento * 48 * rg["t2_atracacao_normal"]
        horas_extras = horas - 48
        custo_extra = comprimento * horas_extras * rg["t2_atracacao_multa"]
        
        memoria_base = f"[{format_br(comprimento)}m x 48h x R$ {format_br(rg['t2_atracacao_normal'])}]"
        memoria_extra = f" + [{format_br(comprimento)}m x {horas_extras}h x R$ {format_br(rg['t2_atracacao_multa'])} (Excedente)]"
        
        return {"valor": custo_base + custo_extra, "memoria": memoria_base + memoria_extra}

    def processar_orcamento(self, req: Dict[str, Any]) -> Dict[str, Any]:
        porto, nav, carga = req["porto"], req["navegacao"], req["carga"]
        rg = self.tarifas[porto]["regras_gerais"]
        rn = self.tarifas[porto][nav]
        
        # Extrato final armazenará dicts com 'valor' e 'memoria'
        extrato = {}
        
        # TABELA I - Acesso Aquaviário
        taxa_tpb = 0.0 if (nav == "Apoio Marítimo" and req["tpb"] < 5000) else rn["t1_tpb"]
        val_acesso = rn["t1_fixa"] + (req["tpb"] * taxa_tpb)
        mem_acesso = f"Fixo R$ {format_br(rn['t1_fixa'])} + ({req['tpb']} TPB x R$ {format_br(taxa_tpb)})"
        if taxa_tpb == 0.0: mem_acesso += " *[Isenção de TPB Aplicada]*"
        extrato["Tab_I_Acesso"] = {"valor": val_acesso, "memoria": mem_acesso}
        
        # TABELA I - Fundeio
        if req["dias_fundeio"] > 0:
            chave_fundeio = "fundeio_operando" if req["fundeio_operacao"] else "fundeio_parado"
            val_fundeio = req["dias_fundeio"] * rg[chave_fundeio]
            extrato["Tab_I_Fundeio"] = {"valor": val_fundeio, "memoria": f"{req['dias_fundeio']} dias x R$ {format_br(rg[chave_fundeio])}"}
        else:
            extrato["Tab_I_Fundeio"] = {"valor": 0.0, "memoria": "Sem registro de fundeio"}
            
        # TABELA II - Atracação
        extrato["Tab_II_Atracacao"] = self.calcular_atracacao(rg, req["comprimento"], req["horas"])
        
        # TABELA III - Operacional
        taxa_carga = rn["Carga"].get(carga, 0.0)
        val_operacional = req["movimentacao"] * taxa_carga
        unidade_lbl = "Unidades" if "Contêiner" in carga else "Ton"
        extrato["Tab_III_Operacional"] = {"valor": val_operacional, "memoria": f"{req['movimentacao']} {unidade_lbl} x R$ {format_br(taxa_carga)}"}
        
        # TABELA IV - Armazenagem
        if req["tipo_area"] != "Nenhuma" and req["area_m2"] > 0 and req["dias_armaz"] > 0:
            taxa_armaz = rg["t4_patio"] if req["tipo_area"] == "Pátio Descoberto" else rg["t4_armazem"]
            val_armaz = req["area_m2"] * req["dias_armaz"] * taxa_armaz
            extrato["Tab_IV_Armazenagem"] = {"valor": val_armaz, "memoria": f"{req['area_m2']}m² x {req['dias_armaz']} dias x R$ {format_br(taxa_armaz)}"}
        else:
            extrato["Tab_IV_Armazenagem"] = {"valor": 0.0, "memoria": "Sem movimentação de área"}
            
        # TABELA V - Equipamentos
        val_equip = (req["qtd_pesagens"] * rg["t5_balanca"]) + (req["horas_guindaste"] * rg["t5_guindaste"])
        mem_equip_parts = []
        if req["qtd_pesagens"] > 0: mem_equip_parts.append(f"({req['qtd_pesagens']} pesagens x R$ {format_br(rg['t5_balanca'])})")
        if req["horas_guindaste"] > 0: mem_equip_parts.append(f"({req['horas_guindaste']}h guindaste x R$ {format_br(rg['t5_guindaste'])})")
        mem_equip = " + ".join(mem_equip_parts) if mem_equip_parts else "Sem requisição de equipamentos"
        extrato["Tab_V_Equipamentos"] = {"valor": val_equip, "memoria": mem_equip}
        
        # TABELA VII - Água
        val_agua = req["volume_agua"] * rg["t7_agua"]
        extrato["Tab_VII_Agua"] = {"valor": val_agua, "memoria": f"{req['volume_agua']}m³ x R$ {format_br(rg['t7_agua'])}" if req["volume_agua"] > 0 else "Sem fornecimento"}
        
        # TABELA VIII - Diversos e ISPS
        val_limpeza = rg["t8_limpeza"] if req["usar_limpeza"] else 0.0
        val_isps = (req["movimentacao"] * rg["t8_isps"]) if req["usar_isps"] else 0.0
        mem_div_parts = []
        if req["usar_limpeza"]: mem_div_parts.append(f"Limpeza (Fixo R$ {format_br(rg['t8_limpeza'])})")
        if req["usar_isps"]: mem_div_parts.append(f"ISPS ({req['movimentacao']} {unidade_lbl} x R$ {format_br(rg['t8_isps'])})")
        mem_div = " + ".join(mem_div_parts) if mem_div_parts else "Isento de taxas adicionais"
        extrato["Tab_VIII_Diversos"] = {"valor": val_limpeza + val_isps, "memoria": mem_div}

        # Calcula o Total Geral somando os valores dos dicionários internos
        extrato["TOTAL_GERAL"] = sum(item["valor"] for item in extrato.values() if isinstance(item, dict))
        
        return extrato

# ==========================================
# CAMADA DE APRESENTAÇÃO (STREAMLIT UI)
# ==========================================
st.set_page_config(page_title="ERP Portuário CDP", layout="wide", page_icon="⚓")
st.title("⚓ Engine de Faturamento Portuário (CDP)")
st.markdown("Sistema parametrizado com diretrizes da ANTAQ/DIREXE, incluindo geração de **Memória de Cálculo** auditável.")

engine = MotorTarifarioCDP()

with st.sidebar:
    st.header("⚙️ Escopo da Operação")
    porto = st.selectbox("Complexo Portuário", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade de Navegação", ["Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Marítimo"])
    carga = st.selectbox("Perfil da Carga (Tabela III)", ["Granel Sólido", "Granel Líquido", "Carga Geral", "Contêiner Cheio", "Contêiner Vazio"])
    
    st.divider()
    if st.button("Limpar Formulário", use_container_width=True):
        st.rerun()

tab1, tab2, tab3 = st.tabs(["🚢 Embarcação e Berço", "⚖️ Movimentação", "🏗️ Infraestrutura e Serviços"])

with tab1:
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("TPB / DWT", min_value=0, value=15000, step=1000)
    comprimento = c2.number_input("Comprimento Linear (m)", min_value=0.0, value=120.0, step=5.0)
    horas = c3.number_input("Horas de Atracação", min_value=0, value=48, help="Penalidade após 48h.")
    
    c4, c5 = st.columns(2)
    dias_fundeio = c4.number_input("Dias em Fundeio", min_value=0, value=0, step=1)
    fundeio_operacao = c5.checkbox("Operação comercial no fundeio?", value=False)

with tab2:
    lbl_unidade = "Unidades (TEU/Caixas)" if "Contêiner" in carga else "Toneladas"
    movimentacao = st.number_input(f"Quantidade a Movimentar ({lbl_unidade})", min_value=0, value=5000, step=100)

with tab3:
    c6, c7, c8 = st.columns(3)
    with c6:
        tipo_area = st.radio("Armazenagem (Tabela IV)", ["Nenhuma", "Pátio Descoberto", "Armazém Coberto"])
        area_m2 = st.number_input("Área (m²)", min_value=0, value=0, step=100, disabled=(tipo_area=="Nenhuma"))
        dias_armaz = st.number_input("Dias Armazenado", min_value=0, value=0, step=1, disabled=(tipo_area=="Nenhuma"))
    with c7:
        qtd_pesagens = st.number_input("Qtd. de Pesagens", min_value=0, value=0, step=10)
        horas_guindaste = st.number_input("Horas Guindaste", min_value=0, value=0, step=1)
    with c8:
        volume_agua = st.number_input("Fornecimento Água (m³)", min_value=0, value=0, step=10)
        usar_limpeza = st.checkbox("Incluir Limpeza de Berço", value=False)
        usar_isps = st.checkbox("Aplicar ISPS Code", value=True)

st.divider()

if st.button("PROCESSAR FATURAMENTO", type="primary", use_container_width=True):
    
    payload = {
        "porto": porto, "navegacao": navegacao, "carga": carga,
        "tpb": tpb, "comprimento": comprimento, "horas": horas,
        "dias_fundeio": dias_fundeio, "fundeio_operacao": fundeio_operacao,
        "movimentacao": movimentacao, 
        "tipo_area": tipo_area, "area_m2": area_m2, "dias_armaz": dias_armaz, 
        "qtd_pesagens": qtd_pesagens, "horas_guindaste": horas_guindaste,
        "volume_agua": volume_agua, "usar_limpeza": usar_limpeza, "usar_isps": usar_isps
    }
    
    res = engine.processar_orcamento(payload)
    
    st.success(f"## Faturamento Total Estimado: R$ {format_br(res['TOTAL_GERAL'])}")
    
    if horas > 48:
        st.warning(f"⚠️ **Regra de Compliance:** Aplicada sobretaxa na Tabela II devido à ocupação do berço por {horas} horas.")
        
    st.markdown("---")
    st.markdown("### Espelho de Conferência (Auditoria e Memória de Cálculo)")
    
    # Renderização da Tabela de Resultados incluindo a Memória de Cálculo
    st.markdown(f"""
    | Referência | Descrição Comercial | Valor Apurado (R$) | Memória de Cálculo (Fatores x Taxas) |
    | :--- | :--- | :--- | :--- |
    | **Tabela I** | Acesso Aquaviário | {format_br(res['Tab_I_Acesso']['valor'])} | `{res['Tab_I_Acesso']['memoria']}` |
    | **Tabela I** | Taxa de Fundeio | {format_br(res['Tab_I_Fundeio']['valor'])} | `{res['Tab_I_Fundeio']['memoria']}` |
    | **Tabela II** | Atracação de Berço | {format_br(res['Tab_II_Atracacao']['valor'])} | `{res['Tab_II_Atracacao']['memoria']}` |
    | **Tabela III** | Infraestrutura Operacional | {format_br(res['Tab_III_Operacional']['valor'])} | `{res['Tab_III_Operacional']['memoria']}` |
    | **Tabela IV** | Armazenagem ({tipo_area}) | {format_br(res['Tab_IV_Armazenagem']['valor'])} | `{res['Tab_IV_Armazenagem']['memoria']}` |
    | **Tabela V** | Uso de Equipamentos | {format_br(res['Tab_V_Equipamentos']['valor'])} | `{res['Tab_V_Equipamentos']['memoria']}` |
    | **Tabela VII** | Fornecimento de Água | {format_br(res['Tab_VII_Agua']['valor'])} | `{res['Tab_VII_Agua']['memoria']}` |
    | **Tabela VIII**| Serviços Diversos / ISPS | {format_br(res['Tab_VIII_Diversos']['valor'])} | `{res['Tab_VIII_Diversos']['memoria']}` |
    """)