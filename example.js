const Sublime = require('sublime');
const SublimePlugin = require('sublime_plugin');

class DuplicateLineCommand extends SublimePlugin.TextCommand {
  line: Sublime.View;

  run(edit: Sublime.Edit, ...args: Array<mixed>): void {
    this.view.sel().forEach(region => {
      if (region.empty()) {
        const line = this.view.line(region);
        const lineContents = this.view.substr(line) + '\n';
        this.view.insert(edit, line.begin(), lineContents);
      } else {
        this.view.insert(edit, region.begin(), this.view.substr(region));
      }
    });
  }

  isEnabled(): boolean {
    return true;
  }

  isVisible(): boolean {
    return true;
  }

  description(): string {
    return None;
  }

  wantEvent(): boolean {
    return false;
  }
}


import sublime, sublime_plugin

class DuplicateLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                line_contents = self.view.substr(line) + '\n'
                self.view.insert(edit, line.begin(), line_contents)
            else:
                self.view.insert(edit, region.begin(), self.view.substr(region))
