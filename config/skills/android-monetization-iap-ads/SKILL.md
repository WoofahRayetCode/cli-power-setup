---
name: android-monetization-iap-ads
description: Google Play Billing (BillingClient 7.x), In-App Purchases, server-side receipt cryptographic verification, Play Integrity API, and AdMob/AppLovin mediation.
---

# Android Monetization, IAP & Ads (`android-monetization-iap-ads`)

Implementing monetization in Android mobile games and applications requires strict compliance with Google Play Store policies, asynchronous billing lifecycles, and cryptographic receipt verification to prevent fraud and client tampering.

This skill governs Google Play Billing Library 7.x integration, pending transaction reconciliation, Play Integrity API attestation, and ad mediation.

---

## 1. Google Play Billing Architecture

```
+-------------------------------------------------------------+
| Client Application (Kotlin / Native C++ Bridge)             |
+-------------------------------------------------------------+
       |                                              ^
       | BillingClient.launchBillingFlow()            | onPurchasesUpdated()
       v                                              |
+-------------------------------------------------------------+
| Google Play BillingClient 7.x                               |
+-------------------------------------------------------------+
       |                                              ^
       | Secure Purchase Token                        | Server Callback
       v                                              |
+-------------------------------------------------------------+
| Backend / Play Integrity Server Verification                |
| - Verify purchaseToken with Google Play Developer API       |
| - Validate RSA-SHA256 signature and package name            |
| - Acknowledge purchase within 3 days or refund triggers     |
+-------------------------------------------------------------+
```

---

## 2. Core Operational Directives

### 1. Mandatory Purchase Acknowledgment
- **The Rule:** Google Play automatically refunds and revokes any purchase that is not explicitly acknowledged within **3 days**.
- Always call `billingClient.acknowledgePurchase()` immediately after server verification or item entitlement is granted.

### 2. Handling Pending Transactions
- Cash/deferred payment methods require handling `Purchase.PurchaseState.PENDING`.
- **The Rule:** Never grant virtual currency or inventory items while purchase state is `PENDING`. Grant entitlements only upon state transition to `PURCHASED`.

### 3. Server-Side Verification First
- Never trust client-side signature verification alone in competitive or paid games.
- Send the `purchaseToken` and `orderId` to your backend server to verify against Google's `androidpublisher/v3` API before unlocking game assets.

---

## 3. Sample Billing Initialization in Kotlin

```kotlin
val billingClient = BillingClient.newBuilder(context)
    .setListener { billingResult, purchases ->
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK && purchases != null) {
            for (purchase in purchases) {
                handlePurchase(purchase)
            }
        }
    }
    .enablePendingPurchases(
        PendingPurchasesParams.newBuilder().enableOneTimeProducts().build()
    )
    .build()

billingClient.startConnection(object : BillingClientStateListener {
    override fun onBillingSetupFinished(billingResult: BillingResult) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
            queryProductDetails()
        }
    }
    override fun onBillingServiceDisconnected() {
        // Implement exponential backoff reconnect
    }
})
```

## Related & Interoperating Skills
- **`android-game-ndk-vulkan`**: Native Android game development using C++20, Android NDK (GameActivity / NativeActivity), Vulkan mobile render...
- **`android-architecture-jetpack`**: Modern Android Architecture (Now in Android standard), Clean Architecture, MVI/MVVM with unidirectional data f...
- **`android-app-engineering`**: Modern Android development in Kotlin, Gradle KTS, foreground services, network tethering/VPN APIs, ProGuard/R8...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
