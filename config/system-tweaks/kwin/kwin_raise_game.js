// One-shot KWin script: put the game window back in front of the terminal (both keep-above) WITHOUT moving keyboard focus. Run by tools/dpms.py after the panel wakes.
workspace.windowList().forEach(function (w) {
    var g = w && ((w.caption && String(w.caption).indexOf("OGSR Engine") === 0) || /steam_app_2427(410|420|430)/.test(String(w.resourceClass || "")));
    var t = w && w.resourceClass && String(w.resourceClass).toLowerCase().indexOf("kitty") >= 0;
    if (g || t) { try { w.keepAbove = true; } catch (e) {} }
    if (g) { try { workspace.raiseWindow(w); } catch (e) {} }
});
