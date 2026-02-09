"""
YouTube Video Downloader
Downloads video and audio streams separately, then merges them using FFmpeg
"""

import os
import subprocess
from pytubefix import YouTube
from pytubefix.cli import on_progress


def download_youtube_video(url, output_dir="downloads"):
    """
    Download YouTube video and audio streams, then merge them
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save downloaded files
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"Fetching video information for: {url}")
        
        # Initialize YouTube object with PO Token support
        yt = YouTube(url, use_po_token=True, on_progress_callback=on_progress)
        
        print(f"\nTitle: {yt.title}")
        print(f"Author: {yt.author}")
        print(f"Duration: {yt.length} seconds")
        print(f"Views: {yt.views:,}")
        
        # Display available streams
        print("\n" + "="*50)
        print("Available streams:")
        print("="*50)
        for i, stream in enumerate(yt.streams):
            print(f"{i:2d}. {stream}")
        
        # Get highest resolution video (video only)
        print("\n" + "="*50)
        print("Downloading video stream...")
        print("="*50)
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        
        if video_stream:
            video_filename = video_stream.download(output_path=output_dir, filename_prefix="video_")
            print(f"✓ Video downloaded: {video_filename}")
        else:
            print("✗ No suitable video stream found")
            return False
        
        # Get highest quality audio
        print("\n" + "="*50)
        print("Downloading audio stream...")
        print("="*50)
        audio_stream = yt.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()
        
        if audio_stream:
            audio_filename = audio_stream.download(output_path=output_dir, filename_prefix="audio_")
            print(f"✓ Audio downloaded: {audio_filename}")
        else:
            print("✗ No suitable audio stream found")
            return False
        
        # Merge video and audio using FFmpeg
        print("\n" + "="*50)
        print("Merging video and audio...")
        print("="*50)
        
        # Clean filename for output
        safe_title = "".join(c for c in yt.title if c.isalnum() or c in (' ', '-', '_')).strip()
        output_filename = os.path.join(output_dir, f"{safe_title}.mp4")
        
        # FFmpeg command to merge
        ffmpeg_command = [
            'ffmpeg',
            '-i', video_filename,
            '-i', audio_filename,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-y',  # Overwrite output file if exists
            output_filename
        ]
        
        result = subprocess.run(ffmpeg_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Successfully merged! Output: {output_filename}")
            
            # Clean up temporary files
            try:
                os.remove(video_filename)
                os.remove(audio_filename)
                print("✓ Temporary files cleaned up")
            except Exception as e:
                print(f"⚠ Warning: Could not delete temporary files: {e}")
            
            return True
        else:
            print(f"✗ FFmpeg error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Main function to test the downloader"""
    
    print("="*60)
    print("YouTube Video Downloader")
    print("="*60)
    print()
    
    # Test URL - replace with your desired video
    test_url = input("Enter YouTube URL (or press Enter for test video): ").strip()
    
    if not test_url:
        # Default test video (short public domain video)
        test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        print(f"Using test video: {test_url}")
    
    # Download and merge
    success = download_youtube_video(test_url)
    
    if success:
        print("\n" + "="*60)
        print("✓ DOWNLOAD COMPLETED SUCCESSFULLY!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("✗ DOWNLOAD FAILED")
        print("="*60)
        print("\nTroubleshooting:")
        print("1. Make sure FFmpeg is installed")
        print("2. Check your internet connection")
        print("3. Verify the YouTube URL is correct")


if __name__ == "__main__":
    main()
