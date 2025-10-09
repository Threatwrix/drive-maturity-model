// DRIVE Maturity Model - Main JavaScript

// State management
let allChecks = [];
let filteredChecks = [];

// Load checks from YAML files or catalog
async function loadChecks() {
    try {
        // For now, load from the catalog JSON
        // In production, this would aggregate all YAML files
        const response = await fetch('catalog/drive_risk_catalog.json');
        const checks = await response.json();

        allChecks = checks;
        filteredChecks = checks;
        renderChecks();
    } catch (error) {
        console.error('Error loading checks:', error);
        document.getElementById('checks-list').innerHTML = `
            <div class="loading">
                <p>Error loading security checks. Please ensure the catalog is available.</p>
                <p style="font-size: 0.9rem; color: var(--color-text-light); margin-top: 16px;">
                    Note: GitHub Pages may require a build step to aggregate YAML files.
                </p>
            </div>
        `;
    }
}

// Render checks list
function renderChecks() {
    const container = document.getElementById('checks-list');

    if (filteredChecks.length === 0) {
        container.innerHTML = `
            <div class="loading">No checks match your filters.</div>
        `;
        return;
    }

    container.innerHTML = filteredChecks.map(check => `
        <div class="check-item" onclick="showCheckDetail('${check.check_id}')">
            <div class="check-id">${check.check_id}</div>
            <div class="check-title">${check.title}</div>
            <div class="check-meta">
                <span class="badge badge-${getSeverityClass(check.severity)}">
                    ${check.severity}
                </span>
                <span class="timeline">${check.platform}</span>
                <span class="timeline">Level ${check.drive_maturity_min || 'N/A'}</span>
                ${check.drive_pillar ? `<span class="timeline">${check.drive_pillar}</span>` : ''}
            </div>
        </div>
    `).join('');
}

// Get severity class for badge styling
function getSeverityClass(severity) {
    const severityLower = (severity || 'medium').toLowerCase();
    return severityLower;
}

// Show check detail modal
function showCheckDetail(checkId) {
    const check = allChecks.find(c => c.check_id === checkId);
    if (!check) return;

    const modal = document.getElementById('check-modal');
    const modalBody = document.getElementById('modal-body');

    // Build modal content
    modalBody.innerHTML = `
        <div class="check-detail">
            <div class="check-detail-header">
                <h2>${check.check_id}: ${check.title}</h2>
                <div class="check-meta">
                    <span class="badge badge-${getSeverityClass(check.severity)}">${check.severity}</span>
                    <span class="timeline">${check.platform}</span>
                    <span class="timeline">Level ${check.drive_maturity_min || 'N/A'}</span>
                </div>
            </div>

            <div class="check-detail-section">
                <h3>Description</h3>
                <p>${check.description || 'No description available.'}</p>
            </div>

            ${check.logic ? `
                <div class="check-detail-section">
                    <h3>Detection Logic</h3>
                    <p>${check.logic}</p>
                </div>
            ` : ''}

            ${check.data_points ? `
                <div class="check-detail-section">
                    <h3>Data Points</h3>
                    <p>${check.data_points}</p>
                </div>
            ` : ''}

            <div class="check-detail-section">
                <h3>Framework Mappings</h3>
                <div class="framework-mappings">
                    ${check.nist_csf_function ? `<div><strong>NIST CSF:</strong> ${check.nist_csf_function} ${check.nist_csf_id || ''}</div>` : ''}
                    ${check.cis_v8_control ? `<div><strong>CIS v8:</strong> ${check.cis_v8_control}</div>` : ''}
                    ${check.cis_m365_benchmark ? `<div><strong>CIS M365:</strong> ${check.cis_m365_benchmark}</div>` : ''}
                    ${check.iso_27001_annex ? `<div><strong>ISO 27001:</strong> ${check.iso_27001_annex}</div>` : ''}
                </div>
            </div>

            ${check.tags ? `
                <div class="check-detail-section">
                    <h3>Tags</h3>
                    <p>${check.tags}</p>
                </div>
            ` : ''}

            <div class="check-detail-section">
                <h3>DRIVE Classification</h3>
                <div class="drive-classification">
                    <div><strong>Pillar:</strong> ${getDrivePillarName(check.drive_pillar)}</div>
                    <div><strong>Minimum Maturity Level:</strong> ${check.drive_maturity_min}</div>
                    <div><strong>Weight:</strong> ${check.drive_weight || 'N/A'}</div>
                </div>
            </div>

            <div class="check-detail-actions">
                <button class="btn btn-primary" onclick="window.open('https://github.com/Threatwrix/drive-risk-catalog', '_blank')">
                    View on GitHub
                </button>
            </div>
        </div>
    `;

    modal.style.display = 'block';
}

// Get DRIVE pillar full name
function getDrivePillarName(pillar) {
    const pillarNames = {
        'D': 'Data Protection',
        'R': 'Risk Management',
        'I': 'Identity Security',
        'V': 'Vulnerability Management',
        'E': 'Exposure Analysis'
    };
    return pillarNames[pillar] || pillar;
}

// Filter checks
function filterChecks() {
    const platformFilter = document.getElementById('platform-filter').value;
    const levelFilter = document.getElementById('level-filter').value;
    const pillarFilter = document.getElementById('pillar-filter').value;
    const searchTerm = document.getElementById('search-input').value.toLowerCase();

    filteredChecks = allChecks.filter(check => {
        // Platform filter
        if (platformFilter && check.platform !== platformFilter) {
            return false;
        }

        // Level filter
        if (levelFilter && check.drive_maturity_min != levelFilter) {
            return false;
        }

        // Pillar filter
        if (pillarFilter && check.drive_pillar !== pillarFilter) {
            return false;
        }

        // Search filter
        if (searchTerm) {
            const searchableText = `${check.check_id} ${check.title} ${check.description || ''}`.toLowerCase();
            if (!searchableText.includes(searchTerm)) {
                return false;
            }
        }

        return true;
    });

    renderChecks();
}

// Modal controls
function closeModal() {
    document.getElementById('check-modal').style.display = 'none';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load checks
    loadChecks();

    // Set up filter event listeners
    document.getElementById('platform-filter').addEventListener('change', filterChecks);
    document.getElementById('level-filter').addEventListener('change', filterChecks);
    document.getElementById('pillar-filter').addEventListener('change', filterChecks);
    document.getElementById('search-input').addEventListener('input', filterChecks);

    // Modal close button
    document.querySelector('.close').addEventListener('click', closeModal);

    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        const modal = document.getElementById('check-modal');
        if (event.target === modal) {
            closeModal();
        }
    });

    // Smooth scrolling for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Draw control graph
    drawControlGraph();
});

// Draw control graph (placeholder - would use Chart.js or D3.js in production)
function drawControlGraph() {
    const canvas = document.getElementById('control-graph-canvas');
    const container = document.getElementById('control-graph-container');

    // Placeholder text
    container.innerHTML = `
        <div style="text-align: center; padding: 48px; color: var(--color-text-light);">
            <h3 style="margin-bottom: 16px; color: var(--color-primary);">Control Graph Visualization</h3>
            <p>Interactive control graph will be rendered here using D3.js or Chart.js.</p>
            <p style="margin-top: 16px; font-size: 0.9rem;">
                This will show:
            </p>
            <ul style="list-style: none; margin-top: 16px; line-height: 2;">
                <li>✓ Check distribution across maturity levels</li>
                <li>✓ Platform coverage visualization</li>
                <li>✓ DRIVE pillar breakdown</li>
                <li>✓ Framework mapping coverage</li>
            </ul>
        </div>
    `;
}

// Additional styling for modal content
const style = document.createElement('style');
style.textContent = `
    .check-detail {
        max-height: 70vh;
        overflow-y: auto;
    }

    .check-detail-header {
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 2px solid var(--color-border);
    }

    .check-detail-header h2 {
        margin-bottom: 12px;
        color: var(--color-primary);
    }

    .check-detail-section {
        margin-bottom: 24px;
    }

    .check-detail-section h3 {
        font-size: 1.2rem;
        color: var(--color-secondary);
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--color-border);
    }

    .framework-mappings div {
        margin-bottom: 8px;
        padding: 8px;
        background: var(--color-bg-dark);
        border-radius: 4px;
    }

    .framework-mappings strong {
        color: var(--color-primary);
        margin-right: 8px;
    }

    .drive-classification div {
        margin-bottom: 8px;
        padding: 8px;
        background: var(--color-bg-dark);
        border-radius: 4px;
    }

    .drive-classification strong {
        color: var(--color-primary);
        margin-right: 8px;
    }

    .check-detail-actions {
        margin-top: 24px;
        padding-top: 16px;
        border-top: 1px solid var(--color-border);
        text-align: center;
    }

    .btn {
        padding: 12px 24px;
        border: none;
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        text-decoration: none;
        display: inline-block;
    }

    .btn-primary {
        background: var(--color-primary);
        color: white;
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 35, 126, 0.3);
    }
`;
document.head.appendChild(style);
