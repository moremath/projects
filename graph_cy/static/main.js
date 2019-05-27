var ajax = function(method, path,  responseCallback) {
    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    r.send()
}

function display_switch(e,btn) {
    var table = sel_ele('#id-table')
    var graph = sel_ele('#id-graph')
    var loading = sel_ele('#id-loading')
    sel_ele('#id-play').play()

    table.style.display="none"
    graph.style.display="none"

    setTimeout(
        function () {
            btn.style.background=''
            loading.style.display="none"
            e.style.display=""

        },
        1000*(Math.random()+0.5)
    )
}


function sel_ele(sel) {
    return document.querySelector(sel)
}


function selected_file(){
    var l = sel_ele('#id-file').files
    if ( l.length ==0 ) {
        return 'call.xls'
    }
    return l[0].name
}

// function bind_btn_event() {
//     var btns= ['#id-btn-table','#id-btn-graph']
//     var routers = ['/table','/graph']
//     var eles =['#id-table','#id-graph']
// }
sel_ele('#id-btn-table').addEventListener('click',function (event) {
    ajax('GET','/table/'+selected_file(),function (html_str) {
        var tbody =sel_ele('#id-table > tbody')
        tbody.innerHTML= html_str
    })
    event.target.style.background='orange'
    sel_ele('#id-loading').style.display=''
    display_switch(sel_ele('#id-table'),event.target)
})

sel_ele('#id-btn-graph').addEventListener('click',function (event) {
    ajax('GET','/graph/'+selected_file(),function (html_str) {
        if (html_str.search("404.png") != -1) {
            sel_ele('#cy').innerHTML = html_str
        }
        else {
            var data = JSON.parse(html_str)
            console.log('ajax!!',typeof data,data.length)
            cy_draw(
                data['id_list'],
                data['link_list'],
            )
        }

    })
    event.target.style.background='orange'
    // sel_ele('#id-loading').style.display=''
    sel_ele('#id-graph').style.display=''
    sel_ele('#id-table').style.display='none'
    sel_ele('#id-play').play()

    setTimeout(
        function () {
            event.target.style.background=''
            sel_ele('#id-loading').style.display="none"
                    },
        1000*(Math.random()+0.5)
    )

})


sel_ele('#id-btn-single').addEventListener(
    'click',
    function () {
    sel_ele('#id-link-single').href = '/one/'+sel_ele('#id-input-single').value
    sel_ele('#id-link-single').click()
        }
    )


sel_ele('#id-btn-double').addEventListener(
    'click',
    function () {
        var  u1 = sel_ele('#id-input-u1').value,u2 = sel_ele('#id-input-u2').value
        ajax('GET','/two?'+'u1='+u1+'&u2='+u2,function (str) {
            alert(str)
        })
    }
)

sel_ele('#id-btn-double-swap').addEventListener('click',function () {
    var  u1 = sel_ele('#id-input-u1').value,u2 = sel_ele('#id-input-u2').value
    sel_ele('#id-input-u1').value = u2
    sel_ele('#id-input-u2').value =u1
})
console.log('done!--main.js-==')