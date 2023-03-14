mkdir -p ../LOG/FOUR/
for j in 4 6 8 9
do
for id in {1..5}
do
timeout 30m python test_args.py fourroom $j $j > ../LOG/FOUR/log_${j}.${id}
done
done
