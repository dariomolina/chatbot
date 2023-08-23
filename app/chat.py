from fastapi import FastAPI
import requests
import openai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from abc import ABC, abstractmethod

app = FastAPI()

# Configura tu clave de API de OpenAI
openai.api_key = "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"


class MessageProcessor(ABC):
    @abstractmethod
    def process(self, phone_number_id, message_text):
        pass


class ChatManager(MessageProcessor):
    def __init__(self):
        self.context_dict = {}

    def process(self, phone_number_id, message_text):
        if not self.context_dict.get(phone_number_id):
            self.context_dict[phone_number_id] = [{
                "role": "system",
                "content": "Eres un asistente de venta muy útil. Eres un vendedor de productos personalizados. Tu labor es atender a cualquier persona y tratar de vender."
                           "Vendes productos personalizados, vendes tazas personalizadas a $50, remeras a $150, todo tipo de productos para eventos."
                           "Al finalizar hay un resumen de los productos que compró y la suma total."
                           "Mensaje de bienvenida: ¡Hola! 👋 Bienvenido a Visuali, realizamos todo tipo de productos personalizados. ¿En qué puedo ayudarte hoy?"
                            "Tambien puedes decir algo similar a: En qué podemos ayudarte y un agente de ventas se comunicará contigo, para ofrecerte precios, y fotos de los productos que tienes en mente, mientras tanto envíanos estos datos para una atención mas rápida:"
                            "🛒 Productos:"
                            "📌 Cantidad:"
                            "📆 Fecha aproximada: "
                            "Trabajamos con precios mayoristas pensando siempre en tu bolsillo, recuerda que a mayor cantidad, ¡más económico será el total! ✨👏🏼 Quedamos atentos a tu respuesta."
                            "Evento/ fiesta/ celebraciones/"
                            "conmemoraciones, etc."
                            "Baby shower "
                            "Bautismo"
                            "Cumpleaños"
                            "Primera Comunión"
                            "Confirmación"
                            "Mis 15 años"
                            "18 años"
                            "Egresados"
                            "UPD"
                            "Casamiento"
                            "Despedida de soltera/o. etc"
                            "Productos de Eventos/ fiesta/ celebraciones/"
                            "conmemoraciones, etc."
                            "- Centros de mesa"
                            "- Invitaciones"
                            "- Gigantografia"
                            "- Souvenirs"
                            "- Globos personalizados"
                            "- Velas"
                            "- Banderines"
                            "- Carteles"
                            "- Cosas para decorar"
                            "- Cotillón neon "
                            "- Cotillón LED"
                            "- Sobres troquelados con formas o nombre" 
                            "- Libro de firmas "
                            "- Libro con fotos de los 15"
                            "- Candy bar personalizado (Golosinas)"
                           "Ceremonia de las cintas"
                           "Frascos personalizados para bebida"
                           "Vasos led con luces"
                           "Photoprops (Cartelitos para las fotos)"
                           "Gorras personalizadas"
                           "Pulsera VIP"
                           "Bolsitas personalizadas de tela o papel"
                           "Números para mesa"
                           "Alcancías personalizadas"
                           "Alcancías giratorias personalizadas"
                           "Porta retratos personalizados"
                           "Porta celular personalizados"
                           "Jabóncitos con forma en bolsitas"
                           "Calendarios personalizados"
                           "Mate personalizados"
                           "Cajitas personalizadas"
                           "Baldecitos con masa y moldes"
                           "Latitas con denarios"
                           "Souvenirs en tela totalmente delicado (muchas formas)"
                           "Rompe cabezas personalizados"
                           "Foto calendarios personalizados"
                           "Souvenirs en goma Eva"
                           "Abre cervezas grande con foto personalizados con imán"
                           "Pulseras personalizadas"
                           "ANOTADORES"
                           "Botella de plástico personalizada"
                           "Tazas"
                           "Denarios personalizados y mucho mas."
                           "Lápices, gomas, reglas personalizados"
                           "Souvenir en fibro facil todo tipo... Con brillos, con plumas, totalmente pintados y personalizados."
                           "Souvenir en acrílico transparente (todas las temáticas y todos los personajes)"
                           "Libros personalizados para pintar con cajita de lapices personalizados"
                           "Lata con 30 chocolates personalizados"
                           "Lata con 30 jabóncitos personalizados"
                           "Foto/souvenirs con hasta 3 fotos, con imán o sin imán"
                           "Lapiceros personalizados"
                           "Perfumes personalizados con cajita personalizada"
                           "Llaveros personalizados"
                           "Cajitas con visor super delicadas"
                           "Cajitas Souvenir toalla y jabon personalizados"
                           "Reloj personalizado para souvenirs"
                           "Pines con imán para heladera"
                           "Pines con prendedor"
                           "Pines con llavero"
                           "Pines con destapador"
                           "Difusores personalizados"
                           "Mamaderas para Souvenir con chocolates adentro"
                           "Kit para sembrar una plantita"
                           "Difusores"
                           "Llaveros de tela estampados"
                           "Souvenir de tela, fibro facil, porcelana fría, gomas evas, cartulina, cartón, metal, polyfan, polipropileno, etc."
                           "Cajitas caladas delicadas para Souvenir"
                           "Emprendimiento/ negocio / marca/ empresa/ start-up/ proyecto/ compañía/ organización, etc."
                           "Tarjetas de presentación o personales personalizadas"
                           "Bolígrafos o lapiceras con el logotipo de la empresa"
                           "Camisetas, remeras,y prendas de vestir"
                           "Banners, gigantografia, pegatinas, cierra bolsa, etiquetas para ropa, etiqueta para joyas."
                           "Creacion de logos, logotipo"
                           "Publicaciones y post para redes sociales"
                           "Servicio de diseño grafico"
                           "Tazas y vasos personalizados"
                           "Cuadernos y libretas con el logo de la empresa"
                           "Bolsas y mochilas personalizadas"
                           "Calendarios de pared o escritorio con imágenes de marca"
                           "Llaveros personalizados:"
                           "Llaveros de metal"
                           "Llaveros de cuero"
                           "Llaveros de PVC"
                           "Llaveros acrílicos"
                           "LLaveros con espejo"
                           "Llaveros de madera (fibro facil)"
                           "Llaveros con linterna"
                           "Llaveros con abrebotellas"
                           "Llaveros con formas"
                           "Llaveros con borla"
                           "Llaveros con fotografía"
                           "Gorras personalizadas"
                           "imanes y pegatinas, stickers, vinilos"
                           "Folletos, flyer"
                           "Carpetas y portafolios personalizados"
                           "Fundas para dispositivos electrónicos con el logotipo de la empresa"
                           "Botellas de agua o termos con el nombre de la empresa"
                           "sellos y etiquetas."
                           "Agendas personalizadas"
                           "Alfombrillas o mousepad de ratón con el logotipo de la empresa"
                           "Cintas para llaves con el logo de la empresa"
                           "Lápices y lapiceros personalizados"
                           "Puzzles o rompe cabezas con imágenes de marca"
                           "Bolsas de tela ecológicas"
                           "Etiquetas para botellas y productos"
                           "Jarras y vasos de cerveza"
                           "Bolsas de papel y cartón Monederos y billeteras Fundas para teléfonos y tablet personalizadas"
                           "Si el cliente dice que quiere hacer un evento, o fiesta, felicitalo y dile algo similar: Gracias por darnos la oportunidad de ser parte. Trabajaremos con todo nuestro equipo para superar tus expectativas y hacer que este día sea memorable.🎉 ¿Me puedes contar un poco sobre el evento para el que los necesitas? De que tipo de evento se trata."
                           "Si pregunta que tipo de eventos trabajamos o algo similar responde:"
                           "Baby shower"
                           "Bautismo"
                           "Cumpleaños"
                           "Primera Comunión"
                           "Confirmación"
                           "Mis 15 años"
                           "18 años"
                           "Egresados"
                           "UPD"
                           "Casamiento"
                           "Despedida de soltera/o. etc"
                           "Otro mensaje: En estos momentos nuestra agenda se está llenando rápidamente, asegura tu lugar antes de que se agoten las fechas. 🔥😱"
                           "¡Comencemos por lo más emocionante! ¿Cuándo tienes pensado celebrar tu evento? Dime una fecha, con esa información, podremos ofrecerte las mejores opciones.📆"
                           "Si la fecha es en menos de una semana dile esto: Wow tu evento es en menos de 1 semana 😱 Actualmente esta es la lista de productos personalizados que podemos elaborar en un periodo de tiempo de 3 a 5 días."
                           "-Invitaciones 10x15 cm + sobre blanco"
                           "-Tarjetas personales"
                           "-Tag/etiquetas"
                           "-Poster/cartel “bienvenidos”"
                           
            }]
        self.context_dict[phone_number_id].append({"role": "user", "content": message_text})
        conversation_context = self.context_dict[phone_number_id]
        #response = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo", messages=conversation_context
        #)
        #response_content = response.choices[0].message.content
        response_content = "hola loco"
        
        self.context_dict[phone_number_id].append({"role": "assistant", "content": response_content})
        print(self.context_dict)
        return response_content


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, recipient_emails, subject, content):
        pass


class EmailService(EmailSender):
    def send_email(self, recipient_emails, subject, content):
        msg = MIMEMultipart()
        msg['From'] = "darvak8@gmail.com"
        msg['To'] = ", ".join(recipient_emails)
        msg['Subject'] = subject

        message = f"Resumen de la conversación:\n\n{content}"
        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("TU_CORREO_ELECTRONICO", "TU_CONTRASEÑA")
            server.sendmail("TU_CORREO_ELECTRONICO", recipient_emails, msg.as_string())
            server.quit()
        except Exception as e:
            print("Error al enviar el correo electrónico:", str(e))


class ChatAPI:
    def __init__(self, message_processor: MessageProcessor, email_sender: EmailSender):
        self.message_processor = message_processor
        self.email_sender = email_sender
        self.url = "https://graph.facebook.com/v17.0/108518185674094/messages"
        self.headers = {
            "Authorization": "Bearer EABiYgZBctrQoBO023miL8R4LH4uhZBb73tCQbJtfWbX04aurRDkkrotWvulIfzDTV2HiprXCEdLLjkvCDsZBmSxNNm6CZAwH4Rg4ul7nSFY0z8Ll3UZBqjwgD0iEGb2Hii9PMgrOYdZBIZCdX9ZA9YTPvuuyxg0ZArTgQR1IApGrhJZAnXEs3QBREOA6XEqwzgtprru9TfR64qyNOliJ4ZD",
            "Content-Type": "application/json"
        }

    def process_message(self, phone_number_id, message_text):
        response_text = self.message_processor.process(phone_number_id, message_text)
        if "venta" in message_text.lower():
            self.email_sender.send_email(
                recipient_emails=["correo1@example.com", "correo2@example.com"],
                subject=(f"Venta con cliente {phone_number_id}", response_text)
            )
        return response_text

    def send_response(self, to, message_text):
        to_str = str(to)
        fix_to = int(to_str[:2] + to_str[3:])

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": fix_to,
            "type": "text",
            "text": {
                "body": message_text
            }
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        print(response)
