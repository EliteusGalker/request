import socketio
import time
import re
from doit import join_inputs
from upload import upload_file

import threading

sio = socketio.Client()


#lista rozpoznawanych spraw DICTONARÓW z danymi

list_of_dicts = []

# blokada, żeby litsta nie została zjeabana jak dwa thredy na raz by chciały coś robić
list_lock = threading.Lock()

# info dla thredów, że dodano nowe info
data_added = threading.Event()

busy_event = threading.Event()

def connection():
    @sio.on('message')
    def on_message(data):
        
        name = data.get('name', 'Unknown') # tego się chyba trzeba będzie pozbyć, jakby w nicu coś dał jak % czy ^
        message = data.get('message', '')
        print(f"{name}: {message}")
        roomSearch = re.search(r'\*(.*?)\*', message)
        
        if roomSearch:
            room = roomSearch.group(1)
            if room != "4441":
                print("New Room:", room)
                
                message1 = {"name": "2_Bartek", "message": f"elo420#{room}#"}
                sio.emit('message', message1)
        else:
            #szukanie czy ktoś wpisał info
            if "%" in message:
                print("jest %")
                substrings = message.split(", ")
                print(substrings)
                email = substrings[0].replace("%", "")
                znak = substrings[1].replace("%", "")
                numer = substrings[2].replace("%", "")
                umowa = substrings[3].replace("%", "")
                room = substrings[4].replace("@", "")
                print(room, email, znak, numer, umowa)
                
                message2 = {"name": "2_Bartek", "message": f"jestem#{room}#"}
                sio.emit('message', message2)


                
                #dodawanie do kolejki jak prześle info 
                dynamic_dict = {
                    'email': email,
                    'znak': znak,
                    'numer': numer,
                    'umowa': umowa,
                    'room': room
                }
                with list_lock:
                    list_of_dicts.append(dynamic_dict)
                    kolejka = len(list_of_dicts) - 1
                    message3 = {"name": "2_Bartek", "message": f"KOLEJKA(({kolejka}))#{room}#"}
                    sio.emit('message', message3)

                    
                data_added.set()

                
                for index, item in enumerate(list_of_dicts):
                    room_name = item['room']
                    print(f"Index {index}: {room_name}")
                    
                #usuwanie z kolejki jak wyjdzie delikwent wcześniej
            else:
                if "^" in message:
                    pattern = r'\^(.*?)\^'
                    match = re.search(pattern, message)
                    last_occurrence = match.group(1)
                    print("usuwanie" + last_occurrence)
                    with list_lock:
                        for item in list_of_dicts:
                            if item.get('room') == last_occurrence:
                                list_of_dicts.remove(item)

                    # Print the updated list of dictionaries
                    for index, item in enumerate(list_of_dicts):
                        room_name = item['room']
                        print(f"Index {index}: {room_name}")

                else:
                    print("No Room found in the string.")

    @sio.on('connect')
    def on_connect():
        print('Connected to chatroom')
        time.sleep(2)
        message1 = {"name": "2_Bartek", "message": "elo420"} 
        sio.emit('message', message1)

    @sio.on('disconnect')
    def on_disconnect():
        print('Disconnected from chatroom')



    headers = {'auth': "12345", 'room': '4441', 'name': '2_Bartek'}


    print(headers)

    # Replace 'https://chatroom-website-url.com' with the actual URL of the chatroom
    sio.connect('http://127.0.0.1:5000', headers=headers)

    sio.wait()


def process(sio):
    while True:
        time.sleep(1)
        print("Thread One is waiting for a notification.")
        data_added.wait()
        busy_event.set()
        time.sleep(1)
        print("PROCCESS WYKRYŁXDD")
        with list_lock:
            now = list_of_dicts[0]
            print(now)
        time.sleep(10)
        sio.emit('message', {"name": "2_Bartek", "message": f"HHTP XD XD XD #{now['room']}#"}) # koniec roboty
        room = now['room']
        upload_file(room)
        print("HHTP XD XD XD")
        with list_lock:
            for item in list_of_dicts:
                if item.get('room') == room:
                    list_of_dicts.remove(item)
            if list_of_dicts:
                for index, item in enumerate(list_of_dicts):
                    room = item.get('room')
                    message3 = {"name": "2_Bartek", "message": f"KOLEJKA({index})#{room}#"}
                    print(message3)
                    sio.emit('message', message3)
                    
            if not list_of_dicts:
                print("Brak Zadań, clearing the event.")
                data_added.clear()  # Clear the event if the list is empty          
        busy_event.clear()




Connectthread = threading.Thread(target=connection)
Connectthread.daemon = True
Processthread = threading.Thread(target=process, kwargs={"sio": sio})
Processthread.daemon = True

Connectthread.start()
Processthread.start()
