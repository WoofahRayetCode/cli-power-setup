// KWin script (Plasma 6): terminal (kitty = Antigravity) and the game window share the "keep above" layer, so every other window stays below both,
// and between the two the GAME is always in front (it is re-raised, without taking focus, whenever the terminal is clicked or typed in); an Antigravity
// update no longer pops over the game. Remove the raiseGame calls at the bottom to go back to "last used is in front".
function isGame(w) { return w && ((w.caption && String(w.caption).indexOf("OGSR Engine") === 0) || /steam_app_2427(410|420|430)/.test(String(w.resourceClass || ""))); }
function isTerm(w) { return w && w.resourceClass && String(w.resourceClass).toLowerCase().indexOf("kitty") >= 0; }
function setup(w) { if (isGame(w) || isTerm(w)) { try { w.keepAbove = true; } catch (e) {} } }
workspace.windowList().forEach(setup);
workspace.windowAdded.connect(function (w) { setup(w); w.captionChanged && w.captionChanged.connect(function () { setup(w); }); });
// a terminal asking for attention (new output) must not raise itself over the game
workspace.windowList().forEach(function (w) { if (isTerm(w) && w.demandsAttentionChanged) w.demandsAttentionChanged.connect(function () { if (w.demandsAttention && isGame(workspace.activeWindow)) w.demandsAttention = false; }); });

function raiseGame() { workspace.windowList().forEach(function (w) { if (isGame(w)) { try { workspace.raiseWindow(w); } catch (e) {} } }); }
workspace.windowActivated && workspace.windowActivated.connect(function (w) { if (isTerm(w)) raiseGame(); });
workspace.windowAdded.connect(function (w) { if (isGame(w)) raiseGame(); else w.captionChanged && w.captionChanged.connect(function () { if (isGame(w)) raiseGame(); }); });

// whenever the stacking order changes and the game is UNDER a terminal, put it back in front (no focus change); the guard flag stops re-entry
var fixing = false;
function enforce() {
    if (fixing) return;
    var so = workspace.stackingOrder, g = -1, t = -1;
    for (var i = 0; i < so.length; i++) { if (isGame(so[i])) g = i; else if (isTerm(so[i])) t = Math.max(t, i); }
    if (g >= 0 && t >= 0 && g < t) { fixing = true; try { workspace.windowList().forEach(function (w) { if (isGame(w) || isTerm(w)) w.keepAbove = true; }); raiseGame(); } catch (e) {} fixing = false; }
}
if (workspace.stackingOrderChanged) workspace.stackingOrderChanged.connect(enforce);
enforce();
