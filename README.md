# Picturesque für Fedora (COPR)

Quellcode-Paket von [Picturesque](https://github.com/denyszorinets/picturesque)
für Fedora. COPR baut das RPM und stellt es als `dnf`-Repository bereit:

https://copr.fedorainfracloud.org/coprs/beneedict/picturesque/

## Installation

```bash
sudo dnf copr enable beneedict/picturesque
sudo dnf install picturesque
```

Updates kommen danach mit:

```bash
sudo dnf upgrade --refresh picturesque
```

## Was im Paket steckt

- Picturesque wird aus dem Upstream-Quellcode gebaut.
- Die Oberfläche läuft mit dem System-WebKitGTK 4.1.
- libvips, LibRaw und libheif kommen aus Fedora.
- `libonnxruntime.so`, `libwebgpu_dawn.so` und der Critic-Helper mit
  llama.cpp liegen unter `/usr/lib/picturesque/`.
- Für HEIC-Fotos ist zusätzlich `libheif-freeworld` aus RPM Fusion nötig
  (Fedora darf den HEVC-Decoder aus Patentgründen nicht mitliefern).

## Selbst bauen

```bash
sudo dnf install mock rpmdevtools
./build-local.sh fedora-45-x86_64
cat build-status.log
```

`build-srpm.sh` lädt die Upstream-Quellen per `spectool` und erzeugt das SRPM
in `srpms/`. `build-local.sh` baut es mit `mock`; das vollständige Log landet
in `build-<chroot>.log`.

## Neue Upstream-Versionen

Die Version steht in `picturesque.spec`. Der wöchentliche GitHub-Workflow
`.github/workflows/update.yml` prüft neue Upstream-Releases und öffnet einen
Pull Request. Nach dem Merge löst der COPR-Webhook einen neuen Build aus.
