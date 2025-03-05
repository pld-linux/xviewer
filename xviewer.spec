#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_without	librsvg	# SVG scaling using librsvg

Summary:	Image viewer which supports many formats
Summary(pl.UTF-8):	Przeglądarka obrazów obsługująca wiele formatów
Name:		xviewer
Version:	3.4.8
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
#Source0Download: https://github.com/linuxmint/xviewer/tags
Source0:	https://github.com/linuxmint/xviewer/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bc1db6b1fd308ed595cf38491ab9fa4b
URL:		https://github.com/linuxmint/xviewer
BuildRequires:	cinnamon-desktop-devel >= 3.2.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	exempi-devel >= 1.99.5
BuildRequires:	gdk-pixbuf2-devel >= 2.19.1
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.38.0
#BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.16}
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libexif-devel >= 1:0.6.14
BuildRequires:	libjpeg-devel >= 8
BuildRequires:	libpeas-devel >= 0.7.4
BuildRequires:	libpeas-gtk-devel >= 0.7.4
BuildRequires:	libportal-devel >= 0.5
BuildRequires:	libportal-gtk3-devel >= 0.5
%{?with_librsvg:BuildRequires:	librsvg-devel >= 2.36.2}
BuildRequires:	meson >= 0.49
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	xapps-devel >= 2.5.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	yelp-tools
BuildRequires:	zlib-devel
Requires(post,postun):	glib2 >= 1:2.38.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	cinnamon-desktop-libs >= 3.2.0
Requires:	exempi >= 1.99.5
Requires:	gdk-pixbuf2 >= 2.19.1
Requires:	glib2 >= 1:2.38.0
Requires:	gtk+3 >= 3.0
Requires:	hicolor-icon-theme
Requires:	libexif >= 1:0.6.14
Requires:	libpeas >= 0.7.4
Requires:	libpeas-gtk >= 0.7.4
%{?with_rsvg:Requires:	librsvg >= 2.36.2}
Requires:	shared-mime-info >= 0.50
Requires:	xapps-libs >= 2.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xviewer is an image viewer which supports many formats, targeted
mainly for Cinnamon environment. It can be used to view single images
or images in a collection.

%description -l pl.UTF-8
Xviewer to przeglądarka obrazów obsługująca wiele formatów, skierowana
głównie dla środowiska Cinnamon. Pozwala oglądać obrazy pojedyncze lub
w kolekcji.

%package devel
Summary:	Header files for Xviewer
Summary(pl.UTF-8):	Pliki nagłówkowe Xviewer
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cinnamon-desktop-devel >= 3.2.0
Requires:	exempi-devel >= 1.99.5
Requires:	libexif-devel >= 0.6.14
Requires:	libjpeg-devel >= 8
Requires:	glib2-devel >= 1:2.38.0
Requires:	gtk+3-devel >= 3.0
Requires:	lcms2-devel >= 2
Requires:	libpeas-devel >= 0.7.4
Requires:	libpeas-gtk-devel >= 0.7.4
%{?with_librsvg:Requires:	librsvg-devel >= 2.36.2}
Requires:	xorg-lib-libX11-devel
Requires:	xapps-devel >= 2.5.0
Requires:	zlib-devel

%description devel
Header files for Xviewer.

%description devel -l pl.UTF-8
Pliki nagłówkowe Xviewer.

%package apidocs
Summary:	Xviewer API documentation
Summary(pl.UTF-8):	Dokumentacja API Xviewer
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
Xviewer API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Xviewer.

%prep
%setup -q

%build
%meson \
	--default-library=shared \
	-Ddocs=%{__true_false apidocs} \
	-Dexempi=enabled \
	-Dexif=enabled \
	-Djpeg=enabled \
	-Dlcms=enabled \
	-Drsvg=%{__enabled_disabled librsvg}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_datadir}}/xviewer/plugins

%meson_install

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_desktop_database_postun
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS README.md THANKS debian/changelog
%attr(755,root,root) %{_bindir}/xviewer
%dir %{_libdir}/xviewer
%attr(755,root,root) %{_libdir}/xviewer/libxviewer.so
%dir %{_libdir}/xviewer/girepository-1.0
%{_libdir}/xviewer/girepository-1.0/Xviewer-3.0.typelib
%dir %{_libdir}/xviewer/plugins
%{_datadir}/glib-2.0/schemas/org.x.viewer.enums.xml
%{_datadir}/glib-2.0/schemas/org.x.viewer.gschema.xml
%{_datadir}/metainfo/xviewer.appdata.xml
%dir %{_datadir}/xviewer
%dir %{_datadir}/xviewer/gir-1.0
%{_datadir}/xviewer/gir-1.0/Xviewer-3.0.gir
%{_datadir}/xviewer/icons
%{_datadir}/xviewer/pixmaps
%dir %{_datadir}/xviewer/plugins
%{_desktopdir}/xviewer.desktop
%{_iconsdir}/hicolor/*x*/apps/xviewer.png
%{_iconsdir}/hicolor/scalable/apps/xviewer.svg

%files devel
%defattr(644,root,root,755)
%{_includedir}/xviewer
%{_pkgconfigdir}/xviewer.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/xviewer
%endif
