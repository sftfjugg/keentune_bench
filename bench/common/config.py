import os
import logging

from configparser import ConfigParser

logger = logging.getLogger('common')

class Config:
    conf_file_path = "/etc/keentune/bench/bench.conf"
    conf = ConfigParser()
    conf.read(conf_file_path)
    logger.info("Load config from {}".format(conf_file_path))

    KEENTUNE_HOME       = conf['bench']['KEENTUNE_HOME']             #/etc/keentune/bench
    KEENTUNE_WORKSPACE  = conf['bench']['KEENTUNE_WORKSPACE']        #/var/keentune/bench
    BENCH_PORT          = conf['bench']['BENCH_PORT']
    FILES_PATH          = os.path.join(KEENTUNE_WORKSPACE, "files")  #/var/keentune/bench/files

    if not os.path.exists(FILES_PATH):
        os.makedirs(FILES_PATH)

    logger.info("keentune-bench install path: {}".format(KEENTUNE_HOME))
    logger.info("keentune-bench workspace: {}".format(KEENTUNE_WORKSPACE))
    logger.info("keentune-bench listenting port: {}".format(BENCH_PORT))