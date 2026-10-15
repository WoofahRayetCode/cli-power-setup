---
name: steamcmd-workshop-pipeline
description: SteamCMD and Steam Workshop publishing pipeline. Use when authoring workshop item VDF manifests, managing content depots, setting visibility, or publishing/updating mods via SteamCMD.
---

# Steam Workshop & SteamCMD Pipeline

This skill guides publishing, updating, and verifying Steam Workshop items using SteamCMD and ZoneForge.

## Workflow & Manifest Discipline

### 1. VDF Configuration (`workshop_item.vdf`)
SteamCMD consumes a Valve Data Format (VDF) file to build workshop items:
```vdf
"workshopitem"
{
    "appid"            "<GAME_APP_ID>"
    "publishedfileid"  "<EXISTING_ITEM_ID_OR_0_FOR_NEW>"
    "contentfolder"    "<ABSOLUTE_PATH_TO_CONTENT_FOLDER>"
    "previewfile"      "<ABSOLUTE_PATH_TO_PREVIEW_IMAGE>"
    "visibility"       "2"   // 0 = Public, 1 = Friends Only, 2 = Private
    "title"            "<MOD_TITLE>"
    "description"      "<MOD_DESCRIPTION>"
    "changenote"       "<RELEASE_NOTES>"
}
```

### 2. Safeguards & Best Practices
- **Default to Private Visibility:**
  - Always set `visibility` to `"2"` (Private) during initial testing.
  - Test the upload end-to-end on Steam, download it through the Steam client, and verify in-game before switching visibility to Public via the web workshop page.
- **Content Folder Cleanliness:**
  - The `contentfolder` must contain *only* the distribution artifacts (e.g. the compiled `.pack` file or clean `gamedata/` structure).
  - Never upload source control folders (`.git`), temporary caches (`.pytest_cache`), raw audio project files (`.wav`), or editor backups.
- **Preview Image Specifications:**
  - Preview file must be a valid PNG or JPEG under 1MB (ideally square, 512x512 or 1024x1024).

### 3. Execution via SteamCMD
- ZoneForge automates this via:
  ```bash
  zoneforge upload --steam-user <YOUR_LOGIN>
  ```
- Or direct SteamCMD invocation:
  ```bash
  steamcmd +login <USER> +workshop_build_item <PATH_TO_VDF> +quit
  ```
- When SteamCMD finishes, extract the resulting `PublishedFileId` from stdout and update your project configuration (`zoneforge.toml`).
