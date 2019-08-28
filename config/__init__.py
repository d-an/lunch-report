from yaml import safe_load

with open('config/config.yml') as f:
    cfg = safe_load(f)
