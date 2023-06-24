const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');

messageForm.addEventListener('submit', event => {
  event.preventDefault();

  const message = messageInput.value.trim();
  if (message.length === 0) {
    return;
  }

  const messageItem = document.createElement('li');
  messageItem.classList.add('mb-3');
  messageItem.innerHTML = `
    <div class="d-flex justify-content-end">
      <div class="d-inline-block">
        <div class="p-3 sent rounded">
          <b>You</b>
          <div class="message-content">
            ${message}
          </div>
        </div>
      </div>
    </div>
  `;

  messagesList.appendChild(messageItem);
  messageInput.value = '';

  fetch('', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: new URLSearchParams({
      'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      message: message
    })
  })
  .then(response => response.json())
  .then(data => {
    const response = data.response;
    const messageItem = document.createElement('li');
    messageItem.classList.add('mb-3');
    messageItem.innerHTML = `
      <div class="d-inline-block">
        <div class="p-3 received rounded">
          <b>AI Chatbot</b>
          <div class="message-content">
            ${response}
          </div>
        </div>
      </div>
    `
    messagesList.appendChild(messageItem);
  })
})