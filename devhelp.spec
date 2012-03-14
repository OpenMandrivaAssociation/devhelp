%define api		3
%define major	0
%define libname %mklibname %{name} %{api} %{major}
%define develname %mklibname -d %{name}

Summary:	API documentation browser for developers
Name:		devhelp
Version:	3.2.0
Release:	1
License:	GPLv2+
Group:		Development/Other
URL:		http://developer.imendio.com/projects/devhelp
Source0:	http://ftp.gnome.org/pub/GNOME/sources/devhelp/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(webkitgtk-3.0)

%description
Devhelp is an API documentation browser for GNOME. It works
natively with Gtk-doc (System used in GTK+ and GNOME for
documentating APIs) and it is possible to create books for other
documentation as well.

%package -n %{libname}
Summary:	Dynamic libraries for devhelp
Group:		%{group}

%description -n %{libname}
this package contains dynamic libraries for devhelp.

%package -n %{develname}
Summary:	Development libraries, include files for devhelp
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development library and headers file for devhelp.

%package -n %{name}-plugins
Summary:	Gedit Plugins for Devhelp
Group:		Editors
Requires:	gedit

%description -n %{name}-plugins
Gedit plugins to use with Devhelp.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std

# owns this dir
mkdir -p %{buildroot}%{_datadir}/%{name}/books

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/devhelp.schemas
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/devhelp
%{_datadir}/icons/hicolor/*

%files -n %{libname}
%{_libdir}/libdevhelp-%{api}.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/devhelp-%{api}.0

%files -n %{name}-plugins
%{_libdir}/gedit/plugins/

