#!/usr/bin/env bash
set -e

pwd

PKGNAME="den"
VERSION=$(python - <<'PY'
import tomllib
with open("pyproject.toml", "rb") as f:
    print(tomllib.load(f)["project"]["version"])
PY
)
PKGREL=1

cat > PKGBUILD <<EOF
# Maintainer: RaghavGohil raghavgohil2004@gmail.com

pkgname=${PKGNAME}
pkgver=${VERSION}
pkgrel=${PKGREL}
pkgdesc="Braindumping for projects made easy."
arch=('any')
url="https://github.com/RaghavGohil/den"
license=('MIT')

depends=('python')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-hatchling')

source=("\$pkgname-\$pkgver.tar.gz::https://github.com/RaghavGohil/den/archive/v\$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "\$srcdir/\$pkgname-\$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "\$srcdir/\$pkgname-\$pkgver"
    python -m installer --destdir="\$pkgdir" dist/*.whl
    
    install -Dm644 LICENSE "\$pkgdir/usr/share/licenses/\$pkgname/LICENSE"
}
EOF

echo "PKGBUILD generated for version $VERSION"