Summary:	DNSSEC and DLV configuration and priming tool
Name:		dnssec-conf
Version:	1.22
Release:	%mkrel 2
License:	GPLv2+
URL:		http://www.xelerance.com/software/dnssec-conf/
Source0:	http://www.xelerance.com/software/%{name}/%{name}-%{version}.tar.gz
Patch0:		dnssec-conf-1.20-borked_xml.diff
Group:		System/Servers
BuildArch:	noarch
Buildrequires:	xmlto
Requires:	python-dns
Requires:	curl
#Requires: a caching nameserver
#Requires bind 9.4.0 if bind is reconfigured.....

%description
DNSSEC configuration and priming tool. Keys are required until the root
is signed, as well as for local unpublished DNSSEC keys to be preloaded
into the recursive nameserver. These DNSSEC configuration files can be
directly included in the bind or unbound nameserver configuration files.
dnssec-conf includes a commandline configuration client for Bind and
Unbound, known DNSSEC keys, URL's to official publication pages of keys,
and harvested keys, as well a script to harvest DNSKEY's from DNS.
See also: system-config-dnssec

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

%build
make

%install
%makeinstall_std \
    PREFIX=%{_prefix} \
    ETCDIR=%{buildroot}%{_sysconfdir} \
    BINDIR=%{buildroot}%{_bindir}\
    SBINDIR=%{buildroot}%{_sbindir} \
    MANDIR=%{buildroot}%{_mandir}

#KEYSDIR=$(ETCDIR)/pki/dnssec-keys

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m0644 packaging/fedora/dnssec.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/dnssec

# until upstream fixes standard DLV setting in 1.21
sed -i 's|#DLV="dlv.isc.org"|DLV="dlv.isc.org"|' %{buildroot}%{_sysconfdir}/sysconfig/dnssec
sed -i 's|DLV="off"|#DLV="off"|' %{buildroot}%{_sysconfdir}/sysconfig/dnssec

%files 
%doc LICENSE README INSTALL
%attr(0755,root,root) %dir %{_sysconfdir}/pki/dnssec-keys
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pki/dnssec-keys/*/*
%attr(0755,root,root) %dir %{_sysconfdir}/pki/dnssec-keys/production
%attr(0755,root,root) %dir %{_sysconfdir}/pki/dnssec-keys/testing
%attr(0755,root,root) %dir %{_sysconfdir}/pki/dnssec-keys/harvest
%attr(0755,root,root) %dir %{_sysconfdir}/pki/dnssec-keys/dlv
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/dnssec
%{_bindir}/dnskey-pull
%{_sbindir}/dnssec-configure
%{_mandir}/*/*
