set terminal postscript enhanced color eps 22 lw 2
set output "uv.eps"
set xlabel "y^+"
set ylabel "-<u^+'v^+'>"
set pointsize 1.2
set xrange [0:110]
plot  \
1-x/110 title "" with l lc 0\
,"< head -n 269 plot/expt/CH12__PG.WL6 | tail -n 65" using 3:4 with p pt 1 lc 3 title "Iwamoto et.at."\
,"< cat graphs/*/uv.xy " using ($1*110.0):(-$2) with l lt 1 lc 1 title "OpenFOAM"
#    EOF
