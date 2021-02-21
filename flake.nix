{
  description = "";
  inputs = {
    nixpkgs-git.url = https://github.com/NixOS/nixpkgs/archive/60330b60655b3fa3a18624bdd7069855bb37af99.tar.gz; # was: 62ef779f2a5050549772722665bedf52f01268d2
  };
  outputs = { nixpkgs-git, ... }@inputs : {
   defaultPackage.x86_64-linux =
     let system = "x86_64-linux"; in
     let nixpkgs = import nixpkgs-git { config = { allowUnfree = true;}; system = system; }; in

     let mypackages = with nixpkgs; [ coreutils python3 sqlite gawk git bash bashInteractive ]; in

     with import nixpkgs-git { system = "x86_64-linux"; };
     symlinkJoin {
       name = "mypackages";
       paths = lib.lists.unique mypackages;
       postBuild = ''echo "links created"'';
     };
  };
}
