set terminal postscript enhanced eps color 22 lw 2 
set output "umean.eps"
f(x)=log(x)/0.41+6
g(x)=x
set key left
set xlabel "y^+"
set ylabel "<u^+>"
set pointsize 1.2
set logscale x 10
set xrange [0.1:110]
set yrange [0:20]
plot g(x)  with l lt 2 lc 0 title "u^+=y^+"\
,f(x) with l lt 2 lc 0 title "u^+=ln(y^+)/0.41+6"\
,"< head -n 201 plot/expt/CH12__PG.WL6" using 3:4 with p pt 1 lc 3 title "Iwamoto et.at."\
,"< cat graphs/*/Uf.xy " using ($1*110.0):2 with l lt 1 lc 1 title "OpenFOAM"
#    EOF
