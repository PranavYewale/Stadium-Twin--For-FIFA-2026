// Dashboard Websocket and Chart Manager

let socket;
let crowdChart, utilityChart;
let crowdHistoryData = [];
let timelineLabels = [];

// Track active zone focus in dashboard
let activeZoneId = 'gate_a';
let allZonesData = {};

// Voice Narration State Caches
const spokenAlerts = new Set();
const congestedZones = new Set();

let httpPollingInterval = null;

function startHttpPolling() {
    if (httpPollingInterval) return;
    logConsole('SYSTEM', 'Initializing AJAX polling fallback loop (3s ticks)...', 'warning');
    
    pollStadiumStatus();
    httpPollingInterval = setInterval(pollStadiumStatus, 3000);
}

function pollStadiumStatus() {
    fetch('/api/simulation/status')
        .then(res => res.json())
        .then(data => {
            updateDashboardWidgets(data);
            updateZoneDetailsPanel(data.zones);
            if (window.update3DStadiumColors) {
                window.update3DStadiumColors(data.zones);
            }
            if (window.updateLiveMapState) {
                window.updateLiveMapState(data.zones);
            }
            
            // Sync with AI recommendations panel if present
            if (data.recommendations && data.recommendations.length > 0) {
                const recsList = document.getElementById('gemini-actions-list');
                const analysisSummary = document.getElementById('gemini-analysis-summary');
                const announcementBox = document.getElementById('gemini-announcement');
                
                if (recsList && analysisSummary && announcementBox) {
                    analysisSummary.textContent = data.recommendations[0].issue || 'All systems nominal.';
                    
                    let html = '';
                    data.recommendations.forEach(action => {
                        let priorityClass = 'badge bg-success';
                        if (action.priority === 'High' || action.priority === 'Critical') priorityClass = 'badge bg-danger';
                        else if (action.priority === 'Medium') priorityClass = 'badge bg-warning text-dark';
                        
                        html += `
                            <div class="p-2 mb-2 rounded bg-dark bg-opacity-20 border border-secondary">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="fw-bold" style="font-size: 13px">${action.title}</span>
                                    <span class="${priorityClass}" style="font-size: 10px">${action.priority}</span>
                                </div>
                                <span class="d-block text-secondary mb-1" style="font-size: 11px">LOCATION: ${action.location || 'Global'}</span>
                                <p class="m-0 text-white" style="font-size: 12.5px">${action.recommendation}</p>
                                <span class="d-block text-info mt-1" style="font-size: 11px">Outcome: ${action.expected_outcome || 'N/A'}</span>
                            </div>
                        `;
                    });
                    recsList.innerHTML = html;
                    
                    // Announcement fallback
                    if (data.alerts && data.alerts.length > 0) {
                        announcementBox.textContent = `ALERT BROADCAST: ${data.alerts[0].message}`;
                    } else {
                        announcementBox.textContent = `WELCOME: Welcome to MetLife Stadium digital twin command center! Make sure to inspect concessions waiting matrices.`;
                    }
                }
            }
            
            // Keep local cache
            data.zones.forEach(z => {
                allZonesData[z.id] = z;
            });
        })
        .catch(err => console.error("Polling error:", err));
}

function initDashboard() {
    // 1. Initialize WebSockets with reconnection configs
    socket = io({
        timeout: 4000,
        reconnectionDelay: 2000
    });
    
    // Set a timer to check if socket fails to connect
    const socketTimeout = setTimeout(() => {
        if (!socket.connected) {
            logConsole('SYSTEM', 'WebSocket connection timeout. Falling back to HTTP polling...', 'warning');
            startHttpPolling();
        }
    }, 4500);
    
    socket.on('connect', () => {
        clearTimeout(socketTimeout);
        logConsole('SYSTEM', 'Connected to Stadium Brain digital twin OS.', 'info');
        if (httpPollingInterval) {
            clearInterval(httpPollingInterval);
            httpPollingInterval = null;
        }
    });
    
    socket.on('connect_error', () => {
        clearTimeout(socketTimeout);
        logConsole('SYSTEM', 'WebSocket connection failed. Falling back to HTTP polling...', 'warning');
        startHttpPolling();
    });

    socket.on('stadium_update', (data) => {
        updateDashboardWidgets(data);
        updateZoneDetailsPanel(data.zones);
        
        // Feed Three.js and Leaflet
        if (window.update3DStadiumColors) {
            window.update3DStadiumColors(data.zones);
        }
        if (window.updateLiveMapState) {
            window.updateLiveMapState(data.zones);
        }

        // Keep local cache & check for new congestions
        data.zones.forEach(z => {
            allZonesData[z.id] = z;
            
            // Narrate if a zone has transitioned to Critical (Red) congestion
            if (z.status === 'Red') {
                if (!congestedZones.has(z.id)) {
                    congestedZones.add(z.id);
                    if (window.speakText) {
                        window.speakText(`Warning: ${z.name} has reached critical congestion levels.`);
                    }
                }
            } else {
                congestedZones.delete(z.id);
            }
        });

        // Feed logs & check for new alerts to narrate
        if (data.alerts && data.alerts.length > 0) {
            data.alerts.forEach(a => {
                if (!document.getElementById(`alert-${a.id}`)) {
                    addAlertToConsole(a);
                }
                
                // Voice narrate newly arrived warnings/critical alerts
                if (!spokenAlerts.has(a.id)) {
                    spokenAlerts.add(a.id);
                    if (window.speakText) {
                        const alertPrefix = a.level === 'critical' ? 'Emergency Alert: ' : 'Notification: ';
                        window.speakText(alertPrefix + a.message);
                    }
                }
            });
        }
        
        updateCharts(data);
    });

    socket.on('ai_recommendation', (data) => {
        updateGeminiRecommendations(data);
    });

    // 2. Initialize Charts
    initCharts();

    // 3. Bind UI buttons
    bindDashboardUI();
}

function initCharts() {
    // Crowd Trend Line Chart
    const ctx1 = document.getElementById('crowdChart');
    if (ctx1) {
        crowdChart = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Stadium Attendance',
                    data: [],
                    borderColor: '#00f0ff',
                    backgroundColor: 'rgba(0, 240, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Utilities Bar Chart
    const ctx2 = document.getElementById('utilityChart');
    if (ctx2) {
        utilityChart = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: ['Energy (kW)', 'Water (L/s)', 'CO2 (kg)'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: ['#9d4edd', '#00f0ff', '#ff0055'],
                    borderWidth: 0,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
}

function updateCharts(data) {
    // Update Crowd trend
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    
    crowdHistoryData.push(data.attendance);
    timelineLabels.push(timeStr);
    
    if (crowdHistoryData.length > 10) {
        crowdHistoryData.shift();
        timelineLabels.shift();
    }
    
    if (crowdChart) {
        crowdChart.data.labels = timelineLabels;
        crowdChart.data.datasets[0].data = crowdHistoryData;
        crowdChart.update('none'); // silent update
    }

    // Update utilities bar
    if (utilityChart && data.sustainability) {
        utilityChart.data.datasets[0].data = [
            data.sustainability.energy_kwh || 0,
            data.sustainability.water_liters || 0,
            data.sustainability.carbon_footprint_kg || 0
        ];
        utilityChart.update('none');
    }
}

function updateDashboardWidgets(data) {
    // Attendance
    const attElement = document.getElementById('val-attendance');
    if (attElement) attElement.textContent = data.attendance.toLocaleString();
    
    const attPctElement = document.getElementById('val-attendance-pct');
    if (attPctElement) {
        const pct = ((data.attendance / 80000) * 100).toFixed(1);
        attPctElement.textContent = `${pct}% Occupied`;
    }

    // Global Risk Level (Average)
    const riskVal = document.getElementById('val-risk');
    if (riskVal && data.zones) {
        const avgRisk = data.zones.reduce((acc, curr) => acc + curr.risk_score, 0) / data.zones.length;
        riskVal.textContent = `${avgRisk.toFixed(1)}%`;
        const riskBar = document.getElementById('val-risk-bar');
        if (riskBar) riskBar.style.width = `${avgRisk}%`;
    }

    // Active Alarms count
    const alarmsElement = document.getElementById('val-alerts');
    if (alarmsElement) {
        alarmsElement.textContent = data.alerts.length;
        if (data.alerts.length > 0) {
            alarmsElement.classList.add('text-danger');
        } else {
            alarmsElement.classList.remove('text-danger');
        }
    }

    // Sustainability score
    const susElement = document.getElementById('val-sustainability');
    if (susElement && data.sustainability) {
        susElement.textContent = `${(data.sustainability.sustainability_score || 100).toFixed(1)}%`;
    }

    // Weather Card
    if (data.weather) {
        const weatherIcon = document.getElementById('weather-indicator');
        if (weatherIcon) weatherIcon.textContent = `${data.weather.temp}°C - ${data.weather.condition}`;
    }

    // Live score details
    if (data.match_info) {
        const scoreSpan = document.getElementById('match-score-span');
        if (scoreSpan) scoreSpan.textContent = `${data.match_info.teams} (${data.match_info.score})`;
    }
}

function selectStadiumZone(zoneId) {
    activeZoneId = zoneId;
    logConsole('OPERATOR', `Focused inspection terminal on sector: ${zoneId}`, 'info');
    
    // Immediately redraw details panel
    if (allZonesData[zoneId]) {
        updateZoneDetailsPanel([allZonesData[zoneId]]);
    }
}

function updateZoneDetailsPanel(zonesArray) {
    const focusedZone = zonesArray.find(z => z.id === activeZoneId);
    if (!focusedZone) return;

    document.getElementById('zone-detail-name').textContent = focusedZone.name;
    document.getElementById('zone-detail-type').textContent = focusedZone.zone_type.toUpperCase();
    document.getElementById('zone-detail-crowd').textContent = `${focusedZone.current_crowd} / ${focusedZone.capacity}`;
    document.getElementById('zone-detail-queue').textContent = focusedZone.queue_length;
    document.getElementById('zone-detail-temp').textContent = `${focusedZone.temperature}°C`;
    document.getElementById('zone-detail-risk').textContent = `${focusedZone.risk_score}%`;
    
    // Status Badge
    const badge = document.getElementById('zone-detail-status');
    badge.className = `color-badge ${focusedZone.status.toLowerCase()}`;
    badge.textContent = focusedZone.status;
    
    // Fetch predictions details from REST API
    fetch(`/api/predictions/${activeZoneId}`)
        .then(res => res.json())
        .then(data => {
            const predContainer = document.getElementById('zone-detail-predictions');
            predContainer.innerHTML = '';
            
            if (data.predictions && data.predictions.length > 0) {
                data.predictions.forEach(p => {
                    const div = document.createElement('div');
                    div.className = 'd-flex justify-content-between align-items-center mb-1 text-secondary';
                    div.style.fontSize = '12.5px';
                    div.innerHTML = `
                        <span>+${p.time_offset} mins:</span>
                        <span><b>${p.predicted_crowd}</b> fans (Risk: ${p.risk_score}%)</span>
                    `;
                    predContainer.appendChild(div);
                });
            } else {
                predContainer.innerHTML = '<span class="text-secondary">Computing forecast vectors...</span>';
            }
        });
}

function updateGeminiRecommendations(data) {
    // Analysis Summary text
    const analysisDiv = document.getElementById('gemini-analysis-summary');
    if (analysisDiv) analysisDiv.textContent = data.analysis;

    // Multilingual announcements
    const announceDiv = document.getElementById('gemini-announcement');
    if (announceDiv) announceDiv.textContent = data.announcement;

    // Action cards
    const actionsContainer = document.getElementById('gemini-actions-list');
    if (actionsContainer) {
        actionsContainer.innerHTML = '';
        if (data.actions && data.actions.length > 0) {
            data.actions.forEach(act => {
                const card = document.createElement('div');
                card.className = 'glass-panel p-2 mb-2';
                card.style.borderLeft = `3px solid ${act.priority === 'High' ? 'var(--neon-red)' : 'var(--neon-cyan)'}`;
                card.innerHTML = `
                    <div class="d-flex justify-content-between mb-1">
                        <span class="fw-bold" style="font-size: 13.5px">${act.title}</span>
                        <span class="badge ${act.priority === 'High' ? 'bg-danger' : 'bg-secondary'}" style="font-size: 10px">${act.priority}</span>
                    </div>
                    <p class="text-secondary mb-1" style="font-size: 12px">${act.description}</p>
                    <div class="d-flex justify-content-between text-secondary" style="font-size: 11px">
                        <span>Deploy: ${act.volunteers_needed} staff</span>
                        <span style="color: var(--neon-green)">Est. Benefit: ${act.expected_outcome}</span>
                    </div>
                `;
                actionsContainer.appendChild(card);
            });
        } else {
            actionsContainer.innerHTML = '<div class="text-secondary text-center">AI analysis clear. Nominal conditions.</div>';
        }
    }
}

function addAlertToConsole(alert) {
    const consoleDiv = document.getElementById('console-log-feed');
    if (!consoleDiv) return;

    const timeStr = new Date(alert.timestamp).toLocaleTimeString();
    const entry = document.createElement('div');
    entry.id = `alert-${alert.id}`;
    entry.className = `log-entry ${alert.level.toLowerCase()}`;
    entry.innerHTML = `[${timeStr}] <b>${alert.level.toUpperCase()}</b>: ${alert.message}`;
    
    consoleDiv.insertBefore(entry, consoleDiv.firstChild);
    
    // Play alert sound or blink if critical
    if (alert.level === 'critical') {
        logConsole('ALERT', `Active danger vector flagged at ${alert.zone_id}!`, 'critical');
    }
}

function logConsole(source, msg, level = 'info') {
    const consoleDiv = document.getElementById('console-log-feed');
    if (!consoleDiv) return;

    const timeStr = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = `log-entry ${level}`;
    entry.innerHTML = `[${timeStr}] <b>${source.toUpperCase()}</b>: ${msg}`;
    consoleDiv.insertBefore(entry, consoleDiv.firstChild);
}

function bindDashboardUI() {
    // Emergency Trigger Button
    const btnEmergency = document.getElementById('btn-trigger-emergency');
    if (btnEmergency) {
        btnEmergency.addEventListener('click', () => {
            if (confirm("WARNING: Confirm stadium-wide critical emergency simulation?")) {
                fetch('/api/emergency/trigger', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        type: 'Fire Alarm',
                        message: 'Smoke and fire indicators detected in East Concourse. Activate all exits.',
                        zone_id: 'gate_b'
                    })
                })
                .then(res => res.json())
                .then(data => {
                    logConsole('EMERGENCY', 'CRITICAL EVACUATION SIRENS ACTIVE.', 'critical');
                });
            }
        });
    }

    // Emergency Reset Button
    const btnReset = document.getElementById('btn-reset-operations');
    if (btnReset) {
        btnReset.addEventListener('click', () => {
            fetch('/api/emergency/resolve', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    logConsole('SYSTEM', 'All emergency protocols resolved. Returning to normal state.', 'info');
                    showNotification('SYSTEM COMMAND', 'All emergency logs resolved. Nominal operations restored.', 'success');
                });
        });
    }

    // Weather scenario buttons
    document.querySelectorAll('.btn-sim-weather').forEach(btn => {
        btn.addEventListener('click', () => {
            const weatherVal = btn.getAttribute('data-weather');
            fetch('/api/simulation/override', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ weather_condition: weatherVal })
            })
            .then(res => res.json())
            .then(data => {
                logConsole('SIMULATOR', `Weather scenario set to: ${weatherVal}`, 'info');
                document.querySelectorAll('.btn-sim-weather').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Show toast notification
                let toastType = 'info';
                let msg = `Climate scenario set to normal weather.`;
                if (weatherVal === 'Heavy Rain') {
                    toastType = 'warning';
                    msg = 'Heavy rainstorm scenario activated stadium-wide.';
                } else if (weatherVal === 'Heatwave') {
                    toastType = 'danger';
                    msg = 'Extreme heatwave scenario active. Utility cooling grid load elevated.';
                }
                showNotification('WEATHER SCENARIO', msg, toastType);
            });
        });
    });

    // Crowd scale modifiers
    let currentCrowdScale = 1.0;
    const btnCrowdInc = document.getElementById('btn-sim-crowd-inc');
    const btnCrowdDec = document.getElementById('btn-sim-crowd-dec');
    
    if (btnCrowdInc) {
        btnCrowdInc.addEventListener('click', () => {
            currentCrowdScale = parseFloat((currentCrowdScale * 1.2).toFixed(2));
            fetch('/api/simulation/override', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ crowd_scale: currentCrowdScale })
            })
            .then(res => res.json())
            .then(data => {
                logConsole('SIMULATOR', `Crowd scaling adjusted to: ${Math.round(currentCrowdScale * 100)}%`, 'warning');
                showNotification('CROWD MODIFIER', `Spectator volume scaled up to ${Math.round(currentCrowdScale * 100)}%.`, 'warning');
            });
        });
    }
    
    if (btnCrowdDec) {
        btnCrowdDec.addEventListener('click', () => {
            currentCrowdScale = parseFloat((currentCrowdScale * 0.8).toFixed(2));
            fetch('/api/simulation/override', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ crowd_scale: currentCrowdScale })
            })
            .then(res => res.json())
            .then(data => {
                logConsole('SIMULATOR', `Crowd scaling adjusted to: ${Math.round(currentCrowdScale * 100)}%`, 'info');
                showNotification('CROWD MODIFIER', `Spectator volume scaled down to ${Math.round(currentCrowdScale * 100)}%.`, 'info');
            });
        });
    }

    // Thermostat climate modifiers
    let currentTempAdjust = 0.0;
    const btnTempInc = document.getElementById('btn-sim-temp-inc');
    const btnTempDec = document.getElementById('btn-sim-temp-dec');
    
    if (btnTempInc) {
        btnTempInc.addEventListener('click', () => {
            currentTempAdjust += 3.0;
            fetch('/api/simulation/override', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ temp_adjust: currentTempAdjust })
            })
            .then(res => res.json())
            .then(data => {
                logConsole('SIMULATOR', `Climate thermostat offset set to: +${currentTempAdjust}°C`, 'warning');
                showNotification('THERMOSTAT MODIFIER', `Climate thermostat offset increased to +${currentTempAdjust}°C.`, 'warning');
            });
        });
    }
    
    if (btnTempDec) {
        btnTempDec.addEventListener('click', () => {
            currentTempAdjust -= 3.0;
            fetch('/api/simulation/override', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ temp_adjust: currentTempAdjust })
            })
            .then(res => res.json())
            .then(data => {
                logConsole('SIMULATOR', `Climate thermostat offset set to: ${currentTempAdjust}°C`, 'info');
                showNotification('THERMOSTAT MODIFIER', `Climate thermostat offset decreased to ${currentTempAdjust}°C.`, 'info');
            });
        });
    }

    // Power Cut Toggle Button
    let powerCutActive = false;
    const btnPowerCut = document.getElementById('btn-sim-power-cut');
    if (btnPowerCut) {
        btnPowerCut.addEventListener('click', () => {
            powerCutActive = !powerCutActive;
            fetch('/api/simulation/override', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ power_cut: powerCutActive })
            })
            .then(res => res.json())
            .then(data => {
                if (powerCutActive) {
                    btnPowerCut.classList.remove('btn-outline-danger');
                    btnPowerCut.classList.add('btn-danger');
                    btnPowerCut.innerHTML = '<i class="fa-solid fa-plug-circle-check me-1"></i>Restore Grid Power';
                    logConsole('SIMULATOR', 'CRITICAL POWER GRID OUTAGE TRIGGERED.', 'critical');
                    showNotification('UTILITY INCIDENT', 'CRITICAL: Grid power outage triggered! Back-up solar batteries loaded.', 'danger');
                } else {
                    btnPowerCut.classList.remove('btn-danger');
                    btnPowerCut.classList.add('btn-outline-danger');
                    btnPowerCut.innerHTML = '<i class="fa-solid fa-plug-circle-xmark me-1"></i>Trigger Power Outage';
                    logConsole('SIMULATOR', 'Grid power restored. Generators offline.', 'info');
                    showNotification('UTILITY RESTORED', 'Main power grid restored. Backup diesel generators returned offline.', 'success');
                }
            });
        });
    }

    // Simulator Hide/Show toggles
    const btnCloseSim = document.getElementById('btn-close-sim');
    const simCard = document.getElementById('simulation-panel-card');
    const btnToggleSim = document.getElementById('btn-toggle-sim-panel');
    
    if (btnCloseSim && simCard && btnToggleSim) {
        btnCloseSim.addEventListener('click', () => {
            simCard.classList.add('d-none');
            btnToggleSim.classList.remove('d-none');
            logConsole('SIMULATOR', 'Simulation panel hidden. Click "Show Simulator" in navbar to restore.', 'info');
        });
        
        btnToggleSim.addEventListener('click', () => {
            simCard.classList.remove('d-none');
            btnToggleSim.classList.add('d-none');
            logConsole('SIMULATOR', 'Simulation panel restored.', 'info');
        });
    }
}

window.selectStadiumZone = selectStadiumZone;
window.initDashboard = initDashboard;

function showNotification(title, message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `glass-toast toast-type-${type}`;
    toast.style.pointerEvents = 'auto';
    
    let icon = 'fa-circle-info text-info';
    if (type === 'success') icon = 'fa-circle-check text-success';
    if (type === 'warning') icon = 'fa-triangle-exclamation text-warning';
    if (type === 'danger') icon = 'fa-circle-exclamation text-danger';

    toast.innerHTML = `
        <div class="glass-toast-header">
            <div>
                <i class="fa-solid ${icon} me-2"></i>
                <span>${title}</span>
            </div>
            <button type="button" class="btn-close-toast" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
        <div class="glass-toast-body">${message}</div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-fade-out');
        setTimeout(() => toast.remove(), 400);
    }, 4500);
}

window.showNotification = showNotification;
