import os

from waitress import serve

import cache_service

PORT = os.environ.get("PORT", 9090)
serve(cache_service.app, host='0.0.0.0', port=PORT)
