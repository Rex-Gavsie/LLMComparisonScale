from openai import OpenAI
import time, random, json
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

def getOAINormalCompletion(intendedModel, messagePrompt, maxTokens):
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
   
    completion = client.completions.create(
        model=intendedModel,
    prompt=messagePrompt,
    max_tokens=maxTokens,
    temperature=0)

    return(completion.choices[0].text)

def doWhatTomSevenSaidChatCompletions(prompt, exponentialDilution, dilutionProportion, iterations):
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
        {"role": "user", "content": f"{prompt}"},   
    ]

    curHistory = templateInput[:]

    responsePhrase = ""
    originalModel = '4'
    probabilityOfOG = (1/2)**dilutionProportion if exponentialDilution else dilutionProportion 

    timesUsedModel = 0

    for i in range(1, iterations):

        curHistory = templateInput[:]+([{"role": "user", "content": f"Continue directly from here: {responsePhrase}"}])
        
        usedModel = '3.5' if random.random() >= probabilityOfOG else '4.5'
        # print(usedModel)

        response = getOAIChatCompletion(usedModel,curHistory,2) + " "
        
        responsePhrase += response

        # set new history, probably shouldn't reset it everytime but eh who cares ig
        


    return responsePhrase

def doWhatTomSevenSaidNormalCompletions(prompt, exponentialDilution, dilutionProportion, iterations, maxTokens) -> str:
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

    maxTokens : int
        max number of tokens generated

    Returns
    -------
    response : str
        A string containing the response
    """

    templatePrompt=f"{prompt}\n\n"

    responsePhrase = ""
    originalModel = 'gpt-3.5-turbo-instruct'
    probabilityOfOG = (1/2)**dilutionProportion if exponentialDilution else dilutionProportion 

    timesUsedModel = 0

    for i in range(0, iterations):
        
        usedModel = 'davinci-002' if random.random() >= probabilityOfOG else originalModel
        # print(usedModel)

        response = getOAINormalCompletion(usedModel,templatePrompt,maxTokens)
        # print(response)
        
        templatePrompt += response
        responsePhrase += response
        # set new history, probably shouldn't reset it everytime but eh who cares ig

    return responsePhrase



# print(doWhatTomSevenSaidNormalCompletions("Write a python script to print 1 to 100",False,1,50,1))

def gpt45TurboCheckOurWork(instruction, response):
    """
    Checking our work with gpt 4.5-turbo

    Parameters
    ----------
    instruction : str
        The given instruction

    response : str
        The generated response
    
    Returns
    -------
    doesItWork : bool
        A boolean representing whether the response would work
    """
    
    template = [
        {"role": "system", "content": "You evaluate whether an input followed an instruction. You output a boolean in JSON with the format \{'result': <Insert Result>\}"},
        {"role": "user", "content": f"Instruction:\n{instruction}\n\nResponse:\n{response}"}
    ]
    
    completion = client.chat.completions.create(
        model='gpt-4-1106-preview',
        response_format={"type": "json_object"},
        messages = template,
        temperature=0
    )

    try:
        doesItWork = json.loads(completion.choices[0].message.content)['result']
    except:
        completion = client.chat.completions.create(
            model='gpt-4-1106-preview',
            response_format={"type": "json_object"},
            messages = template,
            temperature=0
        )
        doesItWork = json.loads(completion.choices[0].message.content)['result']
    
    return(doesItWork)

# print(gpt45TurboCheckOurWork("Write a python script to print 1 to 100","for i in range(1, 101):\n print(i)"))

def calculateSuccessRate(instruction, numTests, exponetialDilution, dilutionProportion, callsPerTest, maxTokensPerGeneration):
    """
    A function that calculates the success rate for a given test, dilution, etc.

    Parameters
    ----------
    instruction : str
        The instruction given to the model

    exponetialDilution : bool
        if true, will dilute the original model by 2 raised to dilutionProportion
    
    dilutionProportion : float
        Proportion of original model (0.7 means 70% original model), or, if exponentialDilution == true, 2^dilutionProportion
    
    callsPerTest : int
        how many times we ask the LLM for a response

    maxTokensPerGeneration : int
        max number of tokens generated per response

    Returns
    -------
    sucessProportion : float
        A float representing the proportion of sucessful attempts
    """

    countOfSucesses = 0

    for i in range (0,numTests):
        response = doWhatTomSevenSaidNormalCompletions(instruction, exponetialDilution, dilutionProportion, callsPerTest, maxTokensPerGeneration)
        success = gpt45TurboCheckOurWork(instruction, response)

        countOfSucesses += 1 if success else 0
    
    return(countOfSucesses/numTests)

# print(calculateSuccessRate("Write a python script to print 1 to 100", 5, False, 1, 15, 1))