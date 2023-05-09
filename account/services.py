import os
from .models import CustomUser, UserImage


def delete_user_image(user: CustomUser):
    try:
        UserImage.objects.filter(owner=user).delete()
        directory = f'media/user_image/{str(user)}'
        if not os.path.isdir(directory):
            print('Created directory', directory)
            os.mkdir(directory)

        for item in os.scandir(directory):
            os.remove(item)
        print('Successful deleted')
    except UserImage.DoesNotExist:
        print('User has no images')


