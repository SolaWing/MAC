function op
    set -l path /Users/wang/Desktop/Bytedance/Repositories/tools/lark_pipeline_worksapce/targets/optimus_$argv[1]/bin/optimus_$argv[1]
    if test -e $path
        ~/bin/ruby/bundleRun.rb $path $argv[2..-1]
    else
        echo optimus_$argv[1] not exist!
        set -l n (basename (status -f) .fish)
        echo "usage: $n (ios|android|desktop|rust) command..."
    end
end
