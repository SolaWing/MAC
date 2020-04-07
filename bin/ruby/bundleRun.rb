#!/usr/bin/env ruby
# frozen_string_literal: true

if ARGV.empty?
  puts <<~HELP
    usage: #{$PROGRAM_NAME} bin_path [args_to_bin]
  HELP
  exit 0
end

$PROGRAM_NAME = ARGV.shift
Dir.chdir(File.expand_path('../', $PROGRAM_NAME)) do
  require 'bundler/setup'
  # help debuger
  begin
    require 'pry'
  rescue LoadError
  end
end
$DEVELOP = true
load $PROGRAM_NAME
