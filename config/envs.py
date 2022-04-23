from environs import Env

env = Env()
env.read_env()


TELEGRAM_BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN")
LOCALIZATION: str = env.str("LOCALIZATION")

DB_HOST: str = env.str("DB_HOST")
DB_PORT: str = env.str("DB_PORT")
DB_DATABASE: str = env.str("DB_DATABASE")
DB_USERNAME: str = env.str("DB_USERNAME")
DB_PASSWORD: str = env.str("DB_PASSWORD")
