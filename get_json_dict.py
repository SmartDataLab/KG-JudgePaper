#%%
import json
from causality_extract import test, CausalityExractor
from tqdm import tqdm

#%%
with open("data/wusong_demo.csv") as f:
    data_list = f.readlines()
#%%
content = "被执行人：张远丰、何振彪、刘东、黎扬山、陆瑞权、邓忠会、王文爝、潘绍堂、农绍立、李明聪、官国春、潘绍宏、甘立奎、董泽琼、刘云祥、刘帅、林科辉、黄应军、吴纯杰。关于上列被执行人没收财产、罚金系列案，（2014）惠中法刑一初字第111号刑事判决书和（2015）粤高法刑一终字第42号刑事裁定书、（2012）惠中法刑二初字第37号刑事附带民事判决书和（2013）粤高法刑三终字第25号刑事判决书、（2012）惠中法刑二初字第55号刑事判决书、（2013）惠中法刑一初字第128号刑事判决书、（2012）惠中法刑二初字第9号刑事判决书和（2012）粤高法刑四终字第209号刑事裁定书、（2013）惠中法刑一初字第121号刑事判决书、（2013）惠中法刑一初字第73号刑事判决书和（2014）粤高法刑三复终第18号刑事裁定书、（2012）惠中法少刑初字第6号刑事判决书、（2011）惠中法少刑初字第11号刑事附带民事判决书、（2011）惠中法刑二初字第67号刑事附带民事判决书和（2012）粤高法刑四终字第176号刑事判决书已发生法律效力，本院刑一、刑二庭根据法律规定移送执行。本院认为，上述同类型的案件，已有批量在辖区惠东县人民法院执行，为提高执行效率，减少执行成本，宜指定该院集中执行。依照《中华人民共和国民事诉讼法》第一百五十四条第一款第（十一）项、《最高人民法院关于高级人民法院统一管理执行工作若干问题的规定》第十四条的规定，裁定如下：一、（2014）惠中法刑一初字第111号刑事判决书和（2015）粤高法刑一终字第42号刑事裁定书、（2012）惠中法刑二初字第37号刑事附带民事判决书和（2013）粤高法刑三终字第25号刑事判决书、（2012）惠中法刑二初字第55号刑事判决书、（2013）惠中法刑一初字第128号刑事判决书、（2012）惠中法刑二初字第9号刑事判决书和（2012）粤高法刑四终字第209号刑事裁定书、（2013）惠中法刑一初字第121号刑事判决书、（2013）惠中法刑一初字第73号刑事判决书和（2014）粤高法刑三复终第18号刑事裁定书、（2012）惠中法少刑初字第6号刑事判决书、（2011）惠中法少刑初字第11号刑事附带民事判决书、（2011）惠中法刑二初字第67号刑事附带民事判决书和（2012）粤高法刑四终字第176号刑事判决书中没收财产、罚金部分，指定惠东县人民法院执行。二、本院（2015）惠中法执字第325-334号案终结执行。三、指定执行文书由惠东县人民法院送达当事人。本裁定送达后立即生效。审判长林晓粤审判员张新建审判员邓庆东二〇一五年七月十三日书记员魏巧玲"
extractor = CausalityExractor()
datas = extractor.extract_main(content)
#%%
cause_src_list = [
    "".join(
        [word.split("/")[0] for word in data["cause"].split(" ") if word.split("/")[0]]
    )
    for data in datas
]
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


json_dict_list = []
e_list = []
for data in tqdm(data_list[:1000]):
    d = json.loads(data)
    content = "".join(get_text_list_from_one(d))
    print(content)
    res = test(content)
    res["content"] = content
    res["title"] = d["title"]
    res["keywords"] = d["keywords"] if "keywords" in d.keys() else []
    json_dict_list.append(res)
# %%
import pickle

pickle.dump(json_dict_list, open("data/json_dict_list_v3.pk", "wb"))

#%%

import pickle
from collections import Counter

d_list = pickle.load(open("data/json_dict_list_v3.pk", "rb"))
# %%
# create event map based on the frequency

keywords_cnt = Counter()
object_cnt = Counter()
action_cnt = Counter()

for d in d_list:
    for keyword in d["keywords"]:
        keywords_cnt[keyword] += 1
    for one_list in d["cause_triple3"]:
        for triple_ in one_list:
            object_cnt[triple_[0][0]] += 1
            object_cnt[triple_[1][0]] += 1
            action_cnt[triple_[2]] += 1
    for one_list in d["effect_triples"]:
        for triple_ in one_list:
            object_cnt[triple_[0][0]] += 1
            object_cnt[triple_[1][0]] += 1
            action_cnt[triple_[2]] += 1
keywords_order = [
    one[0] for one in sorted(keywords_cnt.items(), key=lambda x: x[1], reverse=True)
]
object_order = [
    one[0] for one in sorted(object_cnt.items(), key=lambda x: x[1], reverse=True)
]
action_order = [
    one[0] for one in sorted(action_cnt.items(), key=lambda x: x[1], reverse=True)
]
keywords_order
#%%
keywords2order = dict(zip(keywords_order, range(len(keywords_order))))
object2order = dict(zip(object_order, range(len(object_order))))
action2order = dict(zip(action_order, range(len(action_order))))
# %%
has_keyword = []
has_fact = []
has_object = []
cause = []
do = []
effect = []
case_order = []
fact_order = []
for d in d_list:
    case_order += [d["title"]]
    has_keyword += [
        (len(case_order) - 1, keywords2order[keyword]) for keyword in d["keywords"]
    ]
    for i, (cause_src, effect_src) in enumerate(
        zip(d["cause_src_list"], d["effect_src_list"])
    ):
        fact_order += [cause_src, effect_src]
        has_fact += [
            (len(case_order) - 1, len(fact_order) - 2),
            (len(case_order) - 1, len(fact_order) - 1),
        ]
        cause += [(len(fact_order) - 2, len(fact_order) - 1, d["tags"][i])]
        for triple_ in d["cause_triple3"][i]:
            sub_idx = object2order[triple_[0][0]]
            obj_idx = object2order[triple_[0][0]]
            action_idx = action2order[triple_[2]]
            has_object += [
                (len(fact_order) - 2, sub_idx),
                (len(fact_order) - 2, obj_idx),
            ]
            do += [(sub_idx, action_idx)]
            effect += [(action_idx, obj_idx)]
        for triple_ in d["effect_triples"][i]:
            sub_idx = object2order[triple_[0][0]]
            obj_idx = object2order[triple_[0][0]]
            action_idx = action2order[triple_[2]]
            has_object += [
                (len(fact_order) - 1, sub_idx),
                (len(fact_order) - 1, obj_idx),
            ]
            do += [(sub_idx, action_idx)]
            effect += [(action_idx, obj_idx)]

# %%
# entities save as csv
folder_path = "neo4j_csv/"
with open(folder_path + "keywords.csv", "w") as f:
    f.writelines(
        ["k_id,keyword\n"]
        + [
            "%s,%s\n" % (i, keyword.replace(",", "，"))
            for i, keyword in enumerate(keywords_order)
        ]
    )

# %%
with open(folder_path + "case.csv", "w") as f:
    f.writelines(
        ["c_id,case\n"]
        + ["%s,%s\n" % (i, case.replace(",", "，")) for i, case in enumerate(case_order)]
    )
with open(folder_path + "fact.csv", "w") as f:
    f.writelines(
        ["f_id,fact\n"]
        + ["%s,%s\n" % (i, fact.replace(",", "，")) for i, fact in enumerate(fact_order)]
    )
with open(folder_path + "object.csv", "w") as f:
    f.writelines(
        ["o_id,object\n"]
        + [
            "%s,%s\n" % (i, object_.replace(",", "，"))
            for i, object_ in enumerate(object_order)
        ]
    )
with open(folder_path + "action.csv", "w") as f:
    f.writelines(
        ["a_id,action\n"]
        + [
            "%s,%s\n" % (i, action.replace(",", "，"))
            for i, action in enumerate(action_order)
        ]
    )
#%%

# %%
# save relation link
with open(folder_path + "has_keyword.csv", "w") as f:
    f.writelines(["c_id,k_id\n"] + ["%s,%s\n" % (i, j) for i, j in has_keyword])

# %%
with open(folder_path + "has_fact.csv", "w") as f:
    f.writelines(["c_id,f_id\n"] + ["%s,%s\n" % (i, j) for i, j in has_fact])

with open(folder_path + "cause.csv", "w") as f:
    f.writelines(
        ["f_id1,f_id2,tag\n"] + ["%s,%s,%s\n" % (i, j, tag) for i, j, tag in cause]
    )
#%%
with open(folder_path + "do.csv", "w") as f:
    f.writelines(["o_id,a_id\n"] + ["%s,%s\n" % (i, j) for i, j in set(do)])
with open(folder_path + "effect.csv", "w") as f:
    f.writelines(["a_id,o_id\n"] + ["%s,%s\n" % (i, j) for i, j in set(effect)])

# %%
with open(folder_path + "has_object.csv", "w") as f:
    f.writelines(["f_id,o_id\n"] + ["%s,%s\n" % (i, j) for i, j in set(has_object)])
# %%
