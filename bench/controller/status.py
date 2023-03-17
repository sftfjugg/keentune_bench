import json
import logging

from tornado.web import RequestHandler
from bench.common.system import checkAddressAvaliable

logger = logging.getLogger('common')


class StatusHandler(RequestHandler):
    def get(self):
        logger.info("Get status check reuqests")
        back_json = {"status": "alive"}
        self.write(json.dumps(back_json))
        self.finish()


class AvaliableAddressHandler(RequestHandler):
    def post(self):
        request_data = json.loads(self.request.body)
        agent_address = request_data['agent_address']
        logger.info("Get address check reuqests, agent_address = {}".format(agent_address))

        if not isinstance(agent_address, list):
            agent_address = [agent_address]
        result = checkAddressAvaliable(agent_address)

        logger.info("response address check result: {}".format(result))
        self.write(json.dumps(result))
        self.finish()