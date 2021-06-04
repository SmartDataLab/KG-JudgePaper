#%%
import pandas as pd

with open("../data/wusong.csv") as f:
    data_list = f.readlines()
# %%
data_list[0]
# %%
import json

d = json.loads(data_list[0])
d
# %%
def get_text_list_from_one(d):
    text_list = []
    for p in d["paragraphs"]:
        tmp_text_list = [
            subp["text"]["text"] if type(subp["text"]) == dict else subp["text"]
            for subp in p["subParagraphs"]
        ]
        for tmp in tmp_text_list:
            text_list += [one["text"] if type(one) == dict else one for one in tmp]

    return text_list


".".join(get_text_list_from_one(d))

# %%
from ltp import LTP

ltp = LTP()  # 默认加载 Small 模型
#%%
sents_ex = [
    "被执行人：张远丰、何振彪、刘东、黎扬山、陆瑞权、邓忠会、王文爝、潘绍堂、农绍立、李明聪、官国春、潘绍宏、甘立奎、董泽琼、刘云祥、刘帅、林科辉、黄应军、吴纯杰。",
    "关于上列被执行人没收财产、罚金系列案，（2014）惠中法刑一初字第111号刑事判决书和（2015）粤高法刑一终字第42号刑事裁定书、（2012）惠中法刑二初字第37号刑事附带民事判决书和（2013）粤高法刑三终字第25号刑事判决书、（2012）惠中法刑二初字第55号刑事判决书、（2013）惠中法刑一初字第128号刑事判决书、（2012）惠中法刑二初字第9号刑事判决书和（2012）粤高法刑四终字第209号刑事裁定书、（2013）惠中法刑一初字第121号刑事判决书、（2013）惠中法刑一初字第73号刑事判决书和（2014）粤高法刑三复终第18号刑事裁定书、（2012）惠中法少刑初字第6号刑事判决书、（2011）惠中法少刑初字第11号刑事附带民事判决书、（2011）惠中法刑二初字第67号刑事附带民事判决书和（2012）粤高法刑四终字第176号刑事判决书已发生法律效力，本院刑一、刑二庭根据法律规定移送执行。",
    "本院认为，上述同类型的案件，已有批量在辖区惠东县人民法院执行，为提高执行效率，减少执行成本，宜指定该院集中执行。",
    "依照《中华人民共和国民事诉讼法》第一百五十四条第一款第（十一）项、《最高人民法院关于高级人民法院统一管理执行工作若干问题的规定》第十四条的规定，裁定如下：一、（2014）惠中法刑一初字第111号刑事判决书和（2015）粤高法刑一终字第42号刑事裁定书、（2012）惠中法刑二初字第37号刑事附带民事判决书和（2013）粤高法刑三终字第25号刑事判决书、（2012）惠中法刑二初字第55号刑事判决书、（2013）惠中法刑一初字第128号刑事判决书、（2012）惠中法刑二初字第9号刑事判决书和（2012）粤高法刑四终字第209号刑事裁定书、（2013）惠中法刑一初字第121号刑事判决书、（2013）惠中法刑一初字第73号刑事判决书和（2014）粤高法刑三复终第18号刑事裁定书、（2012）惠中法少刑初字第6号刑事判决书、（2011）惠中法少刑初字第11号刑事附带民事判决书、（2011）惠中法刑二初字第67号刑事附带民事判决书和（2012）粤高法刑四终字第176号刑事判决书中没收财产、罚金部分，指定惠东县人民法院执行。",
    "二、本院（2015）惠中法执字第325-334号案终结执行。",
    "三、指定执行文书由惠东县人民法院送达当事人。",
    "本裁定送达后立即生效。",
    "审判长林晓粤审判员张新建审判员邓庆东二〇一五年七月十三日书记员魏巧玲",
]
seg, hidden = ltp.seg(sents_ex)
#%%
pos = ltp.pos(hidden)
ner = ltp.ner(hidden)
srl = ltp.srl(hidden)
dep = ltp.dep(hidden)
sdp = ltp.sdp(hidden)
# %%
pos
# %%
ner
# %%
seg
# %%
srl
# %%
dep
# %%
sdp
# %%
demo_sents = ["夫妻感情不错", "夫妻感情日渐恶化", "现夫妻感情已经全破裂", "夫妻关系名存实亡"]
#%%
seg, hidden = ltp.seg(demo_sents)
sdp = ltp.sdp(hidden)
sdp
#%%
seg
#%%
pos = ltp.pos(hidden)
pos
#%%
seg
#%%
"夫妻关系名存实亡".split("，")
#%%


def get_triple_iterator(sent_list):
    seg, hidden = ltp.seg(sent_list)
    pos = ltp.pos(hidden)
    sdp = ltp.sdp(hidden)
    verb_types = ["Root", "eSUCC"]
    other_types = ["FEAT"]
    subject_types = ["AGT", "EXP"]
    object_types = ["PAT", "dCONT", "CONT", "DATV", "LINK"]
    for i, sent_sdp in enumerate(sdp):
        verb_list = [tuple_[0] for tuple_ in sent_sdp if tuple_[2] in verb_types]
        sent_triple_list = []
        a_list = [idx + 1 for idx, one in enumerate(pos[i]) if one in ["a", "v", "i"]]

        for a in a_list:
            n_sdp = [tuple_ for tuple_ in sent_sdp if tuple_[1] == a]
            for n_tuple in n_sdp:
                n_child_sdp = [tuple_ for tuple_ in sent_sdp if tuple_[1] == n_tuple[0]]
                for child_tuple in n_child_sdp:
                    if child_tuple[2] in other_types:
                        sent_triple_list += [
                            (
                                (
                                    seg[i][child_tuple[0] - 1],
                                    child_tuple[2],
                                ),
                                (
                                    seg[i][n_tuple[0] - 1],
                                    n_tuple[2],
                                ),
                                seg[i][a - 1],
                            )
                        ]

        for verb in set(verb_list):
            verb_sdp = [tuple_ for tuple_ in sent_sdp if tuple_[1] == verb]
            subject_list = []
            object_list = []
            for tuple_ in verb_sdp:
                subject_list += [tuple_] if tuple_[2] in subject_types else []
                object_list += [tuple_] if tuple_[2] in object_types else []
            if len(subject_list) > 0 and len(object_list) > 0:
                verb_src_word = seg[i][verb - 1]
                sent_triple_list += [
                    (
                        (
                            seg[i][sub_tuple[0] - 1],
                            sub_tuple[2],
                        ),
                        (
                            seg[i][obj_tuple[0] - 1],
                            obj_tuple[2],
                        ),
                        verb_src_word,
                    )
                    for sub_tuple in subject_list
                    for obj_tuple in object_list
                ]
        yield sent_triple_list


list(get_triple_iterator(demo_sents))
# %%
