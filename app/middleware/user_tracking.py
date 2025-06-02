from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.kafka_producer import kafka_producer
import uuid
from datetime import datetime

class UserTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Start time
        session_start = datetime.now()
        
        # Get user ID from request if authenticated
        user_id = None
        if hasattr(request.state, 'user'):
            user_id = request.state.user.id
        
        # Store request start time and path
        request.state.tracking = {
            'session_id': session_id,
            'start_time': session_start,
            'path': request.url.path,
            'click_count': 1  # Each request counts as one click
        }
        
        # Process the request
        response = await call_next(request)
        
        # End time
        session_end = datetime.now()
        
        # Only track if we have a user_id
        if user_id:
            # Prepare tracking data
            tracking_data = {
                'session_id': session_id,
                'session_start': session_start.isoformat(),
                'session_end': session_end.isoformat(),
                'path': request.url.path,
                'click_count': request.state.tracking['click_count']
            }
            
            # Send to Kafka
            kafka_producer.send_user_action(user_id, tracking_data)
        
        return response 