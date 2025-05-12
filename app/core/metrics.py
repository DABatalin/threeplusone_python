from prometheus_client import Counter, Histogram, Gauge
from prometheus_client.metrics import Info

REQUEST_TIME = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint', 'status_code'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]  
)

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

ERROR_COUNT = Counter(
    'http_errors_total',
    'Total number of HTTP errors',
    ['method', 'endpoint', 'status_code', 'error_type']
)

MEMORY_USAGE = Gauge(
    'app_memory_usage_bytes',
    'Memory usage in bytes'
)

APP_INFO = Info(
    'app_info',
    'Application information'
) 