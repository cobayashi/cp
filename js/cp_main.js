csv = new Array();
nodelist = new Array();
var data;
var target_temp;
var query_temp;
var s_temp;
var sendData={};
var sendTag={};
var openData=new Array();
var closeData=new Array();
var knowList=new Array();

onload = function() {
    //検索
    $('form.quicksearch').submit(function(){return search($(".quicksearch__input").val())});//検索ボタン押されたらsearch()にフォーム内容を渡す
    function search(q) {//検索クエリが q にはいる
        $('.result').html("<img src='img/loader.gif' style='margin: 50px'/>");//読み込み中のアニメーションの表示
        query_temp = $('#query').val();//検索したクエリを覚えておく 他の画面から戻るときにつかう
        $.get('cgi/rdf_search.cgi',"query="+q,read);//検索CGIのrdf_search.cgi にクエリを渡す/結果が帰ってきたらreadを実行
        return false;
    }
    function read(text){//検索結果がjson形式でtextにはいる
        var hits = JSON.parse(text);//jsonを配列 hits にいれる
        $('.open_area').hide();
        $('.close_area').hide();
        $('.back_button1').hide();
        $('.back_button2').hide();
        $('.edit_button').hide();
        $('.tag_editer').hide();//いらない部品を隠す
        $('.result').empty();//結果表示スペースの.resultの中を空にする
        var len = hits.length//配列の長さをみる
        for(var i =0; i < len; i++) {//配列の長さだけ繰り返す
            html="<div class='profile' id='"+hits[i].s+"'><div class= 'name'>"+hits[i].name+"</div><div class= 'job'>"+hits[i].job+"</div><div class= 'memo'>"+hits[i].memo+"</div></div>"//結果をhtmlで書く
            $('.result').append(html);//.resultにhtmlを表示
        }
        
    }

    //検索結果からプロフィールをみる
    $(document).on({//検索結果の人の名前(.nameクラスのdiv要素)について
        'click': function(){//クリックされたらこの中身が実行される
            $('.result').html("<img src='img/loader.gif' style='margin: 50px'/>");//読み込みアニメ表示
            var s = $(this).parent().attr("id");//クリックされた親要素に書いてある名前をsに入れる
            s_temp = s;//クリックされた名前を覚えとく
            return get_profile(s);//クリックされた名前をget_profile()に送る
        },
        'mouseenter': function(){//マウスが乗ったら
            $(this).css("cursor","pointer");//マウスカーソルが指になる
            $(this).css("text-decoration","underline");//下線が出てリンクっぽくなる
        },
        'mouseleave': function(){//マウスが離れたら
            $(this).css("cursor","auto");//カーソルが元に戻る
            $(this).css("text-decoration","none");//下線とかが消える
        }
    },'.name');//.nameについて
    function get_profile(s) {//クリックされた名前がsに入る
        $.get('cgi/getprofile.cgi',"s="+encodeURIComponent(s),read_profile);//名前をプロフィール取ってくるCGIのgetprofile.cgiに渡す//結果が帰ってきたらread_profileを実行
        $('.back_button1').show();//前に戻るボタンの表示
        $('.edit_button').show();//編集ボタンの表示
        $('.logLink').hide();
        $('.logList').hide();
        return false;
    }
    function read_profile(html){//結果がhtmlにはいる
        $('.result').empty();//.resultを空っぽに
        $('.result').append(html);//結果を.resultに表示
        target_temp = $("*[name=target]").val();//表示したプロフィールの人物のRDFの主語になってるリソースURIを覚えておく
    }

    /*プロフィールを編集する*/
    //編集フォームマウスオーバー時に背景色を変える
    $(document).on({
        'mouseenter': function(){
            $(this).css("background-color","#eee");
        },
        'mouseleave': function(){
            $(this).css("background-color","#fff");
        }
    },'.job_detail');
    $(document).on({
        'mouseenter': function(){
            $(this).css("background-color","#eee");
        },
        'mouseleave': function(){
            $(this).css("background-color","#fff");
        }
    },'.name_detail');
    $(document).on({
        'mouseenter': function(){
            $(this).css("background-color","#eee");
        },
        'mouseleave': function(){
            $(this).css("background-color","#fff");
        }
    },'.memo_detail');

    //タグ編集ボタン
    $(document).on({//タグ編集ボタン.edit_buttonについて
        'click': function(){//クリックされたら
            sendData ={//sendDataに
                "target" : $("*[name=target]").val(),//編集対象のプロフィールのリソースURI
                "edit_job" : $("*[name=edit_job]").val(),//編集前の所属
                "edit_name" : $("*[name=edit_name]").val(),//編集前の名前
                "edit_memo" : $("*[name=edit_memo]").val(),//編集前のメモ
                "reliability" : $("*[name=reliability]").val()//編集前の信頼度
            };//を入れる
            return edit_tag();//edit_tag()を実行
        }
    },'.edit_button');
    function edit_tag(){
        $.ajax({//rdfデータベースの編集cgiのrdf_edit.cgiにsendDataを送る
            type: "POST",
            url: "cgi/rdf_edit.cgi",
            data: sendData,
            async: false,
            success: function(){
            }
        });
        $.get('cgi/mecab.cgi',"memo="+$("*[name=edit_memo]").val()+"&job="+$("*[name=edit_job]").val(),mecab_read);//メモ内容と所属をmecab.cgiに渡して結果が帰ってきたらmecab_readを実行//mecab.cgiはメモ内容から名詞を抽出してタグ候補にする。あと、タグ候補と所属でデータベースを検索してヒットした人物を関連人物として取ってくる
        return false;   
    }
    //タグをドラッグドロップ可能に
    function tagdraggable(){

        $('.tag').draggable({
            snap:true,
            snapMode:"inner",
            snapTolerance:7
        });
        $('.tag').droppable({
            tolerance: "touch", 
            drop: function(ev, ui) {
                // ドロップされたときにタグを合体
                $("<div class='tag'>"+$(this).text()+ui.draggable.text()+"</div>").appendTo("div.tag_cloud");
                $('.tag').draggable({
                    snap:true,
                    snapMode:"inner",
                    snapTolerance:7
                });
            }
        });

    }
    function mecab_read(html){
        var opentags = [];
        var closetags = [];
        $('.open_tag').each(function(){
            opentags.push($(this).text());//公開タグを配列にいれる
        });
        $('.close_tag').each(function(){
            closetags.push($(this).text());//非公開タグを配列にいれる
        });

        $('.result').empty();
        $('.edit_button').hide();//タグ編集ボタン隠す
        $('.back_button1').hide();//検索結果一覧へ戻るボタン隠す
        $('.back_button2').show();//通常プロフィール画面へ戻るボタンの表示
        //$('.result').html("<img src='img/suimen.png'/>");//--ダサいから消した
        $(".open_area").show();
        $(".close_area").show();
        $(".tag_editer").show();
        // --- 公開エリアのDroppable要素 ---
        $(".open_area").droppable({
            tolerance: "fit",            // Draggable要素が完全に入った場合にDrop可能にする
            hoverClass: "drop_hover",    // Draggable要素が上に乗ったときに適用するクラス
            drop: function(ev, ui) {
                // ドロップされたときにDraggable要素内の文字を配列openDataに追加
                openData.push(ui.draggable.text());
            },
            out: function(ev, ui) {
                // draggable要素が外にでたときその要素を配列から削除
                var point = openData.indexOf(ui.draggable.text());
                openData.splice(point,1);
            }
        });
        // --- 非公開エリアのDroppable要素 ---
        $(".close_area").droppable({
            tolerance: "fit",              // Draggable要素が完全に入った場合にDrop可能にする
            hoverClass: "drop_hover",    // Draggable要素が上に乗ったときに適用するクラス
            drop: function(ev, ui) {
                // ドロップされたときにDraggable要素内の文字を配列に追加
                closeData.push(ui.draggable.text());
            },
            out: function(ev, ui) {
                // draggable要素が外にでたときその要素を配列から削除
                var point = closeData.indexOf(ui.draggable.text());
                closeData.splice(point,1);
            }
        });
        $('.result').append(html);//名刺抽出した結果返してもらってタグ追加
        for(var i =0;i<opentags.length;i++){
            $("<div class='tag' style='position: absolute;top:-350px;left:10px;'>"+opentags[i]+"</div>").appendTo("div.tag_cloud");//もとからあったタグの追加
            openData.push(opentags[i]);
        }
        for(var i =0;i<closetags.length;i++){
            $("<div class='tag' style='position: absolute;top:-100px;left:10px;'>"+closetags[i]+"</div>").appendTo("div.tag_cloud");//もとからあったタグの追加
            closeData.push(closetags[i]);
        }
        tagdraggable();
    }
    $(document).on({//関連人物を表示してる.relationについて
        'click': function(){//クリックされたら
            // --- すでに知人としてknowListに追加されている場合は
            if(knowList.indexOf($( this ).attr( "id" ))!=-1){
                $(this).css("color","#aaa");///文字の色を薄くする
                var p = knowList.indexOf($( this ).attr( "id" ));//knowListに追加されている順番をpに入れる
                knowList.splice(p,1);//knowListのp番目を削除
            // --- 追加されていない場合
            }else{
                $(this).css("color","#777");///文字の色を濃くする
                knowList.push($( this ).attr( "id" ));//knowListに追加する
            }
        },
        'mouseenter': function(){//マウスが乗ったら背景色変える
            $(this).css("background-color","#eee");

        },
        'mouseleave': function(){//マウスが離れたら背景色もどす
            $(this).css("background","none");
        }
    },'.relation');
    //タグを新しく作る
    $(document).on('click','#create', function(){// #createがクリックされたら
        $("<div class='tag'>"+$('#tagvalue').val()+"</div>").appendTo("div.tag_cloud");//#tagvalueに入力された内容を.tagとして.tag_cloudのなかに追加
        tagdraggable();//新しく作った.tagをドラッグ可能に
    });


    //プロフィールへ戻るボタンの処理
    //戻るときにタグ編集内容を保存
    $(document).on('click','.back_button2', function(){//.back_button2がクリックされたら
        sendTag={
            "target" : target_temp,//編集対象のリソースURI
            "open" : openData.join(),//公開タグを連結した文字列
            "close" : closeData.join(),//非公開タグを連結した文字列
            "knows" : knowList.join()//知人リストを連結した文字列
        };
        openData=[];//配列初期化
        closeData=[];
        knowList=[];
        return post_tag();
    });
    function post_tag() {
        $.ajax({
            type: "POST",
            url: "cgi/tag_edit.cgi",
            data: sendTag,
            async: false,
            success: function(){
                $('.result').empty();//.resultを空に
                $('.edit_button').show();//編集ボタン出す
                $('.back_button1').show();//検索結果に戻るボタン出す
                $('.back_button2').hide();//プロフィールに戻るボタン隠す
                $(".tag_editer").hide();//タグ新しく作るやつ隠す
                $(".open_area").hide();//公開タグドロップするとこ隠す
                $(".close_area").hide();//非公開タグドロップするとこ隠す
                back2();//プロフィールにもどるやつ
            }
        });
        $('.result').empty();
        $('.result').html("<img src='img/loader.gif' style='margin: 50px'/>");
        return false;
    }
    function back2() {
        $.get('cgi/getprofile.cgi',"s="+encodeURIComponent(s_temp),reflesh2);
        return false;
    }
    function reflesh2(html){
        $('.tag_editer').hide();
        $('.result').empty();
        $('.result').append(html);
    }

    //編集内容を保存
    $(document).on('click','.back_button1', function(){
        sendData ={
            "target" : $("*[name=target]").val(),
            "edit_job" : $("*[name=edit_job]").val(),
            "edit_name" : $("*[name=edit_name]").val(),
            "edit_memo" : $("*[name=edit_memo]").val(),
            "reliability" : $("*[name=reliability]").val()
        };
        return edit();
    });
    function edit() {
        $.ajax({
            type: "POST",
            url: "cgi/rdf_edit.cgi",
            data: sendData,
            async: false,
            success: function(){
                $('.result').empty();
                $('.back_button1').hide();
                back1();
            }
        });
        $('.result').empty();
        $('.result').html("<img src='img/loader.gif' style='margin: 50px'/>");
        return false;
    }
    function back1() {
        get_profile(s_temp);
        return false;
    }
};