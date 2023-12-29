from openai import OpenAI
import time, random
import keys

client = OpenAI(api_key=keys.openAIStuff['APIKey2'])   # for OpenAI API calls

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a Large Language Model providing next token predictions."},
#     {"role": "user", "content": "Say the phrase \"ChatGPT is a thing\""}
#   ],
#   max_tokens=1
# )

# print(completion.choices[0].message)



def getOAIChatCompletion(modelSelect, messageHistory, maxTokens):
    """
    Get Next Tokens Completion from 3.5-Turbo, 4, or 4.5-Turbo

    Parameters
    ----------
    modelSelect : {'3.5','4','4.5'}
        Choose your model.

    messageHistory : list of messages
        Should contain the system and user messages
    
    maxTokens : int
        Maximum number of tokens generated
    
    Returns
    -------
    response : str
        A string containing only the response to be appended
    """
    if (modelSelect == '3.5'):
        requestedModel = 'gpt-3.5-turbo'
    elif (modelSelect == '4'):
        requestedModel = 'gpt-4'
    elif (modelSelect == '4.5'):
        requestedModel = 'gpt-4-1106-preview'
    else:
        raise Exception(f"{modelSelect} is not a valid model. Please input either '3.5', '4', or '4.5'") 

    completion = client.chat.completions.create(
        model=requestedModel,
    messages=messageHistory,
    max_tokens=maxTokens)

    return(completion.choices[0].message.content)

def doWhatTomSevenSaid(prompt, exponentialDilution, dilutionProportion, iterations):
    """
    The actual loop

    Parameters
    ----------
    prompt : str
        The prompt that will be passed to the model

    exponetialDilution : bool
        if true, will dilute the original model by a factor of dilutionProportion
    
    dilutionProportion : float
        Proportion of original model (0.7 means 70% original model), or, if exponentialDilution == true, 2^dilutionProportion
    
    iterations : int
        temp way of making sure we don't go on forever, I should figure out some sort of end sequence

    Returns
    -------
    response : str
        A string containing only the response to be appended
    """

    templateInput=[
        {"role": "system", "content": "You are attempting to continue the assistant's message. Include a space at the beginning of all new words:"},
        {"role": "user", "content": f"{prompt}"},        
    ]

    curHistory = templateInput[:]

    responsePhrase = ""
    originalModel = '4'
    probabilityOfOG = 2**dilutionProportion if exponentialDilution else dilutionProportion 

    timesUsedModel = 0

    for i in range(1, iterations):

        curHistory = templateInput[:]+([{"role": "assistant", "content": f"{responsePhrase}"}])
        
        usedModel = '3.5' if random.random() >= probabilityOfOG else '4.5'
        print(usedModel)

        response = getOAIChatCompletion(usedModel,curHistory,1)
        
        responsePhrase += response

        # set new history, probably shouldn't reset it everytime but eh who cares ig
        


    return responsePhrase


print(doWhatTomSevenSaid("Spell the alphabet, continuing if you make a mistake",False,1,20))