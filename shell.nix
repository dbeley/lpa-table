with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  buildInputs = [
    pkgs.python311
    python311Packages.pip

    python311Packages.requests
    python311Packages.pandas
    python311Packages.pygithub
    python311Packages.python-gitlab
    python311Packages.beautifulsoup4
    python311Packages.lxml

    pre-commit
  ];

}
