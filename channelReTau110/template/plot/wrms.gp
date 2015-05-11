set terminal postscript enhanced color eps 22 lw 2
set output "wrms.eps"
set xlabel "y^+"
set ylabel "w^+_{rms}"
set pointsize 1.2
set logscale x 10
set xrange [0.1:110]
set yrange [0:1.4]
set key left
plot  \
"< head -n 339 plot/expt/CH12__PG.WL6 | tail -n 65" using 3:6 with p pt 1 lc 3 title "Iwamoto et.at."\
,"< cat graphs/*/w.xy " using ($1*110.0):2 with l lt 1 lc 1 title "OpenFOAM"
#    EOF
