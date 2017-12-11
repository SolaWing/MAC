#!/usr/bin/env osascript -l JavaScript

function escapeCmd(list) {
    var l = list.map( function (item, idx) {
        return `'${item.replace("'", "'\\''")}'`;
    });
    return l.join(" ");
}

function run(argv) {
    if (argv.length === 0) { return; }
    console.log(JSON.stringify(argv));
    console.log(escapeCmd(argv));
    // var evt = Application("System Events");
    // var oldApp = evt.processes.whose({"frontmost": true })[0].name();
    var iterm = Application("iTerm");
    iterm.activate();
    // var win = iterm.createWindowWithDefaultProfile({command: escapeCmd(argv) });
    var win = iterm.createWindowWithDefaultProfile();
    // use write text to ensure PATH env load
    iterm.write(win.currentSession, {text: `${escapeCmd(argv)}; exit;`});
}
