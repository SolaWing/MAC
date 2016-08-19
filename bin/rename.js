#!/usr/bin/env osascript -l JavaScript

function pathSplit(path) {
    var sepIdx = path.lastIndexOf("/", path.length - 1);
    if (sepIdx == -1) { return [ "", path ] }
    return [ path.slice(0, sepIdx+1), path.slice(sepIdx+1) ]
}

function nameSplit(name) {
    var dotIdx = name.lastIndexOf(".", name.length - 1);
    if (dotIdx == -1 || name[name.length - 1] == "/") { return [ name, "" ] }
    return [ name.slice(0, dotIdx), name.slice(dotIdx) ]
}

function escapeRegex(pattern) {
    return pattern.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&")
}

function run(argv) {
  try {
    var app = Application.currentApplication();
    app.includeStandardAdditions = true;

    // check input args
    if (argv.length == 0) { // may change to select file
        argv = app.chooseFile({
            "withPrompt": "choose file to rename",
            "multipleSelectionsAllowed": true,
        });
    }
    argv = argv.map( function (item, idx) {
        return item.toString()
    })
    var fm = $.NSFileManager.defaultManager
    argv.filter( function (item, idx) {
        return fm.fileExistsAtPath(item)
    })
    if (argv.length == 0) {
        app.displayAlert("No files", {"as":"warning", "givingUpAfter": 2});
        return
    }

    // get user input patterns
    var pattern = app.displayDialog(`Input Patterns:
  pattern like "search/replace/flags", and don't have other '/'
        or only have "search"
  search begin with [^/$] to use regex
  replace can use:
        - $& as match string, $n as group n,
        - $\` as prefix, $' as suffix
  flags is "gimu", omit is "g"`, {
        "defaultAnswer": "",
    }).textReturned;
    if (!pattern) { app.displayAlert("empty pattern!", {"givingUpAfter": 2}); return; }

    var patternItems = pattern.split("/");
    var useRegex = false;
    if (patternItems[0] == "") { useRegex = true; patternItems.shift(); }
    var [pattern, replace, flags] = patternItems;
    if (!useRegex && "^$".indexOf(pattern[0]) >= 0 ) { useRegex = true; }
    if (flags === undefined) { flags = "g"; }
    if (replace === undefined) {
        replace = app.displayDialog(`replace: (flags: "${flags}")
    ${pattern}
to:`, { "defaultAnswer": "", }).textReturned;
    }
    if (!replace) {  app.displayAlert("empty replace!", {"givingUpAfter": 2}); return;  }
    if (!useRegex) { pattern = escapeRegex(pattern); }
    pattern = new RegExp(pattern, flags);

    // get and check new name
    var items = argv.reduce( function (sum, item, idx) {
        var [dir, name] = pathSplit(item);
        var [name, ext] = nameSplit(name);
        var newName = name.replace(pattern, replace);
        if (newName == name) { return sum; }
        if (fm.fileExistsAtPath(dir + newName + ext)) { throw `name ${newName} already exist` }
        sum.push({"dir":dir, "name": name, "ext": ext, "newName":newName});
        return sum;
    }, []);

    if (items.length == 0) {
        app.displayAlert("no file need to replace!", {"givingUpAfter":2});
        return;
    }

    // confirm replace
    var cancelText = app.localizedString("Cancel");
    var OKText = app.localizedString("OK");

    var tips = items.map( function (item, idx) {
        return `${idx}: ${item.name}${item.ext} => ${item.newName}${item.ext}`
    });
    var choose = app.chooseFromList(tips, {
        "withPrompt":"confirm rename items:",
        "defaultItems": tips,
        "multipleSelectionsAllowed":true,
        "emptySelectionAllowed":true,
    });
    if (!choose) { return; }
    if (choose.length < items.length) {
        items = choose.reduce( function (sum, item, idx) {
            var idx = Number(item.match(/\d+/)[0]);
            sum.push(items[idx]);
            return sum
        }, []);
    }

    // move files
    fm = $.NSFileManager.defaultManager;
    items.forEach( function (item, idx) {
        var o =  item.dir + item.name + item.ext;
        var n =  item.dir + item.newName + item.ext;
        var err = $();
        fm.moveItemAtPathToPathError(o, n, err);
        if (!err.isNil()) {
            throw err.localizedDescription.js
        }
    });
  } catch (e) {
      if (e.errorNumber == -128) { return; } // user cancel
      throw e;
  }
}
