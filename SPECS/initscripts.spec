%global package_speccommit 77f95d7401e9a3f58eaa4a42cc48dab78bf1b504
%global usver 9.49.41
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}

Summary: The inittab file and the /etc/init.d scripts
Name: initscripts
Version: 9.49.41
# ppp-watch is GPLv2+, everything else is GPLv2
License: GPLv2 and GPLv2+
Group: System Environment/Base
Release: %{?xsrel}%{?dist}
URL: https://github.com/fedora-sysv/initscripts
Source0: initscripts-9.49.41.tar.gz
Patch0: initscripts-9.49.41-fix-setting-of-firewall-ZONE.patch
Patch1: initscripts-9.49.41-fix-incorrect-condition-for-RESOLV_MODS.patch
Obsoletes: initscripts-legacy <= 9.39
Requires: /bin/awk, sed, coreutils
Requires: /sbin/sysctl
Requires: grep
Requires: module-init-tools
Requires: util-linux >= 2.16
Requires: bash >= 3.0
Requires: sysvinit-tools >= 2.87-5
Conflicts: systemd < 23-1
Conflicts: systemd-units < 23-1
Conflicts: lvm2 < 2.02.100-5
Conflicts: dmraid < 1.0.0.rc16-18
Requires: systemd
Requires: iproute, /sbin/arping, findutils
Requires: system-release
Requires: udev >= 125-1
Requires: cpio
Requires: hostname
Requires: setup >= 2.8.72
Conflicts: ipsec-tools < 0.8.0-2
Conflicts: NetworkManager < 0.9.9.0-37.git20140131.el7
Requires(pre): /usr/sbin/groupadd
Requires(post): /sbin/chkconfig, coreutils
Requires(preun): /sbin/chkconfig
%{?systemd_requires}
BuildRequires: glib2-devel popt-devel gettext pkgconfig systemd
Provides: /sbin/service


%description
The initscripts package contains basic system scripts used
during a boot of the system. It also contains scripts which
activate and deactivate most network interfaces.

%package -n debugmode
Summary: Scripts for running in debugging mode
Requires: initscripts
Group: System Environment/Base

%description -n debugmode
The debugmode package contains some basic scripts that are used to run
the system in a debugging mode.

Currently, this consists of various memory checking code.

%prep
%autosetup -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make ROOT=$RPM_BUILD_ROOT SUPERUSER=`id -un` SUPERGROUP=`id -gn` mandir=%{_mandir} install

%find_lang %{name}

%ifnarch s390 s390x
rm -f \
 $RPM_BUILD_ROOT/etc/sysconfig/network-scripts/ifup-ctc \
%else
rm -f \
 $RPM_BUILD_ROOT/etc/sysconfig/init.s390
%endif

touch $RPM_BUILD_ROOT/etc/crypttab
chmod 600 $RPM_BUILD_ROOT/etc/crypttab

%post
%systemd_post brandbot.path rhel-autorelabel.service rhel-autorelabel-mark.service rhel-configure.service rhel-dmesg.service rhel-domainname.service rhel-import-state.service rhel-loadmodules.service rhel-readonly.service

touch /var/log/wtmp /var/run/utmp /var/log/btmp
chown root:utmp /var/log/wtmp /var/run/utmp /var/log/btmp
chmod 664 /var/log/wtmp /var/run/utmp
chmod 600 /var/log/btmp

/usr/sbin/chkconfig --add network
/usr/sbin/chkconfig --add netconsole

%preun
%systemd_preun brandbot.path rhel-autorelabel.service rhel-autorelabel-mark.service rhel-configure.service rhel-dmesg.service rhel-domainname.service rhel-import-state.service rhel-loadmodules.service rhel-readonly.service

if [ $1 = 0 ]; then
  /usr/sbin/chkconfig --del network
  /usr/sbin/chkconfig --del netconsole
fi

%postun
%systemd_postun brandbot.path rhel-autorelabel.service rhel-autorelabel-mark.service rhel-configure.service rhel-dmesg.service rhel-domainname.service rhel-import-state.service rhel-loadmodules.service rhel-readonly.service

# We need to keep this in initscripts until the EOL of RHEL-7.2-EUS:
%triggerun -- initscripts < 9.49.40
if [ $1 -gt 1 ]; then
  systemctl enable brandbot.path rhel-autorelabel.service rhel-autorelabel-mark.service rhel-configure.service rhel-dmesg.service rhel-domainname.service rhel-import-state.service rhel-loadmodules.service rhel-readonly.service &> /dev/null || :
  echo -e "\nUPGRADE: Automatically re-enabling default systemd units:\n\tbrandbot.path\n\trhel-autorelabel.service\n\trhel-autorelabel-mark.service\n\trhel-configure.service\n\trhel-dmesg.service\n\trhel-domainname.service\n\trhel-import-state.service\n\trhel-loadmodules.service\n\trhel-readonly.service\n" || :
fi

%files -f %{name}.lang
%defattr(-,root,root)
%dir /etc/sysconfig/network-scripts
%config(noreplace) %verify(not md5 mtime size) /etc/adjtime
%config(noreplace) /etc/sysconfig/init
%config(noreplace) /etc/sysconfig/netconsole
%config(noreplace) /etc/sysconfig/readonly-root
/etc/sysconfig/network-scripts/ifdown
/usr/sbin/ifdown
/etc/sysconfig/network-scripts/ifdown-post
/etc/sysconfig/network-scripts/ifup
/usr/sbin/ifup
/usr/libexec/initscripts/brandbot
%dir /etc/sysconfig/console
%dir /etc/sysconfig/modules
/etc/sysconfig/network-scripts/network-functions
/etc/sysconfig/network-scripts/network-functions-ipv6
/etc/sysconfig/network-scripts/init.ipv6-global
%config(noreplace) /etc/sysconfig/network-scripts/ifcfg-lo
/etc/sysconfig/network-scripts/ifup-post
/etc/sysconfig/network-scripts/ifdown-ppp
/etc/sysconfig/network-scripts/ifup-ppp
/etc/sysconfig/network-scripts/ifup-routes
/etc/sysconfig/network-scripts/ifdown-routes
/etc/sysconfig/network-scripts/ifup-plip
/etc/sysconfig/network-scripts/ifup-plusb
/etc/sysconfig/network-scripts/ifup-bnep
/etc/sysconfig/network-scripts/ifdown-bnep
/etc/sysconfig/network-scripts/ifup-eth
/etc/sysconfig/network-scripts/ifdown-eth
/etc/sysconfig/network-scripts/ifup-ipv6
/etc/sysconfig/network-scripts/ifdown-ipv6
/etc/sysconfig/network-scripts/ifup-sit
/etc/sysconfig/network-scripts/ifdown-sit
/etc/sysconfig/network-scripts/ifup-tunnel
/etc/sysconfig/network-scripts/ifdown-tunnel
/etc/sysconfig/network-scripts/ifup-aliases
/etc/sysconfig/network-scripts/ifup-ippp
/etc/sysconfig/network-scripts/ifdown-ippp
/etc/sysconfig/network-scripts/ifup-wireless
/etc/sysconfig/network-scripts/ifup-isdn
/etc/sysconfig/network-scripts/ifdown-isdn
%ifarch s390 s390x
/etc/sysconfig/network-scripts/ifup-ctc
%endif
%config(noreplace) /etc/networks
%config(noreplace) /etc/rwtab
%config(noreplace) /etc/statetab
%dir /etc/rwtab.d
%dir /etc/statetab.d
/usr/lib/systemd/rhel-*
/usr/lib/systemd/system/*
/etc/inittab
%dir /etc/rc.d
%dir /etc/rc.d/rc[0-9].d
/etc/rc[0-9].d
%dir /etc/rc.d/init.d
/etc/rc.d/init.d/*
%config(noreplace) /etc/sysctl.conf
%{_sysctldir}/00-system.conf
/etc/sysctl.d/99-sysctl.conf
%exclude /etc/profile.d/debug*
/etc/profile.d/*
/usr/sbin/sys-unconfig
/usr/bin/ipcalc
/usr/bin/usleep
%attr(4755,root,root) /usr/sbin/usernetctl
/usr/sbin/consoletype
/usr/sbin/genhostid
/usr/sbin/sushell
%attr(2755,root,root) /usr/sbin/netreport
/usr/lib/udev/rules.d/*
/usr/lib/udev/rename_device
/usr/lib/udev/udev-kvm-check
/usr/sbin/service
/usr/sbin/ppp-watch
%{_mandir}/man*/*
%dir %attr(775,root,root) /var/run/netreport
%dir /etc/ppp
%dir /etc/ppp/peers
/etc/ppp/ip-up
/etc/ppp/ip-down
/etc/ppp/ip-up.ipv6to4
/etc/ppp/ip-down.ipv6to4
/etc/ppp/ipv6-up
/etc/ppp/ipv6-down
%dir /etc/NetworkManager
%dir /etc/NetworkManager/dispatcher.d
/etc/NetworkManager/dispatcher.d/00-netreport
%doc sysconfig.txt sysvinitfiles static-routes-ipv6 ipv6-tunnel.howto ipv6-6to4.howto changes.ipv6 COPYING
%doc examples
/var/lib/stateless
%ghost %attr(0600,root,utmp) /var/log/btmp
%ghost %attr(0664,root,utmp) /var/log/wtmp
%ghost %attr(0664,root,utmp) /var/run/utmp
%ghost %attr(0644,root,root) /etc/sysconfig/kvm
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/crypttab
%dir %{_tmpfilesdir}
%{_tmpfilesdir}/initscripts.conf
%dir /usr/libexec/initscripts
%dir /usr/libexec/initscripts/legacy-actions
%ghost %{_localstatedir}/log/dmesg
%ghost %{_localstatedir}/log/dmesg.old

%files -n debugmode
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/debug
/etc/profile.d/debug*

%changelog
* Mon Mar 13 2023 Tim Smith <tim.smith@citrix.com> - 9.49.41-2
- Prevent complaints about library paths in initscripts

* Thu Mar 02 2023 Tim Smith <tim.smith@citrix.com> - 9.49.41-1
- First imported release

