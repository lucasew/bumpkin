{
  description = "Tool to do source bumps";
  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
  outputs = { self, nixpkgs, flake-parts }@inputs:
  flake-parts.lib.mkFlake { inherit inputs; } {
    systems = [ "x86_64-linux" "i686-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
    perSystem = { config, pkgs, ... }: {
      packages.default = pkgs.python3Packages.callPackage ./package.nix {};
    };
  };
}
