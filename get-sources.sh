#!
SPEC=${1:-cygwin-binutils.spec}
SRCDIR=${SRCDIR:-$(pwd)}
REF=$(echo %snapshot_commit | rpmspec -q --shell --srpm ${SPEC} 2>/dev/null | tail -2 | head -1)
mkdir -p tmp
cd tmp
git clone --no-checkout git://sourceware.org/git/binutils-gdb.git
cd binutils-gdb
git archive --prefix binutils-${REF}/ --output ${SRCDIR}/binutils.${REF}.tar.gz ${REF}
