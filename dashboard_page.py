import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ─── DONNÉES ─────────────────────────────────────────────────────────────────
EQUIPMENT_DATA = [{"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11ST229", "Designation": "Lights Column Receiver", "Severity": 44.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11ST228", "Designation": "Lights Column", "Severity": 45.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11HX230", "Designation": "Lights Column Reboiler", "Severity": 46.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11HX231", "Designation": "Lights Column Condenser", "Severity": 46.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11HX232", "Designation": "Distilled Acid Cooler", "Severity": 46.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11ST233", "Designation": "H2SO4 Absorption Column", "Severity": 42.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11ST215", "Designation": "Heavies Column", "Severity": 47.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11ST210", "Designation": "HF Stripper Column", "Severity": 41.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11ST206", "Designation": "HF Generator Column", "Severity": 48.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11TK200", "Designation": "SiF4 Generator", "Severity": 46.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11TK201", "Designation": "SiF4 Generator", "Severity": 46.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11TK216", "Designation": "Diluted H2SO4 Circulation Vessel", "Severity": 39.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11HX218", "Designation": "Heavies Column Reboiler", "Severity": 46.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11HX220", "Designation": "Heavies Column Condenser", "Severity": 46.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11ST203", "Designation": "SiF4 Generator Column", "Severity": 46.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11ST209", "Designation": "HF Drying Column", "Severity": 41.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04ST01", "Designation": "Separator", "Severity": 39.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04TK21", "Designation": "Receiver", "Severity": 39.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "CONCENTRATION", "Equipment Tag": "A11ST260", "Designation": "Scrubber I", "Severity": 39.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "CONCENTRATION", "Equipment Tag": "A11ST270", "Designation": "Scrubber II", "Severity": 43.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11TK207", "Designation": "HF Drying Column Receiver", "Severity": 42.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11TK213", "Designation": "Diluted H2SO4 Tank", "Severity": 41.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11TK208", "Designation": "HF Generator Vessel", "Severity": 44.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11TK219", "Designation": "Heavies Column Receiver", "Severity": 44.0, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04HX03A", "Designation": "Ammonia Evaporator A", "Severity": 40.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04HX03B", "Designation": "Ammonia Evaporator B", "Severity": 40.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04HX03C", "Designation": "Ammonia Evaporator C", "Severity": 40.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04HX04A", "Designation": "Ammonia Condenser A", "Severity": 40.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04HX04B", "Designation": "Ammonia Condenser B", "Severity": 40.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04HX04C", "Designation": "Ammonia Condenser C", "Severity": 40.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "FILTRATION", "Equipment Tag": "A11TK254", "Designation": "Concentrated H2SiF6 Tank", "Severity": 38.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "AHF STORAGE", "Equipment Tag": "A11HX107", "Designation": "AHF Circulation Cooler", "Severity": 41.5, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04CM11A", "Designation": "Ammonia Compressor A (Running)", "Severity": 42.0, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04CM11B", "Designation": "Ammonia Compressor B (Running)", "Severity": 42.0, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04CM11C", "Designation": "Ammonia Compressor C (Running)", "Severity": 42.0, "Criticality class": "AA"}, {"Zone": "A04", "Section": "REFRIGERATION UNIT", "Equipment Tag": "A04CM11K", "Designation": "Ammonia Compressor K (Stand-by)", "Severity": 42.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11TK222", "Designation": "Crude Acid Vessel", "Severity": 41.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11TK224", "Designation": "HF Dump Tank", "Severity": 33.5, "Criticality class": "A"}, {"Zone": "A04", "Section": "WATER TREATMENT UNIT", "Equipment Tag": "A04TK035", "Designation": "H2SO4 DOSING TANK", "Severity": 34.5, "Criticality class": "A"}, {"Zone": "A04", "Section": "WATER TREATMENT UNIT", "Equipment Tag": "A04TK034", "Designation": "NaOH DOSING TANK", "Severity": 32.5, "Criticality class": "A"}, {"Zone": "A11", "Section": "CONCENTRATION", "Equipment Tag": "A11HX262", "Designation": "Scrubber I Cooler", "Severity": 36.0, "Criticality class": "A"}, {"Zone": "A11", "Section": "CONCENTRATION", "Equipment Tag": "A11HX272", "Designation": "Scrubber II Cooler", "Severity": 40.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11HX211", "Designation": "Dilute H2SO4 Cooler", "Severity": 35.5, "Criticality class": "A"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11HX235", "Designation": "HF Drying Column Cooler", "Severity": 39.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "CONCENTRATION", "Equipment Tag": "A11TK242", "Designation": "Contactor II", "Severity": 39.5, "Criticality class": "AA"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11PM226A", "Designation": "Reflux Acid Pump", "Severity": 37.0, "Criticality class": "A"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11PM226K", "Designation": "Reflux Acid Pump", "Severity": 37.0, "Criticality class": "A"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11PM227A", "Designation": "Crude Acid Pump", "Severity": 37.0, "Criticality class": "A"}, {"Zone": "A11", "Section": "PURIFICATION", "Equipment Tag": "A11PM227K", "Designation": "Crude Acid Pump", "Severity": 37.0, "Criticality class": "A"}, {"Zone": "A22", "Section": "SILICA SLURRY STORAGE", "Equipment Tag": "A22TK01A", "Designation": "Silica Slurry Storage Tank A", "Severity": 27.5, "Criticality class": "B"}, {"Zone": "A22", "Section": "SILICA SLURRY STORAGE", "Equipment Tag": "A22TK01B", "Designation": "Silica Slurry Storage Tank B", "Severity": 27.5, "Criticality class": "B"}, {"Zone": "A11", "Section": "CONCENTRATION", "Equipment Tag": "A11TK245", "Designation": "Decanter Tank", "Severity": 36.5, "Criticality class": "A"}, {"Zone": "A11", "Section": "FILTRATION", "Equipment Tag": "A11TK252", "Designation": "Filter Feed Tank", "Severity": 36.5, "Criticality class": "A"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11HX205A", "Designation": "HF Generator Reboiler", "Severity": 37.0, "Criticality class": "A"}, {"Zone": "A11", "Section": "GENERATION", "Equipment Tag": "A11HX205K", "Designation": "HF Generator Reboiler", "Severity": 37.0, "Criticality class": "A"}, {"Zone": "A04", "Section": "FIRE FIGHTING SYSTEM", "Equipment Tag": "TK", "Designation": "Fire Water Storage Tank", "Severity": 30.5, "Criticality class": "A"}, {"Zone": "A04", "Section": "COOLANT STORAGE AND DISTRIBUTION", "Equipment Tag": "A04PM03", "Designation": "Ethylene Glycol Feed Pump", "Severity": 31.5, "Criticality class": "A"}, {"Zone": "A11", "Section": "AHF STORAGE", "Equipment Tag": "A11TK105A", "Designation": "AHF Storage Tank", "Severity": 38.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "AHF STORAGE", "Equipment Tag": "A11TK105B", "Designation": "AHF Storage Tank", "Severity": 38.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "AHF STORAGE", "Equipment Tag": "A11TK105C", "Designation": "AHF Storage Tank", "Severity": 38.0, "Criticality class": "AA"}, {"Zone": "A11", "Section": "AHF STORAGE", "Equipment Tag": "A11PM106", "Designation": "AHF Circulation Pump", "Severity": 40.0, "Criticality class": "AA"}]

CRIT_TO_RISK   = {"AA": 5, "A": 4, "B": 3, "C": 2}
CRIT_COLOR     = {"AA": "#DC2626", "A": "#F97316", "B": "#EAB308", "C": "#22C55E"}
INSPECTION_FREQ = {
    "AA": "Trimestrielle (max 3 mois)",
    "A":  "Semestrielle (max 6 mois)",
    "B":  "Annuelle (12 mois)",
    "C":  "Biennale (24 mois)"
}

def get_rbi_score(severity, crit_class):
    if severity is None:
        return None
    prob  = min(severity / 48.0 * 5, 5)
    cons  = CRIT_TO_RISK.get(crit_class, 1)
    return round((prob * cons / 25) * 100, 1)


# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.kpi-card {
    background: white; padding: 20px; border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #2563EB;
    text-align: center; height: 120px;
}
.kpi-label { font-size: 13px; color: #64748B; font-weight: 600; text-transform: uppercase; }
.kpi-value { font-size: 30px; font-weight: 800; color: #1E293B; margin-top: 5px; }
.chart-container { background: white; padding: 20px; border-radius: 15px; border: 1px solid #E2E8F0; }
.rbi-card {
    border-radius: 12px; padding: 16px 20px; margin: 6px 0;
    border-left: 6px solid; box-shadow: 0 2px 8px rgba(0,0,0,0.06); background: white;
}
</style>
""", unsafe_allow_html=True)


# ─── INITIALISATION ───────────────────────────────────────────────────────────
if "dash_page" not in st.session_state:
    st.session_state.dash_page = "main"


# ══════════════════════════════════════════════════════════════════════════════
# FONCTION DASHBOARD PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
def show_dashboard():
    col_header, col_actions = st.columns([3, 1.5])
    with col_header:
        st.title("📊 JESA - Operational Dashboard")
        st.markdown(f"Vue d'ensemble de la maintenance — Projet AHF | **{datetime.now().strftime('%d/%m/%Y')}**")
    with col_actions:
        col_pdf, col_xls = st.columns(2)
        with col_pdf:
            if st.button("📄 PDF", use_container_width=True):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
        with col_xls:
            df_csv = pd.DataFrame({"KPI": ["Interv","Dispo","MTTR","Arrêts"], "Value": [124, 98.2, 3.4, 2]})
            st.download_button("Excel 📗", df_csv.to_csv().encode('utf-8'), "Rapport.csv", use_container_width=True)

    st.markdown("---")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="kpi-card"><div class="kpi-label">Total Interventions</div><div class="kpi-value">124</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="kpi-card" style="border-left-color:#10B981"><div class="kpi-label">Disponibilité Globale</div><div class="kpi-value">98.2%</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi-card" style="border-left-color:#F59E0B"><div class="kpi-label">MTTR Moyen</div><div class="kpi-value">3.4 h</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="kpi-card" style="border-left-color:#EF4444"><div class="kpi-label">Arrêts Critiques</div><div class="kpi-value">2</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Graphiques
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Évolution de la Fiabilité (MTBF)")
        df_trend = pd.DataFrame({'Mois': ['Jan','Fév','Mar','Avr','Mai','Juin'], 'MTBF': [410,430,450,420,480,510]})
        fig_line = px.area(df_trend, x='Mois', y='MTBF', markers=True, color_discrete_sequence=['#2563EB'])
        fig_line.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🛠️ Type d'Interventions")
        fig_pie = px.pie(values=[65,25,10], names=['Préventif','Correctif','Amélioratif'],
                         hole=0.6, color_discrete_sequence=['#10B981','#EF4444','#3B82F6'])
        fig_pie.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c3, c4 = st.columns([1.5, 2])
    with c3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📍 Charge de Maintenance par Zone")
        df_zones = pd.DataFrame({"Zone":["Purification","Generation","Loading","Storage"], "Interv":[45,30,15,10]})
        fig_bar = px.bar(df_zones, x='Zone', y='Interv', color='Zone', color_discrete_sequence=px.colors.qualitative.Set3)
        fig_bar.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🚨 Top 5 Équipements les plus critiques")
        df_crit = pd.DataFrame({"Tag":["A11HX230","A11ST228","A11TK200","A11HX231","A11ST206"], "Downtime":[30,45,80,95,120]})
        fig_crit = px.bar(df_crit, x='Downtime', y='Tag', orientation='h',
                          color='Downtime', color_continuous_scale='Reds')
        fig_crit.update_layout(height=320, coloraxis_showscale=False)
        st.plotly_chart(fig_crit, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Bouton RBI
    col_note, col_rbi = st.columns([2, 1])
    with col_note:
        df_eq = pd.DataFrame(EQUIPMENT_DATA)
        n_aa = (df_eq["Criticality class"] == "AA").sum()
        n_a  = (df_eq["Criticality class"] == "A").sum()
        st.warning(f"⚠️ **{n_aa} équipements en classe AA** et **{n_a} en classe A** nécessitent une évaluation RBI / API 580-581.")
    with col_rbi:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 → Étude d'Inspection des Risques (RBI)", use_container_width=True, type="primary"):
            st.session_state.dash_page = "rbi"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col_sig1, col_sig2 = st.columns([2, 1])
    with col_sig1:
        st.info("**Note de synthèse :** La performance globale est stable. Une attention particulière doit être portée sur l'équipement A11ST206.")
    with col_sig2:
        st.markdown(f"""
        <div style="border:2px dashed #CBD5E1;border-radius:15px;padding:20px;text-align:center;background:#F8FAFC;">
            <p style="font-size:10px;color:#64748B;font-weight:bold;margin-bottom:30px;">VALIDATION RESPONSABLE JESA</p>
            <div style="border:2px solid #1E3A8A;color:#1E3A8A;display:inline-block;padding:5px 15px;
                        font-weight:900;transform:rotate(-3deg);border-radius:5px;">
                APPROUVÉ GMAO<br>
                <span style="font-size:10px;">{datetime.now().strftime('%d/%m/%Y')}</span>
            </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FONCTION PAGE RBI
# ══════════════════════════════════════════════════════════════════════════════
def show_rbi():
    if st.button("← Retour au Dashboard", type="secondary", key="back_rbi_top"):
        st.session_state.dash_page = "main"
        st.rerun()

    st.title("🔍 Étude d'Inspection Basée sur les Risques (RBI)")
    st.markdown(f"**Projet AHF — JESA** | Référence : API 580/581 | Généré le **{datetime.now().strftime('%d/%m/%Y')}**")
    st.markdown("---")

    df = pd.DataFrame(EQUIPMENT_DATA)
    df["RBI Score"]           = df.apply(lambda r: get_rbi_score(r["Severity"], r["Criticality class"]), axis=1)
    df["Fréquence inspection"] = df["Criticality class"].map(INSPECTION_FREQ)
    counts = df["Criticality class"].value_counts()

    # KPIs RBI
    st.subheader("📊 Synthèse du Portefeuille")
    k1, k2, k3, k4, k5 = st.columns(5)
    for col, crit, color in [(k1,"AA","#DC2626"),(k2,"A","#F97316"),(k3,"B","#EAB308"),(k4,"C","#22C55E")]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:{color}">
                <div class="kpi-label">Classe {crit}</div>
                <div class="kpi-value" style="color:{color}">{counts.get(crit,0)}</div>
            </div>""", unsafe_allow_html=True)
    with k5:
        top_score = df["RBI Score"].max()
        top_tag   = df.loc[df["RBI Score"].idxmax(), "Equipment Tag"]
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color:#7C3AED">
            <div class="kpi-label">Score MAX 🏆</div>
            <div class="kpi-value" style="color:#7C3AED;font-size:20px">{top_score}<br>
            <span style="font-size:10px">{top_tag}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Matrice + Donut
    col_mat, col_pie = st.columns([3, 2])
    with col_mat:
        with st.container(border=True):
            st.subheader("🗺️ Matrice de Risque RBI (API 580)")
            df_plot = df.dropna(subset=["RBI Score"]).copy()
            df_plot["Conséquence"] = df_plot["Criticality class"].map(CRIT_TO_RISK)
            df_plot["Probabilité"] = (df_plot["Severity"] / 48.0 * 5).round(2)
            fig_mat = px.scatter(
                df_plot, x="Probabilité", y="Conséquence",
                color="Criticality class",
                color_discrete_map=CRIT_COLOR,
                size="RBI Score", size_max=25,
                hover_name="Equipment Tag",
                hover_data={"Designation": True, "Zone": True, "RBI Score": True},
            )
            fig_mat.add_shape(type="rect", x0=0, x1=2,   y0=0,   y1=2.5, fillcolor="rgba(34,197,94,0.08)",  line_width=0)
            fig_mat.add_shape(type="rect", x0=2, x1=3.5, y0=2.5, y1=4,   fillcolor="rgba(234,179,8,0.08)",  line_width=0)
            fig_mat.add_shape(type="rect", x0=3.5,x1=5.5,y0=3.5, y1=5.5, fillcolor="rgba(220,38,38,0.08)",  line_width=0)
            fig_mat.update_layout(
                height=420, margin=dict(l=10,r=10,t=10,b=10),
                xaxis=dict(range=[0,5.5], tickvals=[1,2,3,4,5],
                           ticktext=["Rare","Peu probable","Possible","Probable","Fréquent"]),
                yaxis=dict(range=[0,5.5], tickvals=[1,2,3,4,5],
                           ticktext=["Négligeable","Mineur","Modéré","Majeur","Catastrophique"]),
            )
            st.plotly_chart(fig_mat, use_container_width=True)

    with col_pie:
        with st.container(border=True):
            st.subheader("🍩 Distribution des classes")
            fig_donut = px.pie(
                names=list(counts.index), values=list(counts.values),
                hole=0.55, color=list(counts.index),
                color_discrete_map=CRIT_COLOR
            )
            fig_donut.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_donut, use_container_width=True)

        with st.container(border=True):
            st.subheader("📍 Par Zone (AA+A)")
            df_zone = df[df["Criticality class"].isin(["AA","A"])].groupby("Zone").size().reset_index(name="count")
            fig_zone = px.bar(df_zone.sort_values("count", ascending=True),
                              x="count", y="Zone", orientation="h",
                              color="count", color_continuous_scale=["#FEF9C3","#DC2626"])
            fig_zone.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), coloraxis_showscale=False)
            st.plotly_chart(fig_zone, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tableau top 20
    with st.container(border=True):
        st.subheader("🔎 Registre RBI — Top 20 par score")
        f1, f2, f3 = st.columns([1, 1, 2])
        with f1:
            filtre_classe = st.multiselect("Classe", ["AA","A","B","C"], default=["AA","A"])
        with f2:
            zones_dispo = sorted(df["Zone"].unique())
            filtre_zone = st.multiselect("Zone", zones_dispo, default=zones_dispo)
        with f3:
            search_rbi = st.text_input("🔍 Recherche Tag / Désignation", "", key="search_rbi")

        df_f = df[df["Criticality class"].isin(filtre_classe) & df["Zone"].isin(filtre_zone)].copy()
        if search_rbi:
            df_f = df_f[
                df_f["Equipment Tag"].str.contains(search_rbi, case=False, na=False) |
                df_f["Designation"].str.contains(search_rbi, case=False, na=False)
            ]
        df_f = df_f.sort_values("RBI Score", ascending=False)

        st.markdown(f"**{len(df_f)} équipements** — affichage des 20 premiers")
        for _, row in df_f.head(20).iterrows():
            crit  = row["Criticality class"]
            color = CRIT_COLOR.get(crit, "#94A3B8")
            score = row["RBI Score"] if pd.notna(row["RBI Score"]) else 0
            bar_w = int(score)
            st.markdown(f"""
            <div class="rbi-card" style="border-left-color:{color}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <span style="font-weight:800;font-size:14px;color:#1E293B">{row['Equipment Tag']}</span>
                        <span style="margin-left:8px;color:#64748B;font-size:12px">{row['Designation']}</span>
                        <span style="margin-left:6px;font-size:11px;color:#94A3B8">| {row['Zone']} — {row['Section']}</span>
                    </div>
                    <div>
                        <span style="background:{color};color:white;border-radius:12px;
                            padding:3px 10px;font-weight:700;font-size:12px">{crit}</span>
                        <span style="margin-left:8px;font-weight:700;color:{color}">{score}/100</span>
                    </div>
                </div>
                <div style="margin-top:6px;background:#F1F5F9;border-radius:4px;height:6px">
                    <div style="background:{color};width:{bar_w}%;height:6px;border-radius:4px"></div>
                </div>
                <div style="font-size:11px;color:#64748B;margin-top:4px">
                    ⏱ <b>Fréquence :</b> {row['Fréquence inspection']}
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_f[["Equipment Tag","Designation","Zone","Section","Criticality class","Severity","RBI Score","Fréquence inspection"]].to_csv(index=False).encode("utf-8")
        st.download_button("📥 Exporter RBI (CSV)", csv_data, "registre_RBI.csv", use_container_width=True)

    # Plan d'action
    st.markdown("---")
    st.subheader("📋 Plan d'Action RBI")
    actions = [
        ("🔴 IMMÉDIAT (0–3 mois)",    f"{counts.get('AA',0)} équipements AA", "Inspection visuelle + CND obligatoire. Épaissimétrie sur colonnes HF/H2SO4.", "#DC2626"),
        ("🟠 COURT TERME (3–6 mois)", f"{counts.get('A',0)} équipements A",   "Inspection planifiée. Suivi corrosion. Analyse de fluides.", "#F97316"),
        ("🟡 MOYEN TERME (6–12 mois)",f"{counts.get('B',0)} équipements B",   "Inspection annuelle standard. Vérification des points de rosée.", "#EAB308"),
        ("🟢 LONG TERME (12–24 mois)",f"{counts.get('C',0)} équipements C",   "Maintenance préventive selon programme GMAO.", "#22C55E"),
    ]
    for titre, nb, desc, color in actions:
        st.markdown(f"""
        <div style="background:white;border-left:5px solid {color};border-radius:10px;
            padding:14px 18px;margin:6px 0;box-shadow:0 2px 6px rgba(0,0,0,0.05)">
            <b style="color:{color};font-size:14px">{titre}</b>
            <span style="margin-left:10px;background:{color};color:white;border-radius:10px;
                padding:2px 10px;font-size:11px;font-weight:700">{nb}</span>
            <p style="margin:6px 0 0;color:#475569;font-size:12px">{desc}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Retour au Dashboard", type="secondary", use_container_width=True, key="back_rbi_bottom"):
        st.session_state.dash_page = "main"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════
# DEBUG
# ════════════════════════════════════════════════════════════════════════

st.write("PAGE =", st.session_state.get("dash_page"))

# ════════════════════════════════════════════════════════════════════════
# ROUTEUR
# ════════════════════════════════════════════════════════════════════════

if st.session_state.get("dash_page") == "rbi":
    show_rbi()
else:
    show_dashboard()