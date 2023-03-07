# Method to write to file content actions (user inputs and outputs)
def write_contents(outputFile,content):
    try :
        content = content['input']
        if((content['bypass']) is False) :
            try:
                outputFile.write(f"> {content['$cardContent']['document']['content']}\n")
            except:
                outputFile.write(f"> Entrada do usuário\n")
    except :
        if(content['action']['type'] == 'SendRawMessage') :
            content = content['action']['settings']
            outputFile.write(f"> Conteúdo dinâmico:  \n\n")
            outputFile.write(f" Type: {content['type']}  \n\n")
            message = content['rawContent'].replace('\n','')
            outputFile.write(f"` {message} `  \n\n")
        else:
            content = content['action']['settings']
            contentType = content['type']
            if(contentType == 'application/vnd.lime.chatstate+json') :
                outputFile.write(f"> Composing: \n\n")
                outputFile.write(f"` Composing por {content['content']['interval']/1000} segundos `\n\n")
            elif(contentType == 'text/plain'):
                outputFile.write(f"> Text Message: \n\n")
                message = content['content'].replace('\n','')
                outputFile.write(f"` {message} `  \n\n")
            elif(contentType == 'application/vnd.lime.select+json'):
                try:
                    quickReply = content['content']
                    getattr(quickReply['scope'])
                    outputFile.write(f"> Quick reply: \n\n")
                    outputFile.write(f"**Message**: ` {quickReply['text']} `\n\n")
                    outputFile.write(f"**Options:**\n\n")
                    options = quickReply['options']
                    for option in options :
                        outputFile.write(f"` {option['text']} `  \n\n")
                except :
                    outputFile.write(" > Menu: ")
                    menu = content['content']
                    outputFile.write(f"**{menu['text']}**\n\n<menu>")
                    for option in menu['options']:
                        outputFile.write(f"<li> {option['text']}</li>")
                    outputFile.write("</menu>\n\n")
            elif(contentType == 'application/vnd.lime.media-link+json'):
                media = content['content']
                if(media['type'] == 'image/jpeg'):
                    outputFile.write(f"> Image: \n\n")
                    outputFile.write(f"**Title**: ` {media['title']} `\n\n")
                    outputFile.write(f"**Subtitle**: ` {media['text']} `\n\n")
                    outputFile.write(f"**Type**: ` {media['type']} `\n\n")
                    outputFile.write(f"**Aspect Ratio**: ` {media['aspectRatio']} `\n\n")
                    outputFile.write(f"![Image]({media['uri']}) \n\n")
                else:
                    outputFile.write(f"> Media: \n\n")
                    outputFile.write(f"[Media]({media['uri']}) \n\n")
            elif(contentType == 'application/vnd.lime.collection+json'):
                outputFile.write(f"> Carrossel:  \n\n")
                carrossel = content['content']
                outputFile.write("|")
                for item in carrossel['items']:
                    outputFile.write(f"{item['header']['value']['title']} | ")
                outputFile.write("\n|")
                for item in carrossel['items']:
                    outputFile.write(f"-- | ")
                outputFile.write("\n|")
                for item in carrossel['items']:
                    outputFile.write(f"![Image]({item['header']['value']['uri']}) <br> <b>Title: </b>{item['header']['value']['title']}<br>")
                    outputFile.write(f"<b>Subtitle: </b>{item['header']['value']['text']} <br>")
                    outputFile.write(f"<br>Options:</br><br>")
                    for option in item['options']:
                        outputFile.write(f"`{option['label']['value']}`<br>")
                    outputFile.write("|")
                outputFile.write("\n\n")
            elif(contentType == 'application/vnd.lime.location+json'):
                outputFile.write("> Location:\n\n")
                outputFile.write(f"```\n\n{content}\n\n```\n\n")
            elif(contentType == 'application/vnd.lime.input+json'):
                outputFile.write("> Ask for location:\n\n")
                outputFile.write(f"**Button:** {content['content']['label']['value']}\n\n")
            elif(contentType == 'application/vnd.lime.web-link+json'):
                outputFile.write("> Web link:\n\n")
                link = content['content']
                outputFile.write(f"**Uri**: ` {link['uri']} `\n\n")
                outputFile.write(f"**Target**: ` {link['target']} `\n\n")
                outputFile.write(f"**Title**: ` {link['title']} `\n\n")
                outputFile.write(f"**Subtitle**: ` {link['text']} `\n\n")

# Method to write on file a block default output
def write_default_output(data,outputFile,currentBlock):
    defaultOutPut = currentBlock['$defaultOutput']['stateId']
    defaultOutputBlock = data['flow'][defaultOutPut]['$title']
    outputFile.write(f" - Default Output: <a href='#" + defaultOutPut + f"'> {defaultOutputBlock} </a> \n\n")

# Method to write on file a block output conditions
def write_output_conditions(data,condition,outputFile,currentBlock):
    try :
        targetBlock = data['flow'][condition['stateId']]['$title']
    except : targetBlock = [condition['stateId']]
    outputFile.write(f" - Go To: <a href='#" + condition['stateId'] + f"'> {targetBlock} </a>\n\n")
    parameters = condition['conditions']
    for parameter in parameters :
        outputFile.write(f"> Condition: {parameter['source']} {parameter['comparison']} {parameter['values']}    \n\n")

# Method to write on file blip actions
def write_actions(outputFile,action):
    outputFile.write(f" - **{action['$title']}**\n\n")
    outputFile.write(f"\t\t Type: {action['type']}\n\n")
    if(action['type'] == 'TrackEvent') :
        outputFile.write(f"> {action['settings']['category']}\n\n")
        outputFile.write(f"> {action['settings']['action']}\n\n")
    elif (action['type'] == 'SetVariable') :
        outputFile.write(f" >{action['settings']['variable']} **=** {action['settings']['value']}\n\n")
    elif (action['type'] == 'ExecuteScript') :
        outputFile.write(f" > Input: {action['settings']['inputVariables']}\n\n")
        outputFile.write("```\n\n")
        outputFile.write(f"{action['settings']['source']}\n")
        outputFile.write("```\n\n")
        outputFile.write(f" > Output: {action['settings']['outputVariable']}\n\n")
    elif (action['type'] == 'Redirect') :
        outputFile.write(f" > Context: {action['settings']['context']['type']} | {action['settings']['context']['value']}\n\n")
        outputFile.write(f" > Address: {action['settings']['address']}\n\n")
    elif (action['type'] == 'MergeContact'):
        outputFile.write("```\n\n")
        outputFile.write(f"{action['settings']}\n")
        outputFile.write("```\n\n")
    elif (action['type'] == 'ProcessHttp'):
        outputFile.write(f"> Headers: {action['settings']['headers']}\n\n")
        outputFile.write(f"> Method: {action['settings']['method']}\n\n")
        outputFile.write(f"> Uri: {action['settings']['uri']}\n\n")
        outputFile.write(f"> Response: {action['settings']['responseBodyVariable']}\n\n")
        outputFile.write(f"> Status: {action['settings']['responseStatusVariable']}\n\n")
    elif (action['type'] == 'ProcessContentAssistant'):
        outputFile.write(f"> Text: {action['settings']['text']}\n\n")
        outputFile.write(f"> Score: {action['settings']['score']}\n\n")
        outputFile.write(f"> Output: {action['settings']['outputVariable']}\n\n")
    elif (action['type'] == 'ProcessCommand'):
        outputFile.write(f"> To: {action['settings']['to']}\n\n")
        outputFile.write(f"> Method: {action['settings']['method']}\n\n")
        outputFile.write(f"> Uri: {action['settings']['uri']}\n\n")
        outputFile.write(f"> Variable: {action['settings']['variable']}\n\n")

# Method to write on file all tags on a block
def write_tags(outputFile,currentBlock):
    for tag in currentBlock['$tags'] :
        outputFile.write("<p style='background-color:"+ tag['background'] +"; border-radius: 25px;padding:5px'>"+ tag['label'] + "</p> \n\n")
