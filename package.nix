{ buildPythonPackage, pytest, callPackage, hatchling }:
let
  bumpkin = buildPythonPackage {
    pname = "bumpkin";
    version = builtins.readFile ./bumpkin/VERSION;
    format = "pyproject";

    src = ./.;

    buildInputs = [ hatchling ];

    checkInputs = [ pytest ];

    passthru = {
      loadBumpkin = callPackage ./bumpkin/sources { inherit bumpkin; };
    };
  };
in bumpkin
