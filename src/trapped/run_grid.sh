mkdir -p ../LOG/GRID/
for j in 4 6 8 9
do
for id in {1..5}
do
timeout 30m python test_args.py gridworld $j $j 0.0 > ../LOG/GRID/log_${j}.${id}
done
done
