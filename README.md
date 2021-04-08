# Elasticsearch
Elasticsearch
## Install and configure 1 node elasticsearch cluster version 7.8.0
```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list

apt-get update && apt-get install elasticsearch=7.8.0
```
---

## Data should be persisted on disk
```
The staging Enviornment makes the data persisted on disk
```
---

## Add 2 more nodes to the cluster without restarting elasticsearch service on first one
```latex
+ Go to yaml configuration file present in /etc/elasticsearch/elasticsearch.yaml
+ Uncomment the following:
    +cluster.name
    +node.name
    +path.data
    +path.logs
    +network.host
    +http.port
    +discovery.seed_hosts
    +cluster.initial_master_nodes
 + Put your desired cluster name in cluster.name Ex: cluster.name: my-application in all the three nodes.
 + Give desired node name for all the 3 nodes of elasticsearch cluster.
 + Leave the configuration for path.data and path.logs as it is!
 + Set the network.host to 0.0.0.0 so that it can relay into any Ips
 + Set the http.port to 9200
 + Give the ips of all the other three nodes in discovery.seed_hosts Ex:    discovery.seed_hosts["10.57.14.9","10.57.14.10","10.57.14.11"]
 + Set the master node in cluster.initial_master_nodes.
```
```bash
After setting up for all node without stopping elastic search start the elastic search service in 2nd and 3rd node.
    
*root@stg-elasticsearchrohit001: systemctl elasticsearch start

+The nodes will get connected automatically with the cluster
+To check the number of cluster in the eleasticsearch:
    
*root@stg-elasticsearchrohit001: curl -XGET "localhost:9200/?pretty"
```
```bash
root@stg-elasticsearchrohit001:/home/rohitj.intern# curl -X GET "localhost:9200/?pretty"
{
  "name" : "node-1",
  "cluster_name" : "my-application",
  "cluster_uuid" : "Wr2EeGtdTFOuf7Obn-8kZg",
  "version" : {
    "number" : "7.12.0",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "78722783c38caa25a70982b5b042074cde5d3b3a",
    "build_date" : "2021-03-18T06:17:15.410153305Z",
    "build_snapshot" : false,
    "lucene_version" : "8.8.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

```
---
## Create 3 indices (books details, author details, publishing company details) on the cluster, set the number of shards to be 3 for each index

```shell
*The commands to create a index and add first document to the index.
curl -XPOST "localhost:9200/books_details/_doc?pretty" -H 'Content-Type: application/json' -d'
{
  "Author": "John Green",
  "Book Name": "The Fault in our stars",
  "Genere": "Romance",
  "Language": "English"
}

*Similary do for the other indices

*Create any random JSON file according to index required from [https://www.mockaroo.com/]
```
---
## Upgrade elasticsearch to version 7.12 without losing the data
```
Stop all the nodes and run the command root@focal:~sudo apt-get upgrade elasticsearch to the latest version available.
```
---
## Capture slow logs for all the indices for queries taking longer than 1ms to respond
```shell
Run the command to capture logs more than 1ms

curl -XPUT 'localhost:9200/books_details/_settings' -H 'Content-Type: application/json' -d '{
"index.search.slowlog.threshold.query.warn": "0ms",
"index.search.slowlog.threshold.query.info": "0ms",
"index.search.slowlog.threshold.query.debug": "0ms",
"index.search.slowlog.threshold.query.trace": "0ms",
"index.search.slowlog.threshold.fetch.warn": "0ms",
"index.search.slowlog.threshold.fetch.info": "0ms",
"index.search.slowlog.threshold.fetch.debug": "0ms",
"index.search.slowlog.threshold.fetch.trace": "0ms"
}'


After running this command run any elastic search query to check log file taking more than 1ms

'curl -X GET "localhost:9200/books_details/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "sort": [
    { "Book Name": "asc" }
  ]
}'

*Use command cat /var/log/log  grep'time = 1.1ms' | tail -1 to grab the query which took more than 1ms.
```
