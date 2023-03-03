{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    entr
    gnumake
    python3
    python3Packages.pylsp-mypy
  ];
  shellHook = ''
    if [ ! -d .venv ]; then
      make virtualenv
    fi
    . .venv/bin/activate
  '';
}
