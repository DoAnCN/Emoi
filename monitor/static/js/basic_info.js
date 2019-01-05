function basicinfo (datahost_json) {
        var obj = datahost_json
        // obj = JSON.parse(text);
        var name = SourceBufferList
        'localhost/monitor/'+id
        var i,id ="";
        var content="";
        for (i=0;i<obj.length;i++){
                if(obj[i].status=='n')
                {
                        obj[i].status='Never Connected';
                }
                if(obj[i].status=='a')
                {
                        obj[i].status='Active';
                }
                if(obj[i].status=='p')
                {
                        obj[i].status='Pending';
                }
                if(obj[i].status=='d')
                {
                        obj[i].status='Disconnected';
                }
                content+=   '<tr>' + 
                        '<td>' + obj[i].name + '</td>' +
                        '<td>' + obj[i].ip + '</td>' + 
                        '<td>' + obj[i].date_add + '</td>' +
                        '<td>' + obj[i].last_alive  + '</td>' +
                        '<td>' + obj[i].status + '</td>' + 
                        '<td>' + obj[i].os + '</td>' + 
                        '</tr>' ;            
        }

        document.getElementById("content-js").innerHTML = content;
  }