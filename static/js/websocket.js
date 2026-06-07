/**
 * WebSocket client for live gas monitoring updates.
 */
(function () {
    'use strict';

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/gas/`;

    window.GasWebSocket = {
        socket: null,
        listeners: [],

        connect: function () {
            if (this.socket && this.socket.readyState <= WebSocket.OPEN) {
                return;
            }

            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                this._notify('connection', { status: 'connected' });
                this._updateConnectionBadge('connected');
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this._notify('message', data);
                    if (data.type === 'gas_update') {
                        this._handleGasUpdate(data);
                    }
                } catch (e) {
                    console.error('WebSocket parse error:', e);
                }
            };

            this.socket.onclose = () => {
                this._notify('connection', { status: 'disconnected' });
                this._updateConnectionBadge('disconnected');
                setTimeout(() => this.connect(), 5000);
            };

            this.socket.onerror = () => {
                this._updateConnectionBadge('error');
            };
        },

        on: function (event, callback) {
            this.listeners.push({ event, callback });
        },

        _notify: function (event, data) {
            this.listeners.forEach((l) => {
                if (l.event === event) l.callback(data);
            });
        },

        _updateConnectionBadge: function (status) {
            const badge = document.getElementById('connection-status');
            if (!badge) return;

            const map = {
                connected: ['bg-success', 'Live'],
                disconnected: ['bg-warning text-dark', 'Reconnecting...'],
                error: ['bg-danger', 'Connection Error'],
            };
            const [cls, text] = map[status] || ['bg-secondary', 'Connecting...'];
            badge.className = `badge ${cls}`;
            badge.textContent = text;
        },

        _handleGasUpdate: function (data) {
            if (data.reading) {
                this._updateReadingRow(data.reading);
            }
            if (data.alert) {
                this._showAlertToast(data.alert);
                this._incrementAlertCount();
            }
            this._updateLastUpdated();
        },

        _updateReadingRow: function (reading) {
            const row = document.querySelector(`#readings-table tr[data-room-id="${reading.room_id}"]`);
            if (!row) return;

            const levelCell = row.querySelector('.gas-level');
            const statusCell = row.querySelector('.status-badge');
            const timeCell = row.querySelector('.reading-time');

            if (levelCell) {
                levelCell.textContent = reading.gas_level;
                levelCell.className = 'gas-level ' + this._levelClass(reading.status);
            }
            if (statusCell) {
                statusCell.textContent = reading.status;
                statusCell.className = `badge status-badge status-${reading.status.toLowerCase()}`;
            }
            if (timeCell) {
                const ts = new Date(reading.timestamp);
                timeCell.textContent = ts.toLocaleTimeString();
            }
        },

        _levelClass: function (status) {
            if (status === 'DANGER') return 'gas-level-danger';
            if (status === 'WARNING') return 'gas-level-warning';
            return '';
        },

        _showAlertToast: function (alert) {
            const container = document.getElementById('live-alert-toast-container');
            if (!container) return;

            const toastEl = document.createElement('div');
            toastEl.className = 'toast show align-items-center text-bg-danger border-0 mb-2';
            toastEl.setAttribute('role', 'alert');
            toastEl.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>DANGER:</strong> ${alert.room_name} — Level ${alert.level}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>`;
            container.appendChild(toastEl);
            setTimeout(() => toastEl.remove(), 8000);
        },

        _incrementAlertCount: function () {
            const el = document.getElementById('stat-total-alerts');
            if (el) {
                el.textContent = parseInt(el.textContent || '0', 10) + 1;
            }
        },

        _updateLastUpdated: function () {
            const el = document.getElementById('last-updated');
            if (el) el.textContent = new Date().toLocaleTimeString();
        },
    };

    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('connection-status') || document.getElementById('readings-table')) {
            window.GasWebSocket.connect();
        }
    });
})();
