function basicinfo (datahost_json) {
        console.log(datahost_json);
        var obj = datahost_json
        // obj = JSON.parse(text);
        var i,stt,content="";
        
        for (i=0;i<obj.length;i++){
                if(obj[i].monitor=='n')
                {
                        stt='Never Connected';
                }
                if(obj[i].monitor=='a')
                {
                        stt='Active';
                }
                if(obj[i].monitor=='p')
                {
                        stt='Pending';
                }
                if(obj[i].monitor=='d')
                {
                        stt='Disconnected';
                }
                content+=   '<tr>' + 
                        '<td>' + obj[i].name + '</td>' +
                        '<td>' + obj[i].ip + '</td>' + 
                        '<td>' + obj[i].date_add + '</td>' +
                        '<td>' + obj[i].last_alive  + '</td>' +
                        '<td>' + stt + '</td>' + 
                        '<td>' + obj[i].os + '</td>' + 
                        '</tr>' ;            
        }
        document.getElementById("content-js").innerHTML = content;
  }