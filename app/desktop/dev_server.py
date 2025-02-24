# Run a desktop server for development:
# - Auto-reload is enabled
# - Extra logging (level+colors) is enabled
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.desktop.studio_server.api.controller.model_controller import connect_provider_api
from app.desktop.studio_server.api.controller.settings_controller import connect_settings_api
from app.desktop.studio_server.api.controller.work_controller import connect_work_api
from app.desktop.studio_server.webhost import connect_webhost

PORT = 5173

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
    


# top level app object, as that's needed by auto-reload
dev_app = make_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.desktop.dev_server:dev_app",
        host="127.0.0.1",
        port=8757,
        reload=True,
    )
