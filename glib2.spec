%define libdir /%{_lib}

Summary: A library of handy utility functions
Name: glib2
Version: 2.15.3
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
Source: http://download.gnome.org/sources/glib/2.15/glib-%{version}.tar.bz2
Source2: glib2.sh
Source3: glib2.csh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig >= 1:0.14
BuildRequires: gamin-devel
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: libselinux-devel
# for sys/inotify.h
BuildRequires: glibc-devel


%description 
GLib is the low-level core library that forms the basis
for projects such as GTK+ and GNOME. It provides data structure
handling for C, portability wrappers, and interfaces for such runtime
functionality as an event loop, threads, dynamic loading, and an 
object system.

This package provides version 2 of GLib.

%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: pkgconfig >= 1:0.14
Requires: %{name} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for 
version 2 of the GLib library. 

# anaconda needs static libs, see RH bug #193143
%package static
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glib2-static package includes static libraries
of version 2 of the GLib library. 

%prep
%setup -q -n glib-%{version}

%build
%configure --disable-gtk-doc --enable-static 
make %{?_smp_mflags}

%check
# abicheck scripts don't work on ppc
%ifnarch ppc ppc64
# FIXME need to make make check work without --enable-debug
#make check
%endif

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# we build into /usr/lib, but we want the libraries (but not 
# the devel stuff) in /lib
./mkinstalldirs $RPM_BUILD_ROOT/%{_lib}
pushd $RPM_BUILD_ROOT%{_libdir}
for name in glib gobject gmodule gthread gio; do
  mv lib${name}-2.0.so.* ../../%{_lib}
  ln -sf ../../%{_lib}/lib${name}-2.0.so.*.* lib${name}-2.0.so
done
popd

## glib2.sh and glib2.csh
./mkinstalldirs $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}

%find_lang glib20

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f glib20.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING NEWS README
%{libdir}/libglib-2.0.so.*
%{libdir}/libgthread-2.0.so.*
%{libdir}/libgmodule-2.0.so.*
%{libdir}/libgobject-2.0.so.*
%{libdir}/libgio-2.0.so.*
%{_sysconfdir}/profile.d/*
%{_libdir}/gio/modules/libgiofam.so

%files devel
%defattr(-, root, root, -)
%{_libdir}/lib*.so
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0
%{_bindir}/*
%doc %{_datadir}/gtk-doc/html/*
%doc %{_mandir}/man1/*

%files static
%defattr(-, root, root, -)
%{_libdir}/lib*.a

%changelog
* Mon Jan 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Tue Jan  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- 2.15.1
- add new BuildRequires
- 
* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-4
- Another attempt

* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-3
- Fix some errors in desktop files handling

* Fri Dec 21 2007 Caolan McNamara <caolanm@redhat.com> - 2.15.0-2
- add jakubs patch in so xulrunner will build and so gcc too

* Thu Dec 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-1
- Update to 2.15.0

* Sat Nov 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.4-1
- Update to 2.14.4

* Wed Nov  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.3-1
- Update to 2.14.3, including a new version of PCRE that
  fixes several vulnerabilities

* Tue Oct 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.2-1
- Update to 2.14.2 (bug fixes)

* Sun Sep 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.1-1
- Update to 2.14.1

* Sat Aug  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-3
- Update License field
- Don't ship ChangeLog

* Thu Jul 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-2
- Fix build issues on ppc

* Thu Jul 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-1
- Update to 2.13.7

* Fri Jun 29 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.6-1
- Update to 2.13.6
- Drop an ancient Conflict

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.5-1
- Update to 2.13.5

* Wed Jun  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.4-1
- Update to 2.13.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.3-1
- Update to 2.13.3

* Wed May 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.2-1
- Update to 2.13.2

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.1-1
- Update to 2.13.1

* Fri Mar  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.11-1
- Update to 2.12.11

* Wed Mar  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.10-1
- Update to 2.12.10

* Fri Feb  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-4
- More package review demands:
 * keep all -devel content in /usr/lib

* Sun Feb  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-3
- More package review feedback:
 * install /etc/profile.d snipplets as 644
 * explain Conflict with libgnomeui
 * remove stale Conflict with glib-devel
 
* Sat Feb  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-2
- Incorporate package review feedback:
 * drop an obsolete Provides:
 * add a -static subpackage
 * explain %%check ppc exception
 * align summaries
 
* Tue Jan 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-1
- Update to 2.12.9

* Mon Jan 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.8-1
- Update to 2.12.8

* Thu Jan  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.7-1
- Update to 2.12.7
- Fix bit-test on x86-64

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.6-1
- Update to 2.12.6

* Mon Dec 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.5-2
- Fix the configure check for broken poll

* Mon Dec 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.5-1
- Update to 2.12.5

* Sun Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.4-1
- Update to 2.12.4

* Wed Aug 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.3-1.fc6
- Update to 2.12.3
- Drop upstreamed patch

* Sun Aug 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.2-2.fc6
- Use Posix monotonic timers for GTimer

* Tue Aug 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.2-1.fc6
- Update to 2.12.2

* Sat Jul 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.12.0-1.1
- rebuild

* Sun Jul  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Jun 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.4-1
- Update to 2.11.4

* Mon Jun 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.3-1
- Update to 2.11.3

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Thu Jun  1 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-6
- Rebuild

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-5
- Fix some fallout

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-4
- Include static libraries, since anaconda needs them (#193143)

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-3
- Keep glibconfig.h in /usr/lib

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-2
- Move glib to /lib

* Mon May 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Tue May 2 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.0-1
- Update to 2.11.0

* Fri Apr 7 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.2-2
- Update to 2.10.2

* Tue Mar 7 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Fri Feb 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Sat Feb 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.6-1
- Update to 2.9.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.9.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.9.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.5-1
- Update to 2.9.5

* Wed Jan 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.4-1
- Update to 2.9.4

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.3-1
- Update to 2.9.3

* Fri Jan  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.2-2
- Update to 2.9.2

* Sun Dec 11 2005 Matthias Clasen <mclasen@redhat.com>
- Specfile cosmetics

* Sat Dec 10 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.1-1
- New upstream version

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.0-1
- New upstream version

* Tue Nov 15 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.4-1
- New upstream version

* Mon Oct  3 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.3-1
- New upstream version

* Mon Sep 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.2-1
- New upstream version

* Sat Aug 23 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.1-1
- New upstream version
- Drop patches

* Sat Aug 13 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.0-1
- New stable upstream version
- Drop patches

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-3
- Fix C++ guards in gstdio.h

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-2
- Another attempt to fix atomic ops on s390

* Tue Aug  3 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-1
- Update to 2.7.6

* Tue Aug  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.5-1
- Update to 2.7.5

* Fri Jul 22 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Fri Jul 15 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Fri Jul  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.2-1
- Update to 2.7.2

* Fri Jul  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Mon Jun 13 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.0-1
- Update to 2.7.0

* Wed Apr  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.4-1
- Update to 2.6.4
- Drop upstreamed patches

* Fri Mar 11 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-4
- Fix #150817

* Wed Mar  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-3
- Rebuild

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-2
- Rebuild with gcc4

* Mon Feb 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-1
- Upgrade to 2.6.3

* Fri Feb  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.2-1
- Upgrade to 2.6.2

* Mon Jan 10 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.1-1
- Upgrade to 2.6.1

* Mon Dec 21 2004 Matthias Clasen <mclasen@redhat.com> - 2.6.0-1
- Upgrade to 2.6.0
 
* Mon Dec 06 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.8-1
- Upgrade to 2.4.8
 
* Wed Oct 13 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.7-1
- Upgrade to 2.4.7
 
* Fri Aug 13 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.6-1
- Update to 2.4.6

* Sun Aug 1 2004 ALan Cox <alan@redhat.com> - 2.4.5-2
- Fixed BuildRoot to use % macro not hardcode /var/tmp

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.5-1
- Update to 2.4.5
- Escape macros in changelog section

* Fri Jul 09 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.4-1
- Update to 2.4.4

* Mon Jun 21 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.2-1
- Require gettext at build time  (#125320)
- Update to 2.4.2 (#125736)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 19 2004 Matthias Clasen <mclasen@redhat.com> 2.4.1-1
- Update to 2.4.1

* Tue Mar 16 2004 Owen Taylor <otaylor@redhat.com> 2.4.0-1
- Update to 2.4.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.3.6-1
- Update to 2.3.6
- Remove gatomic build fix

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Mark McLoughlin <markmc@redhat.com> 2.3.5-1
- Update to 2.3.5
- Fix build on ppc64
- Disable make check on s390 as well - test-thread failing

* Wed Feb 25 2004 Mark McLoughlin <markmc@redhat.com> 2.3.3-1
- Update to 2.3.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Jonathan Blandford <jrb@redhat.com> 2.3.2-1
- new version
- remove 'make check' temporarily

* Mon Sep  8 2003 Owen Taylor <otaylor@redhat.com> 2.2.3-2.0
- Conflict with libgnomeui <= 2.2.0 (#83581, Göran Uddeborg)

* Tue Aug 26 2003 Owen Taylor <otaylor@redhat.com> 2.2.3-1.1
- Version 2.2.3

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 2.2.2-2.0
- Bump for rebuild

* Sun Jun  8 2003 Owen Taylor <otaylor@redhat.com>
- Version 2.2.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Sun Feb  2 2003 Owen Taylor <otaylor@redhat.com>
- Version 2.2.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Owen Taylor <otaylor@redhat.com>
- Add static libraries to build (#78685, Bernd Kischnick)
- Bump-and-rebuild for new redhat-rpm-config

* Fri Dec 20 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.2.0
- Add make check to the build process

* Mon Dec 16 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.5

* Wed Dec 11 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.4

* Mon Dec  2 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.3

* Mon Oct 07 2002 Havoc Pennington <hp@redhat.com>
- Try rebuilding with new arches

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- install glib2.sh and glib2.csh to set G_BROKEN_FILENAMES
- blow away unpackaged files in install

* Thu Aug  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.6
- Remove fixed-ltmain.sh; shouldn't be needed any more.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.4

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 24 2002 Havoc Pennington <hp@redhat.com>
 - rebuild in different environment

* Mon Apr 15 2002 Owen Taylor <otaylor@redhat.com>
- Fix missing .po files (#63336)

* Wed Apr  3 2002 Alex Larsson <alexl@redhat.com>
- Update to version 2.0.1

* Fri Mar  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.0

* Mon Feb 25 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.3.15

* Thu Feb 21 2002 Alex Larsson <alexl@redhat.com>
- Bump for rebuild

* Mon Feb 18 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.3.14

* Fri Feb 15 2002 Havoc Pennington <hp@redhat.com>
- add horrible buildrequires hack

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.3.13.91 cvs snap

* Mon Feb 11 2002 Matt Wilson <msw@redhat.com>
- rebuild from CVS snapshot
- use setup -q

* Thu Jan 31 2002 Jeremy Katz <katzj@redhat.com>
- rebuild

* Tue Jan 29 2002 Owen Taylor <otaylor@redhat.com>
- 1.3.13

* Tue Jan 22 2002 Havoc Pennington <hp@redhat.com>
- attempting rebuild in rawhide

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- remove 64-bit patch now upstream, 1.3.12.90

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- add some missing files to file list, langify

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- add temporary patch to fix GTypeFundamentals on 64-bit

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- Version 1.3.11

* Thu Oct 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.10

* Tue Sep 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.9

* Wed Sep 19 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.8

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
- Move back to standard %%{prefix}

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
- removed libtoolize from %%build

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

