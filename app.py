import streamlit as st
from dataclasses import dataclass
from typing import Dict, Any

# ==========================================
# CAMADA DE NEGÓCIOS (DOMÍNIO)
# ==========================================

class MotorTarifarioCDP:
    """
    Motor central de processamento das tarifas portuárias (DIREXE/2025).
    Desacoplado da interface visual para permitir uso futuro via APIs.
    """
    def __init__(self):
        # Base de Dados Relacional (Matriz Tarifária)
        # Nota do Desenvolvedor: Alimentar com os centavos exatos dos PDFs finais.
        self.tarifas = {
            "Vila do Conde": {
                "t2_atracacao_normal": 0.59, 
                "t2_atracacao_multa": 0.85, # Valor após 48h (exemplo referencial)
                "t4_patio": 2.10, "t4_armazem": 4.50,
                "t5_balanca": 55.00, "t7_agua": 22.00, "t8_isps": 0.35,
                "fundeio_operando": 4417.09, "fundeio_parado": 3155.42,
                
                "Longo Curso": {"t1_fixa": 628.32, "t1_tpb": 0.80, "Carga": {"Granel Sólido": 6.02, "Contêiner Cheio": 73.50, "Carga Geral": 4.91}},
                "Cabotagem": {"t1_fixa": 300.00, "t1_tpb": 0.40, "Carga": {"Granel Sólido": 4.50, "Contêiner Cheio": 50.00, "Carga Geral": 3.00}},
                "Navegação Interior": {"t1_fixa": 150.00, "t1_tpb": 0.15, "Carga": {"Granel Sólido": 2.00, "Contêiner Cheio": 25.00, "Carga Geral": 1.50}},
                "Apoio Marítimo": {"t1_fixa": 100.00, "t1_tpb": 0.10, "Carga": {"Granel Sólido": 0.00, "Contêiner Cheio": 0.00, "Carga Geral": 1.00}} # Geralmente movimentam insumos
            },
            "Belém": {
                "t2_atracacao_normal": 0.59, "t2_atracacao_multa": 0.85,
                "t4_patio": 1.50, "t4_armazem": 3.80,
                "t5_balanca": 55.00, "t7_agua": 18.50, "t8_isps": 0.35,
                "fundeio_operando": 4417.09, "fundeio_parado": 3155.42,
                
                "Longo Curso": {"t1_fixa": 628.32, "t1_tpb": 0.80, "Carga": {"Granel Sólido": 5.00, "Contêiner Cheio": 60.00, "Carga Geral": 4.88}},
                "Cabotagem": {"t1_fixa": 300.00, "t1_tpb": 0.40, "Carga": {"Granel Sólido": 3.00, "Contêiner Cheio": 40.00, "Carga Geral": 3.00}},
                "Navegação Interior": {"t1_fixa": 150.00, "t1_tpb": 0.15, "Carga": {"Granel Sólido": 1.80, "Contêiner Cheio": 20.00, "Carga Geral": 1.50}},
                "Apoio Marítimo": {"t1_fixa": 100.00, "t1_tpb": 0.10, "Carga": {"Granel Sólido": 0.00, "Contêiner Cheio": 0.00, "Carga Geral": 1.00}}
            },
            "Santarém": {
                "t2_atracacao_normal": 0.50, "t2_atracacao_multa": 0.75,
                "t4_patio": 1.20, "t4_armazem": 3.00,
                "t5_balanca": 45.00, "t7_agua": 15.00, "t8_isps": 0.25,
                "fundeio_operando": 3690.75, "fundeio_parado": 2636.55, # Valores variam em Santarém
                
                "Longo Curso": {"t1_fixa": 359.04, "t1_tpb": 0.16, "Carga": {"Granel Sólido": 4.00, "Contêiner Cheio": 50.00, "Carga Geral": 4.91}},
                "Cabotagem": {"t1_fixa": 200.00, "t1_tpb": 0.08, "Carga": {"Granel Sólido": 2.50, "Contêiner Cheio": 35.00, "Carga Geral": 3.00}},
                "Navegação Interior": {"t1_fixa": 100.00, "t1_tpb": 0.05, "Carga": {"Granel Sólido": 1.50, "Contêiner Cheio": 15.00, "Carga Geral": 1.50}},
                "Apoio Marítimo": {"t1_fixa": 80.00, "t1_tpb": 0.05, "Carga": {"Granel Sólido": 0.00, "Contêiner Cheio": 0.00, "Carga Geral": 1.00}}
            }
        }

    def calcular_atracacao(self, porto: str, comprimento: float, horas: int) -> float:
        """Calcula o berço aplicando regra de sobretaxa após 48 horas."""
        p = self.tarifas[porto]
        if horas <= 48:
            return comprimento * horas * p["t2_atracacao_normal"]
        else:
            custo_base = comprimento * 48 * p["t2_atracacao_normal"]
            horas_extras = horas - 48
            custo_extra = comprimento * horas_extras * p["t2_atracacao_multa"]
            return custo_base + custo_extra

    def processar_orcamento(self, req: Dict[str, Any]) -> Dict[str, float]:
        """Recebe o payload da UI e retorna o extrato financeiro processado."""
        porto = req["porto"]
        nav = req["navegacao"]
        
        p_geral = self.tarifas[porto]
        p_nav = self.tarifas[porto][nav]
        
        # 1. Acesso e Fundeio (Tabela I)
        # Isenção de TPB para Apoio Marítimo < 5000 DWT (Exemplo de regra de negócio)
        taxa_tpb = 0.0 if (nav == "Apoio Marítimo" and req["tpb"] < 5000) else p_nav["t1_tpb"]
        custo_acesso = p_nav["t1_fixa"] + (req["tpb"] * taxa_tpb)
        
        custo_fundeio = 0.0
        if req["dias_fundeio"] > 0:
            chave_fundeio = "fundeio_operando" if req["fundeio_operacao"] else "fundeio_parado"
            custo_fundeio = req["dias_fundeio"] * p_geral[chave_fundeio]
            
        # 2. Atracação (Tabela II)
        custo_atracacao = self.calcular_atracacao(porto, req["comprimento"], req["horas"])
        
        # 3. Operacional (Tabela III) - Pega o valor da carga de forma segura com .get()
        taxa_carga = p_nav["Carga"].get(req["carga"], 0.0)
        custo_operacional = req["movimentacao"] * taxa_carga
        
        # 4. Outros (IV a VIII)
        taxa_armazem = p_geral["t4_patio"] if req["tipo_area"] == "Pátio" else (p_geral["t4_armazem"] if req["tipo_area"] == "Armazém" else 0.0)
        custo_armazem = req["area"] * req["dias_armaz"] * taxa_armazem
        custo_isps = req["movimentacao"] * p_geral["t8_isps"] if req["usar_isps"] else 0.0

        return {
            "Acesso (Tabela I)": custo_acesso,
            "Fundeio (Tabela I)": custo_fundeio,
            "Atracação (Tabela II)": custo_atracacao,
            "Operação (Tabela III)": custo_operacional,
            "Armazenagem (Tabela IV)": custo_armazem,
            "Segurança ISPS (Tabela VIII)": custo_isps,
            "TOTAL": sum([custo_acesso, custo_fundeio, custo_atracacao, custo_operacional, custo_armazem, custo_isps])
        }

# ==========================================
# CAMADA DE APRESENTAÇÃO (STREAMLIT UI)
# ==========================================

st.set_page_config(page_title="ERP Portuário - Simulação", layout="wide", page_icon="⚓")
st.title("⚓ Engine de Faturamento Portuário (CDP)")
st.markdown("Protótipo de alta fidelidade com processamento de incidência por Bacia e Tipo de Apoio.")

engine = MotorTarifarioCDP()

with st.sidebar:
    st.header("⚙️ Parâmetros Principais")
    porto = st.selectbox("Porto Alfandegado", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade de Navegação", ["Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Marítimo"])
    carga = st.selectbox("Perfil de Carga", ["Granel Sólido", "Carga Geral", "Contêiner Cheio"])

tab1, tab2, tab3 = st.tabs(["🚢 Embarcação e Berço", "⚓ Fundeio e Operação", "🏗️ Infraestrutura"])

with tab1:
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("TPB / DWT", value=15000, step=1000)
    comprimento = c2.number_input("Comprimento Linear (m)", value=120.0, step=5.0)
    horas = c3.number_input("Horas de Berço", value=48, help="Acima de 48h aplica-se sobretaxa normativa.")

with tab2:
    c4, c5, c6 = st.columns(3)
    dias_fundeio = c4.number_input("Dias ao Largo (Fundeio)", value=0, min_value=0)
    fundeio_operacao = c5.checkbox("Fundeio com Operação Comercial", value=False)
    mov_label = "Unidades" if "Contêiner" in carga else "Toneladas"
    movimentacao = c6.number_input(f"Volume ({mov_label})", value=5000)

with tab3:
    c7, c8 = st.columns(2)
    tipo_area = c7.radio("Uso de Área", ["Nenhum", "Pátio", "Armazém"], horizontal=True)
    area = c7.number_input("Metragem (m²)", value=0, disabled=(tipo_area=="Nenhum"))
    dias_armaz = c8.number_input("Dias Armazenado", value=0, disabled=(tipo_area=="Nenhum"))
    usar_isps = c8.checkbox("Aplicar ISPS Code", value=True)

st.divider()

if st.button("Executar Motor de Cálculo", type="primary", use_container_width=True):
    # Montagem do Payload (Data Transfer Object)
    payload = {
        "porto": porto, "navegacao": navegacao, "carga": carga,
        "tpb": tpb, "comprimento": comprimento, "horas": horas,
        "dias_fundeio": dias_fundeio, "fundeio_operacao": fundeio_operacao,
        "movimentacao": movimentacao, "tipo_area": tipo_area, 
        "area": area, "dias_armaz": dias_armaz, "usar_isps": usar_isps
    }
    
    # Execução isolada das regras de negócio
    resultado = engine.processar_orcamento(payload)
    
    st.success(f"### Faturamento Projetado: R$ {resultado['TOTAL']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.markdown("#### Memória de Cálculo Auditável")
    for chave, valor in resultado.items():
        if chave != "TOTAL" and valor > 0:
            st.write(f"**{chave}:** R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    if horas > 48:
        st.warning("⚠️ **Aviso de Compliance:** Detectada incidência de sobretaxa por ocupação de berço superior a 48 horas.")
    if navegacao == "Apoio Marítimo" and tpb < 5000:
        st.info("ℹ️ **Isenção Aplicada:** Embarcação de Apoio Marítimo inferior a 5.000 DWT teve base de cálculo do TPB ajustada nas regras de acesso.")