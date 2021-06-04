#!/usr/bin/env python3
# coding: utf-8
# File: causality_pattern.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-12

import re, jieba
import jieba.posseg as pseg
from ltp import LTP

ltp = LTP()


class CausalityExractor:
    def __init__(self):
        pass

    """1由果溯因配套式"""

    def ruler1(self, sentence):
        """
        conm2:〈[之]所以,因为〉、〈[之]所以,由于〉、 <[之]所以,缘于〉
        conm2_model:<Conj>{Effect},<Conj>{Cause}
        """
        datas = list()
        word_pairs = [["之?所以", "因为"], ["之?所以", "由于"], ["之?所以", "缘于"]]
        for word in word_pairs:
            pattern = re.compile(
                r"\s?(%s)/[p|c]+\s(.*)(%s)/[p|c]+\s(.*)" % (word[0], word[1])
            )
            result = pattern.findall(sentence)
            data = dict()
            if result:
                data["tag"] = result[0][0] + "-" + result[0][2]
                data["cause"] = result[0][3]
                data["effect"] = result[0][1]
                datas.append(data)
        if datas:
            return datas[0]
        else:
            return {}

    """2由因到果配套式"""

    def ruler2(self, sentence):
        """
        conm1:〈因为,从而〉、〈因为,为此〉、〈既[然],所以〉、〈因为,为此〉、〈由于,为此〉、〈只有|除非,才〉、〈由于,以至[于]>、〈既[然],却>、
        〈如果,那么|则〉、<由于,从而〉、<既[然],就〉、〈既[然],因此〉、〈如果,就〉、〈只要,就〉〈因为,所以〉、 <由于,于是〉、〈因为,因此〉、
         <由于,故〉、 〈因为,以致[于]〉、〈因为,因而〉、〈由于,因此〉、<因为,于是〉、〈由于,致使〉、〈因为,致使〉、〈由于,以致[于] >
         〈因为,故〉、〈因[为],以至[于]>,〈由于,所以〉、〈因为,故而〉、〈由于,因而〉
        conm1_model:<Conj>{Cause}, <Conj>{Effect}
        """
        datas = list()
        word_pairs = [
            ["因为", "从而"],
            ["因为", "为此"],
            ["既然?", "所以"],
            ["因为", "为此"],
            ["由于", "为此"],
            ["除非", "才"],
            ["只有", "才"],
            ["由于", "以至于?"],
            ["既然?", "却"],
            ["如果", "那么"],
            ["如果", "则"],
            ["由于", "从而"],
            ["既然?", "就"],
            ["既然?", "因此"],
            ["如果", "就"],
            ["只要", "就"],
            ["因为", "所以"],
            ["由于", "于是"],
            ["因为", "因此"],
            ["由于", "故"],
            ["因为", "以致于?"],
            ["因为", "以致"],
            ["因为", "因而"],
            ["由于", "因此"],
            ["因为", "于是"],
            ["由于", "致使"],
            ["因为", "致使"],
            ["由于", "以致于?"],
            ["因为", "故"],
            ["因为?", "以至于?"],
            ["由于", "所以"],
            ["因为", "故而"],
            ["由于", "因而"],
        ]

        for word in word_pairs:
            pattern = re.compile(
                r"\s?(%s)/[p|c]+\s(.*)(%s)/[p|c]+\s(.*)" % (word[0], word[1])
            )
            result = pattern.findall(sentence)
            data = dict()
            if result:
                data["tag"] = result[0][0] + "-" + result[0][2]
                data["cause"] = result[0][1]
                data["effect"] = result[0][3]
                datas.append(data)
        if datas:
            return datas[0]
        else:
            return {}

    """3由因到果居中式明确"""

    def ruler3(self, sentence):
        """
        cons2:于是、所以、故、致使、以致[于]、因此、以至[于]、从而、因而
        cons2_model:{Cause},<Conj...>{Effect}
        """

        pattern = re.compile(r"(.*)[,，]+.*(于是|所以|故|致使|以致于?|因此|以至于?|从而|因而)/[p|c]+\s(.*)")
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data["tag"] = result[0][1]
            data["cause"] = result[0][0]
            data["effect"] = result[0][2]
        return data

    """4由因到果居中式精确"""

    def ruler4(self, sentence):
        """
        verb1:牵动、导向、使动、导致、勾起、引入、指引、使、予以、产生、促成、造成、引导、造就、促使、酿成、
            引发、渗透、促进、引起、诱导、引来、促发、引致、诱发、推进、诱致、推动、招致、影响、致使、滋生、归于、
            作用、使得、决定、攸关、令人、引出、浸染、带来、挟带、触发、关系、渗入、诱惑、波及、诱使
        verb1_model:{Cause},<Verb|Adverb...>{Effect}
        """
        pattern = re.compile(
            r"(.*)\s+(牵动|已致|导向|使动|导致|勾起|引入|指引|使|予以|产生|促成|造成|引导|造就|促使|酿成|引发|渗透|促进|引起|诱导|引来|促发|引致|诱发|推进|诱致|推动|招致|影响|致使|滋生|归于|作用|使得|决定|攸关|令人|引出|浸染|带来|挟带|触发|关系|渗入|诱惑|波及|诱使)/[d|v]+\s(.*)"
        )
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data["tag"] = result[0][1]
            data["cause"] = result[0][0]
            data["effect"] = result[0][2]
        return data

    """5由因到果前端式模糊"""

    def ruler5(self, sentence):
        """
        prep:为了、依据、为、按照、因[为]、按、依赖、照、比、凭借、由于
        prep_model:<Prep...>{Cause},{Effect}
        """
        pattern = re.compile(r"\s?(为了|依据|按照|因为|因|按|依赖|凭借|由于)/[p|c]+\s(.*)[,，]+(.*)")
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data["tag"] = result[0][0]
            data["cause"] = result[0][1]
            data["effect"] = result[0][2]

        return data

    """6由因到果居中式模糊"""

    def ruler6(self, sentence):
        """
        adverb:以免、以便、为此、才
        adverb_model:{Cause},<Verb|Adverb...>{Effect}
        """
        pattern = re.compile(r"(.*)(以免|以便|为此|才)\s(.*)")
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data["tag"] = result[0][1]
            data["cause"] = result[0][0]
            data["effect"] = result[0][2]
        return data

    """7由因到果前端式精确"""

    def ruler7(self, sentence):
        """
        cons1:既[然]、因[为]、如果、由于、只要
        cons1_model:<Conj...>{Cause},{Effect}
        """
        pattern = re.compile(r"\s?(既然?|因|因为|如果|由于|只要)/[p|c]+\s(.*)[,，]+(.*)")
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data["tag"] = result[0][0]
            data["cause"] = result[0][1]
            data["effect"] = result[0][2]
        return data

    """8由果溯因居中式模糊"""

    def ruler8(self, sentence):
        """
        3
        verb2:根源于、取决、来源于、出于、取决于、缘于、在于、出自、起源于、来自、发源于、发自、源于、根源于、立足[于]
        verb2_model:{Effect}<Prep...>{Cause}
        """

        pattern = re.compile(
            r"(.*)(根源于|取决|来源于|出于|取决于|缘于|在于|出自|起源于|来自|发源于|发自|源于|根源于|立足|立足于)/[p|c]+\s(.*)"
        )
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data["tag"] = result[0][1]
            data["cause"] = result[0][2]
            data["effect"] = result[0][0]
        return data

    """9由果溯因居端式精确"""

    def ruler9(self, sentence):
        """
        cons3:因为、由于
        cons3_model:{Effect}<Conj...>{Cause}
        """
        pattern = re.compile(r"(.*)是?\s(因为|由于)/[p|c]+\s(.*)")
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data["tag"] = result[0][1]
            data["cause"] = result[0][2]
            data["effect"] = result[0][0]

        return data

    """抽取主函数"""

    def extract_triples(self, sentence):
        infos = list()
        #  print(sentence)
        if self.ruler1(sentence):
            infos.append(self.ruler1(sentence))
        elif self.ruler2(sentence):
            infos.append(self.ruler2(sentence))
        elif self.ruler3(sentence):
            infos.append(self.ruler3(sentence))
        elif self.ruler4(sentence):
            infos.append(self.ruler4(sentence))
        elif self.ruler5(sentence):
            infos.append(self.ruler5(sentence))
        elif self.ruler6(sentence):
            infos.append(self.ruler6(sentence))
        elif self.ruler7(sentence):
            infos.append(self.ruler7(sentence))
        elif self.ruler8(sentence):
            infos.append(self.ruler8(sentence))
        elif self.ruler9(sentence):
            infos.append(self.ruler9(sentence))

        return infos

    """抽取主控函数"""

    def extract_main(self, content):
        sentences = self.process_content(content)
        print(sentences)
        datas = list()
        for sentence in sentences:
            subsents = self.fined_sentence(sentence)
            subsents.append(sentence)
            for sent in subsents:
                sent = " ".join(
                    [word.word + "/" + word.flag for word in pseg.cut(sent)]
                )
                result = self.extract_triples(sent)
                if result:
                    for data in result:
                        if data["tag"] and data["cause"] and data["effect"]:
                            datas.append(data)
        return datas

    """文章分句处理"""

    def process_content(self, content):
        return [sentence for sentence in ltp.sent_split([content]) if sentence]

    """切分最小句"""

    def fined_sentence(self, sentence):
        return re.split(r"[？！，；]", sentence)


"""利用语义依存分析得到三元组关系"""


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


"""测试"""


def test(content):
    content1 = """
    截至2008年9月18日12时，5·12汶川地震共造成69227人死亡，374643人受伤，17923人失踪，是中华人民共和国成立以来破坏力最大的地震，也是唐山大地震后伤亡最严重的一次地震。
    """
    content2 = """
    2015年1月4日下午3时39分左右，贵州省遵义市习水县二郎乡遵赤高速二郎乡往仁怀市方向路段发生山体滑坡，发生规模约10万立方米,导致多辆车被埋，造成交通双向中断。此事故引起贵州省委、省政府的高度重视，省长陈敏尔作出指示，要求迅速组织开展救援工作，千方百计实施救援，减少人员伤亡和财物损失。遵义市立即启动应急救援预案，市应急办、公安、交通、卫生等救援力量赶赴现场救援。目前，灾害已造成3人遇难1人受伤，一辆轿车被埋。
    当地时间2010年1月12日16时53分，加勒比岛国海地发生里氏7.3级大地震。震中距首都太子港仅16公里，这个国家的心脏几成一片废墟，25万人在这场骇人的灾难中丧生。此次地震中的遇难者有联合国驻海地维和部队人员，其中包括8名中国维和人员。虽然国际社会在灾后纷纷向海地提供援助，但由于尸体处理不当导致饮用水源受到污染，灾民喝了受污染的水后引发霍乱，已致至少2500多人死亡。
    """
    content3 = """
    American Eagle 四季度符合预期 华尔街对其毛利率不满导致股价大跌
    我之所以考试没及格，是因为我没有好好学习。
    因为天晴了，所以我今天晒被子。
    因为下雪了，所以路上的行人很少。
    我没有去上课是因为我病了。
    因为早上没吃的缘故，所以今天还没到放学我就饿了.
    因为小华身体不舒服，所以她没上课间操。
    因为我昨晚没睡好，所以今天感觉很疲倦。
    因为李明学习刻苦，所以其成绩一直很优秀。
    雨水之所以不能把石块滴穿，是因为它没有专一的目标，也不能持之以恒。
    他之所以成绩不好，是因为他平时不努力学习。
    你之所以提这个问题，是因为你没有学好关联词的用法。
    减了税,因此怨声也少些了。
    他的话引得大家都笑了，室内的空气因此轻松了很多。
    他努力学习，因此通过了考试。
    既然明天要下雨，就不要再出去玩。
    既然他还是那么固执，就不要过多的与他辩论。
    既然别人的事与你无关，你就不要再去过多的干涉。
    既然梦想实现不了，就换一个你自己喜欢的梦想吧。
    既然别人需要你，你就去尽力的帮助别人。
    既然生命突显不出价值，就去追求自己想要的生活吧。
    既然别人不尊重你，就不要尊重别人。 因果复句造句
    既然题目难做，就不要用太多的时间去想，问一问他人也许会更好。
    既然我们是学生，就要遵守学生的基本规范。
    """

    extractor = CausalityExractor()
    datas = extractor.extract_main(content)
    cause_src_list = [
        "".join(
            [
                word.split("/")[0]
                for word in data["cause"].split(" ")
                if word.split("/")[0]
            ]
        )
        for data in datas
    ]
    effect_src_list = [
        "".join(
            [
                word.split("/")[0]
                for word in data["effect"].split(" ")
                if word.split("/")[0]
            ]
        )
        for data in datas
    ]
    if len(cause_src_list) == 0:
        cause_triples = []
    else:
        cause_triples = list(get_triple_iterator(cause_src_list))
    if len(effect_src_list) == 0:
        effect_triples = []
    else:
        effect_triples = list(get_triple_iterator(effect_src_list))
    for i, data in enumerate(datas):
        print("******" * 4)

        print("cause", cause_src_list[i])
        print("cause_triple", cause_triples[i])
        print("tag", data["tag"])
        print("effect", effect_src_list[i])
        print("effect_triple", effect_triples[i])
    return {
        "tags": [data["tag"] for data in datas],
        "cause_src_list": cause_src_list,
        "cause_triple3": cause_triples,
        "effect_src_list": effect_src_list,
        "effect_triples": effect_triples,
    }


if __name__ == "__main__":
    content4 = """原告：林某甲。.被告：朱某。.原告林某甲诉被告朱某离婚纠纷一案，本院受理后，依法适用简易程序，由审判员黄波涛独任审判，公开开庭进行了审理。原、被告均到庭参加诉讼本案现已审理终结。.原告林某甲诉称：原告于2001年经朋友介绍与被告相识，同年开始谈恋爱，××××年××月登记结婚。婚后生育两女一男。婚后夫妻感情一般，相处几年后发现双方性格不合，经常为家庭琐事吵闹打架。对父母刻薄，搞得兄弟不和。几年前被告以出外做工为由离家出走，把三个孩子给我和妈妈照顾。把家里的所有钱全部拿走，包括家里唯一一台摩托车。由于双方草率结婚，婚后又无法沟通，且夫妻双方分居至今多年，现夫妻感情已经全破裂，夫妻关系名存实亡。故此，特向人民法院提起诉讼。请求判令：原告林某甲与被告朱某解除婚姻关系。三个孩子由本人林某甲抚养。.被告朱某辩称：原告胡编胡说，大话连篇。原告有第三者，原告赔偿我不少于10万元可以离婚，否则不同意离婚。.经审理查明：原、被告在2001年给人介绍相识，××××年××月××日办理结婚登记手续。××××年××月××日生育女儿林某乙，××××年××月××日生育女儿林某丙，××××年××月××日生育儿子林某丁。婚后初期，夫妻感情不错，由于原告家庭经济一般，原、被告与原告的兄弟共同居住一套房屋里，导致妯娌之间因琐事产生了矛盾，原、被告也为此经常发生吵闹，加上被告怀疑原告有第三者，导致夫妻感情日渐恶化。原告曾二次向本院起诉要求离婚，经本院（2013）穗增法民一初字第1418号、（2014）穗增法民一初字第522号判决不准离婚后，双方仍没有和好，现原告再次提出离婚诉求。庭审中，原告表示婚生儿子林某丁可由被告抚养，女儿林某乙、林某丙由自己抚养。无婚后夫妻共同财产和债权债务。被告要求离婚后抚养儿子，并要原告补偿10万元。.另查明，原、被告的婚生儿子林某丁目前随被告生活，婚生女儿林某乙、林某丙随原告生活。.以上事实，有当事人提供的身份证、结婚证、出生医学证明、民事判决书及当事人的陈述等为证。.本院认为，夫妻感情彻底破裂是离婚的法定条件。原告曾向本院起诉要求离婚，经本院判决不准许离婚后，原、被告没有和好。现原告再次起诉要求离婚。为此，本院认定原、被告夫妻感情确已破裂，原告的离婚请求理由成立，本院予以准许。对于婚生子女的抚养问题，本院尊重原、被告双方的意愿，确定林某乙、林某丙由原告抚养，林某丁由被告抚养。依照相关司法解释精神，考虑到被告目前的状况，本院认为原告应给予被告适当的帮助。原告应在可承受的能力范围内，补偿15000元给被告，作为其离婚后的安置费用。离婚后，各人的衣物归各人所有，被告的居住问题自行解决。.综上所述，依照.《中华人民共和国婚姻法》第三十二条第二款.、.第三十六条第一、二款.、.第四十二条.的规定，判决如下：.一、准许原告林某甲与被告朱某离婚。.二、婚生女儿林某乙、林某丙由原告林某甲抚养，婚生儿子林某丁由被告朱某抚养。.三、原告林某甲在本判决发生法律效力后七日内，支付补偿费15000元给被告朱某。.四、离婚后，被告朱某的居住问题自解决。.五、案件受理费150元，由原告林某甲负担。.如上述给付义务人未在规定的期限内履行给付金钱义务的，按.《中华人民共和国民事诉讼法》第二百第五十三条.的规定加倍支付迟延履行期间的债务利息。.如不服本判决，可在判决书送达之日起十五日内，向本院递交上诉状，并按对方当事人的人数提出副本，上诉于广州市中级人民法院。.当事人上诉的，应在递交上诉状次日起七日内按不服本案判决部分向广州市中级人民法院预交上诉案件受理费。逾期不交的，按自动撤回上诉处理。.审判员黄波涛.二〇一四年十一月十七日.书记员朱小智"""
    test(content4)
