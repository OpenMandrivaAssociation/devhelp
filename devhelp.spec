%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api	3
%define major	1
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname -d %{name}

Summary:	API documentation browser for developers
Name:		devhelp
Version:	3.6.1
Release:	8
License:	GPLv2+
Group:		Development/Other
Url:		http://live.gnome.org/devhelp
Source0:	http://ftp.acc.umu.se/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		devhelp-3.3.91-linking.patch

BuildRequires:	desktop-file-utils
BuildRequires:	gnome-common
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig(gconf-2.0) >= 2.6.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.11
BuildRequires:	pkgconfig(gthread-2.0) >= 2.10.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.2
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(python2)

%description
Devhelp is an API documentation browser for GNOME 2. It works
natively with Gtk-doc (System used in GTK+ and GNOME for
documentating APIs) and it is possible to create books for other
documentation as well.

%package -n %{libname}
Summary:	Dynamic libraries for devhelp
Group:		System/Libraries
Suggests:	%{name} = %{version}

%description -n %{libname}
this package contains dynamic libraries for devhelp.

%package -n %{devname}
Summary:	Development files and headers for devhelp
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description -n %{devname}
This package contains the development files and headers for devhelp.

%package -n %{name}-plugins
Summary:	Gedit Plugins for Devhelp
Group:		Editors
Requires:	gedit

%description -n %{name}-plugins
Gedit plugins to use with Devhelp.

%prep
%setup -q
%apply_patches

%build
export PYTHON=%{__python2}
NOCONFIGURE=1 gnome-autogen.sh
autoreconf --install
intltoolize
autoreconf

%configure --disable-static
%make

%install
%makeinstall_std

# owns this dir
mkdir -p %{buildroot}%{_datadir}/%{name}/books

%find_lang %{name}

%preun
%preun_uninstall_gconf_schemas %{name}

%files -f %{name}.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/devhelp.schemas
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/devhelp
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files -n %{libname}
%{_libdir}/lib%{name}-%{api}.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{name}-%{api}.so
%{_libdir}/pkgconfig/lib%{name}-3.0.pc
%{_includedir}/devhelp-3.0/

%files -n %{name}-plugins
%{_libdir}/gedit/plugins/*

