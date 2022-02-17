import signal
import time
from datetime import datetime, timedelta
from threading import Thread

import requests

import root


class PlaybackDispatcher:
    ms: 'root.MS'

    def __init__(self):
        self.alive = False
        self.__loop_thread = Thread(
            target=self.component_loop,
            name='PlaybackDispatcherLoop'
        )
        self.__logger = None
        self.near = root.Near()
        self.iter_time = 15

    @property
    def logger(self) -> 'root.log_lib.Logger':
        if self.__logger is None:
            self.__logger = root.log_lib.get_logger(self.__class__.__name__)
        return self.__logger

    def start(self):
        self.alive = True
        self.add_signals()
        self.__loop_thread.start()

    def serve(self):
        while self.alive:
            time.sleep(1)

    def add_signals(self):
        # Base SIG handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, lambda _, __: self.stop())

    def stop(self):
        self.alive = False
        self.__loop_thread.join()

    def component_loop(self):
        while self.alive:
            iteration_started = datetime.utcnow()
            self.component_iteration()
            while datetime.utcnow() < iteration_started + timedelta(seconds=self.iter_time):
                time.sleep(.1)

    def component_iteration(self):
        from_dt = datetime.utcnow()
        to_dt = from_dt + timedelta(seconds=self.iter_time)
        with root.context.sc as sc:
            self.ms = root.MS(sc.session)
            ad_tasks = self.ms.allocate_pending_playbacks(from_dt, to_dt)
            task_ad_spot_ids = [t.ad_spot_id for t in ad_tasks]
            ad_defaults = self.ms.get_adspot_defaults(from_dt, to_dt, not_ids=task_ad_spot_ids)
            if ad_defaults:
                self.logger.info(f'Fetched {len(ad_tasks)} ad tasks')
                for ad_default in ad_defaults:
                    self.process_ad_default(ad_default)
            if ad_tasks:
                self.logger.info(f'Fetched {len(ad_tasks)} ad tasks')
            for ad_task in ad_tasks:
                while datetime.utcnow() < ad_task.call_at:
                    time.sleep(.1)
                self.process_task(ad_task)

    def process_ad_default(self, ad_default: 'root.dc.AdSpotDefault'):
        try:
            r: 'requests.Response' = requests.post(
                ad_default.api_url,
                json=ad_default.config.to_web()
            )
            if r.status_code < 400:
                raise Exception(r.text)
        except Exception as e:
            self.logger.exception(
                f'Failed to ad default to {ad_default.api_url}. {e}', exc_info=True
            )

    def process_task(self, ad_task: 'root.dc.AdTask'):
        ok = True
        try:
            if ad_task.api_url:
                r: 'requests.Response' = requests.post(
                    ad_task.api_url,
                    json=ad_task.config.to_web()
                )
                if r.status_code < 400:
                    self.logger.info(
                        f'Playback {ad_task.playback_id} was sent to {ad_task.api_url}.'
                        f'File: {ad_task.config.name}'
                    )
                else:
                    ok = False
                    self.logger.warning(
                        f'Failed to sent task to {ad_task.api_url}. '
                        f'Status: {r.status_code}. Response: {r.content}'
                    )
        except Exception as e:
            ok = False
            self.logger.exception(
                f'Failed to sent task to {ad_task.api_url}. {e}', exc_info=True
            )

        if ok:
            self.ms.mark_task_complete(ad_task)
            if not ad_task.primarily:
                self.near.transfer_funds(ad_task.playback_id)
