// Multilingual Translation Dictionary

const TRANSLATIONS = {
    'en': {
        'system_live': 'System Live: Healthy',
        'attendance': 'Attendance',
        'ai_risk': 'AI Risk Score',
        'active_alerts': 'Active Alerts',
        'sustainability': 'Sustainability',
        'realtime_logs': 'Real-time CCTV logs',
        'hvac_solar': 'HVAC & Solar Grid',
        'stadium_3d_title': '3D Digital Twin Stadium Model',
        'live_map_title': 'Live Perimeter & Transit Map',
        'realtime_dynamics': 'Real-time Dynamics',
        'log_console': 'System Log Console',
        'emergency_command': 'Emergency Command',
        'simulate_alert': 'Simulate Alert',
        'reset': 'Reset',
        'simulation_panel': 'Simulation Control Panel',
        'sim_testing_only': 'FOR SIMULATION & TELEMETRY TESTING ONLY',
        'weather_scenarios': 'WEATHER SCENARIOS',
        'clear': 'Clear',
        'rain': 'Rain',
        'heatwave': 'Heatwave',
        'crowd_modifiers': 'CROWD VOLUME MODIFIERS',
        'crowd_inc': 'Crowd +20%',
        'crowd_dec': 'Crowd -20%',
        'climate_thermostat': 'CLIMATE THERMOSTAT',
        'temp_inc': 'Temp +3°C',
        'temp_dec': 'Temp -3°C',
        'power_outage': 'Trigger Power Outage',
        'zone_telemetry': 'Zone Telemetry Details',
        'select_zone': 'Select Stand or Gate',
        'zone_type': 'Zone Type:',
        'current_crowd': 'Current Crowd:',
        'queue_wait': 'Queue Wait:',
        'temperature': 'Temperature:',
        'sector_risk': 'Sector Risk Index:',
        'ai_predictions': 'AI PREDICTION FORECASTS (15-60m)',
        'click_predictions': 'Click any sector to query AI predictions...',
        'gemini_brain': 'Gemini OS Brain',
        'core_analysis': 'CORE ANALYSIS',
        'priority_actions': 'PRIORITY OPERATOR ACTIONS',
        'multilingual_announcement': 'MULTILINGUAL PUBLIC ANNOUNCEMENT',
        'fan_assistant_portal': 'Fan Assistance Portal',
        'chat_welcome': 'Hello! Welcome to FIFA World Cup 2026. Ask me about gates, metro transit, restrooms, or fastest food courts.',
        'show_simulator': 'Show Simulator'
    },
    'es': {
        'system_live': 'Sistema Activo: Saludable',
        'attendance': 'Asistencia',
        'ai_risk': 'Puntaje de Riesgo IA',
        'active_alerts': 'Alertas Activas',
        'sustainability': 'Sostenibilidad',
        'realtime_logs': 'Registros de CCTV en vivo',
        'hvac_solar': 'HVAC y Red Solar',
        'stadium_3d_title': 'Modelo 3D Gemelo Digital',
        'live_map_title': 'Perímetro y Tránsito en Vivo',
        'realtime_dynamics': 'Dinámica en Tiempo Real',
        'log_console': 'Consola de Registro del Sistema',
        'emergency_command': 'Mando de Emergencia',
        'simulate_alert': 'Simular Alerta',
        'reset': 'Restablecer',
        'simulation_panel': 'Panel de Control de Simulación',
        'sim_testing_only': 'SOLO PARA PRUEBAS DE SIMULACIÓN Y TELEMETRÍA',
        'weather_scenarios': 'ESCENARIOS CLIMÁTICOS',
        'clear': 'Despejado',
        'rain': 'Lluvia',
        'heatwave': 'Ola de Calor',
        'crowd_modifiers': 'MODIFICADORES DE MULTITUD',
        'crowd_inc': 'Público +20%',
        'crowd_dec': 'Público -20%',
        'climate_thermostat': 'TERMOSTATO DE CLIMA',
        'temp_inc': 'Temp +3°C',
        'temp_dec': 'Temp -3°C',
        'power_outage': 'Simular Corte de Energía',
        'zone_telemetry': 'Detalles de Telemetría de Zona',
        'select_zone': 'Seleccione Tribuna o Puerta',
        'zone_type': 'Tipo de Zona:',
        'current_crowd': 'Público Actual:',
        'queue_wait': 'Espera en Fila:',
        'temperature': 'Temperatura:',
        'sector_risk': 'Índice de Riesgo de Sector:',
        'ai_predictions': 'PRONÓSTICOS DE IA (15-60m)',
        'click_predictions': 'Haga clic en un sector para consultar pronósticos...',
        'gemini_brain': 'Cerebro del Sistema Gemini',
        'core_analysis': 'ANÁLISIS CENTRAL',
        'priority_actions': 'ACCIONES PRIORITARIAS DEL OPERADOR',
        'multilingual_announcement': 'ANUNCIO PÚBLICO MULTILINGÜE',
        'fan_assistant_portal': 'Portal de Asistencia al Fanático',
        'chat_welcome': '¡Hola! Bienvenidos a la Copa Mundial de la FIFA 2026. Pregúnteme sobre puertas, transporte de metro, baños o comida rápida.',
        'show_simulator': 'Mostrar Simulador'
    },
    'fr': {
        'system_live': 'Système Actif: Sain',
        'attendance': 'Affluence',
        'ai_risk': 'Score de Risque IA',
        'active_alerts': 'Alertes Actives',
        'sustainability': 'Durabilité',
        'realtime_logs': 'Logs CCTV en direct',
        'hvac_solar': 'Réseau CVC et Solaire',
        'stadium_3d_title': 'Modèle Jumeau Numérique 3D',
        'live_map_title': 'Carte Périmètre & Transit',
        'realtime_dynamics': 'Dynamique en Temps Réel',
        'log_console': 'Console de Journalisation',
        'emergency_command': 'Commande d\'Urgence',
        'simulate_alert': 'Simuler une Alerte',
        'reset': 'Réinitialiser',
        'simulation_panel': 'Panneau de Contrôle de Simulation',
        'sim_testing_only': 'POUR TESTS DE SIMULATION ET TÉLÉMÉTRIE UNIQUEMENT',
        'weather_scenarios': 'SCÉNARIOS MÉTÉO',
        'clear': 'Dégagé',
        'rain': 'Pluie',
        'heatwave': 'Canicule',
        'crowd_modifiers': 'MODIFICATEURS DE FOULE',
        'crowd_inc': 'Foule +20%',
        'crowd_dec': 'Foule -20%',
        'climate_thermostat': 'THERMOSTAT DE CLIMAT',
        'temp_inc': 'Temp +3°C',
        'temp_dec': 'Temp -3°C',
        'power_outage': 'Déclencher Panne de Courant',
        'zone_telemetry': 'Détails de Télémétrie de Zone',
        'select_zone': 'Sélectionner une Zone ou Porte',
        'zone_type': 'Type de Zone:',
        'current_crowd': 'Foule Actuelle:',
        'queue_wait': 'Attente en File:',
        'temperature': 'Température:',
        'sector_risk': 'Indice de Risque du Secteur:',
        'ai_predictions': 'PRÉVISIONS D\'IA (15-60m)',
        'click_predictions': 'Cliquez sur une zone pour les prévisions IA...',
        'gemini_brain': 'Système Cerveau Gemini',
        'core_analysis': 'ANALYSE PRINCIPALE',
        'priority_actions': 'ACTIONS OPÉRATEUR PRIORITAIRES',
        'multilingual_announcement': 'ANNONCE PUBLIQUE MULTILINGUE',
        'fan_assistant_portal': 'Portail d\'Assistance aux Fans',
        'chat_welcome': 'Bonjour! Bienvenue à la Coupe du Monde de la FIFA 2026. Posez-moi des questions sur les portes, le métro, les toilettes ou la restauration.',
        'show_simulator': 'Afficher le Simulateur'
    },
    'de': {
        'system_live': 'System Live: Gesund',
        'attendance': 'Besucherzahl',
        'ai_risk': 'KI-Risikobewertung',
        'active_alerts': 'Aktive Alarme',
        'sustainability': 'Nachhaltigkeit',
        'realtime_logs': 'Echtzeit-CCTV-Protokolle',
        'hvac_solar': 'Klimaanlage & Solarnetz',
        'stadium_3d_title': '3D Digitaler Zwilling Modell',
        'live_map_title': 'Live-Umgebungs- & Transitkarte',
        'realtime_dynamics': 'Echtzeit-Dynamik',
        'log_console': 'Systemprotokollkonsole',
        'emergency_command': 'Notfallkommando',
        'simulate_alert': 'Alarm Simulieren',
        'reset': 'Zurücksetzen',
        'simulation_panel': 'Simulation Control Panel',
        'sim_testing_only': 'NUR FÜR SIMULATIONS- UND TELEMETRIETESTS',
        'weather_scenarios': 'WETTERSZENARIEN',
        'clear': 'Klar',
        'rain': 'Regen',
        'heatwave': 'Hitzewelle',
        'crowd_modifiers': 'ZUSCHAUERMODIFIKATOREN',
        'crowd_inc': 'Zuschauer +20%',
        'crowd_dec': 'Zuschauer -20%',
        'climate_thermostat': 'KLIMATHERMOSTAT',
        'temp_inc': 'Temp +3°C',
        'temp_dec': 'Temp -3°C',
        'power_outage': 'Stromausfall Simulieren',
        'zone_telemetry': 'Zonen-Telemetriedetails',
        'select_zone': 'Wählen Sie Tribüne oder Tor',
        'zone_type': 'Zonentyp:',
        'current_crowd': 'Aktuelle Menge:',
        'queue_wait': 'Wartezeit:',
        'temperature': 'Temperatur:',
        'sector_risk': 'Sektor-Risiko-Index:',
        'ai_predictions': 'KI-PROGNOSEN (15-60 Min.)',
        'click_predictions': 'Klicken Sie auf einen Sektor für KI-Prognosen...',
        'gemini_brain': 'Gemini OS Gehirn',
        'core_analysis': 'KERNANALYSE',
        'priority_actions': 'PRIORITÄRE BEDIENERAKTIONEN',
        'multilingual_announcement': 'MEHRSPRACHIGE DURCHSAGE',
        'fan_assistant_portal': 'Fan-Assistent-Portal',
        'chat_welcome': 'Hallo! Willkommen zur FIFA Fussball-Weltmeisterschaft 2026. Fragen Sie mich nach Toren, U-Bahn, WCs oder Restaurants.',
        'show_simulator': 'Simulator Anzeigen'
    },
    'ar': {
        'system_live': 'النظام نشط: سليم',
        'attendance': 'الحضور',
        'ai_risk': 'مؤشر المخاطر الذكي',
        'active_alerts': 'التنبيهات النشطة',
        'sustainability': 'الاستدامة',
        'realtime_logs': 'سجلات كاميرات المراقبة المباشرة',
        'hvac_solar': 'التكييف وشبكة الطاقة الشمسية',
        'stadium_3d_title': 'نموذج التوأم الرقمي ثلاثي الأبعاد',
        'live_map_title': 'خارطة المحيط والنقل المباشر',
        'realtime_dynamics': 'الديناميكيات المباشرة',
        'log_console': 'لوحة سجلات النظام',
        'emergency_command': 'مخفر الطوارئ',
        'simulate_alert': 'محاكاة الطوارئ',
        'reset': 'إعادة ضبط',
        'simulation_panel': 'لوحة التحكم في المحاكاة',
        'sim_testing_only': 'مخصص للتجربة والمحاكاة فقط',
        'weather_scenarios': 'السيناريوهات الجوية',
        'clear': 'صافي',
        'rain': 'مطر',
        'heatwave': 'موجة حر',
        'crowd_modifiers': 'معدلات كثافة الجمهور',
        'crowd_inc': 'زيادة الجمهور +20%',
        'crowd_dec': 'تقليل الجمهور -20%',
        'climate_thermostat': 'منظم حرارة المناخ',
        'temp_inc': 'الحرارة +3°م',
        'temp_dec': 'الحرارة -3°م',
        'power_outage': 'محاكاة انقطاع الكهرباء',
        'zone_telemetry': 'تفاصيل قطاع الملعب',
        'select_zone': 'اختر المدرج أو البوابة',
        'zone_type': 'نوع القطاع:',
        'current_crowd': 'الجمهور الحالي:',
        'queue_wait': 'انتظار الطابور:',
        'temperature': 'درجة الحرارة:',
        'sector_risk': 'مؤشر خطر القطاع:',
        'ai_predictions': 'توقعات الذكاء الاصطناعي (15-60 د)',
        'click_predictions': 'انقر على أي قطاع للاستعلام عن التوقعات...',
        'gemini_brain': 'عقل نظام جيميناي الذكي',
        'core_analysis': 'التحليل الأساسي للملعب',
        'priority_actions': 'الإجراءات التشغيلية ذات الأولوية',
        'multilingual_announcement': 'إذاعة الإعلان العام بلغات متعددة',
        'fan_assistant_portal': 'بوابة مساعدة المشجعين',
        'chat_welcome': 'أهلاً بك في كأس العالم 2026! اسألني عن البوابات، المترو، المطاعم، أو المفقودات.',
        'show_simulator': 'إظهار المحاكي'
    }
};

function setLanguage(lang) {
    const langNames = {
        'en': 'English',
        'es': 'Español',
        'fr': 'Français',
        'de': 'Deutsch',
        'ar': 'العربية'
    };
    
    const langBtn = document.getElementById('lang-current');
    if (langBtn) {
        langBtn.textContent = langNames[lang] || 'English';
    }

    // Set document direction for Arabic (RTL support!)
    if (lang === 'ar') {
        document.body.style.direction = 'rtl';
        document.body.style.textAlign = 'right';
    } else {
        document.body.style.direction = 'ltr';
        document.body.style.textAlign = 'left';
    }

    // Translate all selectors
    document.querySelectorAll('[data-translate]').forEach(el => {
        const key = el.getAttribute('data-translate');
        if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
            if (el.tagName === 'INPUT') {
                el.placeholder = TRANSLATIONS[lang][key];
            } else {
                el.textContent = TRANSLATIONS[lang][key];
            }
        }
    });

    if (window.logConsole) {
        window.logConsole('SYSTEM', `Language switched to: ${langNames[lang]}`, 'info');
    }
}

// Bind Lang elements
function initTranslationBindings() {
    document.querySelectorAll('.lang-opt').forEach(opt => {
        opt.addEventListener('click', (e) => {
            e.preventDefault();
            const lang = opt.getAttribute('data-lang');
            setLanguage(lang);
        });
    });
}

// Hooks
window.TRANSLATIONS = TRANSLATIONS;
window.setLanguage = setLanguage;
window.initTranslationBindings = initTranslationBindings;
