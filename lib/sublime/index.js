/**
 * sublime
 * @flow
 */
'use strict';

const sublime = {

  /**
   * Runs the callback in the main thread after the given delay (in
   * milliseconds). Callbacks with an equal delay will be run in the order they
   * were added.
   */
  setTimeout() {
    throw new Error('sublime.setTimeout(...): Not supported.');
  },

  /**
   * Runs the callback on an alternate thread after the given delay (in
   * milliseconds).
   */
  setAsyncTimeout() {
    throw new Error('sublime.setAsyncTimeout(...): Not supported.');
  },

  /**
   * Sets the message that appears in the status bar.
   */
  statusMessage(string: string): void {

  },
};

module.exports = sublime;
