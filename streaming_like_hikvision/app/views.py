from django.shortcuts import render
from .utils import start_ffmpeg_stream
import logging
import os
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import time

logger = logging.getLogger(__name__)
 

@xframe_options_exempt
@require_http_methods(["GET"])
def video_grid(request):
    rtsp_urls = [

        
        'rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6',
        'rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6',
        'rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6',
        'rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6',
        'rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6',
        'rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6','rtsp://172.16.12.33:8554/video6',
    ]
     
    hls_paths = []
    for index, rtsp_url in enumerate(rtsp_urls, start=1):
        hls_path = start_ffmpeg_stream(rtsp_url, index)
        if hls_path:
            hls_paths.append(hls_path)
        else:
            logger.error(f"Failed to initialize stream {index}")
    
    return render(request, 'app/video_grid.html', {'hls_paths': hls_paths})


def health_check(request, camera_number):
    """Check if the stream files exist and are being updated."""
    media_dir = settings.MEDIA_ROOT
    m3u8_path = os.path.join(media_dir, 'hls', f'camera_{camera_number}', 'playlist.m3u8')

    
    if os.path.exists(m3u8_path):
        # Check if file was modified in the last 5 seconds
        if time.time() - os.path.getmtime(m3u8_path) < 5:
            return JsonResponse({'status': 'ok', 'message': 'Stream is active'})
    
    return JsonResponse({'status': 'error', 'message': 'Stream is not active'}, status=500)


def index(request):
    hls_paths = []
    rtsp_url = "rtsp://172.16.12.33:8554/video6"

    for index in range(1, 3):  # Create two streams
        logger.info(f"Starting stream {index}")
        hls_path = start_ffmpeg_stream(rtsp_url, index)
        
        if hls_path:
            logger.info(f"Stream {index} initialized successfully")
            hls_paths.append(hls_path)
        else:
            logger.error(f"Failed to initialize stream {index}")
    
    return render(request, 'app/video_grid.html', {'hls_paths': hls_paths})



def stream_view(request):
    hls_paths = []
    base_dir = Path(settings.MEDIA_ROOT) / 'hls'
    
    # Loop through the cameras to generate paths for each
    for camera_number in range(1, 21):  # Assuming 20 cameras
        camera_path = base_dir / f'camera_{camera_number}' / 'playlist.m3u8'
        if os.path.exists(camera_path):
            hls_paths.append(str(camera_path))
    
    return render(request, 'streaming_page.html', {'hls_paths': hls_paths})