let socket = new WebSocket('ws://localhost:8888/peers');

socket.onopen = (event) => {
	socket.send('foobar');
};

socket.onmessage = (event) => {
	console.log(event.data);
};
