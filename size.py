import cv2
import os




def avaSize(path):
    src = cv2.imread(path, cv2.IMREAD_UNCHANGED) 
    #percent by which the image is resized 
    #calculate the 50 percent of original dimensions 
    if src.shape[0] < src.shape[1]:
        print('height < width')
        scale_percent = (200 * 100) / (src.shape[1] * 100)
    elif src.shape[0] > src.shape[1]:
        print('height > width')
        scale_percent = (200 * 100) / (src.shape[0] * 100)
    else:
        print('height == width')
        scale_percent = (200 * 100) / (src.shape[0] * 100)
    print(scale_percent)
    width = int(src.shape[1] * scale_percent) 
    height = int(src.shape[0] * scale_percent)
    # dsize
    bsize = (src.shape[1], src.shape[0]) 
    dsize = (width, height) 
    print(src.shape[1] * scale_percent)
    print(dsize)
    # resize image 
    output = cv2.resize(src, dsize)

    cv2.imwrite('./change/change_pick.jpeg',output)
    # str = file.rsplit('.')
    # l = len(str)
    # formatIs = str[l-1]


def ava(usr, file):
    # usr = 'bak'
    # Стартовый путь, в котором вы хотите выполнять поиск
    start_directory = os.path.join('./usrs/', usr)
    # Имя файла, который вы ищете

    # Перебираем директории и поддиректории, начиная с заданной
    for root, _, files in os.walk(start_directory):
        if file in files:
            # Файл найден в текущей директории, формируем абсолютный путь
            absolute_path = os.path.join(root, file)
            print(f"Файл {file} найден по пути: {absolute_path}")
            break  # Если файл найден, выходим из цикла
    # print(absolute_path)
    avaSize(absolute_path)
    # Если файл не найден, выводим сообщение
    if not absolute_path:
        print(f"Файл {file} не найден в заданной директории и её поддиректориях.")


#     my_string = "some.text.example"

# # Разделяем строку на последнем вхождении точки
# parts = my_string.rsplit('.', 1)
#  parts[len-1]
# # parts[0] содержит все символы до последней точки, parts[1] - после нее

#  parts[len-1]
#     after_dot = parts[1]
# else:
#     # В случае, если точка не найдена, обработайте соответствующим образом
#     before_dot = my_string
#     after_dot = ""

# print("Before dot:", before_dot)
# print("After dot:", after_dot)


# import cv2
# def f(new_width, new_height):
#     src = cv2.imread('./images/pick.jpeg', cv2.IMREAD_UNCHANGED) 
#     # # set a new width in pixels
#     if src.shape[0] < src.shape[1]:
#         print('height < width')
#         scale_percent = (new_width * 100) / (src.shape[1] * 100)
#     elif src.shape[0] > src.shape[1]:
#         print('height > width')
#         scale_percent = (new_height * 100) / (src.shape[0] * 100)
#     else:
#         print('height == width')
#         scale_percent = (new_height * 100) / (src.shape[0] * 100)
#     print(scale_percent)
#     width = int(src.shape[1] * scale_percent) 
#     height = int(src.shape[0] * scale_percent)
#     # dsize
#     bsize = (src.shape[1], src.shape[0]) 
#     dsize = (width, height) 
#     print(src.shape[1] * scale_percent)
#     print(dsize)
#     # resize image 
#     output = cv2.resize(src, dsize) 
#     cv2.imwrite('./change/change_pick.jpeg',output)

# f(50, 100)


ava('bak', 'pick.jpeg')