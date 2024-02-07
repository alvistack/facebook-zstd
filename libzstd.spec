# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: libzstd
Epoch: 100
Version: 1.5.5
Release: 1%{?dist}
Summary: Zstd compression library
License: BSD-3-Clause
URL: https://github.com/facebook/zstd/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: lz4-devel
BuildRequires: make
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
export LIBDIR="%{_libdir}"
export PREFIX="%{_prefix}"
%make_build -C lib lib-mt
%make_build -C programs
%make_build -C contrib/pzstd

%check

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
install -D -m755 contrib/pzstd/pzstd %{buildroot}%{_bindir}/pzstd
install -D -m644 programs/zstd.1 %{buildroot}%{_mandir}/man1/pzstd.1

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n zstd
Summary: Zstd binary

%description -n zstd
Zstandard compression binary.

%package -n libzstd1
Summary: Zstd compression library
Group: System/Libraries

%description -n libzstd1
Zstd, short for Zstandard, is a lossless compression algorithm,
targeting faster compression than zlib at comparable ratios.

This subpackage contains the implementation as a shared library.

%package -n libzstd-devel
Summary: Development files for the Zstd compression library
Group: Development/Libraries/C and C++
Requires: libzstd1 = %{epoch}:%{version}-%{release}
Requires: glibc-devel

%description -n libzstd-devel
Zstd, short for Zstandard, is a lossless compression algorithm,
targeting faster compression than zlib at comparable ratios.

Needed for compiling programs that link with the library.

%package -n libzstd-devel-static
Summary: Development files for the Zstd compression library
Group: Development/Libraries/C and C++
BuildRequires: glibc-devel-static
Requires: libzstd-devel = %{epoch}:%{version}-%{release}

%description -n libzstd-devel-static
Zstd, short for Zstandard, is a lossless compression algorithm,
targeting faster compression than zlib at comparable ratios.

Needed for compiling programs that link with the library.

%post -n libzstd1 -p /sbin/ldconfig
%postun -n libzstd1 -p /sbin/ldconfig

%files -n zstd
%license COPYING LICENSE
%{_bindir}/*
%{_mandir}/man1/*

%files -n libzstd1
%license COPYING LICENSE
%{_libdir}/libzstd.so.1*

%files -n libzstd-devel
%license COPYING LICENSE
%{_includedir}/*.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%files -n libzstd-devel-static
%{_libdir}/libzstd.a
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n zstd
Summary: Zstd binary

%description -n zstd
Zstandard compression binary.

%package -n libzstd-devel
Summary: Header files for Zstd library
Requires: libzstd = %{epoch}:%{version}-%{release}

%package -n libzstd-static
Summary: Static variant of the Zstd library
Requires: libzstd-devel = %{epoch}:%{version}-%{release}

%description -n libzstd-devel
Header files for Zstd library.

%description -n libzstd-static
Static variant of the Zstd library.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING LICENSE
%{_libdir}/libzstd.so.*

%files -n zstd
%license COPYING LICENSE
%{_bindir}/*
%{_mandir}/man1/*

%files -n libzstd-devel
%{_includedir}/*
%{_libdir}/libzstd.so
%{_libdir}/pkgconfig/libzstd.pc

%files -n libzstd-static
%{_libdir}/libzstd.a
%endif

%changelog
