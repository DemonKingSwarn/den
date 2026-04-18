#!/usr/bin/env bash
set -e

PKG="den"
EMAIL="raghavgohil2004@gmail.com"
NAME="RaghavGohil"

VERSION=0.2.0
FULL_VERSION="${VERSION}-1"
DATE=$(date -R)

mkdir -p debian

# -------- changelog --------
cat > debian/changelog <<EOF
${PKG} (${FULL_VERSION}) unstable; urgency=medium

  * Release ${VERSION}

 -- ${NAME} <${EMAIL}>  ${DATE}
EOF

# -------- control --------
cat > debian/control <<EOF
Source: ${PKG}
Section: utils
Priority: optional
Maintainer: ${NAME} <${EMAIL}>
Build-Depends: debhelper-compat (= 13), dh-python, python3-all, pybuild-plugin-pyproject, python3-hatchling
Standards-Version: 4.6.2
Homepage: https://github.com/RaghavGohil/den
Rules-Requires-Root: no

Package: ${PKG}
Architecture: all
Depends: \${misc:Depends}, \${python3:Depends}, python3 (>= 3.12)
Description: Context management for projects made easy.
EOF

# -------- rules --------
cat > debian/rules <<'EOF'
#!/usr/bin/make -f

export PYBUILD_NAME=den

%:
	dh $@ --buildsystem=pybuild
EOF

chmod +x debian/rules