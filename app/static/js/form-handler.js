// Form handling JavaScript for the Heart Disease Predictor application

document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.querySelector('form');

    if (predictionForm) {
        // Form validation
        predictionForm.addEventListener('submit', function(event) {
            let isValid = true;

            // Get all required inputs
            const requiredInputs = predictionForm.querySelectorAll('[required]');

            // Check each required input
            requiredInputs.forEach(function(input) {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');

                    // Create error message if it doesn't exist
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorMessage = document.createElement('div');
                        errorMessage.className = 'invalid-feedback';
                        errorMessage.textContent = 'This field is required.';
                        input.parentNode.insertBefore(errorMessage, input.nextElementSibling);
                    }
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            // Prevent form submission if validation fails
            if (!isValid) {
                event.preventDefault();

                // Scroll to the first invalid input
                const firstInvalidInput = predictionForm.querySelector('.is-invalid');
                if (firstInvalidInput) {
                    firstInvalidInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalidInput.focus();
                }
            }
        });

        // Remove validation errors when input changes
        predictionForm.querySelectorAll('input, select').forEach(function(input) {
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    }
});