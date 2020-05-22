from cassandra import connection
from cassandra.cluster import Cluster
from cassandra.policies import TokenAwarePolicy, RoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider

cluster_list = [
  '192.168.41.20',
  '192.168.41.21',
  '192.168.41.22'
]
auth_provider = PlainTextAuthProvider(username='<USERNAME>', password='<PASSWORD>')

try:
  cluster = Cluster(
    cluster_list,
    load_balancing_policy=TokenAwarePolicy(RoundRobinPolicy()),
    auth_provider=auth_provider
  )
  session = cluster.connect()

  session.execute("CREATE KEYSPACE IF NOT EXISTS test WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")
  print("[OK]   Create Keyspace")

  session.execute("""
    CREATE TABLE IF NOT EXISTS test.items (
      id int,
      barcode text,
      date timeuuid,
      description text,
      price decimal,
      PRIMARY KEY (id)
    );
  """)
  print("[OK]   Create table items")

  session.execute("""
    INSERT INTO test.items (
      id, barcode, date, description, price
    ) VALUES (
      1, '979557876225495624879565698956', now(), 'Notebook Dell', 982.53
    );
  """)
  print("[OK]   Insert item")

  items = session.execute("""
    SELECT * FROM test.items
  """)
  print("[OK]   Select inserted item")

  print("==============================================================================")

  for item in items:
    print("{} - {} - {} - {} - ${}".format(item.id, item.barcode, item.date, item.description, item.price))
    print("==============================================================================")

  print("[OK]   Close connection")
  cluster.shutdown()
except Exception as error:
  print("[ERROR]   {}".format(error))