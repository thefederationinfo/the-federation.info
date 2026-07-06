{
  description = "the-federation.info dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # frontend
            nodejs_26
            pnpm

            # backend
            python3
            libpq # runtime lib for psycopg2
            libpq.pg_config # pg_config for psycopg2 source build
            gcc

            # tooling
            git
            ruff
          ];

          shellHook = ''
            if [ ! -d venv ]; then
              python3 -m venv venv
            fi
            . venv/bin/activate
            echo "devenv ready: node $(node -v), pnpm $(pnpm -v), $(python3 --version)"
            echo "python deps: pip install -r dev-requirements.txt"
            echo "frontend deps: pnpm install"
          '';
        };
      });
    };
}
