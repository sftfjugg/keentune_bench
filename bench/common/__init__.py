from logging import config as logconf

logconf_file_path = "/etc/keentune/bench/logging.conf"
logconf.fileConfig(logconf_file_path)