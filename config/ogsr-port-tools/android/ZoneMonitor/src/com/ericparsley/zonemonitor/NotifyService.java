package com.ericparsley.zonemonitor;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.os.Build;
import android.os.IBinder;
import org.json.JSONArray;
import org.json.JSONObject;

/** Foreground service: asks the laptop every 15 s for new events (/api/events) and shows a notification for NEEDS YOU, guardian problems, walker "learned" and Claude's replies.
 *  A quiet low-priority notification keeps it alive; it restarts itself after a reboot (BootReceiver). */
public class NotifyService extends Service {
    private volatile boolean stop = false; private Thread th; private int nid = 100;
    @Override public IBinder onBind(Intent i) { return null; }
    @Override public int onStartCommand(Intent i, int f, int s) {
        NotificationManager nm = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26) {
            nm.createNotificationChannel(new NotificationChannel("keep", "Connection", NotificationManager.IMPORTANCE_MIN));
            nm.createNotificationChannel(new NotificationChannel("alerts", "Needs you / problems", NotificationManager.IMPORTANCE_HIGH));
            nm.createNotificationChannel(new NotificationChannel("updates", "Walker learned / Claude replies", NotificationManager.IMPORTANCE_DEFAULT));
        }
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, "keep") : new Notification.Builder(this);
        b.setContentTitle("Zone Monitor").setContentText("watching the laptop").setSmallIcon(android.R.drawable.stat_notify_sync).setOngoing(true);
        if (Build.VERSION.SDK_INT >= 34) startForeground(1, b.build(), ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE); else startForeground(1, b.build());
        if (th == null || !th.isAlive()) { stop = false; th = new Thread(this::loop); th.start(); }
        return START_STICKY;
    }
    @Override public void onDestroy() { stop = true; super.onDestroy(); }
    private void loop() {
        while (!stop) {
            try {
                Api api = new Api(this);
                if (api.configured()) {
                    android.content.SharedPreferences p = getSharedPreferences("zone", MODE_PRIVATE);
                    long seen = p.getLong("notified", -1);
                    JSONObject st = api.state(); long top = st.optLong("last_event");
                    if (seen < 0) { p.edit().putLong("notified", top).apply(); }          // first run: do not replay old events as notifications
                    else {
                        JSONArray ev = api.events(seen);
                        for (int i = 0; i < ev.length(); i++) { JSONObject e = ev.getJSONObject(i); notify(e.optString("kind"), e.optString("text")); seen = Math.max(seen, e.optLong("id")); }
                        p.edit().putLong("notified", seen).apply();
                    }
                }
            } catch (Exception ignored) { }
            try { Thread.sleep(15000); } catch (InterruptedException e) { return; }
        }
    }
    private void notify(String kind, String text) {
        if (kind.equals("me")) return;
        boolean alert = kind.equals("needs") || kind.equals("guardian");
        String title = kind.equals("needs") ? "NEEDS YOU" : kind.equals("guardian") ? "Helper problem" : kind.equals("learned") ? "Walker learned" : "Claude";
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, alert ? "alerts" : "updates") : new Notification.Builder(this);
        PendingIntent pi = PendingIntent.getActivity(this, 0, new Intent(this, MainActivity.class), PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
        b.setContentTitle(title).setContentText(text.length() > 90 ? text.substring(0, 90) + "…" : text).setStyle(new Notification.BigTextStyle().bigText(text)).setSmallIcon(android.R.drawable.stat_notify_chat).setContentIntent(pi).setAutoCancel(true);
        ((NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE)).notify(nid++, b.build());
    }
}
