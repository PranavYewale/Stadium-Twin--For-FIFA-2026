// Specialist Assistant Operations Bindings

function initAssistantConsole() {
    // 1. Lost Child Search Grid
    const btnLcSearch = document.getElementById('btn-lc-search');
    if (btnLcSearch) {
        btnLcSearch.addEventListener('click', () => {
            const name = document.getElementById('lc-name').value || 'Missing Child';
            const color = document.getElementById('lc-shirt').value || 'Unknown shirt';
            const lastSeen = document.getElementById('lc-last-seen').value;

            fetch('/api/assistant/lost-child', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, color: color, last_seen: lastSeen })
            })
            .then(res => res.json())
            .then(data => {
                const resultBox = document.getElementById('lc-result');
                const resultMsg = document.getElementById('lc-result-msg');
                const resultZone = document.getElementById('lc-result-zone');

                if (resultBox && resultMsg && resultZone) {
                    resultBox.classList.remove('d-none');
                    resultMsg.textContent = data.message;
                    resultZone.textContent = data.spotted_zone.name;
                }

                // Log to operations console
                if (window.logConsole) {
                    window.logConsole('SEARCH GRID', `AI Camera spotted ${name} near ${data.spotted_zone.name}! Volunteer notifications sent.`, 'critical');
                }

                // Voice Narration Alert
                if (window.speakText) {
                    window.speakText(`Alert: missing person matching profile spotted near ${data.spotted_zone.name}. Volunteer dispatch active.`);
                }

                // Trigger flashing Leaflet GIS map marker
                if (window.flashMapMarker) {
                    window.flashMapMarker(data.spotted_zone.id);
                }
            });
        });
    }

    // 2. Digital Accessibility Planner
    let selectedAccessType = 'wheelchair';
    document.querySelectorAll('.btn-acc-type').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.btn-acc-type').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedAccessType = btn.getAttribute('data-type');
        });
    });

    const btnAccGenerate = document.getElementById('btn-acc-generate');
    if (btnAccGenerate) {
        btnAccGenerate.addEventListener('click', () => {
            const source = document.getElementById('acc-source').value;
            const dest = document.getElementById('acc-dest').value;

            fetch('/api/assistant/accessibility', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source: source, destination: dest, type: selectedAccessType })
            })
            .then(res => res.json())
            .then(data => {
                const routeBox = document.getElementById('acc-route-box');
                const waitTime = document.getElementById('acc-wait-time');
                const seating = document.getElementById('acc-seating');
                const directionsList = document.getElementById('acc-directions-list');

                if (routeBox && waitTime && seating && directionsList) {
                    routeBox.classList.remove('d-none');
                    waitTime.textContent = `${data.elevator_wait_min} mins`;
                    seating.textContent = data.seating_block;

                    directionsList.innerHTML = '';
                    data.route.forEach(step => {
                        const li = document.createElement('li');
                        li.textContent = step;
                        directionsList.appendChild(li);
                    });

                    // Log to console
                    if (window.logConsole) {
                        window.logConsole('ACCESSIBILITY', `Step-free route compiled. Estimated elevator wait time: ${data.elevator_wait_min}m.`, 'info');
                    }

                    // Visual/Voice guide for Visually Impaired
                    if (selectedAccessType === 'visually_impaired' && window.speakText) {
                        window.speakText("Accessibility Audio Guide activated: " + data.route.join(". "));
                    }
                }
            });
        });
    }

    // 3. AI Queue Optimizer
    const btnQueueApply = document.getElementById('btn-queue-apply');
    if (btnQueueApply) {
        btnQueueApply.addEventListener('click', () => {
            fetch('/api/assistant/queue-optimize', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    const logBox = document.getElementById('queue-opt-log');
                    if (logBox) {
                        logBox.classList.remove('d-none');
                        logBox.innerHTML = `<i class="fa-solid fa-circle-check me-1"></i>${data.actions.join(', ')}`;
                    }

                    // Reset visual cues in table
                    const qNCurr = document.getElementById('q-n-curr');
                    const qNFore = document.getElementById('q-n-fore');
                    if (qNCurr && qNFore) {
                        qNCurr.textContent = '8 mins';
                        qNFore.textContent = '10 mins';
                        qNFore.className = 'text-success';
                    }

                    if (window.logConsole) {
                        window.logConsole('QUEUE AI', 'Predictive balance applied. Staff reallocated, queues optimized.', 'info');
                    }
                });
        });
    }

    // 4. Fan Sentiment Analyzer (Background Loop)
    function runSentimentUpdates() {
        fetch('/api/assistant/sentiment')
            .then(res => res.json())
            .then(data => {
                const score = document.getElementById('sentiment-happiness-score');
                const hotspots = document.getElementById('sentiment-hotspots');
                const tags = document.getElementById('sentiment-tags');
                
                if (score) {
                    score.textContent = `${data.happiness_score}%`;
                    if (data.happiness_score > 75) {
                        score.className = 'text-success';
                    } else {
                        score.className = 'text-warning';
                    }
                }

                if (hotspots) {
                    hotspots.innerHTML = '';
                    data.hotspots.forEach(h => {
                        const div = document.createElement('div');
                        div.innerHTML = `• <b class="text-warning">${h.location}</b>: ${h.issue}`;
                        hotspots.appendChild(div);
                    });
                }

                if (tags) {
                    tags.innerHTML = '';
                    data.trending_tags.forEach(t => {
                        const span = document.createElement('span');
                        span.className = 'badge bg-secondary';
                        span.style.fontSize = '8.5px';
                        span.textContent = `${t.tag} (x${t.count})`;
                        tags.appendChild(span);
                    });
                }

                // Update Feedback Ticker with a random post
                const postBox = document.getElementById('sentiment-feed-post');
                if (postBox && data.feed && data.feed.length > 0) {
                    const randomPost = data.feed[Math.floor(Math.random() * data.feed.length)];
                    postBox.innerHTML = `<b>${randomPost.user}</b>: "${randomPost.text}"`;
                    if (randomPost.sentiment === 'positive') {
                        postBox.style.color = '#39ff14'; // positive neon green
                    } else {
                        postBox.style.color = '#ff9e00'; // negative orange
                    }
                }
            });
    }

    // Run first update and tick every 10 seconds
    runSentimentUpdates();
    setInterval(runSentimentUpdates, 10000);

    // 5. Header Navigation shortcuts binding (SPA Paging View Switcher)
    function switchDashboardView(viewName) {
        const grid = document.querySelector('.dashboard-grid');
        if (!grid) return;

        // Reset grid classes
        grid.classList.remove('view-single-right', 'view-split-equal');

        // Toggle Active Link states
        document.querySelectorAll('.nav-shortcut').forEach(link => {
            link.classList.remove('active', 'text-info');
            link.classList.add('text-secondary');
            if (link.getAttribute('data-view') === viewName) {
                link.classList.add('active', 'text-info');
                link.classList.remove('text-secondary');
            }
        });

        const allPanels = document.querySelectorAll('.glass-panel');
        
        if (viewName === 'overview') {
            allPanels.forEach(p => {
                if (p.id === 'gemini-panel-card' || p.id === 'fan-portal-card') {
                    p.classList.add('hidden-by-view');
                } else {
                    p.classList.remove('hidden-by-view', 'focused-by-view');
                }
            });
            if (window.map) {
                setTimeout(() => window.map.invalidateSize(), 150);
            }
            return;
        }

        // Hide all by default
        allPanels.forEach(p => {
            p.classList.add('hidden-by-view');
            p.classList.remove('focused-by-view');
        });

        // Helper references
        const mapCard = document.getElementById('map') ? document.getElementById('map').closest('.glass-panel') : null;
        const assistCard = document.getElementById('assistantTabs') ? document.getElementById('assistantTabs').closest('.glass-panel') : null;

        if (viewName === 'gemini') {
            grid.classList.add('view-single-right');
            const card = document.getElementById('gemini-panel-card');
            if (card) card.classList.remove('hidden-by-view');
        } else if (viewName === 'lost-child') {
            grid.classList.add('view-split-equal');
            const tab = document.getElementById('lost-child-tab');
            if (tab) tab.click();
            if (mapCard) mapCard.classList.remove('hidden-by-view');
            if (assistCard) assistCard.classList.remove('hidden-by-view');
        } else if (viewName === 'access') {
            grid.classList.add('view-split-equal');
            const tab = document.getElementById('access-tab');
            if (tab) tab.click();
            if (mapCard) mapCard.classList.remove('hidden-by-view');
            if (assistCard) assistCard.classList.remove('hidden-by-view');
        } else if (viewName === 'queue') {
            grid.classList.add('view-single-right');
            const tab = document.getElementById('queue-tab');
            if (tab) tab.click();
            if (assistCard) assistCard.classList.remove('hidden-by-view');
        } else if (viewName === 'sentiment') {
            grid.classList.add('view-single-right');
            const tab = document.getElementById('sentiment-tab');
            if (tab) tab.click();
            if (assistCard) assistCard.classList.remove('hidden-by-view');
        } else if (viewName === 'chat') {
            grid.classList.add('view-single-right');
            const card = document.getElementById('fan-portal-card');
            if (card) card.classList.remove('hidden-by-view');
        }

        // Force Leaflet map tiles update if map is displayed
        if ((viewName === 'lost-child' || viewName === 'access') && window.map) {
            setTimeout(() => window.map.invalidateSize(), 150);
        }
    }

    document.querySelectorAll('.nav-shortcut').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const view = link.getAttribute('data-view');
            if (view) {
                switchDashboardView(view);
            }
        });
    });

    const logoBtn = document.getElementById('brand-logo-btn');
    if (logoBtn) {
        logoBtn.addEventListener('click', (e) => {
            e.preventDefault();
            switchDashboardView('overview');
        });
    }
}

// Attach to global hooks
window.initAssistantConsole = initAssistantConsole;
