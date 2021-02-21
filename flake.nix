{
  description = "";
  inputs = {
    nixpkgs-git.url = https://github.com/NixOS/nixpkgs/archive/58c19a2b0bbf75e68b1946460737c3f8a74b0f33.tar.gz;
  };
  outputs = { nixpkgs-git, ... }@inputs : {
   defaultPackage.x86_64-linux =
     let system = "x86_64-linux"; in
     let nixpkgs = import nixpkgs-git { config = { allowUnfree = true;}; system = system; }; in

     let mypackages = with nixpkgs; [ coreutils python3 sqlite gawk git file bash bashInteractive ]; in

     with import nixpkgs-git { system = "x86_64-linux"; };
     symlinkJoin {
       name = "mypackages";
       paths = lib.lists.unique mypackages;
       postBuild = ''echo "links created"'';
     };
  };
}
