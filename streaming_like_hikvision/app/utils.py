import os
import time 
import subprocess
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)

def start_ffmpeg_stream(rtsp_url, camera_number):
    """Convert RTSP to HLS using FFmpeg."""
    output_folder = Path(settings.MEDIA_ROOT) / 'hls' / f'camera_{camera_number}'
    output_folder.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Output folder: {output_folder}")
    
    # Clean existing files
    for file in output_folder.glob('*'):
        try:
            file.unlink()
            logger.info(f"Deleted existing file: {file}")
        except Exception as e:
            logger.error(f"Error deleting file {file}: {e}")

    output_path = output_folder / 'playlist.m3u8'

    command = [
    'ffmpeg',
    '-y',
    '-rtsp_transport', 'tcp',
    '-i', rtsp_url,
    '-r', '10',  # Set FPS to 10 (adjust this value as needed)
    '-c', 'copy',
    '-f', 'hls',
    '-hls_time', '2',
    '-hls_list_size', '3',
    '-hls_flags', 'delete_segments+append_list',
    '-hls_segment_filename', str(output_folder / 'segment_%03d.ts'),
    str(output_path)
]

    # command = [
    #     'ffmpeg',
    #     '-y',
    #     '-rtsp_transport', 'tcp',  # Ensure RTSP over TCP for reliability
    #     '-i', rtsp_url,  # Input RTSP stream
    #     '-r', '25',  # Set the frame rate to a more typical value
    #     '-c:v', 'libx264',  # Use H.264 video codec (most widely supported)
    #     '-preset', 'veryfast',  # Use a preset for faster encoding, lower CPU load
    #     '-crf', '23',  # Constant Rate Factor (balance between quality and file size)
    #     '-maxrate', '2000k',  # Cap the bitrate to avoid sudden bandwidth spikes
    #     '-bufsize', '4000k',  # Set a buffer size to smooth out fluctuations
    #     '-f', 'hls',  # Output as HLS format
    #     '-hls_time', '4',  # Segment duration in seconds
    #     '-hls_list_size', '10',  # Keep 10 segments in the playlist
    #     '-hls_flags', 'delete_segments+append_list',  # Ensure playlist is updated dynamically
    #     '-hls_segment_filename', str(output_folder / 'segment_%03d.ts'),  # Segment file naming pattern
    #     str(output_path)  # Output playlist
    # ]



    logger.info(f"FFmpeg command: {' '.join(command)}")

    try:
        # Start FFmpeg process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # Hide console window
        )
        
        # Wait for FFmpeg to start and create files
        max_wait = 10  # Maximum wait time in seconds
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            if process.poll() is not None:
                # Process terminated
                error_output = process.stderr.read()    
                logger.error(f"FFmpeg process terminated: {error_output}")
                return None
                
            if output_path.exists():
                # Check if the m3u8 file has content
                if output_path.stat().st_size > 0:
                    logger.info(f"FFmpeg process started successfully")
                    return f"/media/hls/camera_{camera_number}/playlist.m3u8"
            
            time.sleep(0.5)
        
        # If we get here, the timeout was reached
        logger.error("Timeout waiting for FFmpeg to create output files")
        process.terminate()
        return None
            
    except Exception as e:
        logger.error(f"Failed to start FFmpeg: {e}")
        return None





 


  