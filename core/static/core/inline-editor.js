document.addEventListener('DOMContentLoaded', () => {
    const statusDot = document.getElementById('admin-status-dot');
    const statusText = document.getElementById('admin-status-text');

    function setStatus(state, msg) {
        if (!statusDot || !statusText) return;
        statusDot.className = `status-dot ${state}`;
        statusText.textContent = msg;
    }

    // Récupération sécurisée du token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Envoi de la modification d'un champ
    async function saveField(el) {
        const model = el.dataset.model;
        const id = el.dataset.id;
        const field = el.dataset.field;
        const originalText = el.dataset.originalValue || '';
        const newValue = el.innerText.trim();

        if (newValue === originalText) return;

        setStatus('orange', 'En cours d\'enregistrement...');
        el.classList.add('saving');

        try {
            const response = await fetch('/api/inline-update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ model, id, field, value: newValue })
            });

            const result = await response.json();
            if (response.ok && result.status === 'success') {
                el.dataset.originalValue = newValue;
                setStatus('green', 'Modifications enregistrées');
                el.classList.add('saved-success');
                setTimeout(() => el.classList.remove('saved-success'), 1200);
            } else {
                throw new Error(result.message || 'Erreur');
            }
        } catch (err) {
            setStatus('red', 'Erreur d\'enregistrement !');
            alert(`Erreur : ${err.message}`);
            el.innerText = originalText;
        } finally {
            el.classList.remove('saving');
        }
    }

    // Initialisation des éléments éditables
    document.querySelectorAll('[data-editable="true"]').forEach(el => {
        el.contentEditable = 'true';
        el.dataset.originalValue = el.innerText.trim();

        el.addEventListener('focus', () => {
            el.dataset.originalValue = el.innerText.trim();
        });

        el.addEventListener('blur', () => {
            saveField(el);
        });

        el.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !el.dataset.multiline) {
                e.preventDefault();
                el.blur();
            }
        });
    });
});

// Fonctions globales pour les modales et actions admin
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'flex';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

// Création d'élément via modal
async function handleCreateItem(event, modalId) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    try {
        const response = await fetch('/api/inline-create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        });

        const res = await response.json();
        if (response.ok && res.status === 'success') {
            closeModal(modalId);
            window.location.reload();
        } else {
            alert(res.message || 'Erreur lors de la création');
        }
    } catch (err) {
        alert("Erreur de connexion.");
    }
}

// Suppression directe d'un élément
async function deleteItem(model, id, elementId) {
    if (!confirm("Êtes-vous sûr de vouloir supprimer cet élément définitivement ?")) return;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    try {
        const response = await fetch('/api/inline-delete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ model, id })
        });

        const res = await response.json();
        if (response.ok && res.status === 'success') {
            const el = document.getElementById(elementId);
            if (el) {
                el.style.transition = 'all 0.3s ease';
                el.style.opacity = '0';
                el.style.transform = 'scale(0.8)';
                setTimeout(() => el.remove(), 300);
            }
        } else {
            alert(res.message || 'Erreur lors de la suppression.');
        }
    } catch (err) {
        alert("Erreur de communication avec le serveur.");
    }
}