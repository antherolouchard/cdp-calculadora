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
# A matriz abaixo foi expandida para contemplar TODAS as linhas das tabelas, 
# sem aglutinar categorias que possuem naturezas diferentes na ANTAQ.
# Valores marcados com 0.00 devem ser aferidos com os centavos exatos dos seus prints.

TARIFAS_CDP = {
    "Vila do Conde": {
        "Tabela_I_Fixo": {"Longo Curso": 2261.95, "Cabotagem": 2261.95, "Navegação Interior": 2261.95, "Apoio Portuário": 2261.95, "Apoio Marítimo": 2261.95},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 2.56, "Granel Líquido": 2.30, "Carga Geral": 1.15, "Contêiner Cheio": 0.48, "Contêiner Vazio": 0.48, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 1.16, "Granel Líquido": 2.30, "Carga Geral": 1.15, "Contêiner Cheio": 0.48, "Contêiner Vazio": 0.48, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.48},
            "Apoio Portuário": {"Toda Carga": 0.48},
            "Apoio Marítimo": {"Toda Carga": 0.48}
        },
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_Infra": {"Granel Sólido": 6.02, "Granel Líquido": 8.11, "Carga Geral": 4.91, "Contêiner Cheio": 73.50, "Contêiner Vazio": 36.74, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00},
        "Tabela_IV_Movimentacao": {"Granel Sólido": 6.02, "Granel Líquido": 8.11, "Carga Geral": 4.91, "Contêiner Cheio": 73.50, "Contêiner Vazio": 36.74, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00},
        "Tabela_V_Armazenagem": {"Ad_Valorem_1_Periodo": 0.005},
        "Tabela_VII_Diversos": {"Agua": 15.49},
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
    },
    "Belém": {
        "Tabela_I_Fixo": {"Longo Curso": 628.32, "Cabotagem": 628.32, "Navegação Interior": 628.32, "Apoio Portuário": 628.32, "Apoio Marítimo": 628.32},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 1.14, "Granel Líquido": 0.60, "Carga Geral": 0.23, "Contêiner Cheio": 0.80, "Contêiner Vazio": 0.80, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 0.52, "Granel Líquido": 0.60, "Carga Geral": 0.23, "Contêiner Cheio": 0.80, "Contêiner Vazio": 0.80, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.16},
            "Apoio Portuário": {"Toda Carga": 0.16},
            "Apoio Marítimo": {"Toda Carga": 0.16}
        },
        "Tabela_I_Fundeio": {"Operando": 4417.09, "Parado": 3155.42},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_Infra": {"Granel Sólido": 4.88, "Granel Líquido": 5.10, "Carga Geral": 4.60, "Contêiner Cheio": 60.00, "Contêiner Vazio": 30.00, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00},
        "Tabela_IV_Movimentacao": {"Granel Sólido": 4.88, "Granel Líquido": 5.10, "Carga Geral": 4.60, "Contêiner Cheio": 60.00, "Contêiner Vazio": 30.00, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00},
        "Tabela_V_Armazenagem": {"Ad_Valorem_1_Periodo": 0.005},
        "Tabela_VII_Diversos": {"Agua": 15.49},
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 14.46, "Nao Pavimentada": 11.53}
    },
    "Santarém": {
        "Tabela_I_Fixo": {"Longo Curso": 359.04, "Cabotagem": 359.04, "Navegação Interior": 359.04, "Apoio Portuário": 359.04, "Apoio Marítimo": 359.04},
        "Tabela_I_Var": {
            "Longo Curso": {"Granel Sólido": 3.41, "Granel Líquido": 2.19, "Carga Geral": 0.17, "Contêiner Cheio": 0.16, "Contêiner Vazio": 0.16, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00, "Nenhuma": 0.00},
            "Cabotagem": {"Granel Sólido": 3.58, "Granel Líquido": 0.22, "Carga Geral": 1.15, "Contêiner Cheio": 0.22, "Contêiner Vazio": 0.22, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00, "Nenhuma": 0.00},
            "Navegação Interior": {"Toda Carga": 0.10},
            "Apoio Portuário": {"Toda Carga": 0.10},
            "Apoio Marítimo": {"Toda Carga": 0.10}
        },
        "Tabela_I_Fundeio": {"Operando": 3690.75, "Parado": 2636.55},
        "Tabela_II_Acostagem": {"Longo Curso": 0.59, "Cabotagem": 0.59, "Navegação Interior": 0.59, "Apoio Portuário": 0.33, "Apoio Marítimo": 0.33},
        "Tabela_III_Infra": {"Granel Sólido": 4.91, "Granel Líquido": 4.91, "Carga Geral": 4.91, "Contêiner Cheio": 50.00, "Contêiner Vazio": 25.00, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00},
        "Tabela_IV_Movimentacao": {"Granel Sólido": 4.91, "Granel Líquido": 4.91, "Carga Geral": 4.91, "Contêiner Cheio": 50.00, "Contêiner Vazio": 25.00, "Veículos Roll-on/Roll-off": 0.00, "Animais até 1.000 kg": 0.00, "Animais acima de 1.000 kg": 0.00},
        "Tabela_V_Armazenagem": {"Ad_Valorem_1_Periodo": 0.005},
        "Tabela_VII_Diversos": {"Agua": 15.49},
        "Tabela_VIII_Uso_Temp": {"Pavimentada": 7.23, "Nao Pavimentada": 5.79}
    }
}

# ==========================================
# ENGINE DE NEGÓCIOS
# ==========================================
class MotorTarifarioCDP:
    def processar(self, req: Dict[str, Any]) -> Dict[str, Any]:
        porto_db = TARIFAS_CDP[req["porto"]]
        nav = req["navegacao"]
        carga = req["carga"]
        
        extrato = {}

        # ---------------------------------------------------------
        # TABELA I - Acesso Aquaviário e Fundeio
        # ---------------------------------------------------------
        taxa_fixa_t1 = porto_db["Tabela_I_Fixo"][nav]
        
        # O Acesso Variável depende se a navegação é de longo curso/cabotagem ou as demais
        if nav in ["Navegação Interior", "Apoio Portuário", "Apoio Marítimo"]:
            taxa_var_t1 = porto_db["Tabela_I_Var"][nav]["Toda Carga"]
        else:
            taxa_var_t1 = porto_db["Tabela_I_Var"][nav][carga]
            
        valor_t1_acesso = taxa_fixa_t1 + (req["tpb"] * taxa_var_t1)
        extrato["Tabela I - Acesso Aquaviário"] = {
            "valor": valor_t1_acesso,
            "mem": f"R$ {format_br(taxa_fixa_t1)} (Fixo) + [{format_br(req['tpb'])} TPB x R$ {format_br(taxa_var_t1)}]"
        }

        # Fundeio
        if req["dias_fundeio"] > 0:
            condicao_fundeio = "Operando" if req["fundeio_operando"] else "Parado"
            taxa_fundeio = porto_db["Tabela_I_Fundeio"][condicao_fundeio]
            extrato["Tabela I - Fundeio"] = {
                "valor": req["dias_fundeio"] * taxa_fundeio,
                "mem": f"{req['dias_fundeio']} dia(s) x R$ {format_br(taxa_fundeio)} ({condicao_fundeio})"
            }

        # ---------------------------------------------------------
        # TABELA II - Instalações de Acostagem
        # ---------------------------------------------------------
        if req["horas_atracacao"] > 0:
            taxa_t2 = porto_db["Tabela_II_Acostagem"][nav]
            valor_t2 = req["comprimento"] * req["horas_atracacao"] * taxa_t2
            extrato["Tabela II - Acostagem"] = {
                "valor": valor_t2,
                "mem": f"{format_br(req['comprimento'])}m x {req['horas_atracacao']}h x R$ {format_br(taxa_t2)}"
            }

        # ---------------------------------------------------------
        # TABELA III e IV - Infraestrutura Operacional e Movimentação
        # ---------------------------------------------------------
        if carga != "Nenhuma":
            # Tabela III
            if req["qtd_t3"] > 0:
                taxa_t3 = porto_db["Tabela_III_Infra"][carga]
                extrato["Tabela III - Infra. Operacional"] = {
                    "valor": req["qtd_t3"] * taxa_t3,
                    "mem": f"{format_br(req['qtd_t3'])} ({req['unidade_medida']}) x R$ {format_br(taxa_t3)}"
                }
            
            # Tabela IV
            if req["qtd_t4"] > 0:
                taxa_t4 = porto_db["Tabela_IV_Movimentacao"][carga]
                extrato["Tabela IV - Movimentação"] = {
                    "valor": req["qtd_t4"] * taxa_t4,
                    "mem": f"{format_br(req['qtd_t4'])} ({req['unidade_medida']}) x R$ {format_br(taxa_t4)}"
                }

        # ---------------------------------------------------------
        # TABELA V - Armazenagem (Ad Valorem)
        # ---------------------------------------------------------
        if req["valor_carga_declarado"] > 0:
            taxa_t5 = porto_db["Tabela_V_Armazenagem"]["Ad_Valorem_1_Periodo"]
            extrato["Tabela V - Armazenagem"] = {
                "valor": req["valor_carga_declarado"] * taxa_t5,
                "mem": f"R$ {format_br(req['valor_carga_declarado'])} x {taxa_t5*100}% (Ad Valorem)"
            }

        # ---------------------------------------------------------
        # TABELA VII - Serviços Diversos (Água)
        # ---------------------------------------------------------
        if req["volume_agua"] > 0:
            taxa_t7 = porto_db["Tabela_VII_Diversos"]["Agua"]
            extrato["Tabela VII - Fornecimento de Água"] = {
                "valor": req["volume_agua"] * taxa_t7,
                "mem": f"{format_br(req['volume_agua'])}m³ x R$ {format_br(taxa_t7)}"
            }

        # ---------------------------------------------------------
        # TABELA VIII - Uso Temporário
        # ---------------------------------------------------------
        if req["area_t8"] > 0:
            taxa_t8 = porto_db["Tabela_VIII_Uso_Temp"][req["tipo_piso"]]
            extrato["Tabela VIII - Uso Temporário"] = {
                "valor": req["area_t8"] * taxa_t8,
                "mem": f"{format_br(req['area_t8'])}m² x R$ {format_br(taxa_t8)} ({req['tipo_piso']})"
            }

        extrato["TOTAL_GERAL"] = sum(item["valor"] for item in extrato.values())
        return extrato

# ==========================================
# INTERFACE STREAMLIT FRONT-END
# ==========================================
st.set_page_config(page_title="Simulador CDP Avançado", layout="wide")
st.title("⚓ Motor de Faturamento CDP - DIREXE 2025")
st.markdown("Protótipo com cobertura exaustiva de naturezas de carga (Ro-Ro, Animais, etc).")

motor = MotorTarifarioCDP()

# Opções normativas extraídas das tabelas CDP
OPCOES_CARGA = [
    "Granel Sólido", "Granel Líquido", "Carga Geral", 
    "Contêiner Cheio", "Contêiner Vazio", 
    "Veículos Roll-on/Roll-off", 
    "Animais até 1.000 kg", "Animais acima de 1.000 kg", 
    "Nenhuma"
]

with st.sidebar:
    st.header("⚙️ Configuração Macro")
    porto = st.selectbox("Complexo Portuário", ["Vila do Conde", "Belém", "Santarém"])
    navegacao = st.selectbox("Modalidade de Navegação", [
        "Longo Curso", "Cabotagem", "Navegação Interior", "Apoio Portuário", "Apoio Marítimo"
    ])
    carga = st.selectbox("Natureza Específica da Carga", OPCOES_CARGA)
    
    st.divider()
    if st.button("Limpar Formulário", use_container_width=True):
        st.rerun()

# Inteligência de Interface: Define a unidade de medida correta visualmente e para o cálculo
if "Animais" in carga:
    unidade_medida = "Cabeças"
elif "Veículos" in carga or "Contêiner" in carga:
    unidade_medida = "Unidades"
elif carga == "Nenhuma":
    unidade_medida = "N/A"
else:
    unidade_medida = "Toneladas"

t1, t2, t3 = st.tabs(["🚢 Embarcação (I e II)", "📦 Carga (III, IV e V)", "🏗️ Utilidades (VII e VIII)"])

with t1:
    st.subheader("Base Operacional do Navio/Embarcação")
    c1, c2, c3 = st.columns(3)
    tpb = c1.number_input("TPB / DWT", min_value=0.0, value=15000.0)
    comprimento = c2.number_input("Comprimento Linear (m)", min_value=0.0, value=120.0)
    horas_atracacao = c3.number_input("Permanência no Berço (Horas)", min_value=0, value=48)
    
    st.subheader("Fundeio")
    c4, c5 = st.columns(2)
    dias_fundeio = c4.number_input("Total de Dias em Fundeio", min_value=0, value=0)
    fundeio_operando = c5.checkbox("Realizou operação comercial no fundeio?")

with t2:
    st.subheader(f"Movimentação ({unidade_medida})")
    c6, c7 = st.columns(2)
    
    # Os inputs adaptam seus rótulos baseados na carga selecionada!
    qtd_t3 = c6.number_input(f"Vol. Tabela III ({unidade_medida})", min_value=0.0, value=0.0, disabled=(carga=="Nenhuma"))
    qtd_t4 = c7.number_input(f"Vol. Tabela IV ({unidade_medida})", min_value=0.0, value=0.0, disabled=(carga=="Nenhuma"))
    
    st.subheader("Base Ad Valorem (Tabela V)")
    valor_carga_declarado = st.number_input("Valor Comercial Declarado da Carga (R$)", min_value=0.0, value=0.0)

with t3:
    st.subheader("Tabela VII - Serviços Padronizados")
    volume_agua = st.number_input("Fornecimento de Água (m³)", min_value=0.0, value=0.0)
    
    st.subheader("Tabela VIII - Uso Temporário")
    c8, c9 = st.columns(2)
    area_t8 = c8.number_input("Metragem de Área (m²)", min_value=0.0, value=0.0)
    tipo_piso = c9.radio("Pavimentação", ["Pavimentada", "Nao Pavimentada"], disabled=(area_t8==0.0))

st.divider()

if st.button("PROCESSAR INCIDÊNCIA", type="primary", use_container_width=True):
    payload = {
        "porto": porto, "navegacao": navegacao, "carga": carga,
        "tpb": tpb, "comprimento": comprimento, "horas_atracacao": horas_atracacao,
        "dias_fundeio": dias_fundeio, "fundeio_operando": fundeio_operando,
        "qtd_t3": qtd_t3, "qtd_t4": qtd_t4, "unidade_medida": unidade_medida,
        "valor_carga_declarado": valor_carga_declarado,
        "volume_agua": volume_agua, "area_t8": area_t8, "tipo_piso": tipo_piso
    }
    
    res = motor.processar(payload)
    
    st.success(f"## TOTAL FATURADO: R$ {format_br(res['TOTAL_GERAL'])}")
    st.markdown("### 📋 Memória de Cálculo Oficial (DIREXE)")
    
    html = "| Tabela / Rubrica | Valor Apurado (R$) | Trilha de Auditoria |\n| :--- | :--- | :--- |\n"
    for k, v in res.items():
        if k != "TOTAL_GERAL" and v["valor"] > 0:
            html += f"| **{k}** | R$ {format_br(v['valor'])} | `{v['mem']}` |\n"
            
    if len(res) == 1:
        st.warning("Insira valores maiores que zero nas abas para gerar o extrato.")
    else:
        st.markdown(html)