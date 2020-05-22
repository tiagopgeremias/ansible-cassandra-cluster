# Provisioning a new cluster
  ansible-playbook -i inventory/vagrant/hosts play_cassandra_cluster.yml -e "user_admin=<USERNAME> pass_admin=<PASSWORD>"

# Add a only common node
  ansible-playbook -i inventory/vagrant/hosts play_cassandra_cluster.yml -e "add_node=yes"