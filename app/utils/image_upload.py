import requests
import os
import base64

def upload_to_imagebb(image_file):
    try:
        api_key = '61e3d87e49e4158a72f7254e5159b4d0'  # Using the API key directly for testing
        url = "https://api.imgbb.com/1/upload"
        
        # Reset file pointer
        image_file.seek(0)
        
        # Convert image to base64
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        payload = {
            "key": api_key,
            "image": image_data,
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["data"]["display_url"]
            
        print(f"ImageBB Response: {response.text}")  # Debug logging
        raise Exception("Failed to upload image to ImageBB")
    except Exception as e:
        print(f"Image upload error: {str(e)}")  # Debug logging
        raise Exception(f"Image upload failed: {str(e)}")