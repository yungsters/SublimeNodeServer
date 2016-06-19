/**
 * index.js
 */
'use strict';

const child_process = require('child_process');

child_process.exec(
  'npm install',
  {cwd: __dirname},
  (error, stdout, stderr) => {
    if (error) {
      console.error(stderr);
      throw error;
    }
    require('babel-register');
    require('./SublimeNodeServer.js');
  }
);
