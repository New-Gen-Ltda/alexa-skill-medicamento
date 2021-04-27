# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging 
import ask_sdk_core.utils as ask_utils
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput


from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ("Olá, como vai? Bem vindo ao programa que irá ajudar você a controlar seus remédios! deseja abrir o menu? Caso contrário informe o comando desejado.")
        ask = ("Huuummm não entendi")
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(ask)
                .response
        )

class ListaMedicamentosIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AbrirListaMedicamentosIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #slots = handler_input.request_envelope.request.intent.slots
        #nomeRemedio = slots["nomeRemedio"].value
        speak_output = _("Os medicamentos cadastrados são: {nomeRemedio} ")

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
    
class AtualizarMedicamentosIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AtualizarMedicamentos")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        nomeRemedio = slots["nomeRemedio"].value
        atualizarHorario = slots["atualizarHorario"].value
        atualizarDescricao = slots["atualizarDescricao"].value
        
        attr = handler_input.attributes_manager.persistent_attributes
        nomeRemedio_2 = attr['nomeRemedio']
        horarioRemedio_2 = attr['horarioRemedio'] # month is a string, and we need to convert it to a month index later
        descRemedio_2 = attr['descRemedio']
            # speak_output = 'Thanks, I will remember that you were born {month} {day} {year}.'.format(month=month, day=day, year=year)

        attributes_manager = handler_input.attributes_manager
        lista_1 = nomeRemedio_2
        lista_2 = horarioRemedio_2
        lista_3 = descRemedio_2
        
        x = -1
        while(x<len(lista_1)):
            x+=1
            if(lista_1[x] == nomeRemedio):
                break
        
        lista_2.pop(x)
        lista_3.pop(x)
        lista_2.insert(x,atualizarHorario)
        lista_3.insert(x,atualizarDescricao)
        
        remedio_attributes_2 = {
            "nomeRemedio": lista_1,
            "horarioRemedio": lista_2,
            "descRemedio": lista_3
        }
        
        attributes_manager.persistent_attributes = remedio_attributes_2
        attributes_manager.save_persistent_attributes()

        # type: (HandlerInput) -> Response
        #slots = handler_input.request_envelope.request.intent.slots
        #nomeRemedio = slots["nomeRemedio"].value
        speak_output = "O medicamento {nomeRemedio} agora tem horário de {atualizarHorario} e descrição de {atualizarDescricao}".format(nomeRemedio=nomeRemedio, atualizarHorario=atualizarHorario, atualizarDescricao=atualizarDescricao)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
    
class HasMedicamentoLaunchRequestHandler(AbstractRequestHandler):
    """Handler for launch after they have set their birthday"""

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("nomeRemedio" in attr and "horarioRemedio" in attr and "descRemedio" in attr)

        return attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        nomeRemedio = attr['nomeRemedio']
        horarioRemedio = attr['horarioRemedio'] # month is a string, and we need to convert it to a month index later
        descRemedio = attr['descRemedio']

        # TODO:: Use the settings API to get current date and then compute how many days until user's bday
        # TODO:: Say happy birthday on the user's birthday

        speak_output = "Bem vindo! O medicamento {nomeRemedio} com horário às {horarioRemedio} e descrição {descRemedio} já está cadastrado!".format(nomeRemedio=nomeRemedio, horarioRemedio=horarioRemedio, descRemedio=descRemedio)
        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response

class CadastrarMedicamentoIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CadastrarMedicamentoIntent")(handler_input) 


    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        nomeRemedio = slots["nomeRemedio"].value
        horarioRemedio = slots["horarioRemedio"].value
        descRemedio = slots["descRemedio"].value
        
        attr = handler_input.attributes_manager.persistent_attributes
        nomeRemedio_2 = attr['nomeRemedio']
        horarioRemedio_2 = attr['horarioRemedio'] # month is a string, and we need to convert it to a month index later
        descRemedio_2 = attr['descRemedio']
            # speak_output = 'Thanks, I will remember that you were born {month} {day} {year}.'.format(month=month, day=day, year=year)

        attributes_manager = handler_input.attributes_manager

        remedio_attributes = {
            "nomeRemedio": nomeRemedio,
            "horarioRemedio": horarioRemedio,
            "descRemedio": descRemedio
        }
        
        lista_1 = nomeRemedio_2
        lista_2 = horarioRemedio_2
        lista_3 = descRemedio_2
        
        lista_1.append(nomeRemedio) 
        lista_2.append(horarioRemedio)
        lista_3.append(descRemedio)
        
        remedio_attributes_2 = {
            "nomeRemedio": lista_1,
            "horarioRemedio": lista_2,
            "descRemedio": lista_3
        }
        
        attributes_manager.persistent_attributes = remedio_attributes_2
        attributes_manager.save_persistent_attributes()

        speak_output = "O medicamento {nomeRemedio} com horário às {horarioRemedio} e descrição {descRemedio} foi cadastrado com sucesso!".format(nomeRemedio=nomeRemedio, horarioRemedio=horarioRemedio, descRemedio=descRemedio)


        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
    
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = _("You can say hello to me! How can I help?")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = _("Goodbye!")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = _("Hmm, I'm not sure. You can say Hello or Help. What would you like to do?")
        reprompt = _("I didn't catch that. What can I help you with?")

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = _("Sorry, I had trouble doing what you asked. Please try again.")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


#sb = SkillBuilder()
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

#sb.add_request_handler(HasMedicamentoLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
# sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(CadastrarMedicamentoIntentHandler())
sb.add_request_handler(ListaMedicamentosIntentHandler())
sb.add_request_handler(AtualizarMedicamentosIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()