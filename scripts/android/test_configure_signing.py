import unittest

from configure_signing import DEBUG_SIGNING_CONFIG, configure_signing


class ConfigureSigningTest(unittest.TestCase):
    def test_replaces_debug_release_signing(self):
        generated = (
            "android {\n"
            + DEBUG_SIGNING_CONFIG
            + """    buildTypes {
        release {
            // Caution! In production, you need to generate your own keystore file.
            // see https://reactnative.dev/docs/signed-apk-android.
            signingConfig signingConfigs.debug
            minifyEnabled false
        }
    }
}
"""
        )

        configured = configure_signing(generated)

        self.assertIn("release {\n            storeFile file(System.getenv", configured)
        self.assertIn("signingConfig signingConfigs.release", configured)
        self.assertNotIn("signingConfig signingConfigs.debug\n            minifyEnabled", configured)


if __name__ == "__main__":
    unittest.main()
