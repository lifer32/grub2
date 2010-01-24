#
# Conditional build:
%bcond_with	static	# build static binaries
%bcond_without	grubemu	# build grub-emu binary
#
Summary:	GRand Unified Bootloader
Summary(de.UTF-8):	GRUB2 - ein Bootloader für x86 und ppc
Summary(pl.UTF-8):	GRUB2 - bootloader dla x86 i ppc
Summary(pt_BR.UTF-8):	Gerenciador de inicialização GRUB2
Name:		grub2
Version:	1.97.2
Release:	1
License:	GPL v2
Group:		Base
Source0:	http://alpha.gnu.org/gnu/grub/grub-%{version}.tar.gz
# Source0-md5:	db4d23fb8897523a7e484e974ae3d1c9
Source1:	update-grub
Source2:	update-grub.8
Source3:	grub.sysconfig
Source4:	grub-custom.cfg
URL:		http://www.gnu.org/software/grub/grub-2.en.html
BuildRequires:	autoconf >= 2.53
Patch0:		pld-initrd.patch
Patch1:		pld-sysconfdir.patch
Patch2:		grub-garbage.patch
Patch3:		grub-shelllib.patch
Patch4:		grub-install.in.patch
Patch5:		grub-lvmdevice.patch
Patch6:		pld-mkconfigdir.patch
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	gawk
BuildRequires:	help2man
BuildRequires:	libtool
BuildRequires:	texinfo
%ifarch %{ix86} %{x8664}
BuildRequires:	lzo-devel >= 1.0.2
%endif
%ifarch %{x8664}
BuildRequires:	/usr/lib/libc.so
%if "%{pld_release}" == "ac"
BuildRequires:	libgcc32
%else
BuildRequires:	gcc-multilib
%endif
%endif
BuildRequires:	ncurses-devel
BuildRequires:	sed >= 4.0
%if %{with static}
BuildRequires:	glibc-static
%ifarch %{ix86} %{x8664}
BuildRequires:	lzo-static
%endif
BuildRequires:	ncurses-static
%endif
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.213
Provides:	bootloader
Conflicts:	grub
ExclusiveArch:	%{ix86} %{x8664} ppc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_bindir		%{_sbindir}
%define		_libdir		/boot
%define		_libexecdir	%{_libdir}/grub

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems. In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible
loading of multiple boot images (needed for modular kernels such as
the GNU Hurd).

GRUB 2 is derived from PUPA which was a research project to
investigate the next generation of GRUB. GRUB 2 has been rewritten
from scratch to clean up everything for modularity and portability.

GRUB 2 targets at the following goals:
- Scripting support, such as conditionals, loops, variables and
  functions.
- Graphical interface.
- Dynamic loading of modules in order to extend itself at the run time
  rather than at the build time.
- Portability for various architectures.
- Internationalization. This includes support for non-ASCII character
  code, message catalogs like gettext, fonts, graphics console, and so
  on.
- Real memory management, to make GNU GRUB more extensible.
- Modular, hierarchical, object-oriented framework for file systems,
  files, devices, drives, terminals, commands, partition tables and OS
  loaders.
- Cross-platform installation which allows for installing GRUB from a
  different architecture.
- Rescue mode saves unbootable cases. Stage 1.5 was eliminated.
- Fix design mistakes in GRUB Legacy, which could not be solved for
  backward-compatibility, such as the way of numbering partitions.

%description -l de.UTF-8
GRUB (GRand Unified Boot-loader) ist ein Bootloader, der oft auf
Rechnern eingesetzt wird, auf denen das freie Betriebssystem Linux
läuft. GRUB löst den betagten LILO (Linux-Loader) ab.

GRUB wurde innerhalb des GNU Hurd-Projektes als Boot-Loader entwickelt
und wird unter der GPL vertrieben. Aufgrund seiner höheren
Flexibilität verdrängt GRUB in vielen Linux-Distributionen den
traditionellen Boot-Loader LILO.

%description -l es.UTF-8
Éste es GRUB - Grand Unified Boot Loader - un administrador de
inicialización capaz de entrar en la mayoría de los sistemas
operacionales libres - Linux, FreeBSD, NetBSD, GNU Mach, etc. como
también en la mayoría de los sistemas operacionales comerciales para
PC.

El administrador GRUB puede ser una buena alternativa a LILO, para
usuarios conmás experiencia y que deseen obtener más recursos de su
cargador de inicialización (boot loader).

%description -l pl.UTF-8
GRUB jest bootloaderem na licencji GNU, mającym na celu unifikację
procesu bootowania na systemach x86. Potrafi nie tylko ładować jądra
Linuksa i *BSD: posiada również implementacje standardu Multiboot,
który pozwala na elastyczne ładowanie wielu obrazów bootowalnych
(czego wymagają modułowe jądra, takie jak GNU Hurd).

%description -l pt_BR.UTF-8
Esse é o GRUB - Grand Unified Boot Loader - um gerenciador de boot
capaz de entrar na maioria dos sistemas operacionais livres - Linux,
FreeBSD, NetBSD, GNU Mach, etc. assim como na maioria dos sistemas
operacionais comerciais para PC.

O GRUB pode ser uma boa alternativa ao LILO, para usuários mais
avançados e que querem mais recursos de seu boot loader.

%prep
%setup -q -n grub-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal}
%{__autoheader}
echo timestamp > stamp-h.in
%{__autoconf}
export CFLAGS="-Os %{?debug:-g}"

# mawk stalls at ./genmoddep.awk, so force gawk
AWK=gawk \
%configure \
%{?with_grubemu:--enable-grub-emu} \
	BUILD_CFLAGS="$CFLAGS"
%{__make} -j1 \
	BUILD_CFLAGS="$CFLAGS" \
%if %{with static}
%ifarch %{ix86} %{x8664}
	grub_setup_LDFLAGS="-s -static" \
	grub_mkimage_LDFLAGS="-s -static -llzo" \
%else
	grub_mkimage_LDFLAGS="-s -static" \
%endif
	grub_emu_LDFLAGS="-s -static -lncurses -ltinfo" \
%endif
	pkgdatadir=%{_libexecdir} \
	pkglibdir=%{_libexecdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{_sysconfdir}/grub.d}

%{__make} install \
	pkgdatadir=%{_libexecdir} \
	pkglibdir=%{_libexecdir} \
	DESTDIR=$RPM_BUILD_ROOT

cp -a docs/grub.cfg $RPM_BUILD_ROOT%{_libexecdir}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/update-grub
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man8/update-grub.8
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/grub
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/grub.d/custom.cfg
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# deprecated. we don't need it
rm $RPM_BUILD_ROOT/lib/update-grub_lib

# no junk to /boot/grub (put to -devel?)
rm $RPM_BUILD_ROOT%{_libexecdir}/*.h
rm $RPM_BUILD_ROOT%{_libexecdir}/*.mk

# core.img - bootable image generated by grub-mkimage(1) via grub-install(1)
touch $RPM_BUILD_ROOT%{_libexecdir}/core.img
touch $RPM_BUILD_ROOT%{_libexecdir}/device.map

%clean
rm -rf $RPM_BUILD_ROOT

%post -p %{_sbindir}/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun -p %{_sbindir}/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/grub
%attr(755,root,root) %{_sbindir}/grub-fstest
%attr(755,root,root) %{_sbindir}/grub-install
%attr(755,root,root) %{_sbindir}/grub-mkfont
%attr(755,root,root) %{_sbindir}/grub-mkrescue
%attr(755,root,root) %{_sbindir}/grub-editenv
%attr(755,root,root) %{_sbindir}/grub-mkconfig
%attr(755,root,root) %{_sbindir}/grub-mkelfimage
%attr(755,root,root) %{_sbindir}/update-grub
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_sbindir}/grub-mkimage
%{_mandir}/man1/grub-mkimage.1*
%else
%attr(755,root,root) %{_sbindir}/grub-probe
%attr(755,root,root) %{_sbindir}/grub-mkdevicemap
%{_mandir}/man8/grub-probe.8*
%{_mandir}/man8/grub-mkdevicemap.8*
%endif
%{_mandir}/man1/grub-fstest.1*
%{_mandir}/man1/grub-mkfont.1*
%{_mandir}/man1/grub-mkrescue.1*
%{_mandir}/man1/grub-editenv.1*
%{_mandir}/man8/grub-mkconfig.8*
%{_mandir}/man1/grub-mkelfimage.1*
%{_mandir}/man8/update-grub.8*
%if %{with grubemu}
%attr(755,root,root) %{_sbindir}/grub-emu
%{_mandir}/man8/grub-emu.8*
%endif
/lib/grub-mkconfig_lib

%dir %{_libexecdir}
%config(noreplace) %verify(not md5 mtime size) %{_libexecdir}/grub.cfg
%{_libexecdir}/*.lst
%{_libexecdir}/*.mod
%ifarch %{x8664}
%{_libexecdir}/efiemu*.o
%endif
%ifarch %{ix86} %{x8664} sparc sparc64
%{_libexecdir}/boot.img
%{_libexecdir}/cdboot.img
%{_libexecdir}/diskboot.img
%{_libexecdir}/kernel.img
%{_libexecdir}/lnxboot.img
%{_libexecdir}/pxeboot.img
%endif

# generated by grub at runtime
%ghost %{_libexecdir}/device.map
%ghost %{_libexecdir}/core.img

%dir /lib/grub.d
%doc /lib/grub.d/README
%attr(755,root,root) /lib/grub.d/00_header
%attr(755,root,root) /lib/grub.d/10_linux
%attr(755,root,root) /lib/grub.d/30_os-prober
%attr(755,root,root) /lib/grub.d/40_custom

%dir %attr(750,root,root) /etc/grub.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/grub.d/custom.cfg

%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_sbindir}/grub-mkdevicemap
%attr(755,root,root) %{_sbindir}/grub-probe
%attr(755,root,root) %{_sbindir}/grub-setup
%{_mandir}/man8/grub-mkdevicemap.8*
%{_mandir}/man8/grub-probe.8*
%{_mandir}/man8/grub-setup.8*
%endif

%{_infodir}/grub*.info*
