from PIL import Image


head = Image.open('benefit.png')
border = 133

# Для расположения картинки по центру
def center_dot(coor):
    x = head.size[0] // 2 - coor[0]//2
    y = (head.size[1]-border-coor[1])//2
    return x, y


test_image = Image.open('106044_benefit.jpg')
coordinates = center_dot(test_image.size)  # Координаты для центрирования
head.paste(test_image, (coordinates[0], coordinates[1]+border))

head.save(f'result.{head.format}')
