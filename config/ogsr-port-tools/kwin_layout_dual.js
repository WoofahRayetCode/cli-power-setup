// KWin script (Plasma 6): TWO-SCREEN layout, used by tools/layout.sh when a second screen is attached (the single-screen layout in kwin_layout.js is untouched).
//  main screen (the biggest, the laptop panel): game slot 1280x720 top-left, Antigravity terminal below it (1280 wide, rest of the height), right column: "ops" log terminal on top, system monitor below
//  second screen: STALKER status (left part, full height) + Walker Mind (the rest, full height: a much bigger map)
var GAME_W = 1280, GAME_H = 720, STATUS_W = 960;
function cls(w) { return String(w.resourceClass || "").toLowerCase(); }
function isGame(w) { return /OGSR Engine/.test(String(w.caption || "")) || /steam_app_2427(410|420|430)/.test(String(w.resourceClass || "")); }
function isStatus(w) { var c = cls(w); return c.indexOf("stalker-status") >= 0; }
function isOps(w) { return cls(w).indexOf("stalker-ops") >= 0; }
function isMon2(w) { return cls(w).indexOf("stalker-mon2") >= 0; }
function isMon(w) { return cls(w).indexOf("stalker-mon") >= 0 && !isMon2(w); }
function isMind(w) { return cls(w).indexOf("walker-mind") >= 0 || /^Walker Mind$/.test(String(w.caption || "")); }
function isTerm(w) { return cls(w).indexOf("kitty") >= 0 && !isStatus(w) && !isOps(w) && !isMon(w) && !isMon2(w); }
var busy = false;
function pickScreens() {
    var outs = workspace.screens, main = outs[0], aux = null;
    for (var i = 0; i < outs.length; i++) { var g = outs[i].geometry; if (g.width * g.height > main.geometry.width * main.geometry.height) main = outs[i]; }
    for (var j = 0; j < outs.length; j++) if (outs[j] !== main) aux = outs[j];
    return { main: main, aux: aux };
}
function area(out) { return workspace.clientArea(KWin.MaximizeArea, out, workspace.currentDesktop); }
function apply() {
    if (busy) return; busy = true;
    try {
        var s = pickScreens(); if (!s.aux) { busy = false; return; }
        var M = area(s.main), A = area(s.aux);
        var gw = GAME_W, gh = GAME_H;
        workspace.windowList().forEach(function (w) {
            if (!isGame(w)) return;
            var dw = Math.max(0, Math.round(w.frameGeometry.width - w.clientGeometry.width)), dh = Math.max(0, Math.round(w.frameGeometry.height - w.clientGeometry.height));
            gw = GAME_W + dw; gh = GAME_H + dh;
            try { w.keepAbove = true; w.frameGeometry = { x: M.x, y: M.y, width: gw, height: gh }; print("LAYOUT2 game -> " + M.x + "," + M.y + " " + gw + "x" + gh); } catch (e) { }
        });
        var rightW = M.width - gw, opsH = 260, monH = 340;       // right column: ops log (short), CPU monitor (all 32 threads), then GPU/memory/network/processes
        workspace.windowList().forEach(function (w) {
            var r = null;
            if (isStatus(w)) r = { x: A.x, y: A.y, width: STATUS_W, height: A.height };
            else if (isMind(w)) r = { x: A.x + STATUS_W, y: A.y, width: A.width - STATUS_W, height: A.height };
            else if (isTerm(w)) r = { x: M.x, y: M.y + gh, width: gw, height: M.height - gh };
            else if (isOps(w)) r = { x: M.x + gw, y: M.y, width: rightW, height: opsH };
            else if (isMon(w)) r = { x: M.x + gw, y: M.y + opsH, width: rightW, height: monH };
            else if (isMon2(w)) r = { x: M.x + gw, y: M.y + opsH + monH, width: rightW, height: M.height - opsH - monH };
            if (r) { try { w.keepAbove = true; w.frameGeometry = r; print("LAYOUT2 " + String(w.caption).substring(0, 20) + " -> " + r.x + "," + r.y + " " + r.width + "x" + r.height); } catch (e) { } }
        });
    } finally { busy = false; }
}
apply();
var hooked = {};
function hook(w) {
    if (!w || !(isGame(w) || isStatus(w) || isMind(w) || isOps(w) || isMon(w))) return;
    var key = String(w.internalId);
    if (!hooked[key] && w.frameGeometryChanged) { hooked[key] = true; w.frameGeometryChanged.connect(function () { if (!busy && isGame(w)) apply(); }); }
    apply();
}
workspace.windowList().forEach(hook);
workspace.windowAdded.connect(function (w) { hook(w); if (w.captionChanged) w.captionChanged.connect(function () { hook(w); }); });
workspace.windowRemoved.connect(function (w) { if (isGame(w)) apply(); });
workspace.screensChanged && workspace.screensChanged.connect(apply);
var prevActive = workspace.activeWindow;
workspace.windowActivated.connect(function (w) {
    if (!w) return;
    if (isMind(w) || isOps(w) || isMon(w) || isMon2(w)) { if (prevActive && !(isMind(prevActive) || isOps(prevActive) || isMon(prevActive) || isMon2(prevActive))) { workspace.activeWindow = prevActive; } }
    else prevActive = w;
});
