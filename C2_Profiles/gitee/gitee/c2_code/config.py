config = {}

def get_token():
	return config.get("gitee_token") or config.get("gitee_token")

def set_config(new_config: dict):
	config.update(new_config)