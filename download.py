import urllib.request
from urllib.error import URLError, HTTPError
import json
import os

def open_url(url):
    req = urllib.request.Request(url)
    
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) WebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')
    
    response = urllib.request.urlopen(req)

    return response

def updateContent(fname, chapterName):
    with open('content.html', 'a+', encoding='utf-8') as contentFile:
        # 写入目录
        contentFile.write('<a target="_blank" href="' + fname + '">' + chapterName + '</a><br/>')
    
def main():
    result = None
    # https://m.whzh-cw.com/du/66660/
    # https://m.whzh-cw.com/files/66/66660/66660.json?cdnversions=5195519
    
    json_url = 'https://m.whzh-cw.com/files/66/66660/66660.json?cdnversions=5195519'
    try:
        json_body = open_url(json_url)
        # json_str = json_body.read().decode('utf8')
        result = json.load(json_body)
    except Exception as e:
        print(e)
        return;
    
    '''
    with open('c:/r4r/66660.json') as src:
        result = json.load(src)
    '''

    #https://m.whzh-cw.com/files/article/html555/70/70538/
    
    #print('Articlet Id: ', result['info']['articleid'])
    print('书名：', result['info']['articlename'])
    print('作者：', result['info']['author'])
    print('最新章节ID：', result['info']['lastchapterid'])
    print('最新章节：', result['info']['chapters'])

    # 36174034
    latestChapterNum = int(result['info']['lastchapterid'])

    # 3195
    latestChapterId = int(result['info']['chapters'])

    recordChapterId = ''
    recordFileName = 'update.txt'

    if not os.path.isfile(recordFileName):
        print('>>>记录文件不存在')
    else:
        with open(recordFileName, 'r') as f:
            record = f.read()
            if not len(record):
                print('>>>记录为空！')
                return
            elif record.isdigit():    
                recordChapterId = record
            else:
                print('>>>出现异常！')
                return

    print('>>>记录章节ID：' + recordChapterId)
    
    if int(recordChapterId) >= latestChapterNum:
        print('>>>已更新至最新章节！')
        return
    
    for each in result['list']:
        chapterId = each['chapterid']
        chapterName = each['chaptername']

        if int(chapterId) <= int(recordChapterId):  # 忽略这些内容的下载
            continue

        print('>>>' + chapterName)
        print('>>>' + chapterId)

        recordFile = open('update.txt', 'w')
        recordFile.write(chapterId)
        print('>>>记录完毕! 当前章节为： ' + chapterId)
        recordFile.close()
        
        #https://m.whzh-cw.com/files/article/html555/70/70538/
        url = 'https://m.whzh-cw.com/files/article/html555/70/' + str(result['info']['articleid']) + '/' + str(chapterId) + '.html'
        
        body = None

        try:
            body = open_url(url)
        except HTTPError or UTLError or Exception:
            print('>>>请求异常！')
            break
        
        html = body.read().decode('gbk')

        if html.startswith('var _0x') or html.startswith('var cctxt='):
            print('>>>数据被加密，需要JavaScript解码')
            
            #scriptName = chapterId + '.script.html'
            #with open(scriptName, 'w', encoding='utf-8') as f:
            #    f.write(html)

            fname = chapterId + '.html'
            with open(fname, 'w', encoding='gbk') as f:
                content = '''<!DOCTYPE html>
                            <html>
                            <head>
                                <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
                                <script src="./jquery-1.8.1.min.js"></script>
                            </head>
                            <body>
                                <div id="content"></div>
                            </body>
                            <script type="text/javascript">
                                %s
                                msg=cctxt;
                                $('#content').html(msg);
                            </script>
                            </html>
                        '''
                f.write(content % html)

            # 写入目录
            updateContent(fname, chapterName)
            print('>>', url)
                
        else:
            fname = chapterId + '.html'
            with open(fname, 'w', encoding='utf-8') as f:
                html=html.replace("茵右脚楞夺",'的')
                html=html.replace("茵右脚楞夺",'的')
                html=html.replace("顺困顶枯枵",'是')
                html=html.replace("顶置中夺粗功肖功地",'有')
                html=html.replace("夺回顾功带困顺另",'一')
                html=html.replace("夺回顾功带困", '有')
                html=html.replace("顶置中夺粗功肖功地",'的')
                html=html.replace("茵右脚楞夺",'是')
                html=html.replace("夺回顾功带困",'有')
                html=html.replace("顺困顶枯枵",'，')
            
                f.write(html)
            # 写入目录
            updateContent(fname, chapterName)
            print('>>', url)
        # 保存需要记录到文件中章节ID
        #recordChapterId = chapterId
        
        
    # 更新目录并执行完毕
    #record(recordChapterId)
    print('已执行完毕！')
            
        

if __name__ == '__main__':
    main()
