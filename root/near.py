import json
import os

import root


class Near:
    def __init__(self):
        self.near_env = root.context.near_env
        self.account_id = root.context.near_account_id
        self.setup_env()
        self.__logger = None

    @property
    def logger(self) -> 'root.log_lib.Logger':
        if self.__logger is None:
            self.__logger = root.log_lib.get_logger(self.__class__.__name__)
        return self.__logger

    def setup_env(self):
        os.environ['NEAR_ENV'] = self.near_env

    def transfer_funds(self, playback_id: int):
        try:
            data = json.dumps({'playback_id': playback_id})
            command = f"near call {self.account_id} transfer_funds '{data}' --accountId  {self.account_id}"
            self.logger.info(f'Executing: "{command}"')
            stream = os.popen(command)
            output = stream.read()
            self.logger.info(f'Funds transferred. Output:\n{output}')
        except Exception as e:
            self.logger.exception(
                f'Error while transferring funds: {e}\n',
                exc_info=True
            )
