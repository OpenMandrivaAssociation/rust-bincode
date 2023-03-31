%bcond_without check
%global debug_package %{nil}

%global crate bincode

Name:           rust-%{crate}
Version:        1.3.3
Release:        2
Summary:        Binary serialization / deserialization strategy that uses Serde

# Upstream license specification: MIT
License:        MIT
URL:            https://crates.io/crates/bincode
Source:         %{crates_source}
# Drop dependency on rust-serde-bytes (which in turn requires
# rust-bincode) to avoid circular dependencies.
# Fortunately rust-serde-bytes is used only in tests, so removing
# it is non-fatal.
Patch0:		bincode-1.3.2-drop-circular-dependency.patch

ExclusiveArch:  %{rust_arches}
%if %{__cargo_skip_build}
BuildArch:      noarch
%endif

BuildRequires:  rust-packaging

%global _description %{expand:
Binary serialization / deserialization strategy that uses Serde for
transforming structs into bytes and vice versa!.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages
which use "%{crate}" crate.

%files          devel
%license LICENSE.md
%doc readme.md
%{cargo_registry}/%{crate}-%{version}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages
which use "default" feature of "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{cargo_registry}/%{crate}-%{version}/Cargo.toml

%package     -n %{name}+i128-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+i128-devel %{_description}

This package contains library source intended for building other packages
which use "i128" feature of "%{crate}" crate.

%files       -n %{name}+i128-devel
%ghost %{cargo_registry}/%{crate}-%{version}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif
