# -*- coding: utf-8 -*-
if __name__ == "__main__":
    import uvicorn
    import os

    os.environ["LOG_LEVEL"] = "DEBUG"

    #     LoggerConfig(logging.DEBUG)
    #     log = logging.getLogger()
    #     log.debug("start")
    #
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
