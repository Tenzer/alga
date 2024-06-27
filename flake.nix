{
  inputs = {
    pyproject-nix.url = "github:nix-community/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      nixpkgs,
      pyproject-nix,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        inherit (nixpkgs) lib;
        project = pyproject-nix.lib.project.loadPoetryPyproject { projectRoot = ./.; };

        overlay = _: prev: {
          python3 = prev.python3.override {
            packageOverrides = _: p: {
              cfgs = p.buildPythonPackage rec {
                version = "0.13.0";
                pname = "cfgs";
                format = "pyproject";
                nativeBuildInputs = with p.pythonPackages; [ poetry-core ];
                src = p.fetchPypi {
                  inherit version pname;
                  hash = "sha256-zvR+Z/BRJ4Pug+JMwvOeWyO11MoMMrvXIb1k9IY2Zn4=";
                };
              };
            };
          };
        };

        pkgs = import nixpkgs {
          inherit system;
          overlays = [ overlay ];
        };
        python = pkgs.python3;
      in
      {
        devShells.default =
          let
            arg = project.renderers.withPackages { inherit python; };
            pythonEnv = python.withPackages arg;
          in
          pkgs.mkShell { packages = [ pythonEnv ]; };

        packages.default =
          let
            attrs = project.renderers.buildPythonPackage { inherit python; };
          in
          python.pkgs.buildPythonPackage attrs;
      }
    );
}
