const serverAddr = "ws://192.168.0.187:65432";
const socket = new WebSocket(serverAddr);


socket.addEventListener('open', (event) => {
    console.log('Connected to server via WebSocket!');
});


socket.addEventListener('message', (event) => {
    const responseData = event.data;


    let parsedData;
    try {
        parsedData = JSON.parse(responseData);
    } catch (error) {

        parsedData = { message: responseData.toString() };
    }


    const displayText = parsedData.object_locals
        ? `Object Locals: ${parsedData.object_locals.join(', ')}<br>
           Time Moving: ${parsedData.time_moving}<br>
           Speed: ${parsedData.speed}`
        : parsedData.message;

    console.log(`Received message from server: ${displayText}`);
    document.getElementById("response").innerHTML = displayText;
});
function sendCommand() {
    const speedInput = document.getElementById("speedInput").value;
    const durationInput = document.getElementById("durationInput").value;
    const directionSelect = document.getElementById("directionSelect");
    const direction = directionSelect.options[directionSelect.selectedIndex].value;


    if (!isNaN(speedInput) && speedInput !== "" && !isNaN(durationInput) && durationInput !== "") {
        const speed = parseInt(speedInput, 10);
        const duration = parseInt(durationInput, 10);

        const commandObj = { direction, speed, duration };
        const commandJson = JSON.stringify(commandObj);


        if (socket.readyState === WebSocket.OPEN) {
            socket.send(commandJson);
        } else {
            console.error('WebSocket is not in OPEN state.');
        }
    } else {
        alert("Please enter valid speed and duration values.");
    }
}