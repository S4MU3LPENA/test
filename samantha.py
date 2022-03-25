from http import server
import smtplib
import ssl
import speech_recognition as sr
import pyttsx3
import pywhatkit
import urllib.request
import json
import datetime
import wikipedia
smtplib, ssl
import getpass

# name of the virtual assistant
name = 'samantha'

# your api key
key = 'YOUR_API_KEY_HERE'

# La bandera nos ayuda a cerrar el programa
flag = 1

#crear la conexion
context = ssl.create_default_context()

listener = sr.Recognizer()

engine = pyttsx3.init() # inicialisamos nuestro paquete


voices = engine.getProperty('voices') #traemos la lista de nuestras voces
engine.setProperty('voice', voices[3].id) # setiamos la propiedad voice en voices en la posicion 3 

# edición de la configuración predeterminada
engine. setProperty('rate', 178)
engine.setProperty('volume', 0.7)

def talk(text):
   
    # aqui el asistente virtual puede hablar
    
    engine.say(text)
    engine.runAndWait()

def listen():
   
    # El programa recupera nuestra voz y la envía a otra función
   
    flag = 1
    try:
        with sr.Microphone() as source:
            talk('Hola señor que decea, estoy a su orden')
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()
            
            if name in rec:
                rec = rec.replace(name, '')
                flag = run(rec)
            else:
                talk("Vuelve a intentarlo, no entendi que quisiste decir: " + rec)
    except:
        pass
    return flag

def run(rec):
    
        #Todas las acciones que puede hacer el asistente virtual
    
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        wikipedia.set_lang("es")
        info = wikipedia.summary(order, 1)
        talk(info)
    elif 'salir' in rec:
        flag = 0
        talk("Saliendo...")
    elif 'correo' in rec:
        username = input('Ingrese su correo electronico: ')
        password = input('ingrese su contraseña: ')

        with smtplib.SMTP_SSL("smtp@gmail.com", 465, context=context) as serer:
            server.login(username, password)
            talk("inicio sesion correctamente")
            destinatario = input("ingrese destinatario: ")
            mensaje = input("ingrese su mensaje: ")
            server.sendmail(username, destinatario, mensaje)
            talk('Mensaje enviado')
    else:
        talk("Vuelve a intentarlo, no reconozco lo que dices: " + rec)
    return flag

while flag:
    flag = listen()