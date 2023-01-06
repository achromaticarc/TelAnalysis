import json, jmespath, nltk_analyse,utils, time
from pywebio import input, config
from pywebio.output import put_html,put_text,put_image, put_button, put_code, clear, put_file
from pywebio.input import file_upload as file
from pywebio.session import run_js
from wordcloud import WordCloud
import matplotlib.pyplot as plt
def channel(filename):
    filename = filename.split(".")[0]
    filename = filename.split("/")[1]
    with open(f'asset/{filename}.json', 'r', encoding='utf-8') as f:
        text_list = list()
        #f = f.readlines()
        jsondata = json.load(f)
        name_channel = jmespath.search('name',jsondata)
        put_html(f"<center><h1>{name_channel}</h1><center>")
        messages_find = jmespath.search('messages[*].text',jsondata)
        #print(*messages_find, sep='\n\n-')
        for message in messages_find:
            if str(type(message)) == "<class 'list'>":
                #print(message)
                len_message = len(message)
                for mes in message:
                    # print(mes)
                    try:
                        text = jmespath.search('text',mes)
                        if text is None:
                            mes = utils.remove_emojis(mes)
                            text_list.append(mes)
                        else:
                            text = utils.remove_emojis(text)
                            text_list.append(text)
                            
                    except:
                        mes = utils.remove_emojis(mes)
                        text_list.append(mes)
                        #print(mes)
            else:
                message = message.replace("   "," ").replace("\n","").replace("\t","").strip()
                if len(message) > 4:
                    message = utils.remove_emojis(message)
                    text_list.append(message)
        #print(len(text_list))
        fdist, tokens = nltk_analyse.analyse(text_list, 100)
        all_tokens = list()
        #print(tokens)
        for token in tokens:
            all_tokens.append(token)
            #print(token)
        #print(len(all_tokens))
        all_tokens, data = nltk_analyse.analyse_all(all_tokens, 100)
        #print(all_tokens)
        text_raw = " ".join(data)
        #max_wordss = (10 / 100) * len(data)
        wordcloud = WordCloud().generate(text_raw)
        filename_path = f'asset/{filename}_wordcloud.png'
        wordcloud = wordcloud.to_image()
        wordcloud.save(filename_path)
        img = open(filename_path,'rb').read()
        time.sleep(2)
        put_text("Wordcloud[100]:")
        put_image(img, width='600px')
        put_text(f"\nCount of all tokens: {len(tokens)}")
        put_text("\nСhannel frequency analysis[100]:")
        for i in all_tokens:
            try:
                m = m = f'  {i[0]} - {i[1]}'
                put_code(m)
            except Exception as ex:
                put_text(f"error #7 {ex}")
                pass