{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems =
        function:
        nixpkgs.lib.genAttrs systems (
          system:
          function (
            import nixpkgs {
              inherit system;
              config.allowUnfree = true;
            }
          )
        );
    in
    {
      devShells = forAllSystems (
        pkgs:
        let
          python = pkgs.python39;
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              python

              pyright
              ruff
              isort
              black
            ];

            env = {
              VENV_DIR = "./.venv";
            };

            shellHook = ''
              if [ ! -d $VENV_DIR ]; then
                ${python}/bin/python -m venv $VENV_DIR
              fi

              source ./.venv/bin/activate
            '';
          };
        }
      );
    };
}
