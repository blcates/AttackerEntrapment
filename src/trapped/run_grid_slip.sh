mkdir -p ../LOG/GRID_SLIP/
for sl in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
do
for j in 7 #4 6 8 9
do
for id in {1..5}
do
timeout 30m python test_args.py gridworld $j $j ${sl} > ../LOG/GRID_SLIP/log_${j}_${sl}.${id}
done
done
done
