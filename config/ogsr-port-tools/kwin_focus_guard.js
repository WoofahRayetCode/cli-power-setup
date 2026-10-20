// KWin script (Plasma 6): when the test game window ("OGSR Engine") appears, hand keyboard focus straight back to
// whatever window the user was in, for GUARD_MS only. After that the game is left completely alone, so clicking it
// (or alt-tabbing to it) works normally. Loaded/unloaded by tools/windowed.sh around each harness run.
var GUARD_MS = 0;   // 2026-10-18: no automatic guard when the game window appears (it bounced the user's Alt-Tab); only the harness re-arm below, 2.5 s
var prev = workspace.activeWindow;
var guardUntil = 0;

function isGame(w) {
    return w && w.caption && String(w.caption).indexOf("OGSR Engine") === 0;
}

workspace.windowAdded.connect(function (w) {
    if (isGame(w)) {
        guardUntil = Date.now() + GUARD_MS;
        print("OGSRGUARD added game window; guarding " + GUARD_MS + " ms; user window = " + (prev ? prev.caption : "none"));
    }
});

workspace.windowActivated.connect(function (w) {
    print("OGSRGUARD activated: " + (w ? w.caption : "none") + " guard=" + (Date.now() < guardUntil));
    if (isGame(w)) {
        if (Date.now() < guardUntil && prev && !isGame(prev)) {
            workspace.activeWindow = prev;   // give the user's window back
            print("OGSRGUARD gave focus back to: " + prev.caption);
        }
    } else if (w) {
        prev = w;
    }
});

// The harness re-arms the guard right before it injects keys/clicks into the game (tools/press_key.py, tools/gamectl.py),
// via:  qdbus6 org.kde.kglobalaccel /component/kwin org.kde.kglobalaccel.Component.invokeShortcut OGSRGuardArm
registerShortcut("OGSRGuardArm", "OGSR test harness: re-arm focus guard", "", function () {
    guardUntil = Date.now() + 2500;
    print("OGSRGUARD re-armed (2.5 s); user window = " + (prev ? prev.caption : "none"));
});
