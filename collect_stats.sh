while true; 
do 
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" --no-stream >> stats.csv
sleep 1; 
done
