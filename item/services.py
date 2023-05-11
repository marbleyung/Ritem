import os
from .models import Image


def delete_image(pk: int):
    try:
        image = Image.objects.get(pk=pk)
        owner = image.owner
        directory = f'media/item/{owner}'
        try:
            os.remove(f"{directory}/{image.uuid}.{image.extension}")
            print('Successful deleted from /media/')
        except FileNotFoundError:
            print('This file does not exist')
    except Image.DoesNotExist:
        print('This image does not exist')


