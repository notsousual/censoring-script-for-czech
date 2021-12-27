import requests, json, time, logging, copy

def get_morphodita(x):

    my_response = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/tag?data=" + str(x) + "&convert_tagset=pdt_to_conll2009&output=json")
    my_response.encoding = 'utf8'

    if my_response.ok:
        tagged = json.loads(my_response.text)
        tagged = tagged['result']
        return tagged

    else:
        time.sleep(2.0)
        my_response = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/tag?data=" + str(x) + "&convert_tagset=pdt_to_conll2009&output=json")
        my_response.encoding = 'utf8'
        if my_response.ok:
            tagged = json.loads(my_response.text)
            tagged = tagged['result']
            return tagged
        else:
            logging.warning('{}: {}'.format(my_response.status_code, my_response.reason))
            return

def is_offensive(my_sentences):
    offensive_list = []
    stop_list = {
    'pica',
    'kurva',
    'prdel',
    'curak',
    'hovno',
    'jebat', 
    'zmrd',
    'kokot',
    'teplous',
    'fuck',
    'chuj',
    'shit'
    }

    tagged = get_morphodita(my_sentences)
    lemma_compound = []
    tokens_compound = []
    if tagged:
        for sentence in tagged:
            for word in sentence:
                # print(tagged)
                lemma_compound.append(word['lemma'])

                try:
                    tokens_compound.append([word['token'], word['space']])
                except:
                    tokens_compound.append([word['token']])


        # print(tokens_compound)
        
        for word_index in range(len(lemma_compound)):

            my_response = requests.get('http://lindat.mff.cuni.cz/services/korektor/api/correct?data=' + lemma_compound[word_index] + '&input=horizontal&model=strip_diacritics')
            my_response.encoding = 'utf8'

            if my_response.ok:
                stripped = json.loads(my_response.text)
                stripped = stripped['result']

                if stripped.lower() in stop_list:
                    offensive_list.append(True)
                    stars = ''
                    for x in range(len(tokens_compound[word_index][0])):
                        stars += '*'
                    tokens_compound[word_index][0] = tokens_compound[word_index][0][0] + stars[1:-1] + tokens_compound[word_index][0][-1]
                    

                else:
                    offensive_list.append(False)
               

            else:
                time.sleep(2.0)
                my_response = requests.get('http://lindat.mff.cuni.cz/services/korektor/api/correct?data=' + word + '&input=horizontal&model=strip_diacritics')
                my_response.encoding = 'utf8'
                if my_response.ok:
                    stripped = json.loads(my_response.text)
                    stripped = stripped['result']

                    if stripped.lower() in stop_list:
                        offensive_list.append(True)

                    else:
                        offensive_list.append(False)
        
        print(offensive_list)

        if True in offensive_list:
            print('True, there is an offensive Czech word here!')
            final_string = ''
            for x in tokens_compound:
                for i in x:
                    final_string += i
            print(final_string)  
        
        if True not in offensive_list:
            print("False, there isn't an offensive Czech word here!")
            final_string = ''
            for x in tokens_compound:
                for i in x:
                    final_string += i
            print(final_string)  
        

is_offensive('Achjo. Kurva, ztratila jsem mobil.')