import os
import json
import subprocess
import multiprocessing
import logging

from collections import defaultdict
from tornado.web import RequestHandler

from bench.common.config import Config
from bench.common.system import httpResponse

logger = logging.getLogger('common')

BENCH_PROC = []

class BenchmarkProcess(multiprocessing.Process):
    def __init__(self,
        benchmark_cmd:str, 
        response_ip: str, 
        response_port: str,
        bench_id: int):
        super(BenchmarkProcess, self).__init__()

        self.response_ip = response_ip
        self.response_port = response_port
        self.bench_id = bench_id

        benchmark_cmd_list = benchmark_cmd.split()
        benchmark_cmd_list[1] = os.path.join(
            Config.FILES_PATH, benchmark_cmd_list[1])
        self.benchmark_cmd = " ".join(benchmark_cmd_list)

        self.proc = subprocess.Popen(
            args   = self.benchmark_cmd,
            shell  = True,
            stderr = subprocess.PIPE,
            stdout = subprocess.PIPE
        )
        logger.info("create benchmark process, cmd = {}, pid = {}".format(self.benchmark_cmd, self.proc.pid))

    def _parseBenchmarkResult(self, benchmark_result: str):
        benchmark_result_dict = {}
        
        for equation in benchmark_result.split(","):
            name  = equation.split("=")[0].strip()
            value = equation.split("=")[1].strip()
            benchmark_result_dict[name] = float(value)

        return benchmark_result_dict

    def runbenchmark(self):
        benchmark_result = defaultdict(list)

        try:
            logger.debug("waiting for benchmark runing")
            stdoutdata, stderrdata = self.proc.communicate()
            stdoutdata = stdoutdata.decode('UTF-8', 'strict').strip()
            stderrdata = stderrdata.decode('UTF-8', 'strict').strip()

            if stderrdata != "":
                logger.error("benchmark running stderr: stderr = {stderr}".format(stderr = stderrdata))
                return False, "benchmark running stderr: stderr = {stderr}".format(stderr = stderrdata)

            if stdoutdata == "":
                logger.error("benchmark result error: no output")
                return False, "benchmark result error: no output"

            try:
                benchmark_res = self._parseBenchmarkResult(stdoutdata)
                for k in benchmark_res.keys():
                    benchmark_result[k].append(benchmark_res[k])

            except Exception as e:
                logger.error("wrong benchmark output format of '{}': {}".format(stdoutdata, e))
                return False, "wrong benchmark output format of '{}': {}".format(stdoutdata, e)

        except Exception as e:
            logger.error("benchmark running error: {}".format(e))
            return False, "benchmark running error: {}".format(e)
        
        logger.info("benchmark running sucess: {}".format(benchmark_result))
        return True, dict(benchmark_result)

    def run(self):
        ''' process.start() '''

        suc, res = self.runbenchmark()
        response_data = {
            "suc": suc, 
            "msg": res,
            "bench_id": self.bench_id
        }

        logger.info("response benchmark running result to {response_ip}:{response_port} : {response_data}".format(
            response_port = self.response_port,
            response_ip = self.response_ip,
            response_data = response_data
        ))

        httpResponse(response_data, self.response_ip, self.response_port)
        
    def _terminate(self):
        ''' process.terminate() '''

        logger.info("benchmark process terminated, pid = {}".format(self.pid))
        self.proc.kill()
        self.terminate()


class BenchmarkHandler(RequestHandler):
    def post(self):
        request_data = json.loads(self.request.body)
        self.write(json.dumps({"suc" : True, "msg": "Benchmark is Runing"}))
        self.finish()
        
        proc = BenchmarkProcess(
            benchmark_cmd = request_data["benchmark_cmd"],
            response_ip = request_data['resp_ip'],
            response_port = request_data['resp_port'],
            bench_id = request_data['bench_id'],
        )
        BENCH_PROC.append(proc)
        proc.start()


class BenchmarkTerminateHandler(RequestHandler):
    def get(self):
        logger.info("Get terminate requests, ready to clean {} proc".format(BENCH_PROC.__len__()))
        while BENCH_PROC.__len__() > 0:
            proc = BENCH_PROC.pop()
            proc._terminate()
        
        self.write(json.dumps({"suc" : True, "msg": ""}))