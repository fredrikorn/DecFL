while true; 
do 
docker stats --format "table {{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}" --no-stream >> stats.csv
sleep 0.5;
done
