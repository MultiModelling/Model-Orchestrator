from minio import Minio


class MinIOInterface:

    def __init__(self, api_addr, config=None, logger=None):

        # Configurable API Specification
        self.api_addr = api_addr
        self.config = config

        # Airflow Params
        self.logger = logger

    def init(self):
        self.upload_esdl()

    def upload_esdl(self):
        client = Minio(
            endpoint=self.api_addr,
            secure=self.config['secure'],
            access_key=self.config['access_key'],
            secret_key=self.config['secret_key'],
        )

        # Initialize ESDL Data into MinIO
        input_data = "./data/Hybrid HeatPump.esdl"
        destination_path = "bedrijventerreinommoord/Trial_20220708_1/Scenario_1_II3050_Nationale_Sturing/Experiment_1/MM_workflow_run_1/ESDL_add_price_profile_adapter/Hybrid HeatPump.esdl"

        bucket = destination_path.split("/")[0]
        rest_of_path = "/".join(destination_path.split("/")[1:])

        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)

        client.fput_object(
            bucket, rest_of_path, input_data,
        )