#!/usr/bin/env ruby

if ARGV.empty?
  puts <<~HELP
    usage: #{$0} bin_path [args_to_bin]
  HELP
  exit 0
end
$0 = ARGV.shift
Dir.chdir(File.expand_path('../', $0)) do
  require "bundler/setup"
end
load $0
