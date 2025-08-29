#!/bin/bash
f4pga -vv build --flow vga-tester-basys3.json
mkdir -p build/log
mv *.log build/log/
cp build/basys3/fpga_top.bit vga_tester.bit
