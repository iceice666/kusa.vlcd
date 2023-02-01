
import yaml


with open('./config/settings.yml', encoding='utf-8') as f:
    config = type('config', (object,), yaml.safe_load(f))
