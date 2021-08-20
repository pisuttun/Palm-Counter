var xmlHttp = new XMLHttpRequest();
xmlHttp.open("GET", "https://Palm-Counter.pisutjirarat.repl.co/score?season=1", false );
xmlHttp.send(null);
console.log(xmlHttp.responseText);
var json = JSON.parse(xmlHttp.responseText)
console.log(json)