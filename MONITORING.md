**MONITORING via JMX**  
URL  
`https://www.datadoghq.com/blog/how-to-monitor-cassandra-performance-metrics/`
`https://github.com/influxdata/telegraf/tree/master/plugins/inputs/cassandra`

**CMD**  
docker pull openjdk  

# Or using wget (inst all wget via brew if you don't have it)  
curl -LO https://github.com/jiaqi/jmxterm/releases/download/v1.0.2/jmxterm-1.0.2-uber.jar  

docker run -it --rm --network container:cassandra1 -v $(pwd)/jmxterm:/jmx openjdk java -jar /jmx/jmxterm-1.0.2-uber.jar -l service:jmx:rmi:///jndi/rmi://localhost:7199/jmxrmi  

domains  
info -b org.apache.cassandra.metrics:name=TotalHints,type=Storage  
get -b  org.apache.cassandra.metrics:name=TotalHints,type=Storage -a Count  
