import streamlit as st
import pandas as pd

def show_users_management():
    # --- CSS PRIVÉ POUR PETITS BOUTONS (DESIGN MINIMALISTE) ---
    st.markdown("""
        <style>
        /* Réduire la taille des boutons de choix */
        .stButton > button {
            height: 32px !important;
            padding: 0px 15px !important;
            font-size: 13px !important;
            border-radius: 6px !important;
            border: 1px solid #d1d5db !important;
            background-color: white !important;
            color: #374151 !important;
        }
        .stButton > button:hover {
            border-color: #2563EB !important;
            color: #2563EB !important;
        }
        /* Style de la zone de document */
        .doc-card {
            background: #ffffff;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #f1f5f9;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color: #1e293b;'>👤 Gestion des Profils</h3>", unsafe_allow_html=True)

    if 'step' not in st.session_state:
        st.session_state.step = "select"

    # --- PHASE 1 : PETITS BOUTONS DE CHOIX ---
    if st.session_state.step == "select":
        st.write("<small>Identifier le nouveau profil :</small>", unsafe_allow_html=True)
        c1, c2, c3, _ = st.columns([1, 1, 1, 4]) # 4 colonnes vides pour serrer à gauche
        
        if c1.button("Responsable", use_container_width=True):
            st.session_state.role_choisi = "Responsable"
            st.session_state.step = "form"
            st.rerun()
        if c2.button("Technicien", use_container_width=True):
            st.session_state.role_choisi = "Technicien"
            st.session_state.step = "form"
            st.rerun()
        if c3.button("Autre", use_container_width=True):
            st.session_state.role_choisi = "Autre"
            st.session_state.step = "form"
            st.rerun()

    # --- PHASE 2 : LE FORMULAIRE (LES BOUTONS ONT DISPARU) ---
    elif st.session_state.step == "form":
        col_t, col_b = st.columns([5, 1])
        col_t.markdown(f"**📝 Inscription : {st.session_state.role_choisi}**")
        if col_b.button("✕ Annuler", use_container_width=True):
            st.session_state.step = "select"
            st.rerun()

        with st.form("mini_form"):
            c1, c2 = st.columns(2)
            nom = c1.text_input("Nom")
            prenom = c1.text_input("Prénom")
            mat = c1.text_input("Matricule")
            email = c1.text_input("Email")
            
            tel = c2.text_input("Téléphone")
            bur = c2.text_input("Bureau")
            zone = c2.selectbox("Zone", ["Purification", "Génération", "Atelier"])
            pwd = c2.text_input("Mot de passe", type="password")
            
            if st.form_submit_button("✅ Enregistrer le profil"):
                st.success("Utilisateur ajouté.")
                st.session_state.step = "select"
                st.rerun()

    st.markdown("---")

    # --- PHASE 3 : GESTION DES DOCUMENTS (VALORISANT POUR PFE) ---
    st.markdown("<h4 style='color: #1e293b;'>📂 Espace Ressources Technique</h4>", unsafe_allow_html=True)
    
    # On imagine que 'role' vient de la connexion (S_app.py)
    mon_role = st.session_state.get("role", "Responsable")

    t1, t2 = st.tabs(["📚 Bibliothèque", "⚙️ Administration"])

    with t1:
        # Liste de documents très "pro"
        docs = [
            {"name": "Procedure_Securite_AHF.pdf", "type": "PDF", "date": "12/06/2024"},
            {"name": "Plan_Mecanique_V2.dwg", "type": "Plan", "date": "10/06/2024"},
        ]
        for d in docs:
            st.markdown(f"""
                <div class="doc-card">
                    <div><b>{d['name']}</b><br><small>Type: {d['type']} | {d['date']}</small></div>
                    <div style="color:#2563EB; font-weight:bold; cursor:pointer;">⬇ Télécharger</div>
                </div>
            """, unsafe_allow_html=True)

    with t2:
        if mon_role == "Responsable":
            st.write("🛠️ **Actions réservées aux Responsables**")
            st.file_uploader("Publier un nouveau document technique")
            if st.button("🗑️ Purger l'annuaire"):
                st.warning("Action irréversible")
        else:
            st.error("Accès restreint. Seul un Responsable peut modifier cette zone.")