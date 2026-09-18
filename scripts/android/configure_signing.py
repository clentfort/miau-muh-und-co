#!/usr/bin/env python3
"""Configure the generated Android project to use the release keystore."""

from pathlib import Path

BUILD_FILE = Path("android/app/build.gradle")

SIGNING_CONFIG = """    signingConfigs {
        debug {
            storeFile file('debug.keystore')
            storePassword 'android'
            keyAlias 'androiddebugkey'
            keyPassword 'android'
        }
        release {
            storeFile file(System.getenv('ANDROID_KEYSTORE_FILE'))
            storePassword System.getenv('ANDROID_KEYSTORE_PASSWORD')
            keyAlias System.getenv('ANDROID_KEY_ALIAS')
            keyPassword System.getenv('ANDROID_KEY_PASSWORD')
        }
    }
"""

DEBUG_SIGNING_CONFIG = """    signingConfigs {
        debug {
            storeFile file('debug.keystore')
            storePassword 'android'
            keyAlias 'androiddebugkey'
            keyPassword 'android'
        }
    }
"""


def configure_signing(contents: str) -> str:
    if DEBUG_SIGNING_CONFIG not in contents:
        raise ValueError("Could not find the generated debug signing configuration.")

    contents = contents.replace(DEBUG_SIGNING_CONFIG, SIGNING_CONFIG, 1)
    release_marker = """        release {
            // Caution! In production, you need to generate your own keystore file.
            // see https://reactnative.dev/docs/signed-apk-android.
            signingConfig signingConfigs.debug
"""
    signed_release_marker = """        release {
            signingConfig signingConfigs.release
"""
    if release_marker not in contents:
        raise ValueError("Could not find the generated release build type.")
    return contents.replace(release_marker, signed_release_marker, 1)


def main() -> None:
    BUILD_FILE.write_text(configure_signing(BUILD_FILE.read_text()))


if __name__ == "__main__":
    main()
