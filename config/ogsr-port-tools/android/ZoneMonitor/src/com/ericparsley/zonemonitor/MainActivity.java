package com.ericparsley.zonemonitor;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import org.json.JSONArray;
import org.json.JSONObject;

/** Zone Monitor v2: status card, a chat-style feed (what Claude says, what the system reports, what you sent), quick buttons, a text box to send commands to Claude,
 *  and a background service for notifications (NotifyService). Settings (link + PIN) via the gear. The old web dashboard is one tap away (globe). */
public class MainActivity extends Activity {
    static final int BG = Color.rgb(15, 20, 25), FG = Color.rgb(230, 230, 230), MUT = Color.rgb(138, 145, 153), CYAN = Color.rgb(77, 208, 225), YEL = Color.rgb(255, 213, 79), GRN = Color.rgb(129, 199, 132);
    private final Handler ui = new Handler(Looper.getMainLooper());
    private LinearLayout chat, root;
    private ScrollView scroll;
    private TextView dot, status;
    private EditText input;
    private long last = 0;
    private boolean running = false, polling = false, tabbing = false;
    private String tab = "chat";
    private LinearLayout chatPane;
    private ScrollView textScroll;
    private TextView textView;
    private android.widget.ImageView mindImg;
    private final java.util.ArrayList<Button> tabButtons = new java.util.ArrayList<>();
    private static final String[][] TABS = {{"Chat", "chat"}, {"Status", "status"}, {"Mind", "mind"}, {"Game", "game"}, {"Ops", "ops"}, {"Monitor", "monitor"}, {"Models", "models"}, {"Agenda", "agenda"}};
    private final java.util.ArrayList<String> pendingMine = new java.util.ArrayList<>();

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
        if (Build.VERSION.SDK_INT >= 33) requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, 1);
        if (!new Api(this).configured()) settings(); else build();
    }
    @Override protected void onResume() { super.onResume(); running = true; if (chat != null) { startService(new Intent(this, NotifyService.class)); poll(); tabLoop(); } }
    @Override protected void onPause() { super.onPause(); running = false; }

    int dp(int v) { return (int) (v * getResources().getDisplayMetrics().density + 0.5f); }
    GradientDrawable box(int color, int radius) { GradientDrawable g = new GradientDrawable(); g.setColor(color); g.setCornerRadius(dp(radius)); return g; }
    TextView tv(String s, int color, int sp) { TextView t = new TextView(this); t.setText(s); t.setTextColor(color); t.setTextSize(sp); return t; }

    void build() {
        root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setBackgroundColor(BG); root.setPadding(dp(12), dp(36), dp(12), dp(8)); root.setFitsSystemWindows(false);
        LinearLayout top = new LinearLayout(this); top.setGravity(Gravity.CENTER_VERTICAL);
        dot = tv("●", Color.GRAY, 18); top.addView(dot);
        TextView title = tv("  Zone Monitor", FG, 18); title.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1)); top.addView(title);
        Button web = new Button(this); web.setText("web"); web.setOnClickListener(v -> startActivity(new Intent(this, WebActivity.class))); top.addView(web);
        Button gear = new Button(this); gear.setText("set"); gear.setOnClickListener(v -> settings()); top.addView(gear);
        root.addView(top);
        HorizontalScrollView tabStrip = new HorizontalScrollView(this); tabStrip.setHorizontalScrollBarEnabled(false); LinearLayout tabRow = new LinearLayout(this); tabStrip.addView(tabRow);
        for (final String[] t : TABS) { final Button b = new Button(this); b.setText(t[0]); b.setAllCaps(false); b.setOnClickListener(v -> selectTab(t[1])); tabButtons.add(b); tabRow.addView(b); }
        root.addView(tabStrip);
        chatPane = new LinearLayout(this); chatPane.setOrientation(LinearLayout.VERTICAL);
        textView = tv("", FG, 11); textView.setTypeface(android.graphics.Typeface.MONOSPACE); textView.setTextIsSelectable(true); textView.setPadding(dp(8), dp(8), dp(8), dp(8));
        textScroll = new ScrollView(this); textScroll.addView(textView); textScroll.setVisibility(View.GONE);
        mindImg = new android.widget.ImageView(this); mindImg.setScaleType(android.widget.ImageView.ScaleType.FIT_CENTER); mindImg.setVisibility(View.GONE); mindImg.setBackgroundColor(Color.BLACK);
        status = tv("connecting…", FG, 13); status.setPadding(dp(10), dp(8), dp(10), dp(8)); status.setBackground(box(Color.rgb(28, 36, 44), 10));
        chatPane.addView(status, new LinearLayout.LayoutParams(-1, -2));
        scroll = new ScrollView(this); chat = new LinearLayout(this); chat.setOrientation(LinearLayout.VERTICAL); scroll.addView(chat);
        LinearLayout.LayoutParams sp = new LinearLayout.LayoutParams(-1, 0, 1); sp.topMargin = dp(8); chatPane.addView(scroll, sp);
        HorizontalScrollView hs = new HorizontalScrollView(this); LinearLayout chips = new LinearLayout(this); hs.addView(chips);
        String[][] q = {{"status", "Give me a short status report: what is running, what needs me, and how the auto walker is doing."}, {"problems?", "Are there any problems or failures right now? What are you doing about them?"},
                {"pause walk", "Pause the night walk (create .agents/nightwalk.stop) and tell me when it is paused."}, {"resume walk", "Resume the night walk (remove .agents/nightwalk.stop)."},
                {"walker", "How is the auto walker learning? Summarise .agents/walker_report.md."}, {"next?", "What are you going to work on next?"}};
        for (final String[] c : q) { Button bt = new Button(this); bt.setText(c[0]); bt.setAllCaps(false); bt.setOnClickListener(v -> send(c[1])); chips.addView(bt); }
        chatPane.addView(hs);
        LinearLayout row = new LinearLayout(this);
        input = new EditText(this); input.setHint("message to Claude"); input.setHintTextColor(MUT); input.setTextColor(FG); input.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE | InputType.TYPE_TEXT_FLAG_CAP_SENTENCES);
        input.setMaxLines(4); row.addView(input, new LinearLayout.LayoutParams(0, -2, 1));
        Button go = new Button(this); go.setText("Send"); go.setOnClickListener(v -> { String t = input.getText().toString().trim(); if (!t.isEmpty()) { input.setText(""); send(t); } }); row.addView(go);
        chatPane.addView(row);
        root.addView(chatPane, new LinearLayout.LayoutParams(-1, 0, 1));
        root.addView(textScroll, new LinearLayout.LayoutParams(-1, 0, 1));
        root.addView(mindImg, new LinearLayout.LayoutParams(-1, 0, 1));
        selectTab("chat");
        root.setOnApplyWindowInsetsListener((v, ins) -> {
            int barTop, barBottom;
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets i = ins.getInsets(android.view.WindowInsets.Type.systemBars() | android.view.WindowInsets.Type.ime());
                barTop = i.top; barBottom = i.bottom;
            } else { barTop = ins.getSystemWindowInsetTop(); barBottom = ins.getSystemWindowInsetBottom(); }
            v.setPadding(dp(12), barTop + dp(8), dp(12), barBottom + dp(8));
            return ins;
        });
        setContentView(root);
        last = Math.max(0, getSharedPreferences("zone", MODE_PRIVATE).getLong("shown", 0) - 25);
        startService(new Intent(this, NotifyService.class));
        poll();
    }

    void bubble(String kind, String time, String text) {
        int color = Color.rgb(28, 36, 44), fg = FG; int gravity = Gravity.START; String who = kind;
        if (kind.equals("me")) { color = Color.rgb(0, 96, 100); gravity = Gravity.END; who = "you"; }
        else if (kind.equals("claude")) { color = Color.rgb(36, 46, 58); who = "Claude"; }
        else if (kind.equals("needs")) { color = Color.rgb(92, 72, 0); who = "NEEDS YOU"; }
        else if (kind.equals("learned")) { color = Color.rgb(20, 70, 40); who = "walker learned"; }
        else if (kind.equals("guardian")) { color = Color.rgb(80, 30, 30); who = "guardian"; }
        LinearLayout b = new LinearLayout(this); b.setOrientation(LinearLayout.VERTICAL); b.setPadding(dp(10), dp(6), dp(10), dp(6)); b.setBackground(box(color, 12));
        TextView h = tv(who + "  " + (time.length() >= 16 ? time.substring(11, 16) : time), kind.equals("needs") ? YEL : MUT, 11); b.addView(h);
        TextView t = tv(clean(text), fg, 14); t.setTextIsSelectable(true); b.addView(t);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-2, -2); lp.gravity = gravity; lp.topMargin = dp(6); lp.leftMargin = gravity == Gravity.END ? dp(40) : 0; lp.rightMargin = gravity == Gravity.START ? dp(40) : 0;
        chat.addView(b, lp);
        while (chat.getChildCount() > 120) chat.removeViewAt(0);
    }

    /** the feed is plain text: drop markdown marks (**bold**, `code`, # headings) and turn "- " bullets into dots */
    static String clean(String t) {
        return t.replace("**", "").replace("`", "").replaceAll("(?m)^#+\\s*", "").replaceAll("(?m)^\\s*- ", "• ");
    }

    void selectTab(String name) {
        tab = name;
        for (int i = 0; i < TABS.length; i++) tabButtons.get(i).setAlpha(TABS[i][1].equals(name) ? 1f : 0.55f);
        chatPane.setVisibility(name.equals("chat") ? View.VISIBLE : View.GONE);
        boolean img = name.equals("mind") || name.equals("game");
        textScroll.setVisibility(!name.equals("chat") && !img ? View.VISIBLE : View.GONE);
        mindImg.setVisibility(img ? View.VISIBLE : View.GONE);
        if (!name.equals("chat") && !img) textView.setText("loading…");
        tabLoop();
    }

    /** one loop that keeps the visible non-chat tab fresh: text tabs every 3 s, the Walker Mind picture every 2 s */
    void tabLoop() {
        if (!running || tabbing || tab.equals("chat")) return;
        tabbing = true; final String name = tab; final Api api = new Api(this);
        final int w = Math.max(400, mindImg.getWidth()), h = Math.max(400, mindImg.getHeight());
        new Thread(() -> {
            String txt = null; android.graphics.Bitmap bmp = null; String err = null;
            try {
                if (name.equals("mind")) { byte[] b = api.bytes("/api/mind.png?w=" + w + "&h=" + h); bmp = android.graphics.BitmapFactory.decodeByteArray(b, 0, b.length); }
                else if (name.equals("game")) { byte[] b = api.bytes("/api/game.jpg?w=" + Math.min(w, 1100)); bmp = android.graphics.BitmapFactory.decodeByteArray(b, 0, b.length); }
                else txt = api.tab(name);
            } catch (Exception e) { err = "cannot reach the laptop: " + e.getMessage(); }
            final String ftxt = txt, ferr = err; final android.graphics.Bitmap fbmp = bmp;
            ui.post(() -> {
                tabbing = false;
                if (!name.equals(tab)) { tabLoop(); return; }
                if (ferr != null) { if (name.equals("mind") || name.equals("game")) { textScroll.setVisibility(View.VISIBLE); mindImg.setVisibility(View.GONE); } textView.setText(ferr); }
                else if (fbmp != null) { textScroll.setVisibility(View.GONE); mindImg.setVisibility(View.VISIBLE); mindImg.setImageBitmap(fbmp); }
                else if (ftxt != null) { int y = textScroll.getScrollY(); textView.setText(ftxt); textScroll.post(() -> textScroll.scrollTo(0, y)); }
                ui.postDelayed(this::tabLoop, name.equals("mind") ? 2000 : name.equals("game") ? 1500 : 3000);
            });
        }).start();
    }

    void poll() {
        if (!running || chat == null || polling) return;          // exactly one poll loop (onResume used to start another every time: the feed showed each message several times)
        polling = true;
        final Api api = new Api(this); final long after = last;
        new Thread(() -> {
            String st = null; JSONArray ev = null; boolean ok = true;
            try { JSONObject s = api.state(); ev = api.events(after);
                st = (s.optString("needs").isEmpty() ? "" : "NEEDS YOU: " + s.optString("needs") + "\n") + "now: " + s.optString("now") + "\ngame: " + (s.optBoolean("game") ? "running" : "closed") + "   commands: " + (s.optBoolean("commands_on") ? "on" : "OFF (set a PIN on the laptop)") + "\nwalker: " + s.optString("walker") + "\n" + s.optString("workers");
            } catch (Exception e) { ok = false; st = "cannot reach the laptop: " + e.getMessage(); }
            final String fst = st; final JSONArray fev = ev; final boolean fok = ok;
            ui.post(() -> {
                dot.setTextColor(fok ? GRN : Color.rgb(239, 83, 80)); status.setText(fst);
                if (fev != null) for (int i = 0; i < fev.length(); i++) { JSONObject e = fev.optJSONObject(i); if (e == null) continue; if (e.optLong("id") <= last) continue; if (e.optString("kind").equals("me") && pendingMine.remove(e.optString("text"))) { last = Math.max(last, e.optLong("id")); continue; } bubble(e.optString("kind"), e.optString("t"), e.optString("text")); last = Math.max(last, e.optLong("id")); }
                if (fev != null && fev.length() > 0) { getSharedPreferences("zone", MODE_PRIVATE).edit().putLong("shown", last).apply(); scroll.post(() -> scroll.fullScroll(View.FOCUS_DOWN)); }
                polling = false; ui.postDelayed(this::poll, 4000);
            });
        }).start();
    }

    void send(final String text) {
        final Api api = new Api(this);
        pendingMine.add(text.trim().replaceAll("\\s+", " "));
        bubble("me", java.text.DateFormat.getDateTimeInstance().format(new java.util.Date()).length() > 0 ? "now" : "", text);
        scroll.post(() -> scroll.fullScroll(View.FOCUS_DOWN));
        new Thread(() -> {
            String r; try { r = api.send(text); } catch (Exception e) { r = "NOT SENT: " + e.getMessage(); }
            final String fr = r;
            ui.post(() -> { if (fr.startsWith("NOT SENT")) bubble("guardian", "", fr); });
        }).start();
    }

    void settings() {
        final SharedPreferences p = getSharedPreferences("zone", MODE_PRIVATE);
        LinearLayout box = new LinearLayout(this); box.setOrientation(LinearLayout.VERTICAL); box.setPadding(dp(20), dp(60), dp(20), dp(20)); box.setBackgroundColor(BG);
        box.addView(tv("Zone Monitor setup\n\n1. On the laptop run: python3 tools/statusweb.py url  and paste the link below (with Tailscale use the 100.x.x.x one; in the emulator use http://10.0.2.2:8765/?t=...).\n2. PIN: python3 tools/statusweb.py setpin  prints the PIN that allows sending commands.", FG, 14));
        final EditText u = new EditText(this); u.setHint("http://100.x.x.x:8765/?t=..."); u.setText(p.getString("url", "")); u.setTextColor(Color.WHITE); u.setHintTextColor(MUT); box.addView(u);
        final EditText pn = new EditText(this); pn.setHint("PIN"); pn.setText(p.getString("pin", "")); pn.setTextColor(Color.WHITE); pn.setHintTextColor(MUT); pn.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_VARIATION_PASSWORD); box.addView(pn);
        Button go = new Button(this); go.setText("Save and connect");
        go.setOnClickListener(v -> { String s = u.getText().toString().trim(); if (s.isEmpty()) return; if (!s.startsWith("http")) s = "http://" + s;
            p.edit().putString("url", s).putString("pin", pn.getText().toString().trim()).apply(); stopService(new Intent(this, NotifyService.class)); recreate(); });
        box.addView(go);
        box.setOnApplyWindowInsetsListener((v, ins) -> {
            int top = Build.VERSION.SDK_INT >= 30 ? ins.getInsets(android.view.WindowInsets.Type.systemBars()).top : ins.getSystemWindowInsetTop();
            v.setPadding(dp(20), top + dp(24), dp(20), dp(20));
            return ins;
        });
        setContentView(box);
    }
}
