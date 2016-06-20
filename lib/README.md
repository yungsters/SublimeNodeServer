# sublime / sublime_plugin

`sublime` and `sublime_plugin` are wrappers around the Sublime Text 3 APIs. The
script below was used to generate a loose starting point from the Sublime Text 3
[API Reference](https://www.sublimetext.com/docs/3/api_reference.html).

```js
(function(TYPES) {
  function getPreviousSiblingByTagName(node, tagName) {
    while (node) {
      if (node.nodeName === tagName.toUpperCase()) {
        break;
      }
      node = node.previousElementSibling;
    }
    return node;
  }

  function formatDocblock(text, cols, prefix) {
    const lines = [];
    const remainingCols = cols - prefix.length;
    while (text.length) {
      if (text.length < remainingCols) {
        lines.push(prefix + text);
        break;
      }
      let eol = text.lastIndexOf(' ', remainingCols);
      if (eol < 0) {
        eol = text.indexOf(' ', remainingCols);
        if (eol < 0) {
          eol = text.length;
        }
      }
      lines.push(prefix + text.substr(0, eol));
      text = text.substr(eol + 1);
    }
    return lines.join('\n')
  }

  function toCamelCase(string) {
    return string.split('_').map(
      (part, ii) => ii === 0 ? part : part[0].toUpperCase() + part.substr(1)
    ).join('');
  }

  return Array.from(document.querySelectorAll('table.functions'))
    .filter(table => table.querySelector('th').textContent === 'Methods')
    .map(table => `
/**
 * ${getPreviousSiblingByTagName(table, 'h2').textContent}
 */
${Array.from(table.querySelectorAll('tr'))
  .slice(1)
  .map(tr => ({
    method: tr.children[0].textContent,
    returnValue: tr.children[1].textContent,
    description: tr.children[2].textContent,
  }))
  .map(config => ({
    methodSignature: config.method
      .split('(')
      .map((string, ii) => ii === 0 ? toCamelCase(string) : string)
      .join('('),
    returnType: TYPES[config.returnValue] || config.returnValue,
    description: config.description,
  }))
  .map(config =>
`
  /**
${formatDocblock(config.description, 80, '   * ')}
   */
  ${config.methodSignature}: ${config.returnType} {
    // ...
  },
`
  )
  .join('')
}
`
    );
})({
  None: 'void',
  bool: 'boolean',
  String: 'string',
});
```
