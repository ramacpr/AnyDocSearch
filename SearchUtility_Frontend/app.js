var express = require('express'); // express package for http 
var mysql = require('mysql'); // to connect to the MySQL server
var body_parser = require('body-parser'); // parse the request/response data blocks
var stemmer = require('stemmer');

var app = express(); 

app.set("view engine", "ejs");
// use the body_parser
app.use(body_parser.urlencoded({extended: true}));
// use the css (and other contents) from public folder
app.use(express.static(__dirname + "/public"));

// connect to the web server at localhost:8080
app.listen(8080, 'localhost', function(){
    console.log("========== Web server running on port 8080 ==========\n\n");
});

// connect to the MySQL server at the below ip:port
// the port number is taken from the MySQL's 'SQL Server' 
// reconfigure settings. 
// and the ip is the default ip for MySQL server
var con = mysql.createConnection({
    host: "127.0.0.1",
    port: "3306",
    user: "root",
    password: "Priya12#",
    database: 'searchutility'
});
con.connect(function(err) {
    if (err) throw err;

    console.log("========== MySQL server connected on 127.0.0.1:3306 as root user! ==========\n\n");
});

// when the main page is loaded
app.get("/", async(request, response) => {
    console.log("Initializing the frontend");    
    response.render("home", {data: 0, theWord:""});
});

app.post("/search", async(request, response) => {
    let orgWord = new String(request.body.word);
    if(orgWord.length == 0){
        console.log("cannot search empty text");
        alert("cannot search empty text");
        response.redirect("/");
    }
    else{
        var keyword = stemmer(orgWord.toLowerCase().trim());
        console.log("Post request sent to server. keyword: " + keyword);
        var word = {word: keyword};
        let result = await runSqlQueryAsync("SELECT COUNT(*) as cnt FROM vocabulary WHERE word LIKE '" + "%" + keyword + "%'", true);
        let searchCount = result[0].cnt; 
        // response.redirect("/");
        return response.render("home", {data: searchCount, theWord: orgWord});
    }    
    
});

// call runSqlQuery when the return value is not important
// call runSqlQueryAsync when the return value of the query needs to be captured.
// -- the caller needs to be wrapped in async-await 
// queryString -> the SQL query 
// consoleLogging -> set to true if need console logging for the query results.
function runSqlQuery(queryString, consoleLogging, options = null){   
    con.query(queryString, options, function(err, result, fields) {
        if (err) throw err;
        if(consoleLogging == true){
            console.log("\n--------------------------------------------------")
            console.log(queryString + " --> DONE!");
            console.log(result);
            console.log("--------------------------------------------------")
        }
    });
};

function runSqlQueryAsync(queryString, showResult, options = null){   
    return new Promise((theResults) => {
        con.query(queryString, options, (err, results) =>{
            if(err) throw err; 
            if(showResult == true){
                console.log("\n" + queryString + " --> DONE!");
                console.log(results);
            }
            theResults(results);
        });
    });
};
