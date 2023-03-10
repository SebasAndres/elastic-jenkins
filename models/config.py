class Config:

    def __init__ (self, config_data:dict):

        self.elasticsearch_host = config_data["ELASTIC"]["host"]

        self.mod = config_data["PROGRAM"]["mod"]
        self.run = bool(config_data["PROGRAM"]["run"])
        self.logs = bool(config_data["PROGRAM"]["logs"])

        self.jenkins_user = config_data["JENKINS"]["user"]
        self.jenkins_psw = config_data["JENKINS"]["psw"]
        self.jenkins_url = config_data["JENKINS"]["url_conn"]
        self.jenkins_job = config_data["JENKINS"]["job"]
        self.jenkins_token = config_data["JENKINS"]["token"]

    def get_jenkins_job_url(self) -> str:
        return f"{self.jenkins_url}/job/{self.jenkins_job}/"