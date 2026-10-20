// KWin script (Plasma 6, 1920x1200 screen): game top-left with a 1280x720 DRAWING area, the Claude Code terminal under it, the "STALKER status" window filling the
// right strip, all inside the work area (above the taskbar) and above other windows. Stays loaded: it re-fits whenever the game or status window appears,
// gets its title, or changes size (the engine creates a small window first and resizes it later). Run/reload with tools/layout.sh.
var GAME_W = 1280, GAME_H = 720;
function isGame(w) { return /OGSR Engine/.test(String(w.caption || "")) || /steam_app_2427(410|420|430)/.test(String(w.resourceClass || "")); }
function isStatus(w) { var c = String(w.resourceClass || "").toLowerCase(); return c.indexOf("stalker-status") >= 0 || (c.indexOf("kitty") >= 0 && /STALKER status/.test(String(w.caption || ""))); }
function isTerm(w) { return String(w.resourceClass || "").toLowerCase().indexOf("kitty") >= 0 && !isStatus(w); }
var busy = false;
function apply() {
    if (busy) return; busy = true;
    try {
        var area = workspace.clientArea(KWin.MaximizeArea, workspace.activeScreen, workspace.currentDesktop);   // the screen minus the taskbar/panels
        var X0 = area.x, Y0 = area.y, W = area.width, H = area.height;
        var gw = GAME_W, gh = GAME_H;
        workspace.windowList().forEach(function (w) {
            if (!isGame(w)) return;
            // frame = drawing area + decorations: ask for a frame whose drawing area is exactly GAME_W x GAME_H
            var dw = Math.max(0, Math.round(w.frameGeometry.width - w.clientGeometry.width)), dh = Math.max(0, Math.round(w.frameGeometry.height - w.clientGeometry.height));
            gw = GAME_W + dw; gh = GAME_H + dh;
            try { w.keepAbove = true; w.frameGeometry = { x: X0, y: Y0, width: gw, height: gh }; print("LAYOUT game -> " + X0 + "," + Y0 + " " + gw + "x" + gh + " (client " + GAME_W + "x" + GAME_H + ")"); } catch (e) { print("LAYOUT game error " + e); }
        });
        workspace.windowList().forEach(function (w) {
            var rect = null;
            if (isStatus(w)) rect = { x: X0 + gw, y: Y0, width: W - gw, height: H };
            else if (isTerm(w)) rect = { x: X0, y: Y0 + gh, width: gw, height: H - gh };
            if (rect) { try { w.keepAbove = true; w.frameGeometry = rect; print("LAYOUT " + String(w.caption).substring(0, 20) + " -> " + rect.x + "," + rect.y + " " + rect.width + "x" + rect.height); } catch (e) { print("LAYOUT error " + e); } }
        });
    } finally { busy = false; }
}
apply();
var hooked = {};
function hook(w) {
    if (!w || !(isGame(w) || isStatus(w))) return;
    var key = String(w.internalId);
    if (!hooked[key] && w.frameGeometryChanged) { hooked[key] = true; w.frameGeometryChanged.connect(function () { if (!busy && isGame(w)) apply(); }); }
    apply();
}
workspace.windowList().forEach(hook);
workspace.windowAdded.connect(function (w) { hook(w); if (w.captionChanged) w.captionChanged.connect(function () { hook(w); }); });
