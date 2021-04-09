%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define api	3
%define major	6
%define gir_api 3.0
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname -d %{name}
%define libnamegir %mklibname %{name}-gir %{gir_api}

Summary:	API documentation browser for developers
Name:		devhelp
Version:	40
Release:	0.alpha
License:	GPLv2+
Group:		Development/Other
Url:		http://live.gnome.org/devhelp
Source0:	http://ftp.acc.umu.se/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.alpha.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	gnome-common
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:  pkgconfig(amtk-5)
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.11
BuildRequires:	pkgconfig(gthread-2.0) >= 2.10.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.2
BuildRequires:	pkgconfig(webkit2gtk-4.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(gio-2.0) >= 2.37.3
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libxml2-utils
BuildRequires:	meson
BuildRequires:  gtk-doc

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

%package -n %{libnamegir}
Summary:        GObject Introspection interface description for devhelp
Group:          System/Libraries

%description -n %{libnamegir}
GObject Introspection interface description for devhelp.

%prep
%autosetup -n %{name}-%{version}.alpha -p1

%build
%meson -Denable_gtk_doc=true
%meson_build

%install
%meson_install

find %{buildroot} -name '*.la' -delete

# owns this dir
mkdir -p %{buildroot}%{_datadir}/%{name}/books

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc AUTHORS NEWS README.md
%{_bindir}/*
%{_datadir}/applications/org.gnome.Devhelp.desktop
#{_datadir}/GConf/gsettings/devhelp.convert
%{_datadir}/devhelp
%{_datadir}/glib-2.0/schemas/org.gnome.devhelp.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.libdevhelp-3.gschema.xml
#{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/apps/*.svg
#{_datadir}/icons/hicolor/*/apps/%{name}-symbolic.svg
%{_datadir}/dbus-1/services/org.gnome.Devhelp.service
%{_mandir}/man1/devhelp.1.*
%{_datadir}/metainfo/org.gnome.Devhelp.appdata.xml

%files -n %{libname}
%{_libdir}/lib%{name}-%{api}.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{name}-%{api}.so
%{_libdir}/pkgconfig/lib%{name}-3.0.pc
%{_includedir}/%{name}-3
%{_datadir}/gir-1.0/Devhelp-%{gir_api}.gir
#{_datadir}/gtk-doc/html/devhelp-3/

%files -n %{libnamegir}
%{_libdir}/girepository-1.0/Devhelp-%{gir_api}.typelib

%files -n %{name}-plugins
#{_libdir}/gedit/plugins/*

