%define __libtoolize echo

Summary: A support library for C programming
Name: glib2
Version: 1.3.6
Release: 6
License: LGPL
Group: System Environment/Libraries
Source: glib-%{version}.tar.gz
Source2: fixed-ltmain.sh
BuildRoot: /var/tmp/glib-%{PACKAGE_VERSION}-root
BuildRequires: pkgconfig >= 0.7
Obsoletes: glib-gtkbeta
URL: http://www.gtk.org

# Now in CVS, wont be needed for 1.3.6
Patch: glib-1.3.6-fix.patch

%description
GLib is a widely used library containing utility functions for
C programming, a event loop, an object system, and other
support functionality.

This package is a beta version of the next release of GLib.
You should only install this package if you are a developer
who wants to start developing against new versions of GLib
and the GTK+ widget library.

%package devel
Summary: Header files and static libraries for the GLib package
Group: Development/Libraries
Obsoletes: glib-gtkbeta-devel
Requires: pkgconfig >= 0.7
Requires: %{name} = %{version}

%description devel
The glib2-devel package includes the static libraries and header 
files for the GLib package.

This package is a beta version of the next release of GLib.
You should only install this package if you are a developer
who wants to start developing against new versions of GLib
and the GTK+ widget library.

%changelog
* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Make -devel package require main package (#45388)
- Fix description and summary
- Configure with --disable-gtk-doc

* Wed Jun 20 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add some portability fixes needed at least on s390
- copy config.{guess,sub} instead of calling libtoolize

* Wed Jun 13 2001 Havoc Pennington <hp@redhat.com>
- try a new glib tarball with Makefile changes to work around
  libtool linking to installed .la files
- make -devel require pkgconfig

* Tue Jun 12 2001 Havoc Pennington <hp@redhat.com>
- either libtool or the bad libtool hacks caused link 
  against glib-gobject 1.3.2, rebuild

* Tue Jun 12 2001 Havoc Pennington <hp@redhat.com>
- 1.3.6
- bad libtool workarounds

* Fri May 04 2001 Owen Taylor <otaylor@redhat.com>
- 1.3.5, rename to glib2

* Fri Nov 17 2000 Owen Taylor <otaylor@redhat.com>
- Final 1.3.2

* Mon Nov 13 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.3.2pre1
- Remove pkgconfig

* Sun Aug 13 2000 Owen Taylor <otaylor@redhat.com>
- Call 1.3.1b instead of snap... the snap* naming doesn't
  order correctly.

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- new snapshot with fixed .pc files

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- include .pc files in file list

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- Include pkg-config
- Upgrade to a glib CVS snapshot

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Fri Jul 14 2000 Owen Taylor <otaylor@redhat.com>
- Remove glib-config.1 manpage from build since
  it conflicts with glib-devel. When we go to 
  glib glib1.2 setup, we should add it back

* Fri Jul 07 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.3.1
- Move back to standard %{prefix}

* Thu Jun 8 2000 Owen Taylor <otaylor@redhat.com>
- Rebuild in /opt/gtk-beta

* Tue May 30 2000 Owen Taylor <otaylor@redhat.com>
- New version (adds gobject)

* Wed Apr 25 2000 Owen Taylor <otaylor@redhat.com>
- Don't blow away /etc/ld.so.conf (sorry!)

* Tue Apr 24 2000 Owen Taylor <otaylor@redhat.com>
- Snapshot RPM for Pango testing

* Fri Feb 04 2000 Owen Taylor <otaylor@redhat.com>
- Added fixes from stable branch of CVS

* Thu Oct 7  1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.6

* Fri Sep 24 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.5

* Fri Sep 17 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.4

* Mon Jun 7 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.3

* Thu Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.1

* Fri Feb 26 1999 Michael Fulbright <drmike@redhat.com>
- Version 1.2

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.0pre1

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- new description tags 

* Sun Feb 21 1999 Michael Fulbright <drmike@redhat.com>
- removed libtoolize from %build

* Thu Feb 11 1999 Michael Fulbright <drmike@redhat.com>
- added libgthread to file list

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.15

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.14

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.13

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.12

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated in preparation for the GNOME freeze

* Mon Apr 13 1998 Marc Ewing <marc@redhat.com>
- Split out glib package

%prep
%setup -n glib-%{version}
%patch -p1 -b .fixit

%build
rm ltmain.sh && cp %{SOURCE2} ltmain.sh
for i in config.guess config.sub ; do
	test -f /usr/share/libtool/$i && cp /usr/share/libtool/$i .
done
%configure --disable-gtk-doc
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%doc AUTHORS COPYING ChangeLog NEWS README
%{_prefix}/lib/libglib-1.3.so.*
%{_prefix}/lib/libgthread-1.3.so.*
%{_prefix}/lib/libgmodule-1.3.so.*
%{_prefix}/lib/libgobject-1.3.so.*

%files devel
%defattr(-, root, root)

%{_prefix}/lib/lib*.so
%{_prefix}/lib/*a
%{_prefix}/lib/glib-2.0
%{_prefix}/include/*
# %{_mandir}/man1/*  - conflicts with glib-devel
%{_prefix}/share/aclocal/*
%{_prefix}/bin/*
%{_prefix}/share/gtk-doc/
%{_prefix}/lib/pkgconfig/*
