// Функция для выполнения AJAX-запроса к серверу
function sendAjaxRequest(url, method, data) {
  return new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          resolve(JSON.parse(xhr.responseText));
        } else {
          reject(Error(xhr.statusText));
        }
      }
    };
    xhr.onerror = function() {
      reject(Error('Network Error'));
    };
    xhr.send(data);
  });
}

// Функция для обновления вопроса
function updateQuestion() {
  sendAjaxRequest('/get-current-question/', 'GET')
    .then(function(response) {
      // Обновление текста вопроса
      document.getElementById('question-text').innerText = response.text;

      // Проверка наличия свойства response.options
      var options = response.options && response.options.split(';') || [];

      // Обновление вариантов ответов
      var optionsList = document.getElementById('options-list');
      optionsList.innerHTML = '';

      if (options.length > 0) {
        options.forEach(function(option) {
          var listItem = document.createElement('li');
          var button = document.createElement('button');
          button.textContent = option;
          button.className = 'option-button';
          listItem.appendChild(button);
          optionsList.appendChild(listItem);
        });

        optionsList.style.display = 'block';
      } else {
        optionsList.style.display = 'none';
      }
    })
    .catch(function(error) {
      console.error('Ошибка при получении вопроса:', error);
    });
}

// Обновление контента только вопроса при загрузке и каждые 2 секунды
document.addEventListener('DOMContentLoaded', function() {
  updateQuestion();
  setInterval(updateQuestion, 2000); // Обновление каждые 2 секунды (2000 миллисекунд)
});

// Обработчик события клика на варианте ответа
document.addEventListener('click', function(event) {
  if (event.target.matches('.option-button')) {
    var selectedOption = event.target.textContent;

    var csrfToken = getCookie('csrftoken'); // Получение значения CSRF токена из cookie

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/submit-answer/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken); // Включение CSRF токена в заголовки запроса

    xhr.onload = function() {
      if (xhr.status === 200) {
        console.log('Ответ отправлен:', xhr.responseText);
      } else {
        console.error('Ошибка при отправке ответа:', xhr.statusText);
      }
    };

    xhr.onerror = function() {
      console.error('Ошибка при отправке ответа');
    };

    xhr.send(JSON.stringify({ answer: selectedOption }));
  }
}, false);

// Функция для получения значения cookie по имени
function getCookie(name) {
  var cookieArr = document.cookie.split(';');
  for (var i = 0; i < cookieArr.length; i++) {
    var cookiePair = cookieArr[i].trim().split('=');
    if (cookiePair[0] === name) {
      return decodeURIComponent(cookiePair[1]);
    }
  }
  return null;
}
