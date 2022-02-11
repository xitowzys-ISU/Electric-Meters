from environs import Env

env = Env()
env.read_env()


TELEGRAM_BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN")
