// One-shot KWin script: print the geometry of the game, terminal and status windows (WINGEO lines in the user journal), so tests can verify the 1280x720 layout.
workspace.windowList().forEach(function (w) {
    var c = String(w.resourceClass || "");
    if (/steam_app|stalker-status|kitty/i.test(c) || /OGSR Engine/.test(String(w.caption || ""))) {
        print("WINGEO " + c + " | " + String(w.caption).substring(0, 30) + " | frame " + Math.round(w.frameGeometry.x) + "," + Math.round(w.frameGeometry.y) + " " + Math.round(w.frameGeometry.width) + "x" + Math.round(w.frameGeometry.height) +
              " | client " + Math.round(w.clientGeometry.width) + "x" + Math.round(w.clientGeometry.height) + " | fullscreen=" + w.fullScreen + " keepAbove=" + w.keepAbove);
    }
});
