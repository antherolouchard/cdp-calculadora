import streamlit as st
from typing import Dict, Any

# ==========================================
# CAMADA DE UTILITÁRIOS
# ==========================================
def format_br(valor: float) -> str:
    """Formata float para o padrão monetário (ex: 1.234,56)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================
# CAMADA DE NEGÓCIOS (DOMÍNIO)
# ==========================================
class MotorTarifarioCDP:
    """
    Motor central de processamento das tarifas portuárias da CDP.
    Matriz alimentada rigorosamente com base nas Deliberações DIREXE 06, 07 e 08/2025.
    """
    def __init__(self):
        self.tarifas = {
            "Vila do Conde": {
                "regras_gerais": {
                    "t1_fundeio_operando": 4417.09,
                    "t1_fundeio_parado": 3155.42,
                    "t2_atracacao_metro_dia": 0.59,  
                    "t2_atracacao_multa_48h": 0.57,  
                    "t4_armazenagem_patio": 0.00,    
                    "t4_armazenagem_armazem": 0.00,  
                    "t5_uso_balanca": 0.00,        
                    "t7_fornecimento_agua_m3": 15.49,    
                    "t8_taxa_limpeza_berco": 0.00,    
                    "t8_taxa_isps_code": 0.00       
                },
                "Longo Curso": {
                    "t1_fixa_acesso": 2261.95,          
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 2.56, "t3_operacional": 6.02},       
                        "Granel Líquido": {"t1_tpb": 2.30, "t3_operacional": 8.11},      
                        "Carga Geral": {"t1_tpb": 1.15, "t3_operacional": 4.91},         
                        "Contêiner Cheio": {"t1_tpb": 0.48, "t3_operacional": 73.50},     
                        "Contêiner Vazio": {"t1_tpb": 0.48, "t3_operacional": 36.74}      
                    }
                },
                "Cabotagem": {
                    "t1_fixa_acesso": 2261.95,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 1.16, "t3_operacional": 6.02}, 
                        "Granel Líquido": {"t1_tpb": 2.30, "t3_operacional": 8.11}, 
                        "Carga Geral": {"t1_tpb": 1.15, "t3_operacional": 4.91}, 
                        "Contêiner Cheio": {"t1_tpb": 0.48, "t3_operacional": 73.50}, 
                        "Contêiner Vazio": {"t1_tpb": 0.48, "t3_operacional": 36.74}
                    }
                },
                "Navegação Interior": {
                    "t1_fixa_acesso": 0.00,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.00, "t3_operacional": 0.00}
                    }
                },
                "Apoio Marítimo": {
                    "t1_fixa_acesso": 0.00,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.00, "t3_operacional": 0.00}
                    }
                }
            },
            "Belém": {
                "regras_gerais": {
                    "t1_fundeio_operando": 4417.09,
                    "t1_fundeio_parado": 3155.42,
                    "t2_atracacao_metro_dia": 0.00,  
                    "t2_atracacao_multa_48h": 0.00,  
                    "t4_armazenagem_patio": 0.00,    
                    "t4_armazenagem_armazem": 0.00,  
                    "t5_uso_balanca": 0.00,        
                    "t7_fornecimento_agua_m3": 15.49,    
                    "t8_taxa_limpeza_berco": 0.00,    
                    "t8_taxa_isps_code": 0.00       
                },
                "Longo Curso": {
                    "t1_fixa_acesso": 628.32,          
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 1.14, "t3_operacional": 0.00},       
                        "Granel Líquido": {"t1_tpb": 0.60, "t3_operacional": 0.00},      
                        "Carga Geral": {"t1_tpb": 0.23, "t3_operacional": 0.00},         
                        "Contêiner Cheio": {"t1_tpb": 0.80, "t3_operacional": 0.00},     
                        "Contêiner Vazio": {"t1_tpb": 0.80, "t3_operacional": 0.00}      
                    }
                },
                "Cabotagem": {
                    "t1_fixa_acesso": 628.32,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 0.52, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.60, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 0.23, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.80, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.80, "t3_operacional": 0.00}
                    }
                },
                "Navegação Interior": {
                    "t1_fixa_acesso": 0.00,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.00, "t3_operacional": 0.00}
                    }
                },
                "Apoio Marítimo": {
                    "t1_fixa_acesso": 0.00,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.00, "t3_operacional": 0.00}
                    }
                }
            },
            "Santarém": {
                "regras_gerais": {
                    "t1_fundeio_operando": 4417.09,
                    "t1_fundeio_parado": 3155.42,
                    "t2_atracacao_metro_dia": 0.59,  
                    "t2_atracacao_multa_48h": 0.00,  
                    "t4_armazenagem_patio": 0.00,    
                    "t4_armazenagem_armazem": 0.00,  
                    "t5_uso_balanca": 0.00,        
                    "t7_fornecimento_agua_m3": 15.49,    
                    "t8_taxa_limpeza_berco": 0.00,    
                    "t8_taxa_isps_code": 0.00       
                },
                "Longo Curso": {
                    "t1_fixa_acesso": 359.04,          
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 3.41, "t3_operacional": 0.00},       
                        "Granel Líquido": {"t1_tpb": 2.19, "t3_operacional": 0.00},      
                        "Carga Geral": {"t1_tpb": 0.17, "t3_operacional": 0.00},         
                        "Contêiner Cheio": {"t1_tpb": 0.16, "t3_operacional": 0.00},     
                        "Contêiner Vazio": {"t1_tpb": 0.16, "t3_operacional": 0.00}      
                    }
                },
                "Cabotagem": {
                    "t1_fixa_acesso": 359.04,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 3.58, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.22, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 1.15, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.22, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.22, "t3_operacional": 0.00}
                    }
                },
                "Navegação Interior": {
                    "t1_fixa_acesso": 0.00,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.00, "t3_operacional": 0.00}
                    }
                },
                "Apoio Marítimo": {
                    "t1_fixa_acesso": 0.00,
                    "Carga": {
                        "Granel Sólido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Granel Líquido": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Carga Geral": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Cheio": {"t1_tpb": 0.00, "t3_operacional": 0.00}, 
                        "Contêiner Vazio": {"t1_tpb": 0.00, "t3_operacional": 0.00}
                    }
                }
            }
        }

    def processar_orcamento(self, req: Dict[str, Any]) -> Dict[str, Any]:
        porto, nav, carga = req["porto"], req["navegacao"], req["carga"]
        rg = self.tarifas[porto]["regras_gerais"]
        rn = self.tarifas[porto][nav]
        
        extrato = {}
        
        taxas_carga = rn["Carga"].get(carga, {"t1_tpb": 0.00, "t3_operacional": 0.00})
        
        # TABELA I - Acesso Aquaviário
        taxa_tpb = taxas_carga["t1_tpb"]
        val_acesso = rn["t1_fixa_acesso"] + (req["tpb"] * taxa_tpb)
        mem_acesso = f"Fixo R$ {format_br(rn['t1_fixa_acesso'])} + ({req['tpb']} TPB x R$ {format_br(taxa_tpb)})"
        extrato["Tab_I_Acesso"] = {"valor": val_acesso, "memoria": mem_acesso}
        
        # TABELA I - Fundeio
        if req["dias_fundeio"] > 0:
            chave_fundeio = "t1_fundeio_operando" if req["fundeio_operacao"] else "t1_fundeio_parado"
            val_fundeio = req["dias_fundeio"] * rg[chave_fundeio]
            extrato["Tab_I_Fundeio"] = {"valor": val_fundeio, "memoria": f"{req['dias_fundeio']} dias x R$ {format_br(rg[chave_fundeio])}"}
        else:
            extrato["Tab_I_Fundeio"] = {"valor": 0.0, "memoria": "Sem registo de fundeio"}
            
        # TABELA II - Atracação 
        if req["horas"] > 0:
            val_atracacao = req["comprimento"] * req["horas"] * rg["t2_atracacao_metro_dia"]
            mem_atrac = f"[{format_br(req['comprimento'])}m x {req['horas']}h x R$ {format_br(rg['t2_atracacao_metro_dia'])}]"
            extrato["Tab_II_Atracacao"] = {"valor": val_atracacao, "memoria": mem_atrac}
        else:
            extrato["Tab_II_Atracacao"] = {"valor": 0.0, "memoria": "Sem atracação"}
        
        # TABELA III - Operacional Terrestre
        taxa_op = taxas_carga["t3_operacional"]
        val_operacional = req["movimentacao"] * taxa_op
        unidade_lbl = "Unidades" if "Contêiner" in carga else "Ton"
        extrato["Tab_III_Operacional"] = {"valor": val_operacional, "memoria": f"{req['movimentacao']} {unidade_lbl} x R$ {format_br(taxa_op)}"}
        
        # TABELA IV - Armazenagem
        if req["tipo_area"] != "Nenhuma" and req["area_m2"] > 0 and req["dias_armaz"] > 0:
            taxa_armaz = rg["t4_armazenagem_patio"] if req["tipo_area"] == "Pátio Descoberto" else rg["t4_armazenagem_armazem"]
            val_armaz = req["area_m2"] * req["dias_armaz"] * taxa_armaz
            extrato["Tab_IV_Armazenagem"] = {"valor": val_armaz, "memoria": f"{req['area_m2']}m² x {req['dias_armaz']} dias x R$ {format_br(taxa_armaz)}"}
        else:
            extrato["Tab_IV_Armazenagem"] = {"valor": 0.0, "memoria": "Sem movimentação de área"}
            
        # TABELA V - Equipamentos
        val_equip = (req["qtd_pesagens"] * rg["t5_uso_balanca"])
        mem_equip = f"({req['qtd_pesagens']} pesagens x R$ {format_br(rg['t5_uso_balanca'])})" if req["qtd_pesagens"] > 0 else "Sem requisição"
        extrato["Tab_V_Equipamentos"] = {"valor": val_equip, "memoria": mem_equip}
        
        # TABELA VII - Água
        val_agua = req["volume_agua"] * rg["t7_fornecimento_agua_m3"]
        extrato["Tab_VII_Agua"] = {"valor": val_agua, "memoria": f"{req['volume_agua']}m³ x R$ {format_br(rg['t7_fornecimento_agua_m3'])}" if req["volume_agua"] > 0 else "Sem fornecimento"}
        
        # TABELA VIII - Diversos e ISPS
        val_limpeza = rg["t8_taxa_limpeza_berco"] if req["usar_limpeza"] else 0.0
        val_isps = (req["movimentacao"] * rg["t8_taxa_isps_code"]) if req["usar_isps"] else 0.0
        
        mem_div_parts = []
        if req["usar_limpeza"]: mem_div_parts.append(f"Limpeza (R$ {format_br(rg['t8_taxa_limpeza_berco'])})")
        if req["usar_isps"]: mem_div_parts.append(f"ISPS ({req['movimentacao']} {unidade_lbl} x R$ {format_br(rg['t8_taxa_isps_code'])})")
        
        mem_div = " + ".join(mem_div_parts) if mem_div_parts else "Nenhuma taxa diversa aplicável"
        extrato["Tab_VIII_Diversos"] = {"valor": val_limpeza + val_isps, "memoria": mem_div}

        extrato["TOTAL_GERAL"] = sum(item["valor"] for item in extrato.values() if isinstance(item, dict))
        
        return extrato

# ==========================================
# CAMADA DE APRESENTAÇÃO (STREAMLIT UI)
# ==========================================
st.set_page_config(page_title="Validador Tarifário CDP", layout="wide", page_icon="⚓")
st.title("⚓ Validador de Tarifas Portuárias (CDP)")
st.markdown("Sistema sincronizado estritamente com os normativos **DIREXE 06, 07 e 08/2025** da Companhia Docas do Pará.")

engine = MotorTarifarioCDP()

with st.sidebar:
    st.header("⚙️ Escopo da Operação")
    porto = st.selectbox("Complexo Portuário", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade de Navegação", ["Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Marítimo"])
    carga = st.selectbox("Perfil da Carga (Tabela III)", ["Granel Sólido", "Granel Líquido", "Carga Geral", "Contêiner Cheio", "Contêiner Vazio"])
    
    st.divider()
    if st.button("Nova Simulação", use_container_width=True):
        st.rerun()

tab1, tab2, tab3 = st.tabs(["🚢 Embarcação", "⚖️ Movimentação", "🏗️ Infraestrutura Acessória"])

with tab1:
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("Porte Bruto (TPB/DWT)", min_value=0, value=0, step=1000)
    comprimento = c2.number_input("Metragem Linear (m)", min_value=0.0, value=0.0, step=10.0)
    horas = c3.number_input("Permanência (Horas)", min_value=0, value=0, step=1)
    
    c4, c5 = st.columns(2)
    dias_fundeio = c4.number_input("Dias ao Largo (Fundeio)", min_value=0, value=0, step=1)
    fundeio_operacao = c5.checkbox("Operação comercial realizada no fundeio?", value=False)

with tab2:
    lbl_unidade = "Unidades (TEU/Caixas)" if "Contêiner" in carga else "Toneladas"
    movimentacao = st.number_input(f"Volume Descarregado/Carregado ({lbl_unidade})", min_value=0, value=0, step=100)

with tab3:
    c6, c7, c8 = st.columns(3)
    with c6:
        tipo_area = st.radio("Área de Armazenagem", ["Nenhuma", "Pátio Descoberto", "Armazém Coberto"])
        area_m2 = st.number_input("Área Ocupada (m²)", min_value=0, value=0, step=100, disabled=(tipo_area=="Nenhuma"))
        dias_armaz = st.number_input("Período (Dias)", min_value=0, value=0, step=1, disabled=(tipo_area=="Nenhuma"))
    with c7:
        qtd_pesagens = st.number_input("Serviço de Balança (Qtd)", min_value=0, value=0, step=1)
    with c8:
        volume_agua = st.number_input("Demanda de Água (m³)", min_value=0, value=0, step=10)
        usar_limpeza = st.checkbox("Incidência de Limpeza", value=False)
        usar_isps = st.checkbox("Incidência de ISPS Code", value=False)

st.divider()

if st.button("PROCESSAR INCIDÊNCIA TARIFÁRIA", type="primary", use_container_width=True):
    
    payload = {
        "porto": porto, "navegacao": navegacao, "carga": carga,
        "tpb": tpb, "comprimento": comprimento, "horas": horas,
        "dias_fundeio": dias_fundeio, "fundeio_operacao": fundeio_operacao,
        "movimentacao": movimentacao, 
        "tipo_area": tipo_area, "area_m2": area_m2, "dias_armaz": dias_armaz, 
        "qtd_pesagens": qtd_pesagens, "volume_agua": volume_agua, 
        "usar_limpeza": usar_limpeza, "usar_isps": usar_isps
    }
    
    res = engine.processar_orcamento(payload)
    
    st.success(f"## Faturamento Apurado: R$ {format_br(res['TOTAL_GERAL'])}")
    
    st.markdown("### Espelho Contábil e Memória de Cálculo Oficial")
    
    st.markdown(f"""
    | Base Normativa | Grupo de Incidência | Valor Consolidado (R$) | Trilha de Auditoria (Cálculo) |
    | :--- | :--- | :--- | :--- |
    | **Tabela I** | Acesso Aquaviário | {format_br(res['Tab_I_Acesso']['valor'])} | `{res['Tab_I_Acesso']['memoria']}` |
    | **Tabela I** | Fila / Fundeio | {format_br(res['Tab_I_Fundeio']['valor'])} | `{res['Tab_I_Fundeio']['memoria']}` |
    | **Tabela II** | Instalação de Acostagem | {format_br(res['Tab_II_Atracacao']['valor'])} | `{res['Tab_II_Atracacao']['memoria']}` |
    | **Tabela III** | Infraestrutura Terrestre | {format_br(res['Tab_III_Operacional']['valor'])} | `{res['Tab_III_Operacional']['memoria']}` |
    | **Tabela IV** | Movimentação / Área | {format_br(res['Tab_IV_Armazenagem']['valor'])} | `{res['Tab_IV_Armazenagem']['memoria']}` |
    | **Tabela V** | Uso de Equipamentos | {format_br(res['Tab_V_Equipamentos']['valor'])} | `{res['Tab_V_Equipamentos']['memoria']}` |
    | **Tabela VII** | Uso Temporário (Água) | {format_br(res['Tab_VII_Agua']['valor'])} | `{res['Tab_VII_Agua']['memoria']}` |
    | **Tabela VIII**| Serviços Diversos | {format_br(res['Tab_VIII_Diversos']['valor'])} | `{res['Tab_VIII_Diversos']['memoria']}` |
    """)