/**
 * Dashboard live update helpers (works with GasWebSocket).
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', () => {
        if (!window.GasWebSocket) return;

        window.GasWebSocket.on('message', (data) => {
            if (data.type !== 'gas_update' || !data.reading) return;
            updateStatusCounts(data.reading.status);
        });
    });

    function updateStatusCounts(status) {
        const id = {
            SAFE: 'count-safe',
            WARNING: 'count-warning',
            DANGER: 'count-danger',
        }[status];
        if (id) {
            const el = document.getElementById(id);
            if (el) el.textContent = parseInt(el.textContent || '0', 10) + 1;
        }
    }
})();
