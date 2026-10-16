---
name: android-testing-ci-cd-security
description: Android automated testing (JUnit 5, MockK, Robolectric, Compose UI testing), headless Gradle CI/CD pipelines, Android App Bundle (AAB) generation, R8/ProGuard obfuscation rules, Android Keystore hardware-backed encryption, and release hardening.
---

# Android Testing, CI/CD & Security Hardening

This skill covers unit testing, Jetpack Compose UI testing, headless CI/CD build scripts, R8 bytecode shrinking, and hardware-backed cryptographic security.

---

## 1. Testing Pyramid & Fast Local JVM Testing

### A. Unit Testing with MockK & Turbine (Flow Testing)
* Test ViewModels and Repositories on local JVM without booting Android emulators:
  ```kotlin
  @Test
  fun `loadFeed emits Loading then Success state`() = runTest {
      val repository = mockk<FeedRepository>()
      coEvery { repository.getFeed() } returns listOf(testItem)
      val viewModel = FeedViewModel(repository)

      viewModel.uiState.test {
          assertEquals(FeedUiState.Loading, awaitItem())
          assertEquals(FeedUiState.Success(listOf(testItem)), awaitItem())
          cancelAndIgnoreRemainingEvents()
      }
  }
  ```

### B. Jetpack Compose UI Testing
* Verify UI semantics, accessibility tags, and click interactions locally with Robolectric or on device:
  ```kotlin
  @get:Rule
  val composeTestRule = createComposeRule()

  @Test
  fun submitButton_disabledWhenInputEmpty() {
      composeTestRule.setContent { MyForm(text = "") }
      composeTestRule.onNodeWithText("Submit").assertIsNotEnabled()
  }
  ```

---

## 2. R8 Shrinking, Obfuscation & Mapping Discipline

* **Enable Full Mode in `gradle.properties`:**
  ```properties
  android.enableR8.fullMode=true
  ```
* **Keep Rules (`proguard-rules.pro`):**
  * Never use wildcards like `-keep class ** { *; }` which completely defeat code shrinking.
  * Keep serializable DTOs and JNI entry points strictly:
    ```proguard
    # Keep JNI entry points
    -keepclasseswithmembernames class * {
        native <methods>;
    }
    # Keep Kotlinx Serialization DTOs
    -keepattributes *Annotation*,InnerClasses,EnclosingMethod
    -keepclassmembers class * {
        @kotlinx.serialization.SerialName <fields>;
    }
    ```
* **Archive `mapping.txt`:** Always archive `build/outputs/mapping/release/mapping.txt` with release binaries to deobfuscate Google Play Console stack traces.

---

## 3. Hardware-Backed Security & Keystore

* **Android Keystore:** Generate AES-256 GCM keys backed by Secure Element / StrongBox:
  ```kotlin
  val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
  val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
  keyGenerator.init(
      KeyGenParameterSpec.Builder("secure_app_key", KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
          .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
          .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
          .setKeySize(256)
          .setIsStrongBoxBacked(hasStrongBox(context))
          .build()
  )
  keyGenerator.generateKey()
  ```
* **Network Security Config:** Disallow cleartext HTTP and enforce HTTPS traffic:
  ```xml
  <network-security-config>
      <base-config cleartextTrafficPermitted="false" />
  </network-security-config>
  ```
