{ bumpkin, fetchurl, callPackage }:
{ inputFile, outputFile }:
let
  inputData = builtins.fromJSON (builtins.readFile inputFile);
  outputData = builtins.fromJSON (builtins.readFile outputFile);
  handlers = builtins.mapAttrs (k: v: if v == "directory" then callPackage (./. + "/${k}") {} else null) (builtins.readDir ./.);

  evalNode = { declared, fetched }: handlers.${declared._type} {inherit declared fetched;}; # TODO: implement
  recurseIntoNodes = { declared, fetched }:
  if (builtins.typeOf declared == "set") then
    if (builtins.hasAttr "_type" declared) then
      evalNode { inherit declared fetched; }
    else builtins.mapAttrs (k: v: recurseIntoNodes { 
      declared = declared.${k};
      fetched = fetched.${k};
    }) declared
  else declared;
in recurseIntoNodes {
  declared = inputData;
  fetched = outputData;
}
