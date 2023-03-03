{ buildPythonPackage, pytest }:
buildPythonPackage {
  pname = "bumpkin";
  version = builtins.readFile ./bumpkin/VERSION;

  src = ./.;

  checkInputs = [ pytest ];
}
