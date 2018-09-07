import os
import json5


def get_config():
    configname = os.environ.get('TBDD_PDM_CONFIG', '/etc/tbdd_pdm/config.json')

    with open(configname) as f:
        return json5.load(f)
