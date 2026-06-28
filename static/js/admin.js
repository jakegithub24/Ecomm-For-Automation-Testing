/* ═══════════════════════════════════════════════
   TECHPRICE — Admin JavaScript
   Product modal, form submission, and table/stats updates.
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    initAdminStats();
    initAdminModal();
    initAdminDelete();
});

function initAdminStats() {
    const totalEl = document.getElementById('admin-stat-total');
    const stockEl = document.getElementById('admin-stat-stock');
    const soonEl = document.getElementById('admin-stat-soon');
    const outEl = document.getElementById('admin-stat-out');
    const discEl = document.getElementById('admin-stat-disc');

    if (!totalEl) return;

    const rows = document.querySelectorAll('#admin-table-body tr');
    let total = rows.length;
    let stock = 0;
    let soon = 0;
    let out = 0;
    let disc = 0;

    rows.forEach(row => {
        const state = row.dataset.state;
        if (state === '{{price}}' || state === 'in_stock') stock++;
        else if (state === 'coming soon' || state === 'coming_soon') soon++;
        else if (state === 'out of stock' || state === 'out_of_stock') out++;
        else if (state === 'discontinued') disc++;
    });

    totalEl.textContent = total;
    stockEl.textContent = stock;
    soonEl.textContent = soon;
    outEl.textContent = out;
    discEl.textContent = disc;
}

function initAdminModal() {
    const modal = document.getElementById('product-modal');
    const form = document.getElementById('product-form');
    const openBtn = document.getElementById('open-add-modal');
    const closeBtn = document.getElementById('modal-close');
    const cancelBtn = document.getElementById('modal-cancel');
    const titleEl = document.getElementById('modal-title');

    if (!modal || !form) return;

    const openModal = () => modal.classList.add('open');
    const closeModal = () => {
        modal.classList.remove('open');
        form.reset();
        document.getElementById('product-id').value = '';
    };

    openBtn.addEventListener('click', () => {
        titleEl.innerHTML = '<i class="fa-solid fa-plus"></i> Add Product';
        openModal();
    });

    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    // Edit button click handlers (delegated)
    const tableBody = document.getElementById('admin-table-body');
    if (tableBody) {
        tableBody.addEventListener('click', async (e) => {
            const btn = e.target.closest('.edit-btn');
            if (!btn) return;

            const id = btn.dataset.id;
            try {
                const res = await fetch(`/api/products/${id}`);
                if (!res.ok) throw new Error('Failed to fetch product details.');
                const p = await res.json();

                document.getElementById('product-id').value = p.id;
                document.getElementById('p-name').value = p.name || '';
                document.getElementById('p-brand').value = p.brand || '';
                document.getElementById('p-category').value = p.category || '';
                document.getElementById('p-state').value = p.state || 'coming soon';
                document.getElementById('p-price').value = p.price !== null ? p.price : '';
                document.getElementById('p-original').value = p.original_price !== null ? p.original_price : '';
                document.getElementById('p-image').value = p.image_url || '';
                document.getElementById('p-url').value = p.url || '';
                document.getElementById('p-desc').value = p.description || '';

                titleEl.innerHTML = '<i class="fa-solid fa-pen-to-square"></i> Edit Product';
                openModal();
            } catch (error) {
                window.showToast('Error', error.message, 'error');
            }
        });
    }

    // Form submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const id = document.getElementById('product-id').value;
        const data = {
            name: document.getElementById('p-name').value,
            brand: document.getElementById('p-brand').value,
            category: document.getElementById('p-category').value,
            state: document.getElementById('p-state').value,
            price: parseFloat(document.getElementById('p-price').value) || null,
            original_price: parseFloat(document.getElementById('p-original').value) || null,
            image_url: document.getElementById('p-image').value || null,
            url: document.getElementById('p-url').value || null,
            description: document.getElementById('p-desc').value || null
        };

        const url = id ? `/api/products/${id}` : '/api/products';
        const method = id ? 'PUT' : 'POST';

        try {
            const res = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!res.ok) throw new Error('Failed to save product');

            window.showToast('Success', id ? 'Product updated successfully' : 'Product created successfully', 'success');
            closeModal();
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            window.showToast('Error', error.message, 'error');
        }
    });
}

function initAdminDelete() {
    const modal = document.getElementById('delete-modal');
    const cancelBtn = document.getElementById('delete-cancel');
    const confirmBtn = document.getElementById('delete-confirm');
    const nameEl = document.getElementById('delete-product-name');

    if (!modal) return;

    let deleteId = null;

    const openModal = () => modal.classList.add('open');
    const closeModal = () => {
        modal.classList.remove('open');
        deleteId = null;
    };

    const tableBody = document.getElementById('admin-table-body');
    if (tableBody) {
        tableBody.addEventListener('click', (e) => {
            const btn = e.target.closest('.delete-btn');
            if (!btn) return;

            deleteId = btn.dataset.id;
            const row = btn.closest('tr');
            const name = row.querySelector('.td-name').textContent;
            nameEl.textContent = name;
            openModal();
        });
    }

    cancelBtn.addEventListener('click', closeModal);

    confirmBtn.addEventListener('click', async () => {
        if (!deleteId) return;

        try {
            const res = await fetch(`/api/products/${deleteId}`, { method: 'DELETE' });
            if (!res.ok) throw new Error('Failed to delete product');

            window.showToast('Success', 'Product deleted successfully', 'success');
            closeModal();
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            window.showToast('Error', error.message, 'error');
        }
    });
}
