set terminal postscript eps enhanced color 22 lw 2
set output "executionTime.eps"
set style data line
set key bottom
set xlabel "Time [s]"
set ylabel "CPU TIme [s]"
set y2label "CPU Time per time [-]"
set yrange [0:]
set y2range [0:]
set ytics nomirror
set y2tics nomirror
t0=`head -n 1 logs/executionTime_0 | cut -f 1`
cpu0=`head -n 1 logs/executionTime_0 | cut -f 2`
plot "logs/executionTime_0" using 1:2 title "CPU Time [s]"\
,"" using 1:(($2-cpu0)/($1-t0)) axes x1y2 title "CPU Time per time [-]"\


