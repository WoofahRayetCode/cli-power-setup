package com.ericparsley.zonemonitor;

import android.content.Context;
import android.content.SharedPreferences;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

/** Talks to tools/statusweb.py on the laptop. Settings in SharedPreferences "zone": url (dashboard link with ?t=token), pin, last (last event id seen). Blocking calls: run them off the UI thread. */
final class Api {
    final String base, token, pin;
    Api(Context c) {
        SharedPreferences p = c.getSharedPreferences("zone", Context.MODE_PRIVATE);
        String u = p.getString("url", "");
        String t = "", b = "";
        int q = u.indexOf("?t=");
        if (q > 0) { t = u.substring(q + 3); u = u.substring(0, q); }
        int s = u.indexOf("/", 8);
        b = s > 0 ? u.substring(0, s) : u;
        base = b; token = t; pin = p.getString("pin", "");
    }
    boolean configured() { return !base.isEmpty() && !token.isEmpty(); }
    private String url(String path) throws Exception { return base + path + (path.contains("?") ? "&" : "?") + "t=" + URLEncoder.encode(token, "UTF-8"); }
    String get(String path) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(url(path)).openConnection();
        c.setConnectTimeout(5000); c.setReadTimeout(8000);
        try (BufferedReader r = new BufferedReader(new InputStreamReader(c.getInputStream(), "UTF-8"))) {
            StringBuilder sb = new StringBuilder(); String l;
            while ((l = r.readLine()) != null) sb.append(l).append('\n');
            return sb.toString();
        } finally { c.disconnect(); }
    }
    String tab(String name) throws Exception { return get("/api/tab?name=" + name); }
    /** raw bytes (the Walker Mind picture) */
    byte[] bytes(String path) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(url(path)).openConnection();
        c.setConnectTimeout(5000); c.setReadTimeout(15000);
        try (java.io.InputStream in = c.getInputStream(); java.io.ByteArrayOutputStream o = new java.io.ByteArrayOutputStream()) {
            byte[] b = new byte[16384]; int n; while ((n = in.read(b)) > 0) o.write(b, 0, n); return o.toByteArray();
        } finally { c.disconnect(); }
    }
    JSONObject state() throws Exception { return new JSONObject(get("/api/state")); }
    JSONArray events(long after) throws Exception { return new JSONArray(get("/api/events?after=" + after)); }
    /** returns the server's answer; throws nothing for HTTP errors (403 etc. come back as text) */
    String send(String text) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(url("/send")).openConnection();
        c.setRequestMethod("POST"); c.setDoOutput(true); c.setConnectTimeout(5000); c.setReadTimeout(8000);
        c.setRequestProperty("Content-Type", "application/json");
        JSONObject o = new JSONObject(); o.put("pin", pin); o.put("text", text);
        try (OutputStream os = c.getOutputStream()) { os.write(o.toString().getBytes("UTF-8")); }
        int code = c.getResponseCode();
        java.io.InputStream in = code >= 400 ? c.getErrorStream() : c.getInputStream();
        StringBuilder sb = new StringBuilder();
        if (in != null) try (BufferedReader r = new BufferedReader(new InputStreamReader(in, "UTF-8"))) { String l; while ((l = r.readLine()) != null) sb.append(l); }
        c.disconnect();
        return (code >= 400 ? "NOT SENT (" + code + "): " : "") + sb;
    }
}
