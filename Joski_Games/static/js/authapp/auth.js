document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('show-register').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    });

    document.getElementById('show-login').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';
    });

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        submitForm('loginForm', '{% url "login" %}');
    });

    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault();
        submitForm('registerForm', '{% url "register" %}');
    });

    function submitForm(formId, url) {
        const form = document.getElementById(formId);
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData(form);

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
            .then(data => {
            if (data.success) {
                // Перенаправление на главную страницу
                window.location.href = '/';
            } else {
                showError(data.message || 'Unknown error');
            }
        })
            .catch(error => {
            console.error('Error:', error);
            showError('Введенные данные не корректны. Попробуйте еще раз');
        });
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<span>${message}</span>`;

        document.body.insertBefore(errorDiv, document.body.firstChild);

        errorDiv.classList.add('shake');

        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
});
