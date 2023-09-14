import random 
import string
names = [
    "Ethan", "Psychokid", "Lisa", "Michael", "Sophia", "Liam", "Olivia", "Jackson", "Emma", "Aiden",
    "Isabella", "Lucas", "Mia", "Noah", "Charlotte", "Mason", "Amelia", "Elijah", "Harper", "Logan",
    "Evelyn", "Carter", "Abigail", "Henry", "Emily", "Sebastian", "Elizabeth", "Alexander", "Sofia",
    "James", "Avery", "Benjamin", "Scarlett", "William", "Grace", "Daniel", "Chloe", "Joseph", "Lily",
    "Samuel", "Hannah", "David", "Victoria", "Matthew", "Madison", "Ella", "Aiden", "Samantha", "Oliver",
    "Natalie", "Henry", "Aria", "Joseph", "Addison", "John", "Zoe", "Christopher", "Layla", "Gabriel",
    "Riley", "Evan", "Hazel", "Eli", "Leah", "Joshua", "Audrey", "Ryan", "Claire", "Nathan", "Aubrey",
    "Jack", "Brooklyn", "Andrew", "Stella", "Isaac", "Aaliyah", "Owen", "Skylar", "Caleb", "Lillian",
    "Dylan", "Paisley", "Luke", "Scarlet", "Landon", "Nova", "Wyatt", "Emilia", "Julian", "Violet",
    "Levi", "Luna", "Hunter", "Zara", "Christian", "Haley", "Isaiah", "Eliana", "Thomas", "Ariana",
    "Aaron", "Willow", "Adrian", "Gianna", "Charles", "Elena", "Connor", "Nora", "Eli", "Mila",
    "Josiah", "Kinsley", "Jonathan", "Isla", "Nicholas", "Alice", "Colton", "Sadie", "Jordan", "Hannah",
    "Dominic", "Elizabeth", "Xavier", "Layla", "Jaxon", "Bella", "Jeremiah", "Quinn", "Nathaniel", "Grace",
    "Grayson", "Lucy", "Jace", "Peyton", "Cooper", "Nova", "Tristan", "Liliana", "Carson", "Eleanor",
    "Asher", "Madeline", "Lincoln", "Natalia", "Leo", "Addison", "Cameron", "Elianna", "Adam", "Ella",
    "Theodore", "Holly", "Samuel", "Penelope", "Ian", "Annabelle", "Hudson", "Emery", "Sebastian", "Katherine",
    "Miles", "Marley", "Zachary", "Aurora", "David", "Nina", "Chase", "Leilani", "Blake", "Aubree",
    "Nolan", "Zoey", "Austin", "Delilah", "Gavin", "Lyla", "Levi", "Savannah", "Carter", "Melanie",
    "Kayden", "Jasmine", "Elias", "Willow", "Colin", "Daisy", "Bentley", "Adeline", "Brody", "Athena",
    "Santiago", "Alexa", "Dominic", "Nova", "Jaxson", "Hazel", "Greyson", "Camila", "Adam", "Valentina",
    "John", "Ruby", "Isaiah", "Alice", "Daniel", "Luna", "Joseph", "Alexandra", "Josiah", "Eliza",
    "Julian", "Georgia", "Christopher", "Brielle", "Joshua", "Valeria", "Nicholas", "Vanessa", "Jackson", "Ivy",
    "Aidan", "Clara", "Colton", "Rylee", "Justin", "Reagan", "Robert", "Jordyn", "Henry", "Beatrix",
    "Evan", "Amara", "Max", "Raegan", "Liam", "Genevieve", "Tyler"]

albom_name = ['Summer', 'Nudes', 'IvanZolo2004','TikTok', 'Folder1']
def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length)).replace("'", '').replace('"', '')
    return password

def generate_path(length):
    characters = string.ascii_letters + string.digits
    path = ''.join(random.choice(characters) for _ in range(length))+'.png'.replace("'", '').replace('"', '')
    return path 

