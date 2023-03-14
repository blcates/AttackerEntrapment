mkdir -p ../LOG/ROCK/
for j in 4 6 8 9
do
for id in {1..5}
do
timeout 30m python test_args.py rocksample $j $j > ../LOG/ROCK/log_${j}.${id}
done
done
