{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \uc0\u1058 \u1099  \'97 Codex (\u1089 \u1090 \u1072 \u1088 \u1096 \u1080 \u1081  Node.js \u1080 \u1085 \u1078 \u1077 \u1085 \u1077 \u1088 ). \u1057 \u1086 \u1073 \u1077 \u1088 \u1080  \u1087 \u1086 \u1083 \u1085 \u1086 \u1089 \u1090 \u1100 \u1102  \u1088 \u1072 \u1073 \u1086 \u1095 \u1080 \u1081  MVP-\u1087 \u1088 \u1086 \u1077 \u1082 \u1090 : MCP-\u1089 \u1077 \u1088 \u1074 \u1077 \u1088  (Node.js + TypeScript), \u1082 \u1086 \u1090 \u1086 \u1088 \u1099 \u1081  \u1087 \u1086 \u1079 \u1074 \u1086 \u1083 \u1103 \u1077 \u1090  \u1087 \u1086 \u1076 \u1082 \u1083 \u1102 \u1095 \u1080 \u1090 \u1100  LLM \u1080  \u1080 \u1089 \u1082 \u1072 \u1090 \u1100  \u1090 \u1091 \u1088 \u1099  \u1095 \u1077 \u1088 \u1077 \u1079  \u1087 \u1091 \u1073 \u1083 \u1080 \u1095 \u1085 \u1099 \u1081  \u1087 \u1086 \u1080 \u1089 \u1082  eto.travel, \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1103  \u1085 \u1072 \u1073 \u1083 \u1102 \u1076 \u1072 \u1077 \u1084 \u1099 \u1077  HTTP endpoint\'92\u1099  Tourvisor.\
\
\uc0\u1042 \u1040 \u1046 \u1053 \u1054 : \u1057 \u1076 \u1077 \u1083 \u1072 \u1081  \u1088 \u1077 \u1079 \u1091 \u1083 \u1100 \u1090 \u1072 \u1090  \'93\u1075 \u1086 \u1090 \u1086 \u1074  \u1082  \u1079 \u1072 \u1087 \u1091 \u1089 \u1082 \u1091 \'94: \u1082 \u1086 \u1076 , \u1082 \u1086 \u1085 \u1092 \u1080 \u1075 \u1080 , \u1090 \u1077 \u1089 \u1090 \u1099 , README, \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 \u1099  \u1074 \u1099 \u1079 \u1086 \u1074 \u1086 \u1074 , \u1079 \u1072 \u1097 \u1080 \u1090 \u1072  API-\u1082 \u1083 \u1102 \u1095 \u1086 \u1084 , \u1076 \u1077 \u1087 \u1083 \u1086 \u1081 -\u1086 \u1088 \u1080 \u1077 \u1085 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1085 \u1072 \u1103  \u1089 \u1090 \u1088 \u1091 \u1082 \u1090 \u1091 \u1088 \u1072 .\
\
=====================================================================\
1) \uc0\u1062 \u1045 \u1051 \u1068  MVP\
=====================================================================\
\uc0\u1057 \u1086 \u1073 \u1088 \u1072 \u1090 \u1100  \u1074 \u1077 \u1073 -\u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1085 \u1099 \u1081  MCP-\u1089 \u1077 \u1088 \u1074 \u1077 \u1088  \u1089  \u1076 \u1074 \u1091 \u1084 \u1103  MCP tools:\
1) search_tours \'97 \uc0\u1087 \u1088 \u1080 \u1085 \u1080 \u1084 \u1072 \u1077 \u1090  \u1087 \u1072 \u1088 \u1072 \u1084 \u1077 \u1090 \u1088 \u1099  \u1087 \u1086 \u1080 \u1089 \u1082 \u1072 , \u1076 \u1077 \u1083 \u1072 \u1077 \u1090  modsearch \u8594  polling modresult \u8594  \u1074 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1090  \u1084 \u1072 \u1089 \u1089 \u1080 \u1074  \u1086 \u1092 \u1092 \u1077 \u1088 \u1086 \u1074 .\
2) get_dictionaries \'97 \uc0\u1087 \u1088 \u1086 \u1082 \u1089 \u1080 \u1088 \u1091 \u1077 \u1090  listdev \u1076 \u1083 \u1103  \u1089 \u1087 \u1088 \u1072 \u1074 \u1086 \u1095 \u1085 \u1080 \u1082 \u1086 \u1074  (\u1082 \u1086 \u1076 \u1099  \u8594  \u1085 \u1072 \u1079 \u1074 \u1072 \u1085 \u1080 \u1103 ).\
\
\uc0\u1044 \u1086 \u1087 \u1086 \u1083 \u1085 \u1080 \u1090 \u1077 \u1083 \u1100 \u1085 \u1086  (\u1079 \u1072  \u1092 \u1083 \u1072 \u1075 \u1086 \u1084  env, \u1074 \u1099 \u1082 \u1083 \u1102 \u1095 \u1077 \u1085 \u1086  \u1087 \u1086  \u1091 \u1084 \u1086 \u1083 \u1095 \u1072 \u1085 \u1080 \u1102 ):\
3) get_tour_details \'97 \uc0\u1076 \u1077 \u1088 \u1075 \u1072 \u1077 \u1090  modact \u1087 \u1086  tourid \u1080  \u1074 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1090  \u1089 \u1099 \u1088 \u1086 \u1081  \u1086 \u1090 \u1074 \u1077 \u1090 .\
\
=====================================================================\
2) \uc0\u1060 \u1040 \u1050 \u1058 \u1067  \u1048  \u1048 \u1057 \u1058 \u1054 \u1063 \u1053 \u1048 \u1050 \u1048  \u1048 \u1053 \u1058 \u1045 \u1043 \u1056 \u1040 \u1062 \u1048 \u1048  (\u1053 \u1045  \u1055 \u1056 \u1048 \u1044 \u1059 \u1052 \u1067 \u1042 \u1040 \u1058 \u1068  \u1044 \u1056 \u1059 \u1043 \u1048 \u1045 )\
=====================================================================\
\uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1081  \u1090 \u1086 \u1083 \u1100 \u1082 \u1086  \u1101 \u1090 \u1080  endpoint\'92\u1099  \u1080  \u1087 \u1072 \u1088 \u1072 \u1084 \u1077 \u1090 \u1088 \u1099  (\u1074 \u1089 \u1105  \u1074 \u1079 \u1103 \u1090 \u1086  \u1080 \u1079  Network):\
\
A) \uc0\u1055 \u1086 \u1080 \u1089 \u1082  (\u1080 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103 )\
GET https://tourvisor.ru/xml/modsearch.php\
Query params (\uc0\u1088 \u1077 \u1072 \u1083 \u1100 \u1085 \u1099 \u1077  \u1087 \u1086 \u1083 \u1103 ):\
- datefrom (DD.MM.YYYY)\
- dateto (DD.MM.YYYY)\
- regular (int)\
- nightsfrom (int)\
- nightsto (int)\
- adults (int)\
- child (int)\
- meal (int)\
- rating (int)\
- country (int)\
- departure (int)\
- pricefrom (int)\
- priceto (int)\
- currency (int)\
- actype (int)\
- formmode (int)\
- pricetype (int)\
- referrer (urlencoded, \uc0\u1079 \u1085 \u1072 \u1095 \u1077 \u1085 \u1080 \u1077 : https://eto.travel/search/)\
- session (\uc0\u1076 \u1083 \u1080 \u1085 \u1085 \u1099 \u1081  \u1090 \u1086 \u1082 \u1077 \u1085 )\
\
\uc0\u1054 \u1090 \u1074 \u1077 \u1090  modsearch \u1089 \u1086 \u1076 \u1077 \u1088 \u1078 \u1080 \u1090 :\
- result.requestid (\uc0\u1095 \u1080 \u1089 \u1083 \u1086 )\
- result.currency (\uc0\u1089 \u1090 \u1088 \u1086 \u1082 \u1072 , \u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088  "RUB")\
- result.linkparam (\uc0\u1095 \u1080 \u1089 \u1083 \u1086 )\
- result.links (\uc0\u1086 \u1073 \u1098 \u1077 \u1082 \u1090  \u1089 \u1086  \u1089 \u1089 \u1099 \u1083 \u1082 \u1072 \u1084 \u1080 , \u1074 \u1082 \u1083 \u1102 \u1095 \u1072 \u1103  links.hotellink \u1080  links.searchlink)\
- result.searchident \uc0\u1080  \u1076 \u1088 .\
\
B) \uc0\u1056 \u1077 \u1079 \u1091 \u1083 \u1100 \u1090 \u1072 \u1090 \u1099  (\u1087 \u1091 \u1083 \u1083 \u1080 \u1085 \u1075  \u1073 \u1083 \u1086 \u1082 \u1072 \u1084 \u1080 )\
GET https://search3.tourvisor.ru/modresult.php\
Query params:\
- requestid (\uc0\u1095 \u1080 \u1089 \u1083 \u1086 )\
- lastblock (int, \uc0\u1086 \u1087 \u1094 \u1080 \u1086 \u1085 \u1072 \u1083 \u1100 \u1085 \u1086 )\
- referrer (urlencoded)\
- session (\uc0\u1090 \u1086 \u1082 \u1077 \u1085 )\
\
\uc0\u1054 \u1090 \u1074 \u1077 \u1090  modresult \u1089 \u1086 \u1076 \u1077 \u1088 \u1078 \u1080 \u1090 :\
- data.block[] \'97 \uc0\u1089 \u1087 \u1080 \u1089 \u1086 \u1082  \u1073 \u1083 \u1086 \u1082 \u1086 \u1074 , \u1082 \u1072 \u1078 \u1076 \u1099 \u1081 :\
  - id (int)\
  - operator (int)\
  - hotel[] \'97 \uc0\u1089 \u1087 \u1080 \u1089 \u1086 \u1082  \u1086 \u1090 \u1077 \u1083 \u1077 \u1081 , \u1082 \u1072 \u1078 \u1076 \u1099 \u1081 :\
    - id (int)\
    - price (int)\
    - tour[] \'97 \uc0\u1089 \u1087 \u1080 \u1089 \u1086 \u1082  \u1090 \u1091 \u1088 \u1086 \u1074 , \u1082 \u1072 \u1078 \u1076 \u1099 \u1081  \u1086 \u1073 \u1098 \u1077 \u1082 \u1090  \u1090 \u1091 \u1088 \u1072  \u1089  \u1087 \u1086 \u1083 \u1103 \u1084 \u1080  \u1074 \u1088 \u1086 \u1076 \u1077 :\
      - op (int), dt (YYYY-MM-DD), nt (int), pr (int), id (string),\
      - plus: ml, mf, reg, ct, rm, rmd, hp, prue, prclean, prfuel, pl, nm \uc0\u1080  \u1090 .\u1076 . (\u1089 \u1086 \u1093 \u1088 \u1072 \u1085 \u1103 \u1090 \u1100  \u1082 \u1072 \u1082  \u1082 \u1086 \u1076 \u1099 )\
- data.status.progress (int)\
- data.status.finished (int)\
- data.status.requestid (\uc0\u1095 \u1080 \u1089 \u1083 \u1086 )\
- debug (\uc0\u1086 \u1073 \u1098 \u1077 \u1082 \u1090 )\
\
C) \uc0\u1057 \u1087 \u1088 \u1072 \u1074 \u1086 \u1095 \u1085 \u1080 \u1082 \u1080 \
GET https://tourvisor.ru/xml/listdev.php\
Query params (\uc0\u1085 \u1072 \u1073 \u1083 \u1102 \u1076 \u1072 \u1077 \u1084 \u1099 \u1077  \u1074 \u1072 \u1088 \u1080 \u1072 \u1085 \u1090 \u1099 ):\
- type (\uc0\u1089 \u1090 \u1088 \u1086 \u1082 \u1072 : \u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088  "allhotel" \u1080 \u1083 \u1080  "departure,allcountry,country,region,subregions,operator")\
- hotcountry (int) \'97 \uc0\u1074 \u1089 \u1090 \u1088 \u1077 \u1095 \u1072 \u1083 \u1086 \u1089 \u1100  \u1076 \u1083 \u1103  allhotel\
- flycountry (int) \'97 \uc0\u1074 \u1089 \u1090 \u1088 \u1077 \u1095 \u1072 \u1083 \u1086 \u1089 \u1100  \u1074  \u1076 \u1088 \u1091 \u1075 \u1086 \u1084  \u1087 \u1088 \u1086 \u1075 \u1086 \u1085 \u1077  (\u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1072 \u1090 \u1100  \u1086 \u1087 \u1094 \u1080 \u1086 \u1085 \u1072 \u1083 \u1100 \u1085 \u1086 )\
- flydeparture (int)\
- cndep (int)\
- formmode (int)\
- format=json\
- referrer\
- session\
\
\uc0\u1054 \u1090 \u1074 \u1077 \u1090  listdev \u1089 \u1086 \u1076 \u1077 \u1088 \u1078 \u1080 \u1090 :\
- lists (\uc0\u1086 \u1073 \u1098 \u1077 \u1082 \u1090  \u1089 \u1086  \u1089 \u1083 \u1086 \u1074 \u1072 \u1088 \u1103 \u1084 \u1080 , \u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088  departures.departure[])\
\
D) \uc0\u1044 \u1077 \u1090 \u1072 \u1083 \u1080  \u1087 \u1086  \u1090 \u1091 \u1088 \u1091  (\u1086 \u1087 \u1094 \u1080 \u1086 \u1085 \u1072 \u1083 \u1100 \u1085 \u1086 )\
GET https://tourvisor.ru/xml/modact.php\
Query params:\
- currency (int)\
- tourid (string/int)\
- referrer\
- session (\uc0\u1080 \u1085 \u1086 \u1075 \u1076 \u1072  \u1087 \u1091 \u1089 \u1090 \u1086 \u1081  \u1074  Network; \u1074  \u1087 \u1088 \u1086 \u1077 \u1082 \u1090 \u1077  \u1089 \u1076 \u1077 \u1083 \u1072 \u1090 \u1100  \u1087 \u1086 \u1074 \u1077 \u1076 \u1077 \u1085 \u1080 \u1077  \u1095 \u1077 \u1088 \u1077 \u1079  env-\u1092 \u1083 \u1072 \u1075 )\
\
E) Deep link (MVP)\
\uc0\u1060 \u1072 \u1082 \u1090  \u1080 \u1079  modsearch:\
- result.links.hotellink = "https://tourcart.ru/hotel?cd=<linkparam>#!/hotel="\
\uc0\u1060 \u1072 \u1082 \u1090  \u1080 \u1079  UI:\
- https://eto.travel/search/#tvtourid=<id>\
\uc0\u1042  MVP deep_link \u1074 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1081  \u1082 \u1072 \u1082 :\
- \uc0\u1077 \u1089 \u1083 \u1080  \u1091 \u1076 \u1072 \u1077 \u1090 \u1089 \u1103  \u1089 \u1074 \u1103 \u1079 \u1072 \u1090 \u1100  \u1086 \u1092 \u1092 \u1077 \u1088  \u1089  tvtourid \u1087 \u1086  \u1092 \u1072 \u1082 \u1090 \u1072 \u1084  (\u1082 \u1083 \u1102 \u1095  \u1074  \u1086 \u1090 \u1074 \u1077 \u1090 \u1072 \u1093 ), \u1090 \u1086 \u1075 \u1076 \u1072  "https://eto.travel/search/#tvtourid=<id>"\
- \uc0\u1080 \u1085 \u1072 \u1095 \u1077  deep_link="UNKNOWN"\
\uc0\u1053 \u1077  \u1089 \u1090 \u1088 \u1086 \u1080 \u1090 \u1100  \u1075 \u1080 \u1087 \u1086 \u1090 \u1077 \u1079 \u1099 .\
\
=====================================================================\
3) MCP \uc0\u1058 \u1056 \u1040 \u1053 \u1057 \u1055 \u1054 \u1056 \u1058  \u1048  API\
=====================================================================\
\uc0\u1057 \u1076 \u1077 \u1083 \u1072 \u1081  MCP-\u1089 \u1077 \u1088 \u1074 \u1077 \u1088  \u1095 \u1077 \u1088 \u1077 \u1079  HTTP, \u1087 \u1088 \u1077 \u1076 \u1087 \u1086 \u1095 \u1090 \u1077 \u1085 \u1080 \u1077 : SSE-\u1090 \u1088 \u1072 \u1085 \u1089 \u1087 \u1086 \u1088 \u1090  (\u1080 \u1083 \u1080  \u1086 \u1092 \u1080 \u1094 \u1080 \u1072 \u1083 \u1100 \u1085 \u1099 \u1081  MCP \u1087 \u1072 \u1082 \u1077 \u1090  \u1076 \u1083 \u1103  Node, \u1077 \u1089 \u1083 \u1080  \u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1077 \u1085 ).\
\uc0\u1052 \u1080 \u1085 \u1080 \u1084 \u1072 \u1083 \u1100 \u1085 \u1099 \u1081  \u1085 \u1072 \u1073 \u1086 \u1088 :\
- GET /health -> \{ "ok": true \}\
- MCP endpoint\'92\uc0\u1099  (\u1074 \u1099 \u1073 \u1077 \u1088 \u1080  \u1086 \u1076 \u1080 \u1085  \u1074 \u1072 \u1088 \u1080 \u1072 \u1085 \u1090  \u1080  \u1088 \u1077 \u1072 \u1083 \u1080 \u1079 \u1091 \u1081  \u1087 \u1086 \u1083 \u1085 \u1086 \u1089 \u1090 \u1100 \u1102 ):\
  \uc0\u1042 \u1072 \u1088 \u1080 \u1072 \u1085 \u1090  1 (\u1087 \u1088 \u1077 \u1076 \u1087 \u1086 \u1095 \u1090 \u1080 \u1090 \u1077 \u1083 \u1100 \u1085 \u1086 ): SSE\
   - GET /mcp/sse  (SSE stream)\
   - POST /mcp/call (\uc0\u1074 \u1099 \u1079 \u1086 \u1074  tool)\
  \uc0\u1042 \u1072 \u1088 \u1080 \u1072 \u1085 \u1090  2: \u1077 \u1076 \u1080 \u1085 \u1099 \u1081  JSON endpoint\
   - POST /mcp\
\
\uc0\u1053 \u1091 \u1078 \u1085 \u1086 , \u1095 \u1090 \u1086 \u1073 \u1099  \u1074 \u1085 \u1077 \u1096 \u1085 \u1103 \u1103  \u1085 \u1077 \u1081 \u1088 \u1086 \u1085 \u1082 \u1072  \u1084 \u1086 \u1075 \u1083 \u1072  \u1087 \u1086 \u1076 \u1082 \u1083 \u1102 \u1095 \u1080 \u1090 \u1100 \u1089 \u1103  \u1080  \u1074 \u1099 \u1079 \u1074 \u1072 \u1090 \u1100  tools.\
\
\uc0\u1047 \u1072 \u1097 \u1080 \u1090 \u1072 :\
- \uc0\u1042 \u1089 \u1077  MCP endpoints \u1090 \u1088 \u1077 \u1073 \u1091 \u1102 \u1090  header: x-api-key == MCP_API_KEY\
- /health \uc0\u1084 \u1086 \u1078 \u1085 \u1086  \u1086 \u1089 \u1090 \u1072 \u1074 \u1080 \u1090 \u1100  \u1087 \u1091 \u1073 \u1083 \u1080 \u1095 \u1085 \u1099 \u1084 .\
\
Rate limiting:\
- \uc0\u1084 \u1080 \u1085 \u1080 \u1084 \u1072 \u1083 \u1100 \u1085 \u1099 \u1081  \u1083 \u1080 \u1084 \u1080 \u1090  per IP \u1085 \u1072  MCP endpoints (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088  60 req/min), \u1082 \u1086 \u1085 \u1092 \u1080 \u1075 \u1091 \u1088 \u1080 \u1088 \u1091 \u1077 \u1084 \u1086 .\
\
=====================================================================\
4) TOOLS \uc0\u1048  \u1050 \u1054 \u1053 \u1058 \u1056 \u1040 \u1050 \u1058 \u1067 \
=====================================================================\
Tool 1: get_dictionaries\
Input (JSON Schema + Zod):\
\{\
  "type": "string",\
  "hotcountry": "integer|null",\
  "flycountry": "integer|null",\
  "flydeparture": "integer|null",\
  "cndep": "integer|null",\
  "formmode": "integer|null",\
  "format": "json"\
\}\
Required: type\
\
Output:\
\{\
  "data": \{ ...listdev response... \},\
  "meta": \{ "source": "tourvisor:listdev", "session_used": true \},\
  "warnings": []\
\}\
\
Tool 2: search_tours\
Input (\uc0\u1090 \u1086 \u1083 \u1100 \u1082 \u1086  \u1088 \u1077 \u1072 \u1083 \u1100 \u1085 \u1099 \u1077  \u1087 \u1072 \u1088 \u1072 \u1084 \u1077 \u1090 \u1088 \u1099  modsearch) + limit:\
\{\
  "datefrom": "DD.MM.YYYY",\
  "dateto": "DD.MM.YYYY",\
  "regular": 1,\
  "nightsfrom": 6,\
  "nightsto": 14,\
  "adults": 2,\
  "child": 0,\
  "meal": 0,\
  "rating": 0,\
  "country": 47,\
  "departure": 1,\
  "pricefrom": 0,\
  "priceto": 0,\
  "currency": 0,\
  "actype": 0,\
  "formmode": 0,\
  "pricetype": 0,\
  "limit": 50\
\}\
Required: datefrom, dateto, nightsfrom, nightsto, adults, country, departure\
\
Output:\
\{\
  "offers": [ TourOffer ],\
  "meta": \{\
    "requestid": 0,\
    "finished": 0,\
    "progress": 0,\
    "blocks_seen": 0,\
    "offers_total_collected": 0\
  \},\
  "warnings": []\
\}\
\
TourOffer (\uc0\u1085 \u1086 \u1088 \u1084 \u1072 \u1083 \u1080 \u1079 \u1086 \u1074 \u1072 \u1085 \u1085 \u1099 \u1081  \u1084 \u1080 \u1085 \u1080 \u1084 \u1091 \u1084 ):\
\{\
  "offer_id": "string",              // tour.id\
  "tour_id": "string",               // tour.id (\uc0\u1076 \u1091 \u1073 \u1083 \u1080 \u1088 \u1091 \u1077 \u1084  \u1103 \u1074 \u1085 \u1086 )\
  "price": "number",                 // tour.pr (\uc0\u1080 \u1083 \u1080  hotel.price \u1077 \u1089 \u1083 \u1080  tour.pr \u1086 \u1090 \u1089 \u1091 \u1090 \u1089 \u1090 \u1074 \u1091 \u1077 \u1090 )\
  "currency": "string|UNKNOWN",      // modsearch.result.currency\
  "start_date": "string|UNKNOWN",    // tour.dt\
  "nights": "number|UNKNOWN",        // tour.nt\
  "hotel_id": "number|UNKNOWN",      // hotel.id\
  "operator_id": "number|UNKNOWN",   // tour.op \uc0\u1080 \u1083 \u1080  block.operator\
  "region_id": "number|UNKNOWN",     // tour.reg\
  "country_id": "number|UNKNOWN",    // tour.ct \uc0\u1080 \u1083 \u1080  input.country\
  "departure_id": "number|UNKNOWN",  // input.departure\
  "meal_id": "number|UNKNOWN",       // tour.ml \uc0\u1080 \u1083 \u1080  tour.mf (\u1086 \u1073 \u1072  \u1089 \u1086 \u1093 \u1088 \u1072 \u1085 \u1080 \u1090 \u1100 : meal_id \u1080  meal2_id)\
  "meal2_id": "number|UNKNOWN",\
  "room_id": "number|UNKNOWN",       // tour.rm\
  "deep_link": "string",             // UNKNOWN \uc0\u1080 \u1083 \u1080  eto.travel hash link\
  "source_raw": \{ ... \}              // \uc0\u1080 \u1089 \u1093 \u1086 \u1076 \u1085 \u1099 \u1081  \u1082 \u1091 \u1089 \u1086 \u1082  (tour+hotel+block) \u1076 \u1083 \u1103  \u1076 \u1077 \u1073 \u1072 \u1075 \u1072 \
\}\
\
Tool 3 (\uc0\u1086 \u1087 \u1094 \u1080 \u1086 \u1085 \u1072 \u1083 \u1100 \u1085 \u1086 , \u1074 \u1099 \u1082 \u1083 \u1102 \u1095 \u1080 \u1090 \u1100  \u1095 \u1077 \u1088 \u1077 \u1079  env ENABLE_TOUR_DETAILS=false):\
get_tour_details\
Input: \{ "tourid": "string", "currency": 0 \}\
Output: \{ "data": \{...\}, "meta": \{...\}, "warnings": [...] \}\
\
=====================================================================\
5) \uc0\u1051 \u1054 \u1043 \u1048 \u1050 \u1040  \u1055 \u1059 \u1051 \u1051 \u1048 \u1053 \u1043 \u1040  modresult\
=====================================================================\
\uc0\u1040 \u1083 \u1075 \u1086 \u1088 \u1080 \u1090 \u1084  (\u1088 \u1077 \u1072 \u1083 \u1080 \u1079 \u1086 \u1074 \u1072 \u1090 \u1100  \u1089 \u1090 \u1088 \u1086 \u1075 \u1086 ):\
1) modsearch(params + referrer + session) -> requestid, currency, links, linkparam\
2) lastblock := undefined\
3) seenBlockIds := Set\
4) offers := []\
5) loop until:\
   - timeout TOURVISOR_POLL_TIMEOUT_MS\
   - or finished==1 / progress==100\
   - or offers.length >= limit (\uc0\u1084 \u1086 \u1078 \u1085 \u1086  \u1086 \u1089 \u1090 \u1072 \u1085 \u1086 \u1074 \u1080 \u1090 \u1100  \u1088 \u1072 \u1085 \u1100 \u1096 \u1077 , \u1085 \u1086  meta.progress \u1089 \u1086 \u1093 \u1088 \u1072 \u1085 \u1080 \u1090 \u1100  \u1090 \u1077 \u1082 \u1091 \u1097 \u1080 \u1081 )\
   On each iteration:\
   a) call modresult(requestid, lastblock?, referrer, session)\
   b) if response has data.block:\
      - for each block:\
        if block.id not in seenBlockIds:\
           add to seenBlockIds\
           extract offers from block.hotel[].tour[]\
      - update lastblock to max block.id seen\
   c) update progress/finished from data.status\
   d) sleep TOURVISOR_POLL_INTERVAL_MS\
6) If timeout happens before finished:\
   warnings add "TIMEOUT_PARTIAL_RESULTS"\
7) Return offers normalized + meta\
\
\uc0\u1044 \u1077 \u1076 \u1091 \u1087 :\
- dedup by tour.id (offer_id). Use Map for uniqueness.\
\
=====================================================================\
6) \uc0\u1053 \u1040 \u1057 \u1058 \u1056 \u1054 \u1049 \u1050 \u1048  (.env)\
=====================================================================\
\uc0\u1054 \u1073 \u1103 \u1079 \u1072 \u1090 \u1077 \u1083 \u1100 \u1085 \u1099 \u1077 :\
- PORT=3000\
- MCP_API_KEY=...\
- TOURVISOR_SESSION=...\
- TOURVISOR_REFERRER=https://eto.travel/search/\
- TOURVISOR_SEARCH_HOST=https://tourvisor.ru\
- TOURVISOR_RESULT_HOST=https://search3.tourvisor.ru\
\
\uc0\u1054 \u1087 \u1094 \u1080 \u1086 \u1085 \u1072 \u1083 \u1100 \u1085 \u1099 \u1077 :\
- TOURVISOR_POLL_INTERVAL_MS=500\
- TOURVISOR_POLL_TIMEOUT_MS=45000\
- TOURVISOR_MAX_BLOCKS=50\
- TOURVISOR_MAX_OFFERS=300\
- ENABLE_TOUR_DETAILS=false\
- TOURVISOR_USE_SESSION_FOR_MODACT=true\
\
=====================================================================\
7) \uc0\u1058 \u1056 \u1045 \u1041 \u1054 \u1042 \u1040 \u1053 \u1048 \u1071  \u1050  \u1056 \u1045 \u1055 \u1054 \u1047 \u1048 \u1058 \u1054 \u1056 \u1048 \u1070 \
=====================================================================\
Node 20+, TypeScript.\
Framework: Fastify (\uc0\u1087 \u1088 \u1077 \u1076 \u1087 \u1086 \u1095 \u1090 \u1080 \u1090 \u1077 \u1083 \u1100 \u1085 \u1086 ).\
HTTP client: undici.\
Validation: zod.\
Tests: vitest + nock.\
Logger: pino (\uc0\u1080 \u1083 \u1080  console \u1089  \u1089 \u1090 \u1088 \u1091 \u1082 \u1090 \u1091 \u1088 \u1086 \u1081  json), \u1085 \u1086  pino \u1087 \u1088 \u1077 \u1076 \u1087 \u1086 \u1095 \u1090 \u1080 \u1090 \u1077 \u1083 \u1100 \u1085 \u1077 \u1077 .\
\
\uc0\u1057 \u1090 \u1088 \u1091 \u1082 \u1090 \u1091 \u1088 \u1072  \u1092 \u1072 \u1081 \u1083 \u1086 \u1074  (\u1089 \u1086 \u1079 \u1076 \u1072 \u1090 \u1100  \u1074 \u1089 \u1077 ):\
/src\
  /config\
    env.ts\
  /mcp\
    server.ts\
    tools.ts\
    schemas.ts\
    auth.ts\
  /tourvisor\
    client.ts\
    endpoints.ts\
    polling.ts\
    normalizers.ts\
    dictionaries.ts\
  /utils\
    sleep.ts\
    errors.ts\
    rateLimit.ts\
  index.ts\
/tests\
  search_tours.test.ts\
  get_dictionaries.test.ts\
  polling.test.ts\
Dockerfile\
README.md\
.env.example\
package.json\
tsconfig.json\
\
=====================================================================\
8) README (\uc0\u1054 \u1041 \u1071 \u1047 \u1040 \u1058 \u1045 \u1051 \u1068 \u1053 \u1054 )\
=====================================================================\
\uc0\u1044 \u1086 \u1083 \u1078 \u1077 \u1085  \u1089 \u1086 \u1076 \u1077 \u1088 \u1078 \u1072 \u1090 \u1100 :\
- \uc0\u1041 \u1099 \u1089 \u1090 \u1088 \u1099 \u1081  \u1089 \u1090 \u1072 \u1088 \u1090 \
- \uc0\u1055 \u1088 \u1080 \u1084 \u1077 \u1088  .env\
- \uc0\u1055 \u1088 \u1080 \u1084 \u1077 \u1088 \u1099  \u1074 \u1099 \u1079 \u1086 \u1074 \u1072  MCP tools (curl) \u1089  x-api-key\
- \uc0\u1054 \u1087 \u1080 \u1089 \u1072 \u1085 \u1080 \u1077  \u1087 \u1086 \u1083 \u1077 \u1081  search_tours\
- \uc0\u1054 \u1075 \u1088 \u1072 \u1085 \u1080 \u1095 \u1077 \u1085 \u1080 \u1103 : polling, session, \u1083 \u1080 \u1084 \u1080 \u1090 \u1099 \
- \uc0\u1050 \u1072 \u1082  \u1076 \u1077 \u1087 \u1083 \u1086 \u1080 \u1090 \u1100  (Render/Railway): \u1096 \u1072 \u1075 \u1080 \
\
=====================================================================\
9) \uc0\u1050 \u1056 \u1048 \u1058 \u1045 \u1056 \u1048 \u1048  \u1055 \u1056 \u1048 \u1045 \u1052 \u1050 \u1048 \
=====================================================================\
\uc0\u1057 \u1095 \u1080 \u1090 \u1072 \u1077 \u1084  MVP \u1075 \u1086 \u1090 \u1086 \u1074 \u1099 \u1084 , \u1082 \u1086 \u1075 \u1076 \u1072 :\
1) npm i && npm run dev \uc0\u1087 \u1086 \u1076 \u1085 \u1080 \u1084 \u1072 \u1077 \u1090  \u1089 \u1077 \u1088 \u1074 \u1077 \u1088 \
2) GET /health -> ok:true\
3) Tools \uc0\u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1085 \u1099  \u1080  \u1074 \u1099 \u1079 \u1099 \u1074 \u1072 \u1102 \u1090 \u1089 \u1103 :\
   - search_tours \uc0\u1074 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1090  offers[] (\u1077 \u1089 \u1083 \u1080  API \u1086 \u1090 \u1076 \u1072 \u1077 \u1090  \u1090 \u1091 \u1088 \u1099 )\
   - meta \uc0\u1089 \u1086 \u1076 \u1077 \u1088 \u1078 \u1080 \u1090  requestid/progress/finished\
4) get_dictionaries \uc0\u1074 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1090  lists \u1080 \u1079  listdev\
5) \uc0\u1041 \u1077 \u1079  x-api-key MCP endpoints \u1086 \u1090 \u1076 \u1072 \u1102 \u1090  401\
6) \uc0\u1058 \u1077 \u1089 \u1090 \u1099  \u1087 \u1088 \u1086 \u1093 \u1086 \u1076 \u1103 \u1090 : npm test\
\
=====================================================================\
10) \uc0\u1044 \u1054 \u1055 \u1054 \u1051 \u1053 \u1048 \u1058 \u1045 \u1051 \u1068 \u1053 \u1054  (\u1055 \u1056 \u1054 \u1057 \u1068 \u1041 \u1040 )\
=====================================================================\
- \uc0\u1057 \u1076 \u1077 \u1083 \u1072 \u1081  \u1082 \u1086 \u1076  \u1072 \u1082 \u1082 \u1091 \u1088 \u1072 \u1090 \u1085 \u1099 \u1084 , \u1089  \u1090 \u1080 \u1087 \u1072 \u1084 \u1080 , \u1089  \u1087 \u1086 \u1085 \u1103 \u1090 \u1085 \u1099 \u1084 \u1080  \u1086 \u1096 \u1080 \u1073 \u1082 \u1072 \u1084 \u1080 .\
- \uc0\u1042 \u1089 \u1077  \u1089 \u1090 \u1088 \u1086 \u1082 \u1080  \u1074  \u1088 \u1091 \u1089 \u1089 \u1082 \u1086 \u1084  \u1090 \u1077 \u1082 \u1089 \u1090 \u1077  \u1074  README \u1086 \u1092 \u1086 \u1088 \u1084 \u1083 \u1103 \u1081  \u1088 \u1091 \u1089 \u1089 \u1082 \u1080 \u1084 \u1080  \u1082 \u1072 \u1074 \u1099 \u1095 \u1082 \u1072 \u1084 \u1080  \'ab\'bb.\
- \uc0\u1053 \u1080 \u1082 \u1072 \u1082 \u1080 \u1093  \u1076 \u1086 \u1075 \u1072 \u1076 \u1086 \u1082  \u1074  \u1082 \u1086 \u1076 \u1077  \u1087 \u1086  deep_link: \u1077 \u1089 \u1083 \u1080  \u1092 \u1072 \u1082 \u1090 \u1072  \u1085 \u1077 \u1090  \'97 \u1089 \u1090 \u1072 \u1074 \u1100  UNKNOWN.\
\
\uc0\u1057 \u1075 \u1077 \u1085 \u1077 \u1088 \u1080 \u1088 \u1091 \u1081  \u1087 \u1088 \u1086 \u1077 \u1082 \u1090  \u1087 \u1086 \u1083 \u1085 \u1086 \u1089 \u1090 \u1100 \u1102 . \u1042  \u1082 \u1086 \u1085 \u1094 \u1077  \u1074 \u1099 \u1074 \u1077 \u1076 \u1080 :\
- \uc0\u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099  \u1079 \u1072 \u1087 \u1091 \u1089 \u1082 \u1072 \
- \uc0\u1087 \u1088 \u1080 \u1084 \u1077 \u1088  curl \u1076 \u1083 \u1103  search_tours\
- \uc0\u1087 \u1088 \u1080 \u1084 \u1077 \u1088  curl \u1076 \u1083 \u1103  get_dictionaries\
- \uc0\u1089 \u1087 \u1080 \u1089 \u1086 \u1082  \u1092 \u1072 \u1081 \u1083 \u1086 \u1074 , \u1082 \u1086 \u1090 \u1086 \u1088 \u1099 \u1077  \u1089 \u1086 \u1079 \u1076 \u1072 \u1085 \u1099 .\
}