mkdir -p ../LOG/PUDDLE/
for j in 0.4 0.5 0.6 0.7 0.2 0.3 #4 #6 8 9
do
for id in {1..5}
do

timeout 30m python test_args.py puddle 1 1 $j > ../LOG/PUDDLE/log_${j}.${id}
done
done
