import requests
import io

class ImageServerClient:
    def __init__(self, host: str = "http://89.169.157.72:8080"):
        self.host = host

    def fetch_image_data(self, img_id: int) -> io.BytesIO:
        img_url = f'{self.host}/images/{img_id}'
        try:
            img_data = requests.get(img_url, timeout=5)
        except requests.exceptions.Timeout as to:
            print("Timed out")

        if img_data.status_code != 200:
            raise ValueError(f'Image with id {img_id} is not found')
        img_io = io.BytesIO(img_data.content)
        return img_io
    

if __name__ == '__main__':
    client = ImageServerClient()
    res = client.fetch_image_data(996)
    print(res)