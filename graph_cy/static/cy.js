function nodes(id_list) {
    var o =[]
    for (var i=0;i<id_list.length;i++) {
        o.push({data:{id:id_list[i]}})
    }
    console.log('nodes',o)
    return o
}

function edges(link_list) {
    var o =[]
    for (var i=0;i<link_list.length;i++) {
        o.push(
            {data: {source: link_list[i][0], target: link_list[i][1], relationship: link_list[i][2]}}
        )
    }
    console.log('edges',o)
    return o
}


var cy_draw= function(id_list,link_list){
            cytoscape({
              container: document.getElementById('cy'),
              style: [
                // { selector: 'node[label = "Person"]',
                //   css: {'background-color': '#6FB1FC', 'content': 'data(name)'}
                // },
                { selector: 'node',
                  css: {'background-color': '#F5A45D', 'content': 'data(id)'}
                },
                { selector: 'edge',
                  css: {
                    'content': 'data(relationship)',
                    // 'width': 1,
                    'target-arrow-shape': 'triangle',
                    'line-color': '#ffaaaa',
                    'target-arrow-color': '#ffaaaa'
                    }
                }
              ],
              elements: {
                nodes: nodes(id_list),
                edges: edges(link_list)
              },
              layout: { name: 'cose'}
              // layout: { name: 'breadthfirst'}
              // layout: { name: 'circle'}
              // layout: { name: 'random'}
            });
        }
// cy_draw()
console.log('cy.js DONE')