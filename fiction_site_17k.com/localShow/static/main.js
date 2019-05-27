// config
var table_show_router ='/booktype'
var search_router ='/bookname'
var current_page = 1
var max_page =334
var max_size_show =30
var current_type = ''


var ajax = function(method, path,  responseCallback) {
    console.log('ajax request===>',method,path)
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


function sel_ele(query) {
    return document.querySelector(query)
}

function tbody_template(array_data) {
    return `<tr class="">
                    <td>${array_data[0]}</td>
                    <td style="color: lawngreen" >${array_data[1]}</td>
                    <td class="td6"><span>
                        【<a href="/book/${array_data[3]}" target="_blank"
                            style="color: blueviolet">${array_data[2]}</a>】
                        </span>
                        </td>
                    <td>${array_data[4]}</td>
                    <td class="td6">${array_data[5]}</td>
                    <td class="td8"><em class="fc2">已完结</em></td>
                </tr>`
}
function load_data(tbody,html_str) {
    var rows =JSON.parse(html_str)
    var tbody_str =''
    for (var i=0;i<rows.length;i++) {
        var row = rows[i]
        tbody_str += tbody_template(row)
    }
    tbody.innerHTML =  tbody_str
    sel_ele('#id-play').play()
}

var load_table= function(html_str) {
    var tbody = sel_ele('#id-tbody'),table=sel_ele('#id-table-wrapper'),search= sel_ele('#id-search')
    table.style.display = ''
    sel_ele('#id-table-father').style.display=''
    search.style.display='none'
    load_data( tbody,html_str )
}
var load_search = function(html_str) {
    var table = sel_ele('#id-table-wrapper'),search= sel_ele('#id-search'),tbody=sel_ele('#id-search >div>table>tbody')
    table.style.display ='none'
    search.style.display=''
    load_data( tbody,html_str )
    sel_ele('#id-result-num').innerText = tbody.children.length
}

function bind_nav() {
    var nav_rows = document.querySelectorAll('.cls-nav-row')
    for (var i in nav_rows) {
        var row =nav_rows[i]
        row.addEventListener('click',function (event) {
            var e = event.target
            if ( (e.tagName.toUpperCase() == 'A')  ) {
                var e = e.children[0]
            }
            if ( e.tagName.toUpperCase() == 'SPAN') {
                    current_page = 1
                    var booktype=e.innerText
                    current_type = booktype
                    onTable()
                    // load the status info
                    sel_ele('#id-result-type').innerText=current_type
                    ajax('GET',table_show_router +'/'+current_type+'/'+'about',function (x) {
                        // 男生女生等条目都是最大10000 max num
                        max_page =Math.ceil(parseInt(x)/max_size_show )
                        sel_ele('#id-result-pages').innerText= max_page
                        if (x ==='10000') {
                            x = '9999+'
                        }
                        sel_ele('#id-result-num').innerText =x
                        console.log('---result--page-->',x)
                    })
            }
            // console.log('======',e.tagName)
        })
    }
}

function onTable() {
    var router = table_show_router +'/'+current_type+'/'+ current_page
    ajax('GET',router,load_table)
    sel_ele('#id-current-page').innerText=current_page
}

function onSearch() {
    var word= sel_ele('#id-search-input').value
    ajax('GET',search_router+'/'+word,load_search)
}

function onScroll(n) {
    current_page += n
    if (n==0) {
        var num = sel_ele('#toPage').value
        // if not NaN
        if ( num === num ) {
            current_page = parseInt(num)
        }
    }
    if (current_page < 1) {
        current_page += max_page
    }
    onTable()
}

function main() {
    bind_nav()
    sel_ele('#id-max-size-show').innerText = max_size_show
}
main()


// k("dt").event("click", function() {
// 	this.href = "javascript:";
// 	var i = this.parentNode,
// 		t = i.getElementsByTagName("dd")[0];
// 	t.clientHeight ? (t.style.display = "none", k(".folding", this).html("+ 展开")) : (t.style.display = "block", k(".folding", this).html("- 收起"))
// }),
//
//   k.initShare(k(".fenxiang").item(0)), k.initShare(k(".fenxiang").item(1));