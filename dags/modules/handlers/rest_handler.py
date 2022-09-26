import requests
from airflow import AirflowException

class RestHandler:

    from enum import Enum

    class State(Enum):
        SUCCEEDED = 0
        ERROR = 1
        INITIALIZED = 2
        CONNECTED = 3
        FAILED = 4

    def __init__(self, api_addr, task_instance, config=None, params=None, logger=None, timeout=60):
        """
        @params timeout if after timeout seconds the task has not finished, it will be marked as FAILED.
            Set to 0 to disable timeout, this might hang your workflow, default is 60 seconds.
        """
        if params is None:
            params = {}

        # Configurable API Specification
        self.api_addr = api_addr
        self.api_endpoints = {"status": "/status",
                              "request": "/model/request",
                              "init": "/model/initialize/{}",
                              "run": "/model/run/{}",
                              "progress": "/model/status/{}",
                              "results": "/model/results/{}",
                              "remove": "/model/remove/{}"}

        # API Payload
        self.config = config

        # Handler Params
        self.interval = 2
        self.timeout = timeout

        # Airflow Params
        self.task_instance = task_instance
        self.params = params
        self.logger = logger

        # Identifiers - This should become a local hash map
        self.model_id_list = []

        # Log Initialization
        self.__set_handler_status(self.State.INITIALIZED)
        logger.info('Handler Status Change: ' + str(self.get_handler_status()))

    # Get current status from adapter
    # FIXME: returns this method a Response or a json (Line 58), or...?
    # standardize the adapter_status in a specified response?
    def get_adapter_status(self) -> requests.Response:
        try:
            response = requests.get(self.api_addr + self.api_endpoints['status'])
        except requests.exceptions.RequestException as exception:
            self.__set_handler_status(self.State.FAILED)
            raise AirflowException(exception)

        if response.headers.get('content-type') == 'application/json':
            response = response.json()
        self.logger.info("Endpoint /status responded: " + str(response))

        self.__set_handler_status(self.State.CONNECTED)
        self.logger.info('Handler Status Change: ' + str(self.get_handler_status()))

        return response

    # Request a New Model Instance from Adapter
    def request_model_instance(self) -> requests.Response:
        try:
            response = requests.get(self.api_addr + self.api_endpoints['request'])
        except requests.exceptions.RequestException as exception:
            self.__set_handler_status(self.State.FAILED)
            raise AirflowException(exception)

        if response.headers.get('content-type') == 'application/json':
            response = response.json()
            self.model_id_list.append(response['model_run_id'])
        self.logger.info("Endpoint /model/request responded: " + str(response))

        return response

    # Post a Model Initialization Config
    def init_model_instance(self, model_run_id) -> requests.Response:
        try:
            response = requests.post((self.api_addr + self.api_endpoints['init']).format(model_run_id),
                                     json=self.config)
        except requests.exceptions.RequestException as exception:
            self.__set_handler_status(self.State.FAILED)
            raise AirflowException(exception)

        if response.headers.get('content-type') == 'application/json':
            response = response.json()
            # update model status
        self.logger.info("Endpoint /model/initialize/ responded: " + str(response))

        return response

    # Execute a Model Instance
    def run_model_instance(self, model_run_id) -> requests.Response:
        try:
            response = requests.get((self.api_addr + self.api_endpoints['run']).format(model_run_id))
        except requests.exceptions.RequestException as exception:
            self.__set_handler_status(self.State.FAILED)
            raise AirflowException(exception)

        if response.headers.get('content-type') == 'application/json':
            response = response.json()
            # update model status ?
        self.logger.info("Endpoint /model/run/ responded: " + str(response))

        return response

    # Get Model Run Status
    def get_model_status(self, model_run_id) -> requests.Response:
        try:
            response = requests.get((self.api_addr + self.api_endpoints['status']).format(model_run_id))
        except requests.exceptions.RequestException as exception:
            self.__set_handler_status(self.State.FAILED)
            raise AirflowException(exception)

        if response.headers.get('content-type') == 'application/json':
            response = response.json()
        self.logger.info("Endpoint /model/status/ responded: " + str(response))

        return response

    # Get Model Run Results
    def get_model_results(self, model_run_id) -> requests.Response:
        try:
            response = requests.get((self.api_addr + self.api_endpoints['results']).format(model_run_id))
        except requests.exceptions.RequestException as exception:
            self.__set_handler_status(self.State.FAILED)
            raise AirflowException(exception)

        if response.headers.get('content-type') == 'application/json':
            response = response.json()
        #self.__set_handler_status(self.State.FAILED)
        self.logger.info("Endpoint /model/results/ responded: " + str(response))

        return response

    # Remove Model Run
    def remove_model_instance(self, model_run_id) -> requests.Response:
        try:
            response = requests.get((self.api_addr + self.api_endpoints['remove']).format(model_run_id))
        except requests.exceptions.RequestException as exception:
            self.__set_handler_status(self.State.FAILED)
            raise AirflowException(exception)

        if response.headers.get('content-type') == 'application/json':
            response = response.json()
        self.logger.info("Endpoint /model/remove/ responded: " + str(response))

        return response

    # Get current handler status
    def get_handler_status(self) -> State:
        return self.status

    # Set model handler status
    def __set_handler_status(self, status: State) -> None:
        self.status = status
