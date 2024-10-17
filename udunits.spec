Name:		udunits
Version:	1.12.9
Release:	5
Summary:	A library for manipulating units of physical quantities
License:	Freely distributable (BSD-like)
Group:		Sciences/Mathematics
URL:		https://my.unidata.ucar.edu/content/software/udunits/index.html
Source0:	ftp://ftp.unidata.ucar.edu/pub/udunits/udunits-%{version}.tar.gz
Patch0:		udunits-1.12.9-linuxfixes.patch
Patch1:		udunits-1.12.4-64bit.patch
BuildRequires:	gcc-gfortran, gcc-c++, groff
BuildRequires:	perl-devel
BuildRequires:	bison

%description
The Unidata units utility, udunits, supports conversion of unit specifications 
between formatted and binary forms, arithmetic manipulation of unit 
specifications, and conversion of values between compatible scales of 
measurement. A unit is the amount by which a physical quantity is measured. For
example:

                  Physical Quantity   Possible Unit
                  _________________   _____________
                        time              weeks
                      distance         centimeters
                        power             watts

This utility works interactively and has two modes. In one mode, both an input 
and output unit specification are given, causing the utility to print the 
conversion between them. In the other mode, only an input unit specification is
given. This causes the utility to print the definition -- in standard units -- 
of the input unit.

%package	devel
Group:		Development/Other
Summary:	Headers and libraries for udunits
Requires:	%{name} = %{version}-%{release}

%description	devel
This package contains the files needed for compiling programs using
the udunits library.

%package -n	perl-udunits
Summary:	Perl module for udunits
Group:		Development/Perl
Requires:	%{name}

%description -n	perl-udunits
A perl module for udunits.

%prep
%setup -q
%patch0 -p1 -b .linux~
# Yes, this is a dirty hack.
%ifarch x86_64 ppc64 sparc64
%patch1 -p1
%endif

%build
export CC=gcc
%ifarch x86_64
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
%endif
cd src/
export LD_MATH=-lm 
%configure

# Don't use %make, don't compil...
make all 

%install
cd src/
sed "s?/usr?${RPM_BUILD_ROOT}/usr?" Makefile > Makefile.install
make PREFIX=${RPM_BUILD_ROOT}/%{_prefix} datadir=${RPM_BUILD_ROOT}/%{sysconfdir} \
    sysconfigdir=${RPM_BUILD_ROOT}/%{_sysconfdir} -f Makefile.install install


find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;
rm -rf ${RPM_BUILD_ROOT}/usr/share/man3f

# Nuke perm
find %{buildroot}%{perl_vendorlib} -type d -exec chmod 755 {} \;

%files
%doc src/{COPYRIGHT,README,RELEASE_NOTES,VERSION}
%{_bindir}/udunits
%{_mandir}/man1/udunits.1*
%config(noreplace) %{_sysconfdir}/udunits.dat

%files devel
%{_includedir}/udunits.h
%{_includedir}/udunits.inc
%{_libdir}/libudport.a
%{_libdir}/libudunits.a
%{_mandir}/man3*/udunits.3*


%files -n perl-udunits
%{perl_vendorarch}/*
%{_mandir}/man1/udunitsperl.1*


%changelog
* Wed Feb 15 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.12.9-4
+ Revision: 774133
- regenerate P0 in stead of changing patch fuzz level
- cleanout spec
- fix duplicate packaging of man pages
- mass rebuild of perl extensions against perl 5.14.2

* Thu Jul 22 2010 Jérôme Quelin <jquelin@mandriva.org> 1.12.9-3mdv2011.0
+ Revision: 556782
- perl 5.12 rebuild

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 1.12.9-2mdv2010.0
+ Revision: 445605
- rebuild

* Sun Jan 04 2009 Olivier Thauvin <nanardon@mandriva.org> 1.12.9-1mdv2009.1
+ Revision: 324046
- brequires bison
- remove wrong comment now
- 1.12.9

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.12.4-5mdv2009.0
+ Revision: 255048
- rebuild
- fix description-line-too-long

* Mon Jan 21 2008 Thierry Vignaud <tv@mandriva.org> 1.12.4-3mdv2008.1
+ Revision: 155664
- rebuild for new perl

* Wed Jan 02 2008 Olivier Blin <blino@mandriva.org> 1.12.4-2mdv2008.1
+ Revision: 140924
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Wed Aug 09 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/09/06 20:30:20 (55125)
- rebuild

* Wed Aug 09 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/09/06 20:27:48 (55124)
Import udunits

* Thu Sep 29 2005 Olivier Thauvin <nanardon@mandriva.org> 1.12.4-1mdk
- From Philippe Weill <Philippe.Weill@aero.jussieu.fr>
  - Inital Mandriva spec

* Mon May 09 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-8
- remove hardcoded dist tags

* Fri May 06 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-7
- fix BuildRequires for the FC-3 spec (gcc-g77 vs gcc-gfortran)

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-6.fc4
- use dist tag

* Sat Apr 16 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-5
- x86_64 needs -fPIC

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-4
- use perl macros

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-3
- Corrected license
- Add BuildRequires: groff
- Add perl MODULE_COMPAT requires for perl-udunits
- Roll in fixes from Ed Hill's package
- Make -devel package

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-2
- minor spec cleanup

* Fri Mar 25 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-1
- inital package for Fedora Extras

