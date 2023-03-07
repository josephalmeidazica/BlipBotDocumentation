import json
import codecs
import write_utils

FILE_NAME = 'allcontentstest.json'

file = open(FILE_NAME,encoding="utf8")

outputFile = codecs.open("documentation.txt","a", "utf-8")

data = json.load(file)

#Write flow blocks
outputFile.write('## Flow: \n\n')

# For each block on flow
for id in data['flow']:
    try:
        #Write flow blocks
        if('desk' not in id):
            #Get current block and write its name, also add a HTML anchor to it
            currentBlock = data['flow'][id]
            outputFile.write(f"### <div id='{id}'> {currentBlock['$title']} </div>\n")

            #Write tags
            write_utils.write_tags(outputFile,currentBlock);

            # Write block content
            outputFile.write('1. #### Content: \n\n')
            for content in currentBlock['$contentActions'] :
                write_utils.write_contents(outputFile,content)

            #Write block redirects
            outputFile.write('2. #### Redirects: \n\n')

            #Write default output of a Block
            write_utils.write_default_output(data,outputFile,currentBlock)

            #Write output conditions of a block
            for condition in currentBlock['$conditionOutputs'] :
                write_utils.write_output_conditions(data,condition,outputFile,currentBlock)

            #Write block entering actions
            outputFile.write('3. #### Entering actions: \n\n')
            for action in currentBlock['$enteringCustomActions'] :
                write_utils.write_actions(outputFile,action)

            #Write block leaving actions
            outputFile.write('4. #### Leaving actions: \n\n')
            for action in currentBlock['$leavingCustomActions'] :
                write_utils.write_actions(outputFile,action)

        #Write attendance blocks
        else :
            currentBlock = data['flow'][id]
            outputFile.write(f"### <div id='{id}'> {currentBlock['$title']} </div>\n")
            #Write tags
            write_utils.write_tags(outputFile,currentBlock)
            #Write block redirects
            outputFile.write('1. #### Redirects: \n\n')

            #Write default output of a Block
            write_utils.write_default_output(data,outputFile,currentBlock)

            #Write output conditions of a block
            for condition in currentBlock['$conditionOutputs'] :
                write_utils.write_output_conditions(data,condition,outputFile,currentBlock)
    except Exception as e:
        print(f"Erro on block {id}")
        print(getattr(e, 'message'))

#Write Global Actions
outputFile.write('## Global actions: \n\n')

#Write entering global actions
outputFile.write('### Global Entering Actions: \n\n')
for action in  data['globalActions']['$enteringCustomActions'] :
    write_utils.write_actions(outputFile,action)

#Write leaving global actions
outputFile.write('### Global Leaving Actions: \n\n')
for action in  data['globalActions']['$leavingCustomActions'] :
    write_utils.write_actions(outputFile,action)

file.close()
outputFile.close()




