# Defined in /var/folders/f1/8p757b912ks3nrxmk5n9b0cr0000gn/T//fish.PzqGs9/tt.fish @ line 1
function tt
	mkdir -p (dirname $argv[1]) && echo $argv[1] > $argv[1]
end
