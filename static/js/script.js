var ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = function(event) {
    var messages = document.getElementById('messages');
    var message = document.createElement('li');
    var content = document.createTextNode(event.data);
    
    // Verifica se a mensagem foi enviada pelo próprio usuário
    if (event.data.startsWith("Você: ")) {
        message.classList.add("sent"); // Aplica a classe 'sent' para mensagens enviadas
    } else {
        message.classList.add("received"); // Aplica a classe 'received' para mensagens recebidas
    }

    message.appendChild(content);
    messages.appendChild(message);
};

function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
