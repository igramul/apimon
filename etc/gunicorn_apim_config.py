# Gunicorn configuration file

# Server socket
bind = ":80"

# Worker processes
workers = 1
worker_class = "sync"
threads = 1

# Worker timeout and lifecycle
timeout = 120
graceful_timeout = 30
keepalive = 5

# Worker restart to prevent memory leaks
max_requests = 0  # Disable automatic worker restart
max_requests_jitter = 0

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Process naming
proc_name = "apimon"

# Preload application to save memory
preload_app = False  # Set to False to avoid scheduler conflicts with worker processes

# Worker lifecycle hooks
def post_fork(server, worker):
    """Called after a worker has been forked."""
    import logging
    logging.info(f"Worker spawned (pid: {worker.pid})")

def worker_exit(server, worker):
    """Called when a worker is about to exit."""
    import logging
    logging.info(f"Worker exiting (pid: {worker.pid})")

