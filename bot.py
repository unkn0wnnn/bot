import keyboard
from PIL import ImageGrab,Image
import pytesseract
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError
import time
import csv

#Define the region to be captured (left, upper, right, lower)
box = (0, 50, 650, 530)

wait = False

bot_token = "<your bot token>"
screenshot = ImageGrab.grab(bbox=box)
image_path = 'path to file'


def send_message(chat_id,d_id):
    c_id = str(chat_id)
    try:
        bot = Bot(token=bot_token)
        with open(image_path, 'rb') as f:
            media = InputMediaPhoto(f)
            bot.send_media_group(chat_id=c_id, media=[media])
            print(f'''[*] Image Sent Successfully
Dairy id : {d_id}
Chat id  : {c_id}''')
            
    except TelegramError as e:
        print(f'Error sending image: {e}')

def csv_data():
    rows = []
    col1 = []
    col2 = []
    # open the CSV file
    with open('Id list.csv', 'r') as csvfile:
        # create a reader object
        csvreader = csv.reader(csvfile)
        # iterate through each row in the CSV file
        for row in csvreader:
            # add the row to the rows list
            rows.append(row)
            # add the column
            try:
                col1.append(row[0])
                col2.append(row[1])
            except:
                print("Error got but its okay !!")
    return([col1,col2])

def extract_chatid(u_id):
    csvdata = csv_data()
    d_id_list = csvdata[0][1:]
    c_id_list = csvdata[-1][1:]

    for i in range(len(d_id_list)):
        if int(d_id_list[i]) == u_id:
            return c_id_list[i]
    return "Not Found"        



def extract_id():
    # Set the path of the image file
    img_path = image_path

    # Open the image file
    img = Image.open(img_path)

    #crop the image for specific part
    img = img.crop((163,160,295,200))

    # Convert the image to grayscale
    img = img.convert('L')

    # Use Tesseract library to perform OCR recognition
    text = pytesseract.image_to_string(img)

    # Print the recognized text
    try:
        d_id = int(text)
    except:
        print("Invalid ID")
        return ["Not Found",0]

    chat_id = extract_chatid(d_id)
    
    return [chat_id,d_id]




id_data = extract_id()
chat_id = id_data[0]
d_id = id_data[1]

if chat_id != "Not Found":
    send_message(chat_id,d_id)
else:
    print("[*]ID not found !")




                
def take_ss():
    global screenshot
    screenshot = ImageGrab.grab(bbox=box)

def save_img():
    screenshot.save("screenshot.png")
    print("[*] image saved")




def on_key_event(event):
    if event.event_type == 'down':
        if event.name == "+":
            save_img()
            id_data = extract_id()
            chat_id = id_data[0]
            d_id = id_data[1]
            
            if chat_id != "Not Found":
                send_message(chat_id,d_id)
            else:
                print("[*]ID not found !")
        
keyboard.on_press(on_key_event)
keyboard.wait() 


while True:
    take_ss()




