from pathlib import Path
import streamlit as st
import base64
import pandas as pd
import datetime
from equipements_page import page_equipements
from dashboard_page import show_dashboard
from fiabilite_page import show_fiabilite
from users_page import show_users_management

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# PATH HELPERS
# =========================
BASE_DIR = Path(__file__).parent

def img_path(*stems: str) -> str:
    candidates = []
    for stem in stems:
        if not stem:
            continue
        s = stem.strip()
        candidates.extend([
            s,
            s.replace("  ", " "),
            s.replace(" / ", " "),
            s.replace("/", " "),
        ])
    for stem in dict.fromkeys(candidates):
        for ext in [".png", ".jpg", ".jpeg", ".webp"]:
            p = BASE_DIR / f"{stem}{ext}"
            if p.exists():
                return str(p)
    return candidates[0] if candidates else ""

# =========================
# USERS DATA
# =========================
if "users_data" not in st.session_state:
    st.session_state.users_data = [
        {"Nom": "Admin", "Prenom": "System", "Login": "admin", "Password": "1234", "Type": "Responsable"}
    ]

# =========================
# SESSION
# =========================
if "logged_in"     not in st.session_state: st.session_state.logged_in     = False
if "page"          not in st.session_state: st.session_state.page          = "menu"
if "profil"        not in st.session_state: st.session_state.profil        = None
if "selected_area" not in st.session_state: st.session_state.selected_area = None

# =========================
# BACKGROUND
# =========================
def set_bg():
    try:
        with open("background.jpg", "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    except:
        pass

# =========================
# STYLE
# =========================
st.markdown("""
    <style>
    .login-box {
        background-color: rgba(0,0,0,0.55);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }
    div.stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        color: white;
        font-size: 16px;
        font-weight: 600;
        border: none;
        margin-bottom: 12px;
        text-align: left;
        padding-left: 18px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8, #2563EB);
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================
def login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<p style='color:white;font-weight:600;margin-bottom:6px;'>Utilisateur</p>", unsafe_allow_html=True)
        username = st.text_input("", placeholder="Utilisateur", key="login_username")
        st.markdown("<p style='color:white;font-weight:600;margin-bottom:6px;'>Mot de passe</p>", unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Mot de passe", key="login_password")
        if st.button("Se connecter"):
            user_found = None
            for user in st.session_state.users_data:
                if user["Login"] == username and user["Password"] == password:
                    user_found = user
                    break
            if user_found:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.session_state.role      = user_found["Type"]
                st.rerun()
            else:
                st.error("Accès refusé")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# MENU GAUCHE
# =========================
def menu_gmao():
    with st.sidebar:
        try:
            st.image(img_path("logo"), width=120)
        except:
            pass
        st.markdown("## Menu Principal")
        if st.button("👤 Gestion des utilisateurs"):  st.session_state.page = "users";        st.rerun()
        if st.button("📍 Gestion des affectation"):   st.session_state.page = "affectation";   st.rerun()
        if st.button("⚙️ Gestion d'équipements"):     st.session_state.page = "equipements";   st.rerun()
        if st.button("📦 Gestion PDR"):               st.session_state.page = "pdr";           st.rerun()
        if st.button("🛠️ Gestion d'intervention"):    st.session_state.page = "interventions"; st.rerun()
        if st.button("🔧 Gestion de Maintenance"):    st.session_state.page = "maintenance";   st.rerun()
        if st.button("📊  Dashboard"):                st.session_state.page = "dashboard";     st.rerun()
        if st.button("📈 Calcul fiabilité"):          st.session_state.page = "fiabilite";     st.rerun()
        st.markdown("---")
        if st.button("➜ Déconnexion"):
            st.session_state.logged_in    = False
            st.session_state.page         = "menu"
            st.session_state.profil       = None
            st.session_state.selected_area = None
            st.rerun()

# =========================
# MAIN
# =========================
if not st.session_state.logged_in:
    set_bg()
    login()

else:
    menu_gmao()

    # ── MENU ──
    if st.session_state.page == "menu":
        img = img_path("Welcom")
        if img:
            st.image(img, use_container_width=True)
        else:
            st.title("Menu Principal")

    # ── USERS ──
    elif st.session_state.page == "users":
        if st.button("⬅ Retour au menu principal"):
            st.session_state.page = "menu"
            st.rerun()
        # APPEL DE LA PAGE EXTERNE CORRIGÉE
        show_users_management()

    # ── AFFECTATION PAGE 1 ──
    elif st.session_state.page == "affectation":
        if st.button("⬅ Retour au menu principal"):
            st.session_state.page = "menu"
            st.rerun()
        st.title("📍 Gestion des affectations")
        st.write("Visualisation des différentes zones du projet AHF.")
        st.markdown("---")
        plan = img_path("plan")
        if plan:
            st.image(plan, use_container_width=True)
        else:
            st.warning("Image du plan introuvable.")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("➡ Continuer vers le formulaire"):
                st.session_state.page = "affectation_form"
                st.rerun()

    # ── AFFECTATION FORM PAGE 2 ──
    elif st.session_state.page == "affectation_form":
        if "affectations_data" not in st.session_state:
            st.session_state.affectations_data = []
        if st.button("⬅ Retour vers les zones"):
            st.session_state.page = "affectation"
            st.rerun()
        st.title("📝 Formulaire des affectations")
        st.write("💡Cette interface permet d'affecter un responsable maintenance à une zone du projet.")
        st.markdown("---")
        st.markdown("""
        <style>
        .form-container { background-color:white;padding:30px;border-radius:18px;
            border:1px solid #E5E7EB;box-shadow:0px 4px 14px rgba(0,0,0,0.08);margin-top:20px; }
        .section-title { font-size:24px;font-weight:700;color:#1F2937;margin-bottom:25px; }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Affectation des responsables</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            affectation      = st.selectbox("Affectation", ["AHF Production Zone","AHF Substation Zone","AHF Tank Farm","Central Process Unit","Loading / Dispatch Area","Workshop"])
            matricule        = st.text_input("Matricule responsable maintenance")
            type_responsable = st.selectbox("Type de responsable", ["Responsable Maintenance","Responsable Production","Responsable Électrique","Responsable Zone"])
        with col2:
            nom        = st.text_input("Nom")
            prenom     = st.text_input("Prénom")
            technicien = st.text_input("Technicien affecté à la zone")
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
        with col_btn2:
            if st.button("✔ Valider"):
                st.session_state.affectations_data.append({
                    "Zone": affectation, "Matricule": matricule, "Nom": nom,
                    "Prénom": prenom, "Type": type_responsable, "Technicien": technicien
                })
                st.success("Affectation enregistrée avec succès.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("📋 Liste des affectations")
        if len(st.session_state.affectations_data) > 0:
            st.dataframe(st.session_state.affectations_data, use_container_width=True)
        else:
            st.info("Aucune affectation enregistrée.")

    # ── EQUIPEMENTS ──
    elif st.session_state.page == "equipements":
        page_equipements()

    # ── PDR ──
    elif st.session_state.page == "pdr":
        if st.button("⬅ Retour au menu principal"):
            st.session_state.page = "menu"
            st.rerun()
        st.title("📦 Gestion PDR")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            ref_cpn        = st.text_input("REF_PDR_CPN", placeholder="Référence CPN")
            ref_fr         = st.text_input("REF_PDR_FR", placeholder="Référence fournisseur")
            nb_stock       = st.number_input("NB_PDR_stock", min_value=0, value=0)
            duree_vie      = st.date_input("Durée de vie")
            fournisseur    = st.text_input("Fournisseur")
            tel_fournisseur = st.text_input("TEL Fournisseur")
        with col2:
            email_fournisseur   = st.text_input("E_mail Fournisseur")
            adresse_fournisseur = st.text_area("Adresse Fournisseur")
            stock_min           = st.number_input("Stock minimum", min_value=0, value=0)
            machine             = st.selectbox("MACHINE", ["Choisir...","Machine 1","Machine 2","Machine 3"])
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            valider = st.button("✅ Valider", use_container_width=True)
        with c2:
            vider = st.button("❌ Vider les champs", use_container_width=True)
        if valider:
            nouvelle_pdr = {
                "REF_PDR_CPN": ref_cpn, "REF_PDR_FR": ref_fr,
                "NB_PDR_stock": nb_stock, "Durée de vie": str(duree_vie),
                "Fournisseur": fournisseur, "TEL Fournisseur": tel_fournisseur,
                "E_mail Fournisseur": email_fournisseur,
                "Adresse Fournisseur": adresse_fournisseur,
                "Stock minimum": stock_min, "MACHINE": machine
            }
            st.success("✅ PDR enregistrée avec succès")
            st.write(nouvelle_pdr)

    # ── INTERVENTIONS ──
    elif st.session_state.page == "interventions":
        if "interventions_data" not in st.session_state:
            st.session_state.interventions_data = []

        if st.button("⬅ Retour au menu principal", key="back_interventions"):
            st.session_state.page = "menu"
            st.rerun()

        st.markdown("""
        <div style='display:flex;align-items:center;gap:14px;margin:8px 0 16px'>
            <span style='font-size:34px'>🛠️</span>
            <div>
                <div style='font-size:27px;font-weight:800;color:#0F172A'>Gestion d'intervention</div>
                <div style='font-size:13px;color:#64748B;margin-top:4px'>Création et suivi des fiches d'intervention</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("#### 📋 Identification de l'intervention")
            col_left, col_mid, col_right = st.columns([2, 2, 3])
            with col_left:
                st.markdown("**Demandeur**")
                type_demandeur = st.radio("", ["Responsable", "Autre"], horizontal=True, key="type_demandeur")
                prenom_resp    = st.text_input("Prénom (Responsable)", key="prenom_resp")
                matricule_resp = st.selectbox("Matricule (Responsable)", ["","MAT001","MAT002","MAT003","MAT004"], key="mat_resp")
                if type_demandeur == "Autre":
                    st.text_input("Prénom (Autre)", key="prenom_autre")
                    st.text_input("Matricule (Autre)", key="mat_autre")
                fonction          = st.text_input("Fonction", key="fonction")
                uap               = st.selectbox("UAP", ["","UAP1","UAP2","UAP3","Production","Maintenance"], key="uap")
                type_intervention = st.selectbox("Type", ["","Corrective","Préventive","Prédictive","Améliorative"], key="type_interv")
            with col_mid:
                code_intervention = st.selectbox("Code d'intervention", ["","INT-001","INT-002","INT-003","INT-004","INT-005"], key="code_interv")
                equipement        = st.selectbox("Équipement", ["","A11ST229","A11ST228","A11HX230","A11HX231","A11HX232","A11ST233","A11ST215","A11ST210","A11ST206","A11TK200"], key="equipement_interv")
                date_interv       = st.date_input("Date", key="date_interv")
                heure_interv      = st.time_input("Heure", key="heure_interv")
                equipement_arret  = st.selectbox("Équipement en arrêt", ["","Oui","Non"], key="eq_arret")
            with col_right:
                description_panne = st.text_area("Description de la panne ou de l'anomalie constatée", height=220, key="desc_panne")

        with st.container(border=True):
            st.markdown("#### 👷 Technicien de maintenance")
            c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 2])
            with c1: prenom_tech    = st.text_input("Prénom Tech Maintenance", key="prenom_tech")
            with c2: nom_tech       = st.text_input("Nom", key="nom_tech")
            with c3: matricule_tech = st.selectbox("Matricule", ["","TECH001","TECH002","TECH003","TECH004"], key="mat_tech")
            with c4: recu_le        = st.date_input("Reçu le", key="recu_le")
            with c5: heure_recu     = st.time_input("Heure reçu", key="heure_recu")

        with st.container(border=True):
            st.markdown("#### 🔧 Travaux effectués & PDR")
            col_travaux, col_pdr, col_fin = st.columns([3, 3, 2])
            with col_travaux:
                description_travaux = st.text_area("Description des travaux effectués", height=220, key="desc_travaux")
            with col_pdr:
                pdr_ref = st.text_input("PDR utilisée", key="pdr_ref")
                if st.button("🔄 Changer la pièce", key="changer_piece"):
                    st.info("Sélection PDR — à implémenter.")
                st.markdown("**Stock PDR disponible**")
                pdr_data_dict = {
                    "REF PDR CPN":     ["qqs","00125151","KDBCKJ","OKJF","EZJKMBEZJK","EZKJJCBKEJ"],
                    "NB_PDR_en_STOCK": [9, 9, 11, 1, 4, 7]
                }
                st.dataframe(pd.DataFrame(pdr_data_dict), use_container_width=True, hide_index=True)
            with col_fin:
                fin_le    = st.date_input("Fin le", key="fin_le")
                heure_fin = st.time_input("Heure fin", key="heure_fin")

        st.markdown("<br>", unsafe_allow_html=True)
        _, col_next, _ = st.columns([4, 1, 1])
        with col_next:
            if st.button("Suivant ➡", key="next_interv", use_container_width=True):
                st.session_state.page = "interventions_appro"
                st.rerun()

    elif st.session_state.page == "interventions_appro":
        if "interventions_data" not in st.session_state:
            st.session_state.interventions_data = []

        if st.button("⬅ Retour à l'intervention", key="back_appro"):
            st.session_state.page = "interventions"
            st.rerun()

        st.markdown("""
        <div style='display:flex;align-items:center;gap:14px;margin:8px 0 16px'>
            <span style='font-size:34px'>✅</span>
            <div>
                <div style='font-size:27px;font-weight:800;color:#0F172A'>Approbation & Durée</div>
                <div style='font-size:13px;color:#64748B;margin-top:4px'>Validation et durée de l'intervention</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("#### ✅ Approbation responsable maintenance")
            col1, col2 = st.columns(2)
            with col1:
                date_appro  = st.date_input("Date approbation", key="date_appro")
                heure_appro = st.time_input("Heure approbation", key="heure_appro")
            with col2:
                st.markdown("**Durée d'intervention**")
                duree_intervention = st.text_area("", height=100, key="duree_interv")
                if st.button("🧮 Calculer la durée d'intervention", key="calc_duree"):
                    try:
                        debut = datetime.datetime.combine(st.session_state.get("date_interv"), st.session_state.get("heure_interv"))
                        fin   = datetime.datetime.combine(st.session_state.get("fin_le"), st.session_state.get("heure_fin"))
                        duree = fin - debut
                        heures, reste = divmod(int(duree.total_seconds()), 3600)
                        minutes = reste // 60
                        st.success(f"✅ Durée : {heures}h {minutes}min")
                    except:
                        st.warning("Vérifiez les dates/heures en page précédente.")

        st.markdown("<br>", unsafe_allow_html=True)
        col_modif, col_enreg, col_vider, _ = st.columns([1, 1, 1, 3])
        with col_modif:
            if st.button("✏️ Modifiée", key="btn_modifiee", use_container_width=True):
                st.info("Modification enregistrée.")
        with col_enreg:
            if st.button("✅ Enregistrer", key="save_interv", use_container_width=True):
                fiche = {
                    "Code": st.session_state.get("code_interv", ""),
                    "Équipement": st.session_state.get("equipement_interv", ""),
                    "Type": st.session_state.get("type_interv", ""),
                    "Date appro": str(date_appro),
                    "Heure appro": str(heure_appro),
                }
                st.session_state.interventions_data.append(fiche)
                st.success("✅ Fiche d'intervention enregistrée !")
        with col_vider:
            if st.button("🗑️ Vider les champs", key="clear_interv", use_container_width=True):
                st.session_state.page = "interventions"
                st.rerun()

        if len(st.session_state.interventions_data) > 0:
            st.markdown("---")
            st.markdown("#### 📋 Historique")
            st.dataframe(pd.DataFrame(st.session_state.interventions_data), use_container_width=True, hide_index=True)

    # ── MAINTENANCE ──
    elif st.session_state.page == "maintenance":
        if st.button("⬅ Retour au menu principal"):
            st.session_state.page = "menu"
            st.rerun()
        st.title("🔧 Gestion de Maintenance Préventive")
        tab1, tab2 = st.tabs(["➕ Ajouter MP", "✏️ Modifier MP"])
        with tab1:
            c1, c2, c3 = st.columns(3)
            with c1:
                affectation_mp = st.selectbox("Affectation", ["Choisir...","UAP1","UAP2","UAP3"])
                code_machine   = st.selectbox("Code Machine", ["Choisir...","MBR01","MBR02","A11HX230","A11ST229"])
                frequence      = st.number_input("Fréquence", min_value=0, value=0)
            with c2:
                week        = st.number_input("Week", min_value=0, value=0)
                designation = st.text_input("Désignation")
                duree_mp    = st.number_input("Durée d'intervention (h)", min_value=0, value=0)
            with c3:
                mois_mp = st.selectbox("Mois", ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"])
                semaine_mp = st.selectbox("Semaine", list(range(1, 53)))
                realisation = st.radio("Réalisation", ["Oui","Non"])
            if st.button("✅ Valider", use_container_width=True, key="add_mp"):
                st.success("Maintenance préventive ajoutée.")
        with tab2:
            st.subheader("Recherche & Modification")
            data_mp = pd.DataFrame({"Désignation Machine": ["Machine à braider","Twistage"], "Mois": ["Juin","Juin"]})
            st.dataframe(data_mp, use_container_width=True, height=150)
            if st.button("✏️ Modifier", use_container_width=True, key="modify_mp"):
                st.success("Maintenance modifiée.")

    # ── DASHBOARD ──
    elif st.session_state.page == "dashboard":
        if st.button("⬅ Retour au menu principal"):
            st.session_state.page = "menu"
            st.rerun()
        show_dashboard()

    # ── FIABILITE ──
    elif st.session_state.page == "fiabilite":
        if st.button("⬅ Retour au menu principal"):
            st.session_state.page = "menu"
            st.rerun()
        show_fiabilite()