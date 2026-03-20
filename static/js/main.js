document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });

    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });

    const shareUrlInput = document.getElementById('shareUrl');
    if (shareUrlInput) {
        const copyBtn = shareUrlInput.nextElementSibling;
        
        copyBtn.addEventListener('click', function() {
            shareUrlInput.select();
            document.execCommand('copy');
            
            const originalHtml = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i>';
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-success');
            
            setTimeout(() => {
                this.innerHTML = originalHtml;
                this.classList.remove('btn-success');
                this.classList.add('btn-outline-primary');
            }, 1500);
        });
    }

    const toggleBtns = document.querySelectorAll('.toggle-responses');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const responsesContainer = document.querySelector(this.dataset.target);
            if (responsesContainer.style.display === 'none') {
                responsesContainer.style.display = 'block';
                this.innerHTML = '<i class="fas fa-chevron-up me-1"></i>مخفی کردن پاسخ‌ها';
            } else {
                responsesContainer.style.display = 'none';
                this.innerHTML = '<i class="fas fa-chevron-down me-1"></i>نمایش پاسخ‌ها';
            }
        });
    });
    
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fadeIn');
    });
}); 