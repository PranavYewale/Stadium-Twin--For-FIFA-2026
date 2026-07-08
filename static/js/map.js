// Leaflet.js Traffic and Transit Mapping

let map;
let markersMap = {};
let heatCircles = {};

// Coordinates around MetLife Stadium (FIFA World Cup 2026 Venue)
const STADIUM_COORDS = [40.8135, -74.0743];

const MAP_LOCATIONS = {
    'gate_a': { coords: [40.8148, -74.0743], name: 'Gate A (North)' },
    'gate_b': { coords: [40.8135, -74.0722], name: 'Gate B (East)' },
    'gate_c': { coords: [40.8135, -74.0764], name: 'Gate C (West)' },
    'vip_entrance': { coords: [40.8118, -74.0743], name: 'VIP Club Entrance' },
    'parking_east': { coords: [40.8140, -74.0680], name: 'Parking Lot East' },
    'parking_west': { coords: [40.8130, -74.0810], name: 'Parking Lot West' },
    'parking_vip': { coords: [40.8105, -74.0743], name: 'VIP Parking Lot' },
    'metro_station': { coords: [40.8170, -74.0720], name: 'Metro Transit Hub' },
    'bus_stop': { coords: [40.8100, -74.0780], name: 'Stadium Bus Terminal' }
};

const COLOR_MAP = {
    'Green': '#39ff14',
    'Yellow': '#ffff00',
    'Orange': '#ff9e00',
    'Red': '#ff0055'
};

function initLiveMap() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // 1. Initialize Map on Stadium
    map = L.map('map', {
        center: STADIUM_COORDS,
        zoom: 15,
        zoomControl: false,
        attributionControl: false
    });

    // 2. Load Dark Mode Tile Layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 20
    }).addTo(map);

    // 3. Add Main Stadium Circle
    const stadiumBoundary = L.circle(STADIUM_COORDS, {
        color: '#00f0ff',
        fillColor: '#1e293b',
        fillOpacity: 0.2,
        radius: 180,
        weight: 2
    }).addTo(map);
    stadiumBoundary.bindPopup("<b>FIFA World Cup 2026 Arena</b>");

    // 4. Render Markers and Dynamic Telemetry Heat-Circles
    Object.keys(MAP_LOCATIONS).forEach(id => {
        const loc = MAP_LOCATIONS[id];
        
        // Add Marker
        const marker = L.marker(loc.coords).addTo(map);
        marker.bindPopup(`<b>${loc.name}</b><br><span id="popup-${id}">Loading status...</span>`);
        
        // Set up click action to match 3D select
        marker.on('click', () => {
            if (window.selectStadiumZone) {
                window.selectStadiumZone(id);
            }
        });
        
        markersMap[id] = marker;

        // Add Heat-Circle (Simulates crowd density heatmap layer)
        const circle = L.circle(loc.coords, {
            color: '#39ff14',
            fillColor: '#39ff14',
            fillOpacity: 0.15,
            radius: 80,
            weight: 1
        }).addTo(map);
        
        heatCircles[id] = circle;
    });
}

// Websocket callback to update positions and sizes dynamically
function updateLiveMapState(zonesArray) {
    if (!zonesArray || !map) return;

    zonesArray.forEach(z => {
        const circle = heatCircles[z.id];
        const marker = markersMap[z.id];
        
        if (circle && marker) {
            const status = z.status || 'Green';
            const color = COLOR_MAP[status] || '#39ff14';
            
            // Adjust radius and color based on congestion
            const fillRatio = z.current_crowd / maxVal(1, z.capacity);
            const radius = 60 + (fillRatio * 90); // Swell radius based on size
            
            circle.setRadius(radius);
            circle.setStyle({
                color: color,
                fillColor: color,
                fillOpacity: 0.12 + (fillRatio * 0.15)
            });

            // Update Popup telemetry details
            const popupContent = `
                Type: ${z.zone_type.toUpperCase()}<br>
                Occupancy: ${z.current_crowd} / ${z.capacity}<br>
                Queue Wait: ${z.queue_length} people<br>
                <b>Risk Index: ${z.risk_score}% [${z.status}]</b>
            `;
            marker.setPopupContent(`<b>${z.name}</b><br>${popupContent}`);
        }
    });
}

function maxVal(a, b) {
    return a > b ? a : b;
}

let activeFlashCircle = null;

function flashMapMarker(zoneId) {
    if (!map) return;
    const loc = MAP_LOCATIONS[zoneId];
    if (!loc) return;
    
    // Clear old flash circle
    if (activeFlashCircle) {
        map.removeLayer(activeFlashCircle);
    }
    
    // Create new flashing circle
    activeFlashCircle = L.circle(loc.coords, {
        color: '#ff0055',
        fillColor: '#ff0055',
        fillOpacity: 0.5,
        radius: 120,
        weight: 3
    }).addTo(map);
    
    // Pan to the location
    map.panTo(loc.coords);
    
    // Make it pulse visually
    let growing = true;
    let radius = 120;
    const interval = setInterval(() => {
        if (!activeFlashCircle || !map.hasLayer(activeFlashCircle)) {
            clearInterval(interval);
            return;
        }
        if (growing) {
            radius += 8;
            if (radius > 180) growing = false;
        } else {
            radius -= 8;
            if (radius < 70) growing = true;
        }
        activeFlashCircle.setRadius(radius);
    }, 50);
    
    // Auto remove after 15 seconds
    setTimeout(() => {
        if (activeFlashCircle) {
            map.removeLayer(activeFlashCircle);
            activeFlashCircle = null;
        }
    }, 15000);
}

// Global hooks
window.initLiveMap = initLiveMap;
window.updateLiveMapState = updateLiveMapState;
window.flashMapMarker = flashMapMarker;
