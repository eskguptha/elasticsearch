
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# ES Instalation
	step-1:
		wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.4.1/elasticsearch-2.4.1.deb
	step-2:
		sudo dpkg -i elasticsearch-2.4.1.deb
		sudo chmod -R 0755 /etc/elasticsearch/
	    sudo nano /etc/elasticsearch/elasticsearch.yml
	    # add below lines at end of the above file
		script.engine.groovy.inline.update: on
		script.inline: on
		script.indexed: on
 
	step-3:
	    sudo service elasticsearch start
		curl -X GET 'http://127.0.0.1:9200'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# log generation
#activate virtualenv and install below pkg
pip install elasticsearch==2.4.1
cd es_demo
python log_genrator.py
python es_insert.py

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ES Commands

# es start
sudo service elasticsearch start

# es restart
sudo service elasticsearch restart

#es stop
sudo service elasticsearch stop

#cluster health
curl 'http://127.0.0.1:9200/_cluster/health'

# Get ES STATUS
curl -X GET 'http://127.0.0.1:9200'

# Find all Indices
curl 'http://127.0.0.1:9200/_cat/indices?v'

# Get document by id
curl -XGET 'http://127.0.0.1:9200/<index_name>/<doc_type>/<uid>'

# Mapping
curl -XGET 'http://127.0.0.1:9200/<index_name>/_mapping/

# Remove index
curl -XDELETE 'http://127.0.0.1:9200/<index_name>'

#Match All
curl -XGET 'http://127.0.0.1:9200/<index_name>/_search?pretty' -d '
{
  "query":{  "match_all": {}  }
}'

# Chrome plugin Install
Sense (Beta) elasticsearch
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
