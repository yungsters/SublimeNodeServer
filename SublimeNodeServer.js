/**
 * SublimeNodeServer.js
 */
'use strict';

const net = require('net');

const SERVER_ADDRESS = process.argv[2];

const server = net.createServer(socket => {
  socket.on('data', data => {
    console.log('[SublimeNodeServer] Received: ' + data);
  });
}).on('error', error => {
  throw error;
});

server.listen(SERVER_ADDRESS, () => {
  const address = server.address();
  console.log('[SublimeNodeServer] Listening on `%s`.', address);
});
