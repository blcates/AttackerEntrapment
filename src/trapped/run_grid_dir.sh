mkdir -p ../LOG/GRID_DIR/
for sl in gridworld gridworld2 gridworld3 gridworld4
do
for j in 7 #4 6 8 9
do
for id in {1..5}
do
timeout 30m python test_args_dirs.py ${sl} $j $j 0.0 > ../LOG/GRID_DIR/log_${j}_${sl}.${id}
done
done
done
