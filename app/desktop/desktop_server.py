import contextlib
import threading
import time
from contextlib import asynccontextmanager
from fastapi.concurrency import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.desktop.studio_server.api.controller.settings_controller import connect_settings_api
from app.desktop.studio_server.api.controller.work_controller import connect_work_api
from app.desktop.studio_server.webhost import connect_webhost
from app.desktop.studio_server.api.controller.model_controller import connect_provider_api

PORT = 8757

@asynccontextmanager
async def lifespan():
    yield

def make_app(lifespan=None):
    app = FastAPI(
        title="XH Agent Server",
        summary="A REST API for the XH Agent datamodel.",
        description="Learn more about XH Agent at https://github.com/Yezery/XH_Agent",
        lifespan=lifespan,
    )

    connect_provider_api(app)
    connect_settings_api(app)
    connect_work_api(app)
    # Important: webhost must be last, it handles all other URLs
    connect_webhost(app)
    @app.get("/ping")
    def ping():
        return "pong"


    allowed_origins = [
        f"http://localhost:{PORT}",
        f"http://127.0.0.1:{PORT}",
        f"https://localhost:{PORT}",
        f"https://127.0.0.1:{PORT}",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
    


def server_config(port=PORT):
    return uvicorn.Config(
        make_app(),
        host="localhost",
        port=port,
        log_level="warning",
        use_colors=False,
    )


class ThreadedServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        self.stopped = False
        thread = threading.Thread(target=self.run_safe, daemon=True)
        thread.start()
        try:
            while not self.started and not self.stopped:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()

    def run_safe(self):
        try:
            self.run()
        finally:
            self.stopped = True

    def running(self):
        return self.started and not self.stopped


def run_studio():
    uvicorn.run(make_app(), host="127.0.0.1", port=PORT, log_level="warning")


def run_studio_thread():
    thread = threading.Thread(target=run_studio)
    thread.start()
    return thread
