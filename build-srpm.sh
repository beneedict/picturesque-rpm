#!/bin/sh
# Build the source RPM for picturesque.
#
# Upstream sources are downloaded with spectool; the local desktop file is
# staged next to them. rpmbuild resolves Source entries relative to
# _sourcedir, so everything has to live in one directory.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

cp "$here"/picturesque.desktop "$stage"/

spectool -g -R \
    --define "_sourcedir $stage" \
    "$here/picturesque.spec" >/dev/null

mkdir -p "$here/srpms"
rpmbuild -bs \
    --define "_sourcedir $stage" \
    --define "_srcrpmdir $here/srpms" \
    "$here/picturesque.spec"

echo "SRPM: $(ls -t "$here"/srpms/*.src.rpm | head -n1)"
