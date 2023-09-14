import os

from main_sql import main_sql_func

def real_main():
    sql_engine = main_sql_func()

def push_image_to_database(image_name, user_name):
    user_folder = "/" + str(user_name)
    if os.path.exists(user_folder):
        pass
    else:
        os.mkdir(user_folder)
    image_path = user_folder + "/" + image_name
    if image_exists():
        # copy image to imagepath
        pass
    else:
        # add 1 to name and push
        pass

def get_all_user_images_from_database(user_name):
    result = []
    # from sql
    return result

def image_exists(image_name, user_name):
    image_path = "/" + user_name + "/" + image_name
    if os.path.exists(image_path):
        return True
    else:
        return False
    
real_main()
    

    


