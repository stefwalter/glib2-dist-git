%global _changelog_trimtime %(date +%s -d "1 year ago")

# See https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%global __python %{__python3}

Summary: A library of handy utility functions
Name: glib2
Version: 2.49.7
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
#VCS: git:git://git.gnome.org/glib
Source: http://download.gnome.org/sources/glib/2.49/glib-%{version}.tar.xz

BuildRequires: perl-generators
BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: libselinux-devel
BuildRequires: pkgconfig(libpcre)
# for sys/inotify.h
BuildRequires: glibc-devel
BuildRequires: zlib-devel
# for sys/sdt.h
BuildRequires: systemtap-sdt-devel
# Bootstrap build requirements
BuildRequires: automake autoconf libtool
BuildRequires: gtk-doc
BuildRequires: python3-devel
BuildRequires: libffi-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: chrpath

# for GIO content-type support
Recommends: shared-mime-info

%description
GLib is the low-level core library that forms the basis for projects
such as GTK+ and GNOME. It provides data structure handling for C,
portability wrappers, and interfaces for such runtime functionality
as an event loop, threads, dynamic loading, and an object system.


%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for the GLib library.

%package doc
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The glib2-doc package includes documentation for the GLib library.

%package fam
Summary: FAM monitoring module for GIO
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: gamin-devel

%description fam
The glib2-fam package contains the FAM (File Alteration Monitor) module for GIO.

%package static
Summary: glib static
Requires: %{name}-devel = %{version}-%{release}

%description static
The %{name}-static subpackage contains static libraries for %{name}.

%package tests
Summary: Tests for the glib2 package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The glib2-tests package contains tests that can be used to verify
the functionality of the installed glib2 package.

%prep
%setup -q -n glib-%{version}

%build
# Support builds of both git snapshots and tarballs packed with autogoo
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
           --with-python=%{__python3} \
           --with-pcre=system \
           --enable-systemtap \
           --enable-static \
           --enable-installed-tests
)

make %{?_smp_mflags}

%install
# Use -p to preserve timestamps on .py files to ensure
# they're not recompiled with different timestamps
# to help multilib: https://bugzilla.redhat.com/show_bug.cgi?id=718404
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"
# Also since this is a generated .py file, set it to a known timestamp,
# otherwise it will vary by build time, and thus break multilib -devel
# installs.
touch -r gio/gdbus-2.0/codegen/config.py.in $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/codegen/config.py
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.{pyc,pyo}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/*.{pyc,pyo}

# Multilib fixes for systemtap tapsets; see
# https://bugzilla.redhat.com/718404
for f in $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/*.stp; do
    (dn=$(dirname ${f}); bn=$(basename ${f});
     mv ${f} ${dn}/%{__isa_bits}-${bn})
done

mv  $RPM_BUILD_ROOT%{_bindir}/gio-querymodules $RPM_BUILD_ROOT%{_bindir}/gio-querymodules-%{__isa_bits}

touch $RPM_BUILD_ROOT%{_libdir}/gio/modules/giomodule.cache

# bash-completion scripts need not be executable
chmod 644 $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/*

%find_lang glib20


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%transfiletriggerin -- %{_libdir}/gio/modules
/bin/gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerpostun -- %{_libdir}/gio/modules
/bin/gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerin -- %{_datadir}/glib-2.0/schemas
/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%transfiletriggerpostun -- %{_datadir}/glib-2.0/schemas
/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f glib20.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/libglib-2.0.so.*
%{_libdir}/libgthread-2.0.so.*
%{_libdir}/libgmodule-2.0.so.*
%{_libdir}/libgobject-2.0.so.*
%{_libdir}/libgio-2.0.so.*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gdbus
%{_datadir}/bash-completion/completions/gsettings
%{_datadir}/bash-completion/completions/gapplication
%dir %{_datadir}/glib-2.0
%dir %{_datadir}/glib-2.0/schemas
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%{_bindir}/gio
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%{_bindir}/gapplication
%{_mandir}/man1/gio.1*
%{_mandir}/man1/gio-querymodules.1*
%{_mandir}/man1/glib-compile-schemas.1*
%{_mandir}/man1/gsettings.1*
%{_mandir}/man1/gdbus.1*
%{_mandir}/man1/gapplication.1*

%files devel
%{_libdir}/lib*.so
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/bash-completion/completions/gresource
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gtester
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/gresource
%{_datadir}/glib-2.0/codegen
%attr (0755, root, root) %{_bindir}/gtester-report
%{_mandir}/man1/glib-genmarshal.1*
%{_mandir}/man1/glib-gettextize.1*
%{_mandir}/man1/glib-mkenums.1*
%{_mandir}/man1/gobject-query.1*
%{_mandir}/man1/gtester-report.1*
%{_mandir}/man1/gtester.1*
%{_mandir}/man1/gdbus-codegen.1*
%{_mandir}/man1/glib-compile-resources.1*
%{_mandir}/man1/gresource.1*
%{_datadir}/gdb/
%{_datadir}/gettext/
%{_datadir}/systemtap/

%files doc
%doc %{_datadir}/gtk-doc/html/*

%files fam
%{_libdir}/gio/modules/libgiofam.so

%files static
%{_libdir}/libgio-2.0.a
%{_libdir}/libglib-2.0.a
%{_libdir}/libgmodule-2.0.a
%{_libdir}/libgobject-2.0.a
%{_libdir}/libgthread-2.0.a

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
* Tue Sep 13 2016 Kalev Lember <klember@redhat.com> - 2.49.7-1
- Update to 2.49.7

* Sun Aug 28 2016 Kalev Lember <klember@redhat.com> - 2.49.6-1
- Update to 2.49.6

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 2.49.5-1
- Update to 2.49.5
- Own /usr/share/gdb and /usr/share/systemtap directories

* Tue Aug 16 2016 Miro Hrončok <mhroncok@redhat.com> - 2.49.4-3
- Use Python 3 for the RPM Python byte compilation

* Wed Jul 27 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.49.4-2
- Switch to Python 3 (#1286284)

* Thu Jul 21 2016 Kalev Lember <klember@redhat.com> - 2.49.4-1
- Update to 2.49.4

* Sun Jul 17 2016 Kalev Lember <klember@redhat.com> - 2.49.3-1
- Update to 2.49.3

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 2.49.2-1
- Update to 2.49.2

* Wed Jun 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.49.1-2
- Soften shared-mime-info dependency (#1266118)

* Fri May 27 2016 Florian Müllner <fmuellner@redhat.com> - 2.49.1-1
- Update to 2.49.1

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 2.48.1-1
- Update to 2.48.1

* Wed Apr 06 2016 Colin Walters <walters@redhat.com> - 2.48.0-2
- Explicitly require system pcre, though we happened to default to this now
  anyways due to something else pulling PCRE into the buildroot
  Closes rhbz#1287266

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 2.48.0-1
- Update to 2.48.0

* Thu Mar 17 2016 Richard Hughes <rhughes@redhat.com> - 2.47.92-1
- Update to 2.47.92

* Wed Feb 24 2016 Colin Walters <walters@redhat.com> - 2.47.6.19.gad2092b-2
- git snapshot to work around https://bugzilla.gnome.org/show_bug.cgi?id=762637
- Add --with-python=/usr/bin/python explicitly to hopefully fix a weird
  issue I am seeing where librepo fails to build in epel7 with this due to
  us requiring /bin/python.

* Wed Feb 17 2016 Richard Hughes <rhughes@redhat.com> - 2.47.6-1
- Update to 2.47.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.47.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 David King <amigadave@amigadave.com> - 2.47.5-1
- Update to 2.47.5

* Wed Dec 16 2015 Kalev Lember <klember@redhat.com> - 2.47.4-1
- Update to 2.47.4

* Wed Nov 25 2015 Kalev Lember <klember@redhat.com> - 2.47.3-1
- Update to 2.47.3

* Wed Nov 25 2015 Kalev Lember <klember@redhat.com> - 2.47.2-1
- Update to 2.47.2

* Mon Nov 09 2015 Kevin Fenzi <kevin@scrye.com> - 2.47.1-2
- Add full path redirect output to null and || : to triggers.

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 2.47.1-1
- Update to 2.47.1

* Mon Oct 19 2015 Kalev Lember <klember@redhat.com> - 2.46.1-2
- Backport an upstream fix for app launching under wayland (#1273146)

* Wed Oct 14 2015 Kalev Lember <klember@redhat.com> - 2.46.1-1
- Update to 2.46.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.46.0-1
- Update to 2.46.0

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 2.45.8-1
- Update to 2.45.8

* Tue Sep 01 2015 Kalev Lember <klember@redhat.com> - 2.45.7-1
- Update to 2.45.7

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 2.45.6-1
- Update to 2.45.6

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 2.45.5-1
- Update to 2.45.5

* Fri Aug 14 2015 Matthias Clasen <mclasen@redhat.com> - 2.45.4-2
- Add file triggers for gio modules and gsettings schemas

* Tue Jul 21 2015 David King <amigadave@amigadave.com> - 2.45.4-1
- Update to 2.45.4

* Wed Jun 24 2015 Kalev Lember <klember@redhat.com> - 2.45.3-2
- Backport a patch to fix notification withdrawing in gnome-software

* Wed Jun 24 2015 David King <amigadave@amigadave.com> - 2.45.3-1
- Update to 2.45.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 David King <amigadave@amigadave.com> - 2.45.2-1
- Update to 2.45.2

* Thu Apr 30 2015 Kalev Lember <kalevlember@gmail.com> - 2.45.1-1
- Update to 2.45.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 2.44.0-1
- Update to 2.44.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 2.43.92-1
- Update to 2.43.92

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.43.91-1
- Update to 2.43.91

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.43.90-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 18 2015 David King <amigadave@amigadave.com> - 2.43.90-1
- Update to 2.43.90
- Update man pages glob in files section

* Tue Feb 10 2015 Matthias Clasen <mclasen@redhat.com> - 2.43.4-1
- Update to 2.43.4

* Tue Jan 20 2015 David King <amigadave@amigadave.com> - 2.43.3-1
- Update to 2.43.3

* Wed Dec 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.43.2-1
- Update to 2.43.2

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 2.43.1-1
- Update to 2.43.1

* Thu Oct 30 2014 Florian Müllner <fmuellner@redhat.com> - 2.43.0-1
- Update to 2.43.0

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.42.0-1
- Update to 2.42.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.5-1
- Update to 2.41.5

* Thu Sep  4 2014 Matthias Clasen <mclasen@redhat.com> 2.41.4-3
- Don't remove rpath from gdbus-peer test - it doesn't work without it

* Thu Sep 04 2014 Bastien Nocera <bnocera@redhat.com> 2.41.4-2
- Fix banshee getting selected as the default movie player

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.4-1
- Update to 2.41.4

* Sat Aug 16 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.3-1
- Update to 2.41.3

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Stef Walter <stefw@redhat.com> - 2.41.2-2
- Fix regression with GDBus array encoding rhbz#1122128

* Mon Jul 14 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.2-1
- Update to 2.41.2

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2.41.1-2
- fix license handling

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 2.41.1-1
- Update to 2.41.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.0-1
- Update to 2.41.0

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 2.39.92-1
- Update to 2.39.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 2.39.91-1
- Update to 2.39.91

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 2.39.90-1
- Update to 2.39.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.39.4-1
- Update to 2.39.4

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 2.39.3-1
- Update to 2.39.3

* Sun Dec 22 2013 Richard W.M. Jones <rjones@redhat.com> - 2.39.2-2
- Re-add static subpackage so that we can build static qemu as
  an AArch64 binfmt.

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 2.39.2-1
- Update to 2.39.2

* Mon Dec 09 2013 Richard Hughes <rhughes@redhat.com> - 2.39.1-2
- Backport a patch from master to stop gnome-settings-daemon crashing.

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 2.39.1-1
- Update to 2.39.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 2.39.0-1
- Update to 2.39.0

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.38.0-1
- Update to 2.38.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.93-1
- Update to 2.37.93

* Mon Sep 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.7-1
- Update to 2.37.7

* Wed Aug 21 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.6-1
- Update to 2.37.6

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.37.5-2
- Perl 5.18 rebuild

* Thu Aug  1 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.5-1
- Update to 2.37.5

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.37.4-2
- Perl 5.18 rebuild

* Tue Jul  9 2013 Matthias Clasen <mclasen@redhat.com> - 2.37.4-1
- Update to 2.37.4

* Thu Jun 20 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.2-1
- Update to 2.37.2

* Tue May 28 2013 Matthias Clasen <mclasen@redhat.com> - 2.37.1-1
- Update to 2.37.1
- Add a tests subpackage

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.0-1
- Update to 2.37.0

* Sat Apr 27 2013 Thorsten Leemhuis <fedora@leemhuis.info> - 2.36.1-2
- Fix pidgin freezes by applying patch from master (#956872)

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.9-1
- Update to 2.35.9

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.8-1
- Update to 2.35.8

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.7-1
- Update to 2.35.7

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.4-1
- Update to 2.35.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.3-1
- Update to 2.35.3

* Sat Nov 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.2-1
- Update to 2.35.2

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.1-1
- Update to 2.35.1
- Drop upstreamed codegen-in-datadir.patch
