/**
 * SublimeNodeServer.js
 * @flow
 */
'use strict';

const net = require('net');

const SERVER_ADDRESS = process.argv[2];

const server = net.createServer(socket => {
  let buffer = '';
  socket.on('data', data => {
    buffer += data;
    let eol;
    while ((eol = buffer.indexOf('\n')) >= 0) {
      const message = JSON.parse(buffer.substr(0, eol));
      buffer = buffer.substr(eol + 1);
      console.log('[SublimeNodeServer] Received: %s', message);
    }
  });
});

server.on('error', error => {
  throw error;
});

server.listen(SERVER_ADDRESS, () => {
  const address = server.address();
  console.log('[SublimeNodeServer] Listening on `%s`.', address);
});
