with import <nixpkgs> { };

let
  python = python312.withPackages (ps: [
    ps.requests
    ps.pandas
    ps.pygithub
    ps.python-gitlab
    ps.beautifulsoup4
    ps.lxml
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python
    pre-commit
  ];
}
