%global run_testsuite 0

%undefine cygwin_build_32bit 

Name:           cygwin-binutils
Version:        2.39
Release:        2%{?dist}
Summary:        Cross-compiled version of binutils for Cygwin environments

License:        GPLv2+ and LGPLv2+ and GPLv3+ and LGPLv3+
Group:          Development/Libraries

URL:            https://www.gnu.org/software/binutils/
Source0:        https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz
Patch1:         binutils-2.37-cygwin-config-rpath.patch
Patch1000:      w32api-sysroot.patch
Patch1001:      binutils-textdomain.patch


BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  texinfo
BuildRequires:  zlib-devel
BuildRequires:  cygwin64-filesystem >= 7
%if %{run_testsuite}
BuildRequires:  dejagnu
BuildRequires:  sharutils
%endif
Provides:       bundled(libiberty)

%description
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Cygwin executables and DLLs.

%package -n cygwin64-binutils
Summary:        Cross-compiled version of binutils for the Cygwin64 environment
Requires:       cygwin64-filesystem >= 7

%description -n cygwin64-binutils
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Cygwin executables and DLLs.


%prep
%autosetup -n binutils-%{version} -p1


%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
  --build=%_build --host=%_host \
  --target=%{cygwin64_target} \
  --with-sysroot=%{cygwin64_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir} \
  --with-system-zlib \
  --disable-gdb \
  --disable-libdecnumber \
  --disable-readline \
  --disable-sim
make all %{?_smp_mflags}


%check
%if !%{run_testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
  make -k check < /dev/null || :
  echo ====================TESTING CYGWIN64 =========================
  cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
  echo ====================TESTING CYGWIN64 END=====================
  for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
  do
    ln $file binutils-%{cygwin64_$(basename $file) || :}
  done
  tar cjf binutils-%{cygwin64_target}.tar.bz2 binutils-%{cygwin64_*.{sum,log}}
  uuencode binutils-%{cygwin64_target}.tar.bz2 binutils-%{cygwin64_target}.tar.bz2
  rm -f binutils-%{cygwin64_target}.tar.bz2 binutils-%{cygwin64_*.{sum,log}}
%endif


%install
make install DESTDIR=$RPM_BUILD_ROOT

# These files conflict with ordinary binutils.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/bfd-plugins/libdep.*

%find_lang cygwin-binutils
%find_lang cygwin-bfd
%find_lang cygwin-gas
%find_lang cygwin-gprof
%find_lang cygwin-ld
%find_lang cygwin-opcodes
cat cygwin-bfd.lang >> cygwin-binutils.lang
cat cygwin-gas.lang >> cygwin-binutils.lang
cat cygwin-gprof.lang >> cygwin-binutils.lang
cat cygwin-ld.lang >> cygwin-binutils.lang
cat cygwin-opcodes.lang >> cygwin-binutils.lang


%files -n cygwin64-binutils -f cygwin-binutils.lang
%doc COPYING
%{_mandir}/man1/*
%{_bindir}/*
%{_prefix}/%{cygwin64_target}/bin/*
%{_prefix}/%{cygwin64_target}/lib/ldscripts


%changelog
* Fri Dec 23 2022 Corinna Vinschen <vinschen@redhat.com> - 2.39-2
- drop 32 bit support

* Thu Dec 22 2022 Corinna Vinschen <vinschen@redhat.com> - 2.39-1
- new version

* Thu Aug 26 2021 Yaakov Selkowitz <yselkowi@redhat.com> - 2.37-1
- new version

* Wed Apr 01 2020 Yaakov Selkowitz <yselkowi@redhat.com> - 2.34-1
- new version

* Wed Dec 19 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 2.31.1-1
- new version

* Wed Nov 15 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 2.29.1-1
- new version

* Sun Mar 06 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.25.1-1
- new version

* Mon Aug 11 2014 Yaakov Selkowitz <yselkowitz@cygwin.com> - 2.24.51-3
- Patch ld to not export __dso_handle.

* Tue Jun 10 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.24.51-2
- Updated snapshot to fix resource section alignment.

* Wed Mar 26 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.24.51-1
- Updated snapshot with default manifest support.
- Enable NLS.

* Wed Jun 26 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.23.52-1
- Make package compliant with new Cygwin packaging scheme.
- Add Cygwin 64bit support.
- Add generic package containing tools which can used by both toolchains.

* Thu Mar 28 2013 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.23.51-2
- Fix w32api sysroot patch for 64bit BFD support.

* Sun Mar 10 2013 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.23.51-1
- Version bump.
- Enable pei-x86-64 support so i686 tools can work properly on cyglsa64.dll.

* Tue Mar 27 2012 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.22.51-2
- Fix --enable-auto-image-base for latest Cygwin releases.

* Sun Oct 23 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.22.51-1
- Version bump to match Cygwin distro.

* Sun Jul 31 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.21.53-1
- Version bump to match Cygwin distro.

* Sun Jul 10 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.21.1-1
- Version bump.

* Thu May 26 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 14 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.21-2
- Accomodate w32api libs in sys-root/usr/lib/w32api.

* Wed Feb 16 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 2.21-1
- Initial RPM release, largely based on mingw32-binutils.
