#!/usr/bin/env bash
# Build Zone Monitor with the Android SDK command-line tools only (no Gradle):  android/ZoneMonitor/build.sh [install]
# aapt2 (resources) -> javac (against android.jar) -> d8 (dex) -> zip -> zipalign -> apksigner (debug key, created on first run). Output: build/zonemonitor.apk
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
SDK="${ANDROID_HOME:-$HOME/Android/Sdk}"; BT="$SDK/build-tools/$(ls "$SDK/build-tools" | sort -V | tail -1)"; PL="$SDK/platforms/android-35/android.jar"
[[ -f "$PL" ]] || PL="$(ls -d "$SDK"/platforms/android-*/android.jar | sort -V | tail -1)"
rm -rf build && mkdir -p build/gen build/classes build/dex
"$BT/aapt2" compile --dir res -o build/res.zip
"$BT/aapt2" link -o build/base.apk -I "$PL" --manifest AndroidManifest.xml --java build/gen build/res.zip --min-sdk-version 24 --target-sdk-version 35
javac --release 11 -Xlint:-options -classpath "$PL" -d build/classes $(find src build/gen -name '*.java')
"$BT/d8" --release --lib "$PL" --min-api 24 --output build/dex $(find build/classes -name '*.class')
python3 - <<'PYZ'
import shutil, zipfile
shutil.copy("build/base.apk", "build/unsigned.apk")
with zipfile.ZipFile("build/unsigned.apk", "a", zipfile.ZIP_DEFLATED) as z: z.write("build/dex/classes.dex", "classes.dex")
PYZ
"$BT/zipalign" -f -p 4 build/unsigned.apk build/aligned.apk
KS="$HOME/.android/zonemonitor.keystore"
[[ -f "$KS" ]] || { mkdir -p "$HOME/.android"; keytool -genkeypair -keystore "$KS" -storepass zonemonitor -keypass zonemonitor -alias zone -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Zone Monitor" >/dev/null 2>&1; }
"$BT/apksigner" sign --ks "$KS" --ks-pass pass:zonemonitor --key-pass pass:zonemonitor --out build/zonemonitor.apk build/aligned.apk
"$BT/apksigner" verify build/zonemonitor.apk && echo "built: $(pwd)/build/zonemonitor.apk ($(du -h build/zonemonitor.apk | cut -f1))"
[[ "${1:-}" == "install" ]] && adb install -r build/zonemonitor.apk
