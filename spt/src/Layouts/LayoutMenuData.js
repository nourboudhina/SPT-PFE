import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";

const Navdata = () => {
    const history = useHistory();
    const [isDashboard, setIsDashboard] = useState(false);
    const [isRDV, setIsRDV] = useState(false);
    const [isPAY, setIsPAY] = useState(false);
    const [isAPC, setIsAPC] = useState(false);
    const [isHRDV, setIsHRDV] = useState(false);

    
    const [isPlanning, setIsPlanning] = useState(false);
    


    // Authentication
    const [isSignIn, setIsSignIn] = useState(false);
    const [isSignUp, setIsSignUp] = useState(false);
    const [isPasswordReset, setIsPasswordReset] = useState(false);
    const [isPasswordCreate, setIsPasswordCreate] = useState(false);
    const [isLockScreen, setIsLockScreen] = useState(false);
    const [isLogout, setIsLogout] = useState(false);
    const [isSuccessMessage, setIsSuccessMessage] = useState(false);
    const [isVerification, setIsVerification] = useState(false);
    const [isError, setIsError] = useState(false);

    // Pages
    const [isProfile, setIsProfile] = useState(false);
    const [isLanding, setIsLanding] = useState(false);



    const [iscurrentState, setIscurrentState] = useState('Dashboard');

    function updateIconSidebar(e) {
        if (e && e.target && e.target.getAttribute("subitems")) {
            const ul = document.getElementById("two-column-menu");
            const iconItems = ul.querySelectorAll(".nav-icon.active");
            let activeIconItems = [...iconItems];
            activeIconItems.forEach((item) => {
                item.classList.remove("active");
                var id = item.getAttribute("subitems");
                if (document.getElementById(id))
                    document.getElementById(id).classList.remove("show");
            });
        }
    }

    useEffect(() => {
        document.body.classList.remove('twocolumn-panel');
        if (iscurrentState !== 'Dashboard') {
            setIsDashboard(false);
        }
        if (iscurrentState !== 'HRDV') {
            setIsApps(false);
        }
        if (iscurrentState !== 'Paiement') {
            setIsAuth(false);
        }
        if (iscurrentState !== 'Plannig') {
            setIsPages(false);
        }
        if (iscurrentState !== 'APC') {
            setIsBaseUi(false);
        }
        if (iscurrentState !== 'Chat') {
            setIsAdvanceUi(false);
        }
        if (iscurrentState !== 'Patient') {
            setIsForms(false);
        }
        if (iscurrentState !== 'Administration') {
            setIsTables(false);
        }
        if (iscurrentState !== 'APC_List') {
            setIsCharts(false);
        }
        if (iscurrentState !== 'RDV') {
            setIsIcons(false);
        }
        if (iscurrentState !== 'PAY') {
            setIsMaps(false);
        }
    }, [
        history,
        iscurrentState,
        isDashboard,
        isRDV,
        isPAY,
        isPlanning,
        isAPC,
        isAPC_List,
        isPatient,
        isChat,
        isHRDV,
        isPaiement,
        isAdministration
    ]);

    const menuItems = [
        {
            label: "Menu",
            isHeader: true,
        },
        {
            id: "dashboard",
            label: "Dashboards",
            icon: "ri-dashboard-2-line",
            link: "/#",
            stateVariables: isDashboard,
            click: function (e) {
                e.preventDefault();
                setIsDashboard(!isDashboard);
                setIscurrentState('Dashboard');
                updateIconSidebar(e);
            },
        },
        
        {
            label: "pages",
            isHeader: true,
        },
        {
            id: "RDV",
            label: "Rendez-vous",
            icon: "ri-apps-2-line",
            link: "/apps-HistoriqueRDV",
            click: function (e) {
                e.preventDefault();
                setIsApps(!isRDV);
                setIscurrentState('RDV');
                updateIconSidebar(e);
            },
            stateVariables: isRDV,
        },
        {
            id: "PAY",
            label: "Historique_Paiement",
            icon: "ri-account-circle-line",
            link: "/Historique-paiement",
            click: function (e) {
                e.preventDefault();
                setIsAuth(!isPAY);
                setIscurrentState('PAY');
                updateIconSidebar(e);
            },
            stateVariables: isPAY,
            
                
        },
        {
            id: "APC",
            label: "APC",
            icon: "ri-pages-line",
            link: "/apc-list",
            click: function (e) {
                e.preventDefault();
                setIsPages(!isAPC);
                setIscurrentState('APC');
                updateIconSidebar(e);
            },
            stateVariables: isAPC,
        },
        {
            id: "Planning",
            label: "Landing",
            icon: "ri-rocket-line",
            link: "/Planning",
            stateVariables: isLanding,
            click: function (e) {
                e.preventDefault();
                setIsLanding(!isLanding);
                setIscurrentState('Landing');
                updateIconSidebar(e);
            },
           
        },
        {
            label: "Chat",
            isHeader: true,
        },
        {
            id: "Chat",
            label: "Chat",
            icon: "ri-pencil-ruler-2-line",
            link: "/Chat-list",
            click: function (e) {
                e.preventDefault();
                setIsBaseUi(!isChat);
                setIscurrentState('Chat');
                updateIconSidebar(e);
            },
            stateVariables: isChat,
            
        },
        
        
        
    ];
    return <React.Fragment>{menuItems}</React.Fragment>;
};
export default Navdata;