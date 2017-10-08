# coding=UTF-8
import re
import sys
import traceback
import json
import requests
import time
from bs4 import BeautifulSoup
import random

sys.path.append("..")
import DataBase.DatabaseDAL


def main():

    try:
        ##需要改数据库名

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        list = dbDAL.query("SELECT ci_Id,ci_Classfiy_Id,ci_URL FROM Tab_WangYiYun_Classfiy_Item where ci_Song_Num is null order by ci_Id")


        num=0
        while len(list)>num:
            (ci_Id, ci_Classfiy_Id,  ci_URL)=list[num]
            try:
                if(dbDAL is None):
                    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
                time.sleep(random.randint(2,5))
                obj={}
                obj={"ci_Id":ci_Id}
                obj["ci_Tags"]=""
                obj["ci_Song_Num"] = "0"
                obj["ci_Play_Num"] = "0"
                obj["ci_Fav_Num"] = "0"
                obj["ci_Share_Num"] = "0"
                obj["ci_Comment_Num"] = "0"

                # try:
                url = "http://music.163.com/"
                url+=ci_URL
                r = requests.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.content, "html.parser")

                nodeAList=bsObj.findAll(name="a",attrs={"class":"u-tag"})
                nodeSongNum = bsObj.find(id="playlist-track-count")  #歌曲数
                nodePlayNum = bsObj.find(id="play-count")             #播放次数
                nodeFavNum = bsObj.find(name="a",attrs={"data-res-action":"fav"})  # 收藏
                nodeShareNum = bsObj.find(name="a", attrs={"data-res-action": "share"})  # 分享
                nodeCommentNum = bsObj.find(name="a", attrs={"data-res-action": "comment"})  # 评论

                tagsList=[]
                for nodeA in nodeAList:
                    tagsList.append(nodeA.get_text().strip())
                obj["ci_Tags"]="、".join(tagsList)

                # if nodeSongNum is not None:
                #     songNum=nodeSongNum.get_text();
                #     songNum=re.findall(r"\d+\d*", songNum)[0]
                #     obj["ci_Song_Num"]=songNum
                # if nodeFavNum is not None:
                #     favNum=nodeFavNum.get_text();
                #     favNum=re.findall(r"\d+\d*", favNum)[0]
                #     obj["ci_Fav_Num"]=favNum
                # if nodePlayNum is not None:
                #     playNum=nodePlayNum.get_text();
                #     playNum=re.findall(r"\d+\d*", playNum)[0]
                #     obj["ci_Play_Num"]=playNum
                # if nodeShareNum is not None:
                #     shareNum=nodeShareNum.get_text();
                #     shareNum=re.findall(r"\d+\d*", shareNum)[0]
                #     obj["ci_Share_Num"]=shareNum
                # if nodeCommentNum is not None:
                #     commentNum=nodeCommentNum.get_text();
                #     commentNum=re.findall(r"\d+\d*", commentNum)[0]
                #     obj["ci_Comment_Num"]=commentNum
                if nodeSongNum is not None:
                    songNum=nodeSongNum.get_text();
                    arr=re.findall(r"\d+\d*", songNum)
                    if len(arr)>0 :
                        songNum = arr[0]
                    obj["ci_Song_Num"]=songNum

                if nodeFavNum is not None:
                    favNum=nodeFavNum.get_text();
                    arr = re.findall(r"\d+\d*", favNum)
                    if len(arr)>0 :
                        favNum=arr[0]
                    obj["ci_Fav_Num"]=favNum

                if nodePlayNum is not None:
                    playNum=nodePlayNum.get_text();
                    arr=re.findall(r"\d+\d*", playNum)
                    if len(arr) > 0:
                        playNum=arr[0]
                    obj["ci_Play_Num"]=playNum

                if nodeShareNum is not None:
                    shareNum=nodeShareNum.get_text();
                    arr = re.findall(r"\d+\d*", shareNum)
                    if len(arr) > 0:
                        shareNum = arr[0]
                    obj["ci_Share_Num"]=shareNum

                if nodeCommentNum is not None:
                    commentNum=nodeCommentNum.get_text();
                    arr = re.findall(r"\d+\d*", commentNum)
                    if len(arr) > 0:
                        commentNum = arr[0]
                    obj["ci_Comment_Num"]=commentNum

                try:

                    objList=[];
                    objList.append(obj)
                    print "正在入库....更新。标签：{0}, url:{1}".format(obj["ci_Tags"],ci_URL).decode("utf8")
                    status= dbDAL.update(tableName="Tab_WangYiYun_Classfiy_Item", list=objList, whereTuple=("ci_Id",))
                    if status==-1 :
                        num += 1
                        continue
                    divNode=bsObj.find(id="song-list-pre-cache")
                    if divNode is None:
                        num += 1
                        continue
                    NodeTextarea=divNode.find(name="textarea")
                    responseJson = json.loads(NodeTextarea.get_text())
                    index=0
                    songList=[]
                    while len(responseJson) > len(songList):

                        song={"cis_Classfiy_Item_Id":ci_Id}
                        try:
                            pass
                            jsonObj=responseJson[index]
                            song["cis_SongName"]=jsonObj["name"]
                            singerList=[]
                            for singer in jsonObj["artists"]:
                                singerList.append(singer["name"])
                            song["cis_Singer"]="/".join(singerList)
                        except:
                            traceback.print_exc()
                            continue
                        else:
                            songList.append(song)
                            index+=1
                    print "正在入库...,个数：{0},{1}".format(len(songList),ci_URL).decode("utf8")
                    status = dbDAL.insert(tableName="Tab_WangYiYun_Classfiy_Item_Songs", list=songList)
                    if status == -1:
                        num += 1
                        continue
                except:
                    traceback.print_exc()
                    num += 1
                    continue

            except:
                traceback.print_exc()
                time.sleep(random.randint(15,30))
                continue
            else:
                num+=1

    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()



if __name__=="__main__":
    main()