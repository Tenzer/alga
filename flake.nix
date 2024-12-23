{
  description = "CLI for remote controlling LG webOS TVs";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      poetry2nix,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        alga =
          { poetry2nix, lib }:
          poetry2nix.mkPoetryApplication {
            projectDir = self;
            preferWheels = true;
          };
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            poetry2nix.overlays.default
            (final: _: {
              alga = final.callPackage alga { };
            })
          ];
        };
      in
      {
        packages.default = pkgs.alga;
        legacyPackages = pkgs;
      }
    );
}
