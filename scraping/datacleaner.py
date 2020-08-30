def num_there(s):
    return any(i.isdigit() for i in s)


def sentence_eraser(plaintext):
    sentence_with_number_index = []
    numberExists = False
    plaintextlist = plaintext.replace('\n', '').split('。')
    plaintext = ''
    for i in range(len(plaintextlist)):
        if num_there(plaintextlist[i]):
            sentence_with_number_index.append(i)
    number = 0
    for i in sentence_with_number_index:
        plaintextlist.pop(i - number)
        number = number + 1
    for i in plaintextlist:
        if len(i) > 0:
            plaintext = plaintext + i + '。'
    return plaintext
# coding=gbk


def wiki_dataset_cleaner(plaintext):
    for i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣•〃「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏?aeiouvüāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜAEIOUVÜĀĒĪŌŪǕÁÉÍÓÚǗǍĚǏǑǓǙÀÈÌÒÙǛ"#$%&\'()*+,-/:;<=>@[]^_`{|}~".!?ê█■':
        else:
            plaintext = plaintext.replace(i, "")

    return plaintext.replace(" ", "")

    """ for some reason 顏色指引????????劇集????????
    綜藝脫口騷節目????????紀錄片專題片????????選騷音樂節目????????
    真人騷節目????????文化社科節目????????生活服務節目註標嘅節目湖南衛視擁有完整版權。
    註標的節目湖南衛視擁有完整版權。以下劇目喺網絡平台全部由芒果全網獨播。 
    does not get filtered

    additional symbols not accounted for:
    ∈\\^∈\\^τ∈\\\\×\\^\\ and occasionally japanese

    english question marks keep appearing

    &nbsp; - denotes color

    """


dataFile = open("raw_training_data.txt", "r", encoding="utf-8")
newFile = open("training_data.txt", "w", encoding="utf-8")
plaintext = dataFile.read()
newFile.write(wiki_dataset_cleaner(sentence_eraser(plaintext)))

dataFile.close()
newFile.close()
