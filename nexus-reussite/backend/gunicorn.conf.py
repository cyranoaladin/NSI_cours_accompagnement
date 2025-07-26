"""
Gunicorn configuration for Nexus Réussite Backend
Production-optimized settings
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
worker_class = "gevent"
workers = int(os.environ.get("GUNICORN_WORKERS", 4))
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 120
keepalive = 5

# Restart workers after this many requests, with up to 100 random jitter
max_requests = 1000
max_requests_jitter = 100

# The maximum number of pending connections
backlog = 2048

# Restart workers after this many seconds
max_worker_memory = 256 * 1024 * 1024  # 256MB

# Preload application code before the worker processes are forked
preload_app = True

# Enable worker memory usage monitoring
worker_tmp_dir = "/dev/shm" if os.path.exists("/dev/shm") else None

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'nexus-reussite-backend'

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Environment variables for the application
raw_env = [
    f"FLASK_APP=src.app:create_app()",
    f"FLASK_ENV={os.environ.get('FLASK_ENV', 'production')}",
]

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Nexus Réussite Backend server is ready. Listening on: %s", server.address)

def worker_int(worker):
    """Called just after a worker has been signalled by the master process."""
    worker.log.info("Worker %s interrupted", worker.pid)

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker %s spawned (pid: %s)", worker.age, worker.pid)

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    worker.log.info("Worker %s aborted", worker.pid)

def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forked child, re-executing.")

def pre_request(worker, req):
    """Called just before a worker processes the request."""
    worker.log.debug("%s %s", req.method, req.path)

def post_request(worker, req, environ, resp):
    """Called after a worker processes the request."""
    pass

def child_exit(server, worker):
    """Called just after a worker has been exited, in the master process."""
    server.log.info("Worker %s exited", worker.pid)

def worker_exit(server, worker):
    """Called just after a worker has been exited, in the worker process."""
    server.log.info("Worker %s exited", worker.pid)

def nworkers_changed(server, new_value, old_value):
    """Called just after num_workers has been changed."""
    server.log.info("Number of workers changed from %s to %s", old_value, new_value)

def on_exit(server):
    """Called just before exiting Gunicorn."""
    server.log.info("Nexus Réussite Backend shutting down")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading Nexus Réussite Backend")

# Application callable
wsgi_module = "src.app:create_app()"
