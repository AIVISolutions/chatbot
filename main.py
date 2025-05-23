from fastapi import FastAPI
from gradio.routes import mount_gradio_app
from chatbot_aiva import iface

app = FastAPI()
mount_gradio_app(app, iface, path="/")