while true; 
do 
    docker stats --format "table {{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}," --no-stream | awk -v date="$(date +%T)" '{print $0, date}' >> performance/stats.csv
done