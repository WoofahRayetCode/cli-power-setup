package com.ericparsley.zonemonitor;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class BootReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context c, Intent i) {
        try { if (new Api(c).configured()) c.startForegroundService(new Intent(c, NotifyService.class)); } catch (Exception ignored) { }
    }
}
