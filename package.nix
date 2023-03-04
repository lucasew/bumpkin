{ buildPythonPackage, pytest, callPackage }:
let
  bumpkin = buildPythonPackage {
    pname = "bumpkin";
    version = builtins.readFile ./bumpkin/VERSION;

    src = ./.;

    checkInputs = [ pytest ];

    passthru = {
      loadBumpkin = callPackage ./bumpkin/sources { inherit bumpkin; };
    };
  };
in bumpkin
