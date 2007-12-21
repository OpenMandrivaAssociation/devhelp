%define _requires_exceptions libnspr4\\|libplc4\\|libplds4\\|libnss\\|libsmime3\\|libsoftokn\\|libssl3\\|libgtkembedmoz\\|libxpcom

%define lib_major 0
%define api_version 1
%define libname %mklibname %{name}- %{api_version} %{lib_major}
%define libnamedev %mklibname -d %{name}- %{api_version}

%define build_with_firefox 1

# Build with mozilla instead of firefox
%{?_with_mozilla: %global build_with_firefox 0}
%{?_without_mozilla: %global build_with_firefox 1}

%if %build_with_firefox
%define firefox_version %(rpm -q mozilla-firefox --queryformat %{VERSION})
%endif

Summary:	API documentation browser for developers
Name:		devhelp
Version:	0.16.1
Release:	%mkrel 4
License:	GPL
Group:		Development/Other
URL:		http://www.imendio.com/projects/devhelp/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/devhelp/%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
%if %{build_with_firefox}
%if %mdkversion < 200700
Requires:	mozilla-firefox = %firefox_version
%else 
Requires: 	%mklibname mozilla-firefox %{firefox_version}
%endif
%else
Requires:	mozilla = %(rpm -q mozilla --queryformat %{VERSION})
%endif
BuildRequires:	libwnck-devel
BuildRequires:	gtk+2-devel >= 2.3.1
BuildRequires:	libglade2.0-devel
BuildRequires:	libGConf2-devel
%if %{build_with_firefox}
BuildRequires:  mozilla-firefox-devel
%else
BuildRequires:	mozilla-devel 
%endif
BuildRequires:	ImageMagick
BuildRequires:  intltool
BuildRequires:  desktop-file-utils

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Devhelp is an API documentation browser for GNOME 2. It works
natively with Gtk-doc (System used in GTK+ and GNOME for
documentating APIs) and it is possible to create books for other
documentation as well.

%package -n %{libname}
Summary:	Dynamic libraries for devhelp
Group:		%{group}
Requires:	%{name} >= %{version}

%description -n %{libname}
this package contains dynamic libraries for devhelp.


%package -n %{libnamedev}
Summary:	Static libraries, include files for devhelp
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Obsoletes:  %mklibname -d %{name}- 1 0

%description -n %{libnamedev}
Static library and headers file for devhelp.

%package -n %{name}-plugins
Summary:	Gedit Plugins for Devhelp
Group:		Editors
Requires:	gedit

%description -n %{name}-plugins
Gedit plugins to use with Devhelp.

%prep
%setup -q
touch *

%build
%configure2_5x --disable-install-schemas \
%if %{build_with_firefox}
%if %mdkversion < 200710
--with-mozilla=mozilla-firefox 
%endif
%endif

%make

%install
rm -rf %{buildroot}

%makeinstall_std

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Development-Tools" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/devhelp.desktop

# owns this dir
mkdir -p %{buildroot}%{_datadir}/%{name}/books

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%define schemas devhelp
%post_install_gconf_schemas %schemas

%preun
%preun_uninstall_gconf_schemas %schemas

%postun

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README INSTALL
%_sysconfdir/gconf/schemas/devhelp.schemas
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/devhelp
%{_datadir}/icons/hicolor/*

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libdevhelp-%{api_version}.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/*a
%{_libdir}/pkgconfig/*
%{_includedir}/devhelp-1.0

%files -n %{name}-plugins
%defattr(-, root, root)
%{_libdir}/gedit-2/plugins/


