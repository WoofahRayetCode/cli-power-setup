---
name: android-app-engineering
description: Modern Android development in Kotlin, Gradle KTS, foreground services, network tethering/VPN APIs, ProGuard/R8 rules, and release keystore signing.
---

# Android App Engineering & Kotlin Development

This skill standardizes modern native Android development in Kotlin, enforcing clean architecture, efficient background task execution, and reproducible Gradle KTS builds.

---

## 📱 Core Focus Areas

1. **Modern Architecture:** Jetpack Compose, ViewModel, StateFlow, Kotlin Coroutines, and Dependency Injection.
2. **Background & Networking:** Long-running foreground services, Wi-Fi/USB network tethering, local VPN APIs, and wake locks.
3. **Build & Release Pipeline:** Gradle Kotlin DSL (`build.gradle.kts`), Version Catalogs (`libs.versions.toml`), ProGuard/R8 shrinking, and cryptographic keystore signing.

---

## ⚙️ 1. Foreground Services & Network Tethering

When building persistent background tools (like `tetherfusenet`), Android's aggressive battery optimizations (`Doze mode`) will kill background tasks unless properly elevated:

### Foreground Service Architecture
* Declare proper service types in `AndroidManifest.xml`:
  ```xml
  <service
      android:name=".service.TetherService"
      android:foregroundServiceType="connectedDevice|dataSync"
      android:exported="false" />
  ```
* Provide continuous user visibility via ongoing notification channels:
  ```kotlin
  val notification = NotificationCompat.Builder(this, CHANNEL_ID)
      .setContentTitle("Tether Active")
      .setContentText("Routing network traffic...")
      .setSmallIcon(R.drawable.ic_tether)
      .setOngoing(true)
      .build()
  startForeground(NOTIFICATION_ID, notification)
  ```
* Request `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` only when indispensable.

---

## 🛠️ 2. Gradle Kotlin DSL (`build.gradle.kts`) Standards

* **Use Version Catalogs (`gradle/libs.versions.toml`):** Avoid hardcoding library versions across modules.
* **ProGuard / R8 Rules (`proguard-rules.pro`):**
  * Prevent reflection-based JSON/serialization classes from being stripped:
    ```proguard
    -keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod
    -keepclassmembers class * {
        @com.google.gson.annotations.SerializedName <fields>;
    }
    ```
* **Clean Release Keystore Configuration:**
  * Keep production keystores out of git tracking (`.gitignore`); inject credentials via environment variables:
    ```kotlin
    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("KEYSTORE_PATH") ?: "release.keystore")
            storePassword = System.getenv("KEYSTORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }
    ```

---

## 🧪 3. Verification & Build Commands

* **Run Lint Audits:** `./gradlew lintDebug`
* **Run Unit Tests:** `./gradlew testDebugUnitTest`
* **Assemble Release APK:** `./gradlew assembleRelease`
* **Analyze APK Size:** Use `apkanalyzer` to verify DEX method counts and resource shrinking.
