import requests


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )

        return res.json()


    def greeting(self, user: str):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            json={
                'user': user,
            },
        )

        return res.json()

    def read_plate_by_id(self, plate_id: int):
        res = requests.get(
            f'{self.host}/id/{plate_id}'
        )
        return res

    def read_multiple_plates(self, plate_ids: list[int]):
        res = requests.post(
            f'{self.host}/readplates',
            json={
                'ids': plate_ids,
            }
        )
        return res


if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080')
    # get single plate num
    res = client.read_plate_by_id(10022)
    # get multiple plate nums
    # res = client.read_multiple_plates([10022, 9965])
    print(res.text)