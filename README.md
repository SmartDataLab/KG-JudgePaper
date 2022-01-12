# 法律文书知识图谱构建

## Quick Start

需要安装好 neo4j(图数据库)和 ltp(哈工大自然语言处理工具)

```
cd src
python get_json_dict.py
cp neo4j_csv/*.csv /var/lib/neo4j/import/
cypher-shell #
# 执行 neo4j_csv/neo4j_import_script.txt 中的数据导入命令
```

## 代码解释

构建法律文书图谱，首先聚焦于关注的实体（对应于知识图谱的节点），法律文书的标题（Case）、案件重点(Keyword)、案件关键事实（Fact）、案件重要对象(Obeject)、案件关键动作(Action)是我们关注的对象。其中法律裁判文书有一个重要特征，重视因果推断逻辑，有因果关联的事实是我们关注的重点，其中涉及的对象和动作也有重要意义。

基于此，对于不同节点，我们关心以下关系：

(1) (Case,Keyword,has_keyword)

(2) (Case,Fact,has_fact)

(3) (Fact1,Fact2,Casue) Cause 可以是不同的因果类型

(4) (Fact,Object,has_object)

(5) (Object,Action,do)

(6) (Action,Object,Effect)

最主要的两个任务是从文本中找到 Fact，再从 Fact 找到 Object、Action。对于第一个任务，采用因果规则的字串匹配，来寻找具有因果逻辑的事实，再对事实进行语义依存分析，根据语义依存分析的理论，关于动词与形容词，分别设计一套针对解析树的匹配规则。

## 节点数据统计

- 法律文书的标题（Case）1000
- 案件重点(Keyword) 418
- 案件关键事实（Fact） 19800
- 案件重要对象(Obeject) 8020
- 案件关键动作(Action) 2248

## 关系数据统计

(1) (Case,Keyword,has_keyword) 1745

(2) (Case,Fact,has_fact) 19800

(3) (Fact1,Fact2,Casue) 9900

(4) (Fact,Object,has_object) 44107

(5) (Object,Action,do) 28187

(6) (Action,Object,Effect) 28187

## 因果逻辑匹配

主要包括以下几个步骤：  
1、因果知识库的构建。因果知识库的构建包括因果连词库，结果词库、因果模式库等。  
2、文本预处理。这个包括对文本进行噪声移除，非关键信息去除等。  
3、因果事件抽取。这个包括基于因果模式库的因果对抽取。  
4、事件表示。这是整个因果图谱构建的核心问题，因为事件图谱本质上是联通的，如何选择一种恰当（短语、短句、句子主干）等方式很重要。  
5、事件融合。事件融合跟知识图谱中的实体对齐任务很像  
6、事件存储。事件存储是最后步骤，基于业务需求，可以用相应的数据库进行存储，比如图数据库等。

Fact1 -因果类别-> Fact2

## 依存语义分析

利用 ltp 进行 sdp(Semantic Dependency Parsing),具体结果的符号参考 ltp 官网。

### 针对动词

依存分析中最接近根节点的动词以及接续动词作为 Action，其对于的主体和客体为实体。

(('被告人', 'AGT'), ('犯', 'dCONT'), '判处')

### 针对形容词的匹配规则

FEAT -a-> AGT

例子：

["夫妻感情不错", "夫妻感情日渐恶化", "现夫妻感情已经全破裂", "夫妻关系名存实亡"]

## 访问图数据库

对于 python 可以利用 py2neo 工具

```py
from py2neo import Graph
graph = Graph()
def match_object_name(graph, val):
    sql = (
        "MATCH (n2:FACT)-[rel]->(n1) WHERE n1.object=~'.*"
        + str(val)
        + ".*' RETURN n1, rel, n2 LIMIT 40;"
    )
    answer = graph.run(sql).data()
    return answer
match_object_name(graph,"夫妻")
```

更多匹配请参考 neo4j 的 sql 语法
