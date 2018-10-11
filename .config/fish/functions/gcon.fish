# Defined in /var/folders/f1/8p757b912ks3nrxmk5n9b0cr0000gn/T//fish.opQXH0/gcon.fish @ line 2
function gcon -d "git checkout {branch}; and pull newest source"
	set branch $argv[1]
        git push . "$branch@{u}:$branch"
        git checkout "$branch"
end
