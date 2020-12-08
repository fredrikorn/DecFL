while true; 
do 
    docker stats --format "table {{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}" --no-stream >> stats.csv
    gdate +"%T.%3N" >> stats.csv
done