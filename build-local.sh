#!/bin/sh
# Build the RPM in mock for one or more chroots.
#
# Runs detached from the calling shell (setsid + nohup), so an interrupted
# terminal session or tool call does not kill the build. Progress and the
# final result are written to build-<chroot>.log and build-status.log.
#
# Usage: ./build-local.sh [chroot ...]
#        default: fedora-45-x86_64
set -eu

here=$(cd "$(dirname "$0")" && pwd)
chroots=${*:-fedora-45-x86_64}

cd "$here"
./build-srpm.sh >/dev/null

srpm=$(ls -t srpms/*.src.rpm | head -n1)
: > build-status.log

for chroot in $chroots; do
    log="$here/build-$chroot.log"
    echo "start $chroot $(date -Is)" >> build-status.log
    setsid nohup mock -r "$chroot" --enable-network --rebuild "$srpm" \
        > "$log" 2>&1 &
    pid=$!
    echo "pid $pid" >> build-status.log
    if wait "$pid"; then status=0; else status=$?; fi
    echo "end $chroot status=$status $(date -Is)" >> build-status.log
    grep -E "Bad exit|CMake Error|error:" "$log" | tail -5 >> build-status.log || true
    ls -l /var/lib/mock/"$chroot"/result/*.rpm >> build-status.log 2>/dev/null || true
done
echo "done $(date -Is)" >> build-status.log
