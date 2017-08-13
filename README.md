# elasticsearch
# ES Install
# step-1:
wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.4.1/elasticsearch-2.4.1.deb
#step-2:
  sudo dpkg -i elasticsearch-2.4.1.deb
  sudo chmod -R 0755 /etc/elasticsearch/
    sudo nano /etc/elasticsearch/elasticsearch.yml
    # add below lines at end of the above file
  script.engine.groovy.inline.update: on
  script.inline: on
  script.indexed: on

#step-3:
  sudo service elasticsearch restart
curl -X GET 'http://127.0.0.1:9200'

Generate Random user event documents by date  
Generate user event documents by size in each file

