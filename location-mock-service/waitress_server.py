import os

from waitress import serve

import location_service

PORT = os.environ.get("PORT", 9090)
serve(location_service.app, host='0.0.0.0', port=PORT)
