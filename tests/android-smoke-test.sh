#!/usr/bin/env bash

set -euo pipefail

MODE="${1:-}"

if [[ "$MODE" != "standalone" && "$MODE" != "http" ]]; then
    echo "Usage: $0 <standalone|http>"
    exit 1
fi

echo "========================================"
echo "Android smoke test"
echo "Mode: $MODE"
echo "========================================"

echo "========================================"
echo "Android device"
echo "========================================"

adb devices

adb shell getprop ro.build.version.release
adb shell getprop ro.product.model

echo "========================================"
echo "Configure connectivity"
echo "========================================"

if [[ "$MODE" == "http" ]]; then
    echo "Setting up ADB reverse for HTTP backend..."
    adb reverse tcp:8000 tcp:8000

    echo "ADB reverse:"
    adb reverse --list
fi

echo "========================================"
echo "Locate APK"
echo "========================================"

APK="$(find apk -type f -name "*.apk" | head -n 1)"

if [[ -z "$APK" ]]; then
    echo "ERROR: No APK found."
    echo "Contents of apk/:"
    find apk -maxdepth 5 -print
    exit 1
fi

echo "APK=$APK"

echo "========================================"
echo "Install APK"
echo "========================================"

adb install -r "$APK"

echo "APK installed successfully."

echo "========================================"
echo "Find package/activity"
echo "========================================"

BUILD_TOOLS="$ANDROID_HOME/build-tools/$(ls "$ANDROID_HOME/build-tools" | sort -V | tail -n 1)"

PACKAGE="$(
    "$BUILD_TOOLS/aapt" dump badging "$APK" |
    sed -n "s/^package: name='\([^']*\)'.*/\1/p"
)"

ACTIVITY="$(
    "$BUILD_TOOLS/aapt" dump badging "$APK" |
    sed -n "s/^launchable-activity: name='\([^']*\)'.*/\1/p"
)"

echo "PACKAGE=$PACKAGE"
echo "ACTIVITY=$ACTIVITY"

if [[ -z "$PACKAGE" ]]; then
    echo "ERROR: Could not determine APK package."
    exit 1
fi

if [[ -z "$ACTIVITY" ]]; then
    echo "ERROR: Could not determine launchable activity."
    exit 1
fi

echo "========================================"
echo "Launch application"
echo "========================================"

adb shell am force-stop "$PACKAGE"

adb shell am start \
    -n "$PACKAGE/$ACTIVITY"

echo "Application launch command completed."

echo "========================================"
echo "Wait for application"
echo "========================================"

sleep 15

echo "========================================"
echo "Check application process"
echo "========================================"

if ! adb shell pidof "$PACKAGE"; then
    echo "ERROR: Application process is not running."

    echo "========================================"
    echo "Recent application logcat"
    echo "========================================"

    adb logcat -d -t 300 \
        | grep -i "$PACKAGE" \
        || true

    exit 1
fi

echo "Application is running."

sleep 10

if ! adb shell pidof "$PACKAGE"; then
    echo "ERROR: Application stopped unexpectedly."

    echo "========================================"
    echo "Recent application logcat"
    echo "========================================"

    adb logcat -d -t 500 \
        | grep -i "$PACKAGE" \
        || true

    exit 1
fi

echo "========================================"
echo "Android smoke test passed"
echo "Mode: $MODE"
echo "Package: $PACKAGE"
echo "========================================"