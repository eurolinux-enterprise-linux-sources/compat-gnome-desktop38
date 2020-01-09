%define gtk3_version                      3.3.6
%define glib2_version                     2.35.0
%define startup_notification_version      0.5
%define gtk_doc_version                   1.9
%define gsettings_desktop_schemas_version 3.5.91
%define po_package                        gnome-desktop-3.0

Summary: Compat package with gnome-desktop 3.8 libraries
Name: compat-gnome-desktop38
Version: 3.8.4
Release: 2%{?dist}
URL: http://www.gnome.org
Source0: http://download.gnome.org/sources/gnome-desktop/3.8/gnome-desktop-%{version}.tar.xz
Patch0: 0001-default-input-sources-Switch-ja_JP-default-to-ibus-k.patch
Patch1: dont-use-locale-archive.patch

License: GPLv2+ and LGPLv2+
Group: System Environment/Libraries

# needed for GnomeWallClock
Requires: gsettings-desktop-schemas >= %{gsettings_desktop_schemas_version}

Requires: redhat-menus

# Make sure to update libgnome schema when changing this
Requires: system-backgrounds-gnome

# Make sure that gnome-themes-standard gets pulled in for upgrades
Requires: gnome-themes-standard

BuildRequires: gnome-common
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gobject-introspection-devel
BuildRequires: gsettings-desktop-schemas-devel >= %{gsettings_desktop_schemas_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: libxkbfile-devel
BuildRequires: xkeyboard-config-devel
BuildRequires: gettext
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: automake autoconf libtool intltool
BuildRequires: itstool
BuildRequires: iso-codes-devel

%description
Compatibility package with gnome-desktop 3.8 librarires.

%package -n compat-libgnome-desktop3-7
Summary: Compat package with gnome-desktop 3.8 libraries
# Explicitly conflict with older gnome-desktop3 packages that ship libraries
# with the same soname as this compat package
Conflicts: gnome-desktop3 < 3.10

%description -n compat-libgnome-desktop3-7
Compatibility package with gnome-desktop 3.8 librarires.

%prep
%setup -q -n gnome-desktop-%{version}
%patch0 -p1
%patch1 -p1 -b .dont-use-locale-archive

%build
%configure --with-pnp-ids-path="/usr/share/hwdata/pnp.ids"
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# stuff we don't want
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/girepository-1.0/GnomeDesktop-3.0.typelib
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
rm -rf $RPM_BUILD_ROOT%{_libexecdir}
rm -rf $RPM_BUILD_ROOT%{_datadir}

%post -n compat-libgnome-desktop3-7 -p /sbin/ldconfig

%postun -n compat-libgnome-desktop3-7 -p /sbin/ldconfig

%files -n compat-libgnome-desktop3-7
%doc COPYING COPYING.LIB
%{_libdir}/lib*.so.*

%changelog
* Fri Nov 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.8.4-2
- Use same subpackage naming as in other el7-gnome-3-14 compat packages

* Fri Nov 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.8.4-1
- gnome-desktop3 compat package for el7-gnome-3-14
