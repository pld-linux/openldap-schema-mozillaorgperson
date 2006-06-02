Summary:	Mozilla LDAP schema
Summary(pl):	Schemat LDAP dla Mozilli
Name:		openldap-schema-mozillaorgperson
Version:	0.6.3
Release:	0.2
Epoch:		0
License:	?
Group:		Networking/Daemons
Source0:	mozillaOrgPerson.schema
URL:		https://bugzilla.mozilla.org/show_bug.cgi?id=116692
BuildRequires:	rpmbuild(macros) >= 1.304
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

%description
This package contains LDAPv3 schema for use with the Mozilla Address
Book.

%description -l pl
Ten pakiet zawiera schemat LDAPv3 do u¿ywania z ksi±¿k± adresow±
Mozilli.

%prep
%setup -q -c -T
cp %{SOURCE0} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{schemadir}

install *.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%openldap_schema_register %{schemadir}/mozillaOrgPerson.schema -d cosine,inetorgperson,core
%service -q ldap restart

%postun
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/mozillaOrgPerson.schema
	%service -q ldap restart
fi

%files
%defattr(644,root,root,755)
%{schemadir}/*.schema
