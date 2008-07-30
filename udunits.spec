%define version 1.12.4
%define release %mkrel 5

Name: udunits
Version: %version
Release: %release
Summary: A library for manipulating units of physical quantities
License: Freely distributable (BSD-like)
Group: Sciences/Mathematics
URL: http://my.unidata.ucar.edu/content/software/udunits/index.html
# Upstream actually packages it as a .tar.Z, I repackaged to prevent ncompress 
# as a dependency.
Source0: udunits-1.12.4.tar.bz2
Patch0: udunits-1.12.4-linuxfixes.patch
Patch1: udunits-1.12.4-64bit.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-gfortran, gcc-c++, groff
BuildRequires: perl-devel

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

%package devel
Group: Development/Other
Summary: Headers and libraries for udunits
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the files needed for compiling programs using
the udunits library.

%package -n perl-udunits
Summary: Perl module for udunits
Group: Development/Perl
Requires: %{name}

%description -n perl-udunits
A perl module for udunits.

%prep
%setup -q
%patch0 -p1
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
rm -rf $RPM_BUILD_ROOT
cd src/
sed "s?/usr?${RPM_BUILD_ROOT}/usr?" Makefile > Makefile.install
make PREFIX=${RPM_BUILD_ROOT}/%{_prefix} datadir=${RPM_BUILD_ROOT}/%{sysconfdir} \
    sysconfigdir=${RPM_BUILD_ROOT}/%{_sysconfdir} -f Makefile.install install


find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;
rm -rf ${RPM_BUILD_ROOT}/usr/share/man3f

# Nuke perm
find %{buildroot}%{perl_vendorlib} -type d -exec chmod 755 {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc src/{COPYRIGHT,README,RELEASE_NOTES,VERSION}
%{_bindir}/udunits
%{_mandir}/man1/udunits*
%config(noreplace) %{_sysconfdir}/udunits.dat

%files devel
%defattr(-,root,root)
%{_includedir}/udunits.h
%{_includedir}/udunits.inc
%{_libdir}/libudport.a
%{_libdir}/libudunits.a
%{_mandir}/man3*/udunits*


%files -n perl-udunits
%defattr(-,root,root)
%{perl_vendorarch}/*
%{_mandir}/man1/udunitsperl*

