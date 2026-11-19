%global debug_package %{nil}
%global _hardened_build 1

Name:           picturesque
Version:        0.2.0
Release:        1%{?dist}
Summary:        Cull photos: series, best shots and local AI
License:        GPL-3.0-or-later
URL:            https://github.com/denyszorinets/picturesque
Source0:        %{url}/archive/refs/tags/v%{version}/picturesque-%{version}.tar.gz
Source1:        picturesque.desktop

ExclusiveArch:  x86_64

BuildRequires:  cargo >= 1.99
BuildRequires:  rust >= 1.99
BuildRequires:  nodejs >= 22
BuildRequires:  npm
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  clang-devel
BuildRequires:  make
BuildRequires:  patchelf
BuildRequires:  python3
BuildRequires:  glslc
BuildRequires:  vulkan-headers
BuildRequires:  vulkan-loader-devel
BuildRequires:  spirv-headers-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  webkit2gtk4.1-devel
BuildRequires:  javascriptcoregtk4.1-devel
BuildRequires:  libsoup3-devel
BuildRequires:  gtk3-devel
BuildRequires:  glib2-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  atk-devel
BuildRequires:  libayatana-appindicator-gtk3-devel
BuildRequires:  librsvg2-devel
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel
BuildRequires:  vips-devel >= 8.18
BuildRequires:  LibRaw-devel >= 0.22
BuildRequires:  libheif-devel
BuildRequires:  desktop-file-utils

Requires:       vips >= 8.18
Requires:       LibRaw >= 0.22
Requires:       libheif
Requires:       libayatana-appindicator-gtk3
Requires:       hicolor-icon-theme
# HEIC decoding needs the HEVC plugin from RPM Fusion; optional.
Recommends:     libheif-freeworld

%description
Picturesque imports photos into a clean library, groups bursts into series,
highlights the best shots with technical analysis and on-device AI, and
exports your picks.

The application runs its analysis and AI models locally. The ONNX Runtime and
the built-in critic helper are included in the package; no photo leaves the
computer.

%prep
%autosetup -n picturesque-%{version}

%build
export CARGO_HOME="$PWD/.cargo-home"
export CARGO_BUILD_JOBS=%{_smp_build_ncpus}
export NUM_JOBS=%{_smp_build_ncpus}
export CMAKE_BUILD_PARALLEL_LEVEL=%{_smp_build_ncpus}
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

npm ci --no-audit --no-fund

# ONNX Runtime shared library and the critic helper with llama.cpp.
make ort-dylib ORT_PROFILE=release
make critic-libs ORT_PROFILE=release

# Tauri builds the front end through beforeBuildCommand and the release app.
npx tauri build --no-bundle

%install
install -Dpm 0755 target/release/picturesque-desktop \
    %{buildroot}%{_bindir}/picturesque-desktop

install -d %{buildroot}%{_prefix}/lib/picturesque
install -pm 0755 target/release/libonnxruntime.so \
    target/release/libwebgpu_dawn.so \
    %{buildroot}%{_prefix}/lib/picturesque/
cp -a target/release/critic %{buildroot}%{_prefix}/lib/picturesque/

install -Dpm 0644 %{SOURCE1} \
    %{buildroot}%{_datadir}/applications/Picturesque.desktop

install -Dpm 0644 src-tauri/icons/32x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/picturesque-desktop.png
install -Dpm 0644 src-tauri/icons/128x128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/picturesque-desktop.png
install -Dpm 0644 src-tauri/icons/128x128@2x.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256@2/apps/picturesque-desktop.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/Picturesque.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/picturesque-desktop
%{_prefix}/lib/picturesque/
%{_datadir}/applications/Picturesque.desktop
%{_datadir}/icons/hicolor/32x32/apps/picturesque-desktop.png
%{_datadir}/icons/hicolor/128x128/apps/picturesque-desktop.png
%{_datadir}/icons/hicolor/256x256@2/apps/picturesque-desktop.png

%changelog
* Thu Nov 19 2026 Benedikt Nimmervoll <beneedict@users.noreply.github.com> - 0.2.0-1
- Initial package for Picturesque 0.2.0.
- Built from source with the bundled ONNX Runtime and critic helper.
