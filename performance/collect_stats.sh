while true; 
do 
    docker stats --format "table {{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}," --no-stream | awk -v date="$(gdate +%T.%3N)" '{print $0, date}' >> stats.csv
done