import naverBlogCrop
import Visual_review
import db_Insert
import time

def main_find(conn, text):
    num, title_array, link_array, img_array, img_numx, context_array, data_array, date_array, nicname_array = naverBlogCrop.naver_cralwler(conn, text)

    import Grade_review
    add_array = []
    check_array = []
    count_array = []

    file=open('context.txt','w')
    for x in range(len(title_array)):
        print("================================================================")
        print("번호 : " + str(x))
        print("제목 : " + title_array[x])
        print("링크 : " + link_array[x])
        print("이미지 링크 : " + img_array[x])
        print("이미지 개수 : " + str(img_numx[x]))
        print("내용(간략) : " + context_array[x])
        print("날짜 : " + date_array[x])
        print("닉네임 : " + nicname_array[x])

        add_count = data_array[x].count('후원') + data_array[x].count('무료') + data_array[x].count('광고') + data_array[x].count('업체') + data_array[x].count('제공')
        if(int(img_numx[x]) >= 15):
            add_array.append('사진 광고')
            print("광고 여부 : " + add_array[x])

        elif(add_count >= 4):
            add_array.append('업체 광고')
            print("광고 여부 : " + add_array[x])

        elif(nicname_array.count(nicname_array[x]) >= 4):
            add_array.append('닉네임 광고')
            print("광고 여부 : " + add_array[x])

        elif(len(data_array[x]) >= 1000):
            add_array.append('글 광고')
            print("광고 여부 : " + add_array[x])
        
        else:
            add_array.append('청정')
            print("광고 여부 : " + add_array[x])

        db_Insert.db_update2(conn, str(x)+text, add_array[x])
        if(add_array[x] == '청정'):
            try:
                file.write(data_array[x] + '\n')
                check = Grade_review.Grade(title_array[x] + context_array[x])
                check_array.append(check)
            except:
                check_array.append('중립')
        else:
            check_array.append('중립')
        
        db_Insert.db_update3(conn, str(x)+text, check_array[x])
        print("긍/부정 : " + check_array[x])
        try:
            print("광고 퍼센트 : " + str( ( 1 - float ( add_array.count('청정') / len(add_array) ) ) * 100 ) )
            print("긍/부정 퍼센트 : " + str( float ( check_array.count('긍정') / ( len(check_array) - check_array.count('중립') ) ) * 100 ) )
        except:
            pass
        print("")

    try:
        addper = ( ( 1 - float ( add_array.count('청정') / len(add_array) ) )  * 100 )
        actper = float ( check_array.count('긍정') / ( len(check_array) - check_array.count('중립') ) * 100 )

        print("광고 퍼센트 : " + str(addper))
        print("긍/부정 퍼센트 : " + str(actper))
        
        addnum = len(add_array) - add_array.count('청정')
        actnum = check_array.count('긍정')
        db_Insert.db_insert2(conn, str(1), str(num), str(addnum), str(actnum), str(round(addper, 1)), str(round(actper, 1)))

    except:
        pass
    print("")
    file.close()

    Visual_review.visual_main()
    file=open('count.txt','r')
    for x in range(3):
        count_array.append( file.readline().split('\n')[0] )
    file.close()
    print(count_array)
    db_Insert.db_insert3(conn, str(count_array))
    print("")

while(1):
    conn = db_Insert.db_setting()
    check = 0
    db_Insert.db_delete2(conn)
    while(not check):
        check = db_Insert.db_search(conn, "0")
        time.sleep(0.1)

    print(check[0][0])
    db_Insert.db_delete1(conn)
    db_Insert.db_delete3(conn)
    db_Insert.db_delete4(conn)
    main_find(conn, check[0][0])

    db_Insert.db_update(conn, check[0][0], "1")
    
    conn.close()

# conn = db_Insert.db_setting()
# db_Insert.db_update(conn, "검색", "0")