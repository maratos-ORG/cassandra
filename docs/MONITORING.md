# 📈 MONITORING via JMX

## 🔗 Useful Links

- [How to monitor Cassandra performance metrics (Datadog blog)](https://www.datadoghq.com/blog/how-to-monitor-cassandra-performance-metrics/)
- [Telegraf Cassandra input plugin (GitHub)](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/cassandra)

---

## 🛠️ Commands
### Pull JDK image (needed for JMX tools)
```bash  
docker pull openjdk  

#Download jmxterm
curl -LO https://github.com/jiaqi/jmxterm/releases/download/v1.0.2/jmxterm-1.0.2-uber.jar

#Run jmxterm inside Docker  
docker run -it --rm \
  --network container:cassandra1 \
  -v $(pwd)/jmxterm:/jmx \
  openjdk \
  java -jar /jmx/jmxterm-1.0.2-uber.jar \
  -l service:jmx:rmi:///jndi/rmi://localhost:7199/jmxrmi
```



docker run -it --rm --network container:cassandra1 -v $(pwd)/jmxterm:/jmx openjdk java -jar /jmx/jmxterm-1.0.2-uber.jar -l service:jmx:rmi:///jndi/rmi://localhost:7199/jmxrmi  

## 🔍 Sample JMX Commands
```bash
#List available domains
domains

#Show info for TotalHints
info -b org.apache.cassandra.metrics:name=TotalHints,type=Storage

#Get hint count
get -b org.apache.cassandra.metrics:name=TotalHints,type=Storage -a Count

