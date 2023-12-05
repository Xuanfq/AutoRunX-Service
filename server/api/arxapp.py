
from django.contrib.auth.models import User
from .models import App, ErrorLog
from django.db import transaction
from datetime import datetime
from django.utils import timezone
from threading import Thread, Lock, Timer
from subprocess import PIPE, Popen
import os
import sys
import zipfile
import signal
import websockets
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from .lib.threadtk import ThreadWithReturnValue


# app controller
class AppController(Thread):
    def __init__(self, id, run_config_path) -> None:
        Thread.__init__(self, name=id)
        self.id = id
        self._run_config_path = run_config_path
        self._run_workspace_path = os.path.join(os.path.dirname(self._run_config_path),
                                                'workspace')
        self._run_workspace_zip_path = os.path.join(os.path.dirname(self._run_config_path),
                                                    '{}.zip'.format(str(id)))
        print(self._run_config_path, self._run_workspace_path,
              self._run_workspace_zip_path)
        # self._cmd_run = 'autorunx -d -f {config} '.format(config=self._run_config_path)
        self._cmd_run = """
        echo "hello";
        sleep 2;
        i=1;
        max=100000;
        while true
        do 
            echo "out $i";
            sleep 2;
            i=`expr $i + 1`
        done
        sleep 1;
        echo "a";
        sleep 5;
        echo "b";
        sleep 5;
        echo "c";
        sleep 5;
        echo "d";
        sleep 5;
        echo "e";
        sleep 5;
        echo "f";
        sleep 5;
        echo "g";
        sleep 5;
        echo "h";
        sleep 15;
        echo "world"
        """.format(
            os.path.join(self._run_workspace_path, 'test.log'))
        self._process = None
        self._schedule_timer = None
        self._status_abort = False
        self._status_started = False
        self._status_lock = Lock()
        self._on_start_callback = None
        self._on_start_callback_args = []
        self._on_start_callback_kwargs = {}
        self._on_end_callback = None
        self._on_end_callback_args = []
        self._on_end_callback_kwargs = {}
        self._on_abort_callback = None
        self._on_abort_callback_args = []
        self._on_abort_callback_kwargs = {}
        self._on_error_callback = None
        self._on_error_callback_args = []
        self._on_error_callback_kwargs = {}
        self._on_stdio_callback = None
        if not os.path.exists(self._run_workspace_path):
            os.mkdir(self._run_workspace_path)

    def _compress_workspace_to_resultzip(self):
        folder_path = self._run_workspace_path
        zip_file_path = self._run_workspace_zip_path
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    zip_file.write(file_path, os.path.relpath(
                        file_path, folder_path))

    def on_start_callback(self, fn, sync_fn=True, *args, **kwargs):
        self._on_start_callback = fn if sync_fn else async_to_sync(fn)
        self._on_start_callback_args = args
        self._on_start_callback_kwargs = kwargs

    def on_end_callback(self, fn, sync_fn=True, *args, **kwargs):
        self._on_end_callback = fn if sync_fn else async_to_sync(fn)
        self._on_end_callback_args = args
        self._on_end_callback_kwargs = kwargs

    def on_abort_callback(self, fn, sync_fn=True, *args, **kwargs):
        self._on_abort_callback = fn if sync_fn else async_to_sync(fn)
        self._on_abort_callback_args = args
        self._on_abort_callback_kwargs = kwargs

    def on_error_callback(self, fn, sync_fn=True, *args, **kwargs):
        self._on_error_callback = fn if sync_fn else async_to_sync(fn)
        self._on_error_callback_args = args
        self._on_error_callback_kwargs = kwargs

    def on_stdio_callback(self, fn, sync_fn=True):
        """stdio when app is running

        Args:
            fn (function): callback function, param: stdin,stdout_str,stderr_str
        """
        def f(*args, **kwargs):
            try:
                func = fn if sync_fn else async_to_sync(fn)
                func(*args, **kwargs)
            except:
                self._on_stdio_callback = None
        self._on_stdio_callback = f

    def run(self):
        self.cancel_schedule()
        # change status
        with self._status_lock:
            self._status_started = True
        # start callback
        if self._on_start_callback:
            self._on_start_callback(*self._on_start_callback_args,
                                    **self._on_start_callback_kwargs)
        # exec
        self._process = Popen(self._cmd_run, stdin=None,
                              stdout=PIPE, stderr=PIPE, shell=True,
                              preexec_fn=os.setsid)
        stdin = self._process.stdin
        stdout = self._process.stdout
        stderr = self._process.stderr
        errinfo = ''
        while stdout.readable():
            output = stdout.read(1)
            print('out:', output)
            if not output:
                break
            if self._on_stdio_callback is not None:
                msg = output.decode('utf-8')
                print('send out')
                self._on_stdio_callback(stdin, msg, None)
        while stderr.readable():
            output = stderr.read(1)
            print('err:', output)
            if not output:
                break
            if self._on_stdio_callback is not None:
                msg = output.decode('utf-8')
                errinfo = f'{errinfo}{msg}'
                print('send err')
                self._on_stdio_callback(stdin, None, msg)
        if self._on_stdio_callback is not None:
            self._on_stdio_callback(None, None, None)
        # self._process.wait()
        # outinfo, errinfo = self._process.communicate()
        # outinfo = outinfo.decode()
        # errinfo = errinfo.decode()
        self._compress_workspace_to_resultzip()
        # abort callback
        if self._status_abort and self._on_abort_callback:
            self._on_abort_callback(*self._on_abort_callback_args,
                                    **self._on_abort_callback_kwargs)
        # error callback
        if len(errinfo) > 0:
            if self._on_error_callback:
                self._on_error_callback(*self._on_error_callback_args,
                                        **self._on_error_callback_kwargs,
                                        error=errinfo)
        print('end:', self.id, errinfo)
        # end callback
        if self._on_end_callback:
            self._on_end_callback(*self._on_end_callback_args,
                                  **self._on_end_callback_kwargs)

    def communicate(self) -> (bytes, bytes):
        if self._status_started:
            return self._stdout, self._stderr
        return None, None

    def schedule(self, start_datetime: datetime):
        with self._status_lock:
            if self._status_started:
                return False
            if self._schedule_timer is not None:
                self._schedule_timer.cancel()
            self._schedule_timer = Timer(start_datetime.timestamp() -
                                         datetime.now().timestamp(), self.start)
            self._schedule_timer.start()
            return True

    def cancel_schedule(self):
        with self._status_lock:
            if self._status_started:
                return False
            if self._schedule_timer is not None:
                self._schedule_timer.cancel()
                return True
        return False

    def abort(self):
        with self._status_lock:
            if self._status_started:
                self._status_abort = True
                # self._process.send_signal(2)  # ctrl + c
                # kill all subprocess
                os.killpg(self._process.pid, signal.SIGTERM)
                return True
        return False


# app manager
class AppManager:
    def __init__(self, app_base_path, websocket_support=True, websocket_port=8765, token_auth_funcion=None, max_app_num=9999) -> None:
        self._app_base_path = app_base_path
        self._max_app = 9999
        self._pool_map = {}
        self._pool_map_lock = Lock()
        self._websocket_support = websocket_support
        self._websocket_port = websocket_port
        self._websocket = None
        self._token_auth_funcion = token_auth_funcion
        self._fault_detect_recovery()
        if websocket_support:
            self._start_websocket_server(port=websocket_port)

    def _start_websocket_server(self, port=8765):
        async def handler(websocket, path):
            # ACCEPT_SIGNAL and REFUSE_SIGNAL appear at the same time,
            ACCEPT_SIGNAL = '^^^^^^^^^^ACCEPT^^^^^^^^^^'
            REFUSE_SIGNAL = '^^^^^^^^^^REFUSE^^^^^^^^^^'
            cmd = None
            params = []
            # gateway
            if path.startswith('/api/app/'):
                cmd_param = path.replace('/api/app/', '').split('/')
                cmd, params = cmd_param[0], cmd_param[1:]
            else:
                return
            print(cmd, params)
            # auth/login
            token = await websocket.recv()
            user = None
            if self._token_auth_funcion is not None:
                flag, username = self._token_auth_funcion(token)
                if not flag:
                    await websocket.send(REFUSE_SIGNAL)
                    return

                def get_user(username):
                    return User.objects.filter(username=username)[0]
                # need to open django async in setting file
                t = ThreadWithReturnValue(target=get_user, args=(username,))
                t.start()
                user = t.join()
                await websocket.send(ACCEPT_SIGNAL)
            else:
                await websocket.send(REFUSE_SIGNAL)  # default refuse
                return
            # cmd/params: appmonitor/appid
            if cmd == 'appmonitor' and len(params) == 1:
                appid = params[0]

                def exist_app(user, appid):
                    return len(App.objects.filter(owner=user,
                                                  id=appid,
                                                  delete_time=None)) > 0
                t = ThreadWithReturnValue(
                    target=exist_app, args=(user, appid))
                t.start()
                exist = t.join()
                if not exist or appid not in self._pool_map:
                    await websocket.send(REFUSE_SIGNAL)
                    return

                async def app_stdio_handler(stdin, stdout_str, stderr_str):
                    if stdout_str is not None:
                        await websocket.send(stdout_str)
                    elif stderr_str is not None:
                        await websocket.send(stderr_str)
                    else:
                        await websocket.send(REFUSE_SIGNAL)
                        return
                self._pool_map[appid].on_stdio_callback(
                    app_stdio_handler, sync_fn=False)
                # await app message sent finish
                try:
                    await websocket.recv()
                except:
                    pass

        async def main():
            async with websockets.serve(handler, "localhost", port):
                print(f'AppManager Websocket Service: ws://localhost:{port}')
                await asyncio.Future()  # run forever
        self._websocket = Thread(target=lambda: asyncio.run(
            main()), name='AppManagerWebSocket')
        self._websocket.start()  # 迁移时注释

    def _fault_detect_recovery(self):
        """fault detect and recovery
        warning: need to block database?
        """
        app_query_result = App.objects.filter(delete_time=None)
        sched_list = []
        start_list = []
        for app in app_query_result:
            appid = str(app.id)
            with self._pool_map_lock:
                if appid not in self._pool_map and \
                        (app.plan_start_time is not None or app.start_running_time is not None) \
                        and app.end_running_time is None:
                    appc = AppController(appid, os.path.join(
                        self._app_base_path, str(app.run_config_file)))
                    appc.on_start_callback(self._on_start_callback, id=appid)
                    appc.on_end_callback(self._on_end_callback, id=appid)
                    appc.on_abort_callback(self._on_abort_callback, id=appid)
                    appc.on_error_callback(self._on_error_callback, id=appid)
                    self._pool_map[appid] = appc
                    if app.plan_start_time is not None and app.plan_start_time.timestamp() - datetime.now().timestamp() > 0:
                        # appc.schedule(app.plan_start_time)
                        sched_list.append((appc, app.plan_start_time))
                    else:
                        # appc.start()
                        start_list.append(appc)
                    ErrorLog(owner=app.owner,
                             error='The system is down and running again',
                             error_type='system/app',
                             error_data='appid=%s' % appid,).save()
        for appc, plan_start_time in sched_list:
            appc.schedule(plan_start_time)
        for appc in start_list:
            appc.start()

    def _on_start_callback(self, id):
        id = str(id)
        with transaction.atomic():
            app_query_result = App.objects.filter(id=id, delete_time=None)
            if len(app_query_result) == 0:
                return
            app = app_query_result[0]
            app.start_running_time = datetime.now()
            app.save()

    def _on_end_callback(self, id):
        id = str(id)
        with transaction.atomic():
            app_query_result = App.objects.filter(id=id, delete_time=None)
            if len(app_query_result) == 0:
                return
            app = app_query_result[0]
            app.end_running_time = datetime.now()
            app.save()
            with self._pool_map_lock:
                if id in self._pool_map:
                    # delete id
                    self._pool_map.pop(id, None)

    def _on_abort_callback(self, id):
        id = str(id)
        with transaction.atomic():
            app_query_result = App.objects.filter(id=id, delete_time=None)
            if len(app_query_result) == 0:
                return
            app = app_query_result[0]
            app.abort_running_time = datetime.now()
            app.save()

    def _on_error_callback(self, id, error):
        id = str(id)
        with transaction.atomic():
            app_query_result = App.objects.filter(id=id, delete_time=None)
            if len(app_query_result) == 0:
                return
            app = app_query_result[0]
            app.run_time_error = str(error)
            app.save()
        ErrorLog(owner=app.owner,
                 error=str(error)[0:64],
                 error_type='app',
                 error_data=str(error)).save()

    def create(self, app: App):
        appid = str(app.id)
        with self._pool_map_lock:
            if appid in self._pool_map or len(self._pool_map) >= self._max_app:
                return False
            appc = AppController(appid, os.path.join(
                self._app_base_path, str(app.run_config_file)))
            appc.on_start_callback(self._on_start_callback, id=appid)
            appc.on_end_callback(self._on_end_callback, id=appid)
            appc.on_abort_callback(self._on_abort_callback, id=appid)
            appc.on_error_callback(self._on_error_callback, id=appid)
            self._pool_map[appid] = appc
            return True

    def start(self, id: str):
        id = str(id)
        with self._pool_map_lock:
            if id in self._pool_map:
                self._pool_map[id].start()

    def schedule(self, id: str, start_datetime: datetime):
        id = str(id)
        with self._pool_map_lock:
            if id in self._pool_map:
                self._pool_map[id].schedule(start_datetime)

    def cancel_schedule(self, id: str):
        id = str(id)
        with self._pool_map_lock:
            if id in self._pool_map:
                self._pool_map[id].cancel_schedule()

    def abort(self, id: str):
        id = str(id)
        with self._pool_map_lock:
            if id in self._pool_map:
                self._pool_map[id].abort()

    def exist(self, appid):
        appid = str(appid)
        with self._pool_map_lock:
            if appid in self._pool_map:
                return True
            return False
