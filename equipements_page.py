import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent
IMG_DIR = BASE_DIR / "images_equipements"

# --- FONCTION IMAGE ---
def get_base64_image(image_filename):
    try:
        paths_to_try = [IMG_DIR / image_filename, IMG_DIR / f"{image_filename}.png", IMG_DIR / f"{image_filename}.jpg"]
        for p in paths_to_try:
            if p.exists():
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode()
        return None
    except: return None

TAG_TO_IMAGE = {
    "A11ST229": "récepteur colonne.png", "A11ST228": "colonne légère",
    "A11HX230": "rebouilleur", "A11HX231": "Condenseur",
    "A11HX232": "Refroidisseur industriel", "A11ST233": "Colonne d'absorption",
    "A11ST215": "colonne", "A11ST210": "colonne_stripping",
    "A11ST206": "generateur_hf", "A11TK200": "reservoir_procede",
}

def get_data():
    return pd.DataFrame([
        {"Tag":"A11ST229", "Nom":"Lights Column Receiver", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"PURIFICATION", "Type":"Réservoir", "Marque":"Sulzer", "Date":"12/03/2018", "Resp":"Ahmed", "MTBF":"450h", "MTTR":"3.2h", "Dispo":"99.3%"},
        {"Tag":"A11ST228", "Nom":"Lights Column", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"PURIFICATION", "Type":"Colonne", "Marque":"Koch", "Date":"05/07/2019", "Resp":"Ahmed", "MTBF":"520h", "MTTR":"2.5h", "Dispo":"99.5%"},
        {"Tag":"A11HX230", "Nom":"Lights Column Reboiler", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"PURIFICATION", "Type":"Echangeur", "Marque":"Alfa Laval", "Date":"20/01/2018", "Resp":"Salma", "MTBF":"380h", "MTTR":"4.1h", "Dispo":"98.9%"},
        {"Tag":"A11HX231", "Nom":"Lights Column Condenser", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"PURIFICATION", "Type":"Echangeur thermique", "Marque":"Alfa Laval", "Date":"15/09/2020", "Resp":"Youssef", "MTBF":"325 h", "MTTR":"4.2 h", "Dispo":"98.7 %"},
        {"Tag":"A11HX232", "Nom":"Distilled Acid Cooler", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"PURIFICATION", "Type":"Echangeur", "Marque":"Alfa Laval", "Date":"10/04/2018", "Resp":"Ahmed", "MTBF":"460h", "MTTR":"2.8h", "Dispo":"99.4%"},
        {"Tag":"A11ST233", "Nom":"H2SO4 Absorption Column", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"GENERATION", "Type":"Colonne", "Marque":"Koch", "Date":"22/11/2017", "Resp":"Ahmed", "MTBF":"500h", "MTTR":"5.0h", "Dispo":"99.0%"},
        {"Tag":"A11ST215", "Nom":"Heavies Column", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"PURIFICATION", "Type":"Colonne", "Marque":"Sulzer", "Date":"08/06/2019", "Resp":"Ahmed", "MTBF":"470h", "MTTR":"3.1h", "Dispo":"99.3%"},
        {"Tag":"A11ST210", "Nom":"HF Stripper Column", "Statut":"En maintenance", "Crit":"AA", "Zone":"A11", "Section":"GENERATION", "Type":"Colonne", "Marque":"Koch", "Date":"30/08/2018", "Resp":"Youssef", "MTBF":"350h", "MTTR":"6.2h", "Dispo":"98.2%"},
        {"Tag":"A11ST206", "Nom":"HF Generator Column", "Statut":"En service", "Crit":"AA", "Zone":"A11", "Section":"GENERATION", "Type":"Colonne", "Marque":"Koch", "Date":"14/02/2017", "Resp":"Salma", "MTBF":"490h", "MTTR":"2.9h", "Dispo":"99.4%"},
        {"Tag":"A11TK200", "Nom":"SiF4 Generator", "Statut":"En panne", "Crit":"AA", "Zone":"A11", "Section":"GENERATION", "Type":"Réservoir", "Marque":"API", "Date":"25/10/2019", "Resp":"Ahmed", "MTBF":"210h", "MTTR":"12.0h", "Dispo":"94.6%"},
    ])

# --- VUE DÉTAILLÉE (PLEIN ÉCRAN) ---
def show_details(tag):
    df = get_data()
    eq = df[df["Tag"] == tag].iloc[0]
    
    if st.button("⬅ Retour à la liste"):
        st.session_state.eq_view = "grid"
        st.rerun()
    
    st.markdown(f"## 📄 Fiche Équipement : {tag}")
    col_img, col_info = st.columns([1.2, 1])
    with col_img:
        b64 = get_base64_image(TAG_TO_IMAGE.get(tag, ""))
        if b64: st.markdown(f'<div style="background:white; padding:10px; border-radius:15px; border:1px solid #E2E8F0;"><img src="data:image/png;base64,{b64}" style="width:100%; border-radius:10px;"></div>', unsafe_allow_html=True)
    with col_info:
        st.markdown(f"### {eq['Nom']}")
        st.write(f"📍 **Zone :** {eq['Zone']} | **Type :** {eq['Type']}")
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("MTBF", eq["MTBF"])
        c2.metric("MTTR", eq["MTTR"])
        c3.metric("Dispo", eq["Dispo"])
        st.write(f"👤 **Responsable :** {eq['Resp']}")
        st.button("🔧 Historique Interventions", use_container_width=True)

# --- PAGE PRINCIPALE (GESTION DE L'AFFICHAGE UNIQUE) ---
def page_equipements():
    # Initialisation interne à la page
    if "eq_view" not in st.session_state: st.session_state.eq_view = "grid"
    
    if st.session_state.eq_view == "details" and st.session_state.get("selected_tag"):
        show_details(st.session_state.selected_tag)
    else:
        # STYLE DE LA GRILLE (4 COLONNES)
        st.markdown("""
            <style>
            .eq-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; overflow: hidden; 
                       height: 380px; display: flex; flex-direction: column; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 10px; }
            .img-container { height: 180px; width: 100%; background-color: #F8FAFC; display: flex; align-items: center; justify-content: center; }
            .img-container img { width: 100%; height: 100%; object-fit: contain; }
            .card-content { padding: 12px; flex-grow: 1; display: flex; flex-direction: column; }
            .eq-tag { font-size: 15px; font-weight: 800; color: #1E293B; }
            .eq-nom { font-size: 11px; color: #64748B; height: 32px; overflow: hidden; margin-bottom:10px; }
            .badge { padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 700; margin-right:5px; }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("## ⚙️ Gestion des Équipements")
        df = get_data()
        
        col_count = 4
        for i in range(0, len(df), col_count):
            cols = st.columns(col_count)
            for j, col in enumerate(cols):
                if i + j < len(df):
                    eq = df.iloc[i + j]
                    b64 = get_base64_image(TAG_TO_IMAGE.get(eq["Tag"], ""))
                    with col:
                        img_html = f'<img src="data:image/png;base64,{b64}">' if b64 else '<div style="font-size:50px;">🏭</div>'
                        st.markdown(f"""
                            <div class="eq-card">
                                <div class="img-container">{img_html}</div>
                                <div class="card-content">
                                    <div class="eq-tag">{eq["Tag"]}</div>
                                    <div class="eq-nom">{eq["Nom"]}</div>
                                    <div>
                                        <span class="badge" style="background:#DCFCE7; color:#166534;">{eq["Statut"]}</span>
                                        <span class="badge" style="background:#DBEAFE; color:#1E40AF;">Crit. {eq["Crit"]}</span>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("Voir détails", key=f"btn_{eq['Tag']}", use_container_width=True):
                            st.session_state.selected_tag = eq["Tag"]
                            st.session_state.eq_view = "details"
                            st.rerun()