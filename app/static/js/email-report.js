// Email report handling JavaScript for the Heart Disease Predictor application

document.addEventListener('DOMContentLoaded', function() {
    // Handle email report buttons
    const emailButtons = document.querySelectorAll('.email-report, #emailReportBtn');

    emailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const reportId = this.getAttribute('data-report-id');

            // Disable button and show loading state
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';

            // Send AJAX request
            fetch(`/email/${reportId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Show alert based on response
                const alertClass = data.success ? 'alert-success' : 'alert-danger';
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert ${alertClass} alert-dismissible fade show`;
                alertDiv.innerHTML = `
                    ${data.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;

                // Insert alert at the top of the container
                const container = document.querySelector('.container');
                container.insertBefore(alertDiv, container.firstChild);

                // Reset button state
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-envelope me-2"></i>Email Report';

                // Scroll to top to show the alert
                window.scrollTo({ top: 0, behavior: 'smooth' });

                // Auto-dismiss alert after 5 seconds
                setTimeout(() => {
                    const bsAlert = new bootstrap.Alert(alertDiv);
                    bsAlert.close();
                }, 5000);
            })
            .catch(error => {
                console.error('Error:', error);

                // Reset button state
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-envelope me-2"></i>Email Report';

                // Show error alert
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-danger alert-dismissible fade show';
                alertDiv.innerHTML = `
                    Failed to send email. Please try again.
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;

                const container = document.querySelector('.container');
                container.insertBefore(alertDiv, container.firstChild);

                // Scroll to top to show the alert
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    });
});