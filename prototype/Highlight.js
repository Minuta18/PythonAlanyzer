var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    mode: 'text/x-python',
    matchBrackets: true,
});

editor.setOption('theme', 'xq-light');
editor.setSize('100%', '100%');
editor.save();

