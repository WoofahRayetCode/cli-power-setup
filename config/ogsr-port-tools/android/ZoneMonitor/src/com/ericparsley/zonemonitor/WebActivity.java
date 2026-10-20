package com.ericparsley.zonemonitor;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

/** Zone Monitor: a thin shell around the STALKER port's status dashboard (tools/statusweb.py on the laptop).
 *  First start asks for the dashboard link once (it contains the secret token) and keeps it; the screen stays on while the app is open.
 *  The "Change link" button is shown on the error page and by long-pressing the volume-down key. Read/command features live in the web page itself. */
public class WebActivity extends Activity {
    private static final String PREFS = "zone", KEY = "url";
    private WebView web;

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        String url = getSharedPreferences(PREFS, MODE_PRIVATE).getString(KEY, "");
        if (url.isEmpty()) askForLink(""); else showDashboard(url);
    }

    private void askForLink(String current) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(48, 96, 48, 48);
        box.setBackgroundColor(Color.rgb(15, 20, 25));
        TextView t = new TextView(this);
        t.setText("Zone Monitor\n\nPaste the dashboard link from the laptop (run: python3 tools/statusweb.py url). With Tailscale use the 100.x.x.x address.");
        t.setTextColor(Color.rgb(230, 230, 230));
        t.setTextSize(16);
        final EditText in = new EditText(this);
        in.setHint("http://100.x.x.x:8765/?t=...");
        in.setText(current);
        in.setTextColor(Color.WHITE);
        in.setHintTextColor(Color.GRAY);
        in.setSingleLine(false);
        Button go = new Button(this);
        go.setText("Connect");
        go.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                String u = in.getText().toString().trim();
                if (u.isEmpty()) return;
                if (!u.startsWith("http")) u = "http://" + u;
                getSharedPreferences(PREFS, MODE_PRIVATE).edit().putString(KEY, u).apply();
                showDashboard(u);
            }
        });
        box.addView(t);
        box.addView(in);
        box.addView(go);
        setContentView(box);
    }

    private void showDashboard(final String url) {
        web = new WebView(this);
        web.setBackgroundColor(Color.rgb(15, 20, 25));
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);          // the page remembers the command PIN in localStorage
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new WebViewClient() {
            @Override public void onReceivedError(WebView v, int code, String desc, String failing) {
                if (failing != null && failing.startsWith(url.split("\\?")[0])) {
                    v.loadData("<body style='background:#0f1419;color:#e6e6e6;font:16px sans-serif;padding:24px'>Cannot reach the laptop.<br><br>Is Tailscale on, and the laptop awake? Retrying every 10 s.<br><br><small>" + desc + "</small><script>setTimeout(function(){location.href='" + url + "'},10000)</script>", "text/html", "utf-8");
                }
            }
        });
        setContentView(web);
        web.loadUrl(url);
    }

    @Override public boolean onKeyLongPress(int keyCode, KeyEvent e) {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            askForLink(getSharedPreferences(PREFS, MODE_PRIVATE).getString(KEY, ""));
            return true;
        }
        return super.onKeyLongPress(keyCode, e);
    }

    @Override public boolean onKeyDown(int keyCode, KeyEvent e) {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) { e.startTracking(); return true; }
        if (keyCode == KeyEvent.KEYCODE_BACK && web != null && web.canGoBack()) { web.goBack(); return true; }
        return super.onKeyDown(keyCode, e);
    }

    @Override protected void onResume() { super.onResume(); if (web != null) web.onResume(); }
    @Override protected void onPause() { if (web != null) web.onPause(); super.onPause(); }
}
