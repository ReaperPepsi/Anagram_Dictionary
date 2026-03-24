import yaml

with open("/Users/reaper_pepsi/Anagram_Dictionary/app/config/database_config_file.yaml", 'r') as config_file:
    config = yaml.full_load(config_file)

connection_string = {
    "username": config['database']['username'],
    "password": config['database']['password'],
    "server": config['database']['server'],
    "database_instance": config['database']['database']
}

# create DATABASE URL
DATABASE_URL = f"postgresql+psycopg://{connection_string['username']}:{connection_string['password']}@{connection_string['server']}/{connection_string['database_instance']}"


